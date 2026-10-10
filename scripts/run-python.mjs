import { spawn } from 'node:child_process';
import { existsSync } from 'node:fs';

const python = '.local/agntid-venv/bin/python';
if (!existsSync(python)) { console.error('Run npm run setup:sdk first.'); process.exit(1); }
const child = spawn(python, process.argv.slice(2), { stdio: 'inherit', env: process.env });
child.once('error', () => { console.error('Python SDK runner failed to start.'); process.exitCode = 1; });
child.once('exit', (code) => { process.exitCode = code ?? 1; });
