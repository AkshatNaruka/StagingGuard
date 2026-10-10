import { access } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';

const exists = async (file) => { try { await access(file); return true; } catch { return false; } };
const reports = [];
const report = (name, ok, detail) => { reports.push(ok); console.log(`${ok ? 'OK' : 'TODO'} ${name}: ${detail}`); };
report('Node', Number(process.versions.node.split('.')[0]) >= 22, process.versions.node);
report('Dependencies', await exists('node_modules/@modelcontextprotocol/server'), 'npm ci installs the locked MCP v2 SDK');
report('Local environment', await exists('.env'), 'npm run setup creates it without overwriting existing settings');
report('Official AgntID docs', await exists('docs/vendor/agntid-context.md'), 'authenticated reference saved locally');
const docker = spawnSync('docker', ['info', '--format', '{{.ServerVersion}}'], { encoding: 'utf8', timeout: 10_000 });
report('Docker engine', docker.status === 0, docker.status === 0 ? docker.stdout.trim() : 'start OrbStack or Docker Desktop');
const codex = spawnSync('codex', ['mcp', 'get', 'devfolio'], { encoding: 'utf8', timeout: 10_000 });
report('Devfolio configuration', codex.status === 0, 'registration check only; live MCP calls verify authentication');
report('AgntID proxy setting', Boolean(process.env.AGNTID_MCP_URL), 'set the exact portal-generated MCP URL in .env; no credential values are printed');
try {
  const response = await fetch('http://127.0.0.1:18080/health', { signal: AbortSignal.timeout(3000) });
  report('AgntID runtime health', response.ok, `HTTP ${response.status}; portal Connected and Applied must also be checked`);
} catch { report('AgntID runtime health', false, 'run docker compose up -d in runtime/'); }
console.log('\nTODO items are reported without treating local rehearsal as live integration.');
console.log('MANUAL Verify Operational / Connected, Setup 5 of 5, Applied sync, and allowed/denied Reporting records in AgntID.');
if (process.argv.includes('--strict') && reports.some((ok) => !ok)) process.exitCode = 1;
