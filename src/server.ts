import { StdioServerTransport } from '@modelcontextprotocol/server/stdio';
import { createContext, readConfig } from './config.js';
import { RehearsalRuntime } from './runtime.js';
import { createToolServer } from './tools.js';
import { startHttp } from './http.js';

async function main() {
  const config = readConfig();
  const runtime = await RehearsalRuntime.create(createContext(), { auditPath: '.local/audit.jsonl' });
  if (config.TRANSPORT === 'stdio') {
    const server = createToolServer(runtime);
    await server.connect(new StdioServerTransport());
    console.error('Local rehearsal MCP on stdio; all tickets are synthetic.');
    const close = () => { void server.close().finally(() => process.exit(0)); };
    process.once('SIGINT', close); process.once('SIGTERM', close);
  } else {
    const http = await startHttp(runtime, config.PORT);
    console.error(`Local rehearsal MCP: http://127.0.0.1:${config.PORT}/mcp`);
    const close = () => { http.closeAllConnections(); http.close(() => process.exit(0)); };
    process.once('SIGINT', close); process.once('SIGTERM', close);
  }
}
main().catch(() => { console.error('Startup failed. Check .env, the selected port, and writable .local storage.'); process.exitCode = 1; });
