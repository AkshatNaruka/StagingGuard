import { z } from 'zod';
import { randomUUID } from 'node:crypto';

const id = z.string().regex(/^[a-zA-Z0-9_-]{1,64}$/);
const envSchema = z.object({
  PORT: z.coerce.number().int().min(1).max(65535).default(8787),
  TRANSPORT: z.enum(['http', 'stdio']).default('http'),
  DEMO_AGENT_ID: id.default('support-agent'),
  DEMO_TASK_ID: id.default('reply-to-t100'),
  DEMO_TENANT_ID: id.default('acme'),
  DEMO_TICKET_IDS: z.string().default('T100').transform((value) => value.split(',').map((item) => item.trim())).pipe(z.array(id).min(1)),
  DEMO_TASK_TTL_SECONDS: z.coerce.number().int().min(1).max(3600).default(300),
});

export interface TaskContext {
  readonly leaseId: string;
  readonly agentId: string;
  readonly taskId: string;
  readonly tenantId: string;
  readonly ticketIds: readonly string[];
  readonly expiresAt: number;
}

export function readConfig(env: NodeJS.ProcessEnv = process.env) {
  const parsed = envSchema.safeParse(env);
  if (!parsed.success) throw new Error('Invalid local settings. Check PORT, TRANSPORT, IDs, ticket list, and TTL in .env.');
  return parsed.data;
}

export function createContext(now = Date.now(), env: NodeJS.ProcessEnv = process.env): TaskContext {
  const config = readConfig(env);
  return Object.freeze({
    leaseId: randomUUID(),
    agentId: config.DEMO_AGENT_ID,
    taskId: config.DEMO_TASK_ID,
    tenantId: config.DEMO_TENANT_ID,
    ticketIds: Object.freeze(config.DEMO_TICKET_IDS),
    expiresAt: now + config.DEMO_TASK_TTL_SECONDS * 1000,
  });
}
