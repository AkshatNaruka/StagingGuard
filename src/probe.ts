import assert from 'node:assert/strict';
import { Client, StreamableHTTPClientTransport } from '@modelcontextprotocol/client';
import { createContext } from './config.js';
import { RehearsalRuntime } from './runtime.js';
import { startHttp } from './http.js';

const local = process.argv.includes('--local');
const live = process.argv.includes('--agntid');
if (local === live) throw new Error('Choose exactly one: --local or --agntid.');
const http = local ? await startHttp(await RehearsalRuntime.create(createContext(Date.now(), {})), 0) : undefined;
const address = http?.address();
const endpoint = local && address && typeof address !== 'string' ? `http://127.0.0.1:${address.port}/mcp` : process.env.AGNTID_MCP_URL;
const client = new Client({ name: 'agntid-starter-probe', version: '0.1.0' });
try {
  if (!endpoint) throw new Error('Set AGNTID_MCP_URL using the portal-generated client configuration.');
  const url = new URL(endpoint);
  if (url.username || url.password || url.search) throw new Error('Use a clean MCP URL; credentials belong in the documented auth header or OAuth flow.');
  if (url.protocol !== 'https:' && !(url.protocol === 'http:' && ['127.0.0.1', 'localhost', '[::1]'].includes(url.hostname))) throw new Error('Use HTTPS or local loopback HTTP.');
  const headers: Record<string, string> = {};
  if (live && (process.env.AGNTID_AUTH_HEADER || process.env.AGNTID_AUTH_VALUE)) {
    if (!process.env.AGNTID_AUTH_HEADER || !process.env.AGNTID_AUTH_VALUE) throw new Error('Configure both auth setting names from the Quick Start.');
    headers[process.env.AGNTID_AUTH_HEADER] = process.env.AGNTID_AUTH_VALUE;
  }
  await client.connect(new StreamableHTTPClientTransport(url, { requestInit: { headers, redirect: 'error' } }), { timeout: 15_000 });
  const tools = await client.listTools();
  console.log(`${local ? 'LOCAL REHEARSAL' : 'AGNTID CONNECTIVITY ONLY'}: ${tools.tools.length} visible tools.`);
  if (local) {
    assert.equal(tools.tools.length, 3);
    const allowed = await client.callTool({ name: 'support_get_ticket', arguments: { ticketId: 'T100' } });
    const denied = await client.callTool({ name: 'support_get_ticket', arguments: { ticketId: 'T200' } });
    assert.equal(allowed.isError, false);
    assert.equal(denied.isError, true);
    console.log('Real MCP initialize, list, allowed read, and denied read passed.');
  } else console.log('Discovery succeeded. A tool list alone does not prove AgntID policy enforcement; run the documented allowed/denied tests and inspect Reporting.');
} catch {
  console.error('Probe failed. Check runtime health, portal-generated URL, review state, and required auth. No credentials or raw server errors are printed.');
  process.exitCode = 1;
} finally {
  await client.close();
  if (http) { http.closeAllConnections(); await new Promise<void>((resolve) => http.close(() => resolve())); }
}
