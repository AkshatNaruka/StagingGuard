import { createServer } from 'node:http';
import type { Server } from 'node:http';
import { localhostHostValidation, localhostOriginValidation, NodeStreamableHTTPServerTransport } from '@modelcontextprotocol/node';
import { createToolServer } from './tools.js';
import type { RehearsalRuntime } from './runtime.js';

export async function startHttp(runtime: RehearsalRuntime, port = 8787): Promise<Server> {
  const validateHost = localhostHostValidation();
  const validateOrigin = localhostOriginValidation();
  const http = createServer(async (req, res) => {
    if (!validateHost(req, res) || !validateOrigin(req, res)) return;
    if (req.url === '/health' && req.method === 'GET') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ status: 'ready', enforcement: 'local-rehearsal-only', taskExpired: Date.now() >= runtime.context.expiresAt }));
      return;
    }
    if (req.url !== '/mcp') { res.writeHead(404); res.end(); return; }
    const server = createToolServer(runtime);
    const transport = new NodeStreamableHTTPServerTransport({ sessionIdGenerator: undefined, enableJsonResponse: true });
    res.once('close', () => { void server.close(); });
    try { await server.connect(transport); await transport.handleRequest(req, res); }
    catch { if (!res.headersSent) { res.writeHead(500); res.end('MCP request failed.'); } else res.end(); }
  });
  http.requestTimeout = 15_000;
  await new Promise<void>((resolve, reject) => { http.once('error', reject); http.listen(port, '127.0.0.1', () => { http.off('error', reject); resolve(); }); });
  return http;
}
