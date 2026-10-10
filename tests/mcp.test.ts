import assert from 'node:assert/strict';
import { test } from 'node:test';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { request } from 'node:http';
import { Client, StreamableHTTPClientTransport } from '@modelcontextprotocol/client';
import { createContext } from '../src/config.js';
import { RehearsalRuntime } from '../src/runtime.js';
import { startHttp } from '../src/http.js';

test('real HTTP MCP supports discovery, scope denials, and hostile Origin/Host rejection', async () => {
  const directory = await mkdtemp(join(tmpdir(), 'agntid-http-'));
  const runtime = await RehearsalRuntime.create(createContext(Date.now(), {}), { directory });
  const http = await startHttp(runtime, 0);
  const address = http.address(); assert.ok(address && typeof address !== 'string');
  const url = `http://127.0.0.1:${address.port}/mcp`;
  const client = new Client({ name: 'starter-test', version: '0.1.0' });
  try {
    await client.connect(new StreamableHTTPClientTransport(new URL(url)), { timeout: 5000 });
    const list = await client.listTools();
    assert.deepEqual(list.tools.map((tool) => tool.name).sort(), ['support_draft_reply', 'support_get_ticket', 'support_send_reply']);
    assert.ok(!list.tools.some((tool) => tool.name.includes('approve')));
    const allowed = await client.callTool({ name: 'support_get_ticket', arguments: { ticketId: 'T100' } });
    assert.equal(allowed.isError, false);
    const denied = await client.callTool({ name: 'support_get_ticket', arguments: { ticketId: 'T200' } });
    assert.equal(denied.isError, true);
    assert.ok(!JSON.stringify(denied).includes('Synthetic Customer C'));
    const extra = await client.callTool({ name: 'support_get_ticket', arguments: { ticketId: 'T100', approved: true } });
    assert.equal(extra.isError, true);
    assert.equal((await fetch(url, { headers: { Origin: 'https://untrusted.example' } })).status, 403);
    // Native fetch normalizes Host in newer Node releases; send it explicitly.
    const hostileHostStatus = await new Promise<number | undefined>((resolve, reject) => {
      const req = request(url, { headers: { Host: 'untrusted.example' } }, (res) => { res.resume(); res.once('end', () => resolve(res.statusCode)); });
      req.once('error', reject); req.end();
    });
    assert.equal(hostileHostStatus, 403);
  } finally {
    await client.close(); http.closeAllConnections();
    await new Promise<void>((resolve) => http.close(() => resolve()));
    await rm(directory, { recursive: true, force: true });
  }
});
