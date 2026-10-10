import { createHash, randomUUID } from 'node:crypto';
import { appendFile, mkdir, readFile, rename, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { z } from 'zod';
import type { TaskContext } from './config.js';

export const toolNames = ['support_get_ticket', 'support_draft_reply', 'support_send_reply'] as const;
export type ToolName = typeof toolNames[number];
export const ticketInput = z.object({ ticketId: z.string().regex(/^T\d{1,8}$/).describe('Ticket ID, for example T100.') }).strict();
export const replyInput = ticketInput.extend({ reply: z.string().trim().min(1).max(2000).describe('Exact proposed customer reply; approval is bound to this text.') }).strict();
const ticketSchema = z.object({ id: z.string(), tenantId: z.string(), subject: z.string(), message: z.string(), customer: z.string() }).strict();
const policySchema = z.object({
  version: z.literal(1), enforcement: z.literal('local-rehearsal-only'),
  rules: z.array(z.object({ tool: z.enum(toolNames), effect: z.enum(['allow', 'require_approval', 'deny']), resource: z.literal('task tenant and ticket allowlist') }).strict()),
  defaultEffect: z.literal('deny'),
}).strict();
const approvalSchema = z.object({
  requestId: z.string().regex(/^[a-f0-9]{64}$/), leaseId: z.string(), taskId: z.string(), agentId: z.string(),
  tenantId: z.string(), tool: z.literal('support_send_reply'), ticketId: z.string(), reply: z.string(), expiresAt: z.number(),
}).strict();
export type ApprovalRequest = z.infer<typeof approvalSchema>;
type Ticket = z.infer<typeof ticketSchema>;
export interface AuditEvent {
  eventId: string; time: string; enforcement: 'local-rehearsal-only';
  agentId: string; taskId: string; tool: string; ticketId: string | null;
  outcome: string; code: string;
}
export interface ToolOutcome {
  ok: boolean; enforcement: 'local-rehearsal-only'; code: string;
  data?: Record<string, unknown>; approvalRequestId?: string;
}

function isMissing(error: unknown): boolean {
  return error instanceof Error && 'code' in error && error.code === 'ENOENT';
}

export class ApprovalStore {
  constructor(readonly directory: string) {}

  private file(area: 'pending' | 'approved' | 'consumed', requestId: string) {
    if (!/^[a-f0-9]{64}$/.test(requestId)) throw new Error('Invalid approval request ID.');
    return join(this.directory, area, `${requestId}.json`);
  }

  async prepare() {
    await Promise.all(['pending', 'approved', 'consumed'].map((area) => mkdir(join(this.directory, area), { recursive: true, mode: 0o700 })));
  }

  async request(request: ApprovalRequest) {
    await this.prepare();
    try {
      await writeFile(this.file('pending', request.requestId), JSON.stringify(request, null, 2), { flag: 'wx', mode: 0o600 });
    } catch (error) {
      if (!(error instanceof Error && 'code' in error && error.code === 'EEXIST')) throw error;
    }
  }

  async review(requestId: string): Promise<ApprovalRequest> {
    return approvalSchema.parse(JSON.parse(await readFile(this.file('pending', requestId), 'utf8')));
  }

  async approve(requestId: string, now = Date.now()) {
    const request = await this.review(requestId);
    if (request.expiresAt <= now) throw new Error('Approval expired. Start a new task.');
    await rename(this.file('pending', requestId), this.file('approved', requestId));
  }

  async consume(expected: ApprovalRequest, now: number): Promise<boolean> {
    let stored: ApprovalRequest;
    try { stored = approvalSchema.parse(JSON.parse(await readFile(this.file('approved', expected.requestId), 'utf8'))); }
    catch (error) { if (isMissing(error)) return false; throw error; }
    if (stored.expiresAt <= now || JSON.stringify(stored) !== JSON.stringify(expected)) return false;
    try { await rename(this.file('approved', expected.requestId), this.file('consumed', expected.requestId)); return true; }
    catch (error) { if (isMissing(error)) return false; throw error; }
  }
}

export class RehearsalRuntime {
  readonly events: AuditEvent[] = [];
  readonly outbox: Array<{ ticketId: string; reply: string }> = [];
  private constructor(
    readonly context: TaskContext,
    readonly approvals: ApprovalStore,
    private readonly tickets: Ticket[],
    private readonly policy: z.infer<typeof policySchema>,
    private readonly clock: () => number,
    private readonly auditPath?: string,
  ) {}

  static async create(context: TaskContext, options: { directory?: string; clock?: () => number; auditPath?: string } = {}) {
    const tickets = z.array(ticketSchema).parse(JSON.parse(await readFile(new URL('../fixtures/tickets.json', import.meta.url), 'utf8')));
    const policy = policySchema.parse(JSON.parse(await readFile(new URL('../policies/rehearsal.json', import.meta.url), 'utf8')));
    const approvals = new ApprovalStore(join(options.directory ?? '.local', 'approvals'));
    await approvals.prepare();
    return new RehearsalRuntime(context, approvals, tickets, policy, options.clock ?? Date.now, options.auditPath);
  }

  private async outcome(tool: string, ticketId: string | null, result: Omit<ToolOutcome, 'enforcement'>): Promise<ToolOutcome> {
    const event: AuditEvent = {
      eventId: randomUUID(), time: new Date(this.clock()).toISOString(), enforcement: 'local-rehearsal-only',
      agentId: this.context.agentId, taskId: this.context.taskId, tool, ticketId,
      outcome: result.ok ? 'allowed' : result.code === 'APPROVAL_REQUIRED' ? 'approval_required' : 'denied', code: result.code,
    };
    if (this.auditPath) await appendFile(this.auditPath, `${JSON.stringify(event)}\n`, { mode: 0o600 });
    this.events.push(event);
    return { ...result, enforcement: 'local-rehearsal-only' };
  }

  async call(tool: string, input: unknown): Promise<ToolOutcome> {
    const schema = tool === 'support_get_ticket' ? ticketInput : replyInput;
    const parsed = schema.safeParse(input);
    if (!parsed.success) return this.outcome(tool, null, { ok: false, code: 'INVALID_INPUT' });
    const args = parsed.data;
    const ticketId = args.ticketId;
    if (this.clock() >= this.context.expiresAt) return this.outcome(tool, ticketId, { ok: false, code: 'TASK_EXPIRED' });
    const rule = this.policy.rules.find((item) => item.tool === tool);
    if (!rule || rule.effect === 'deny') return this.outcome(tool, ticketId, { ok: false, code: 'TOOL_DENIED' });
    const ticket = this.tickets.find((item) => item.id === ticketId);
    if (!this.context.ticketIds.includes(ticketId) || !ticket || ticket.tenantId !== this.context.tenantId) {
      return this.outcome(tool, ticketId, { ok: false, code: 'RESOURCE_DENIED' });
    }
    if (tool === 'support_get_ticket') return this.outcome(tool, ticketId, { ok: true, code: 'TICKET_READ', data: { ...ticket } });
    if (!('reply' in args) || typeof args.reply !== 'string') return this.outcome(tool, ticketId, { ok: false, code: 'INVALID_INPUT' });
    if (tool === 'support_draft_reply') return this.outcome(tool, ticketId, { ok: true, code: 'REPLY_DRAFTED', data: { ticketId, reply: args.reply, sent: false } });

    const requestFields = {
      leaseId: this.context.leaseId, taskId: this.context.taskId, agentId: this.context.agentId,
      tenantId: this.context.tenantId, tool: 'support_send_reply' as const, ticketId, reply: args.reply, expiresAt: this.context.expiresAt,
    };
    const request: ApprovalRequest = { requestId: createHash('sha256').update(JSON.stringify(requestFields)).digest('hex'), ...requestFields };
    if (rule.effect !== 'require_approval') return this.outcome(tool, ticketId, { ok: false, code: 'UNSAFE_LOCAL_POLICY' });
    if (!await this.approvals.consume(request, this.clock())) {
      await this.approvals.request(request);
      return this.outcome(tool, ticketId, { ok: false, code: 'APPROVAL_REQUIRED', approvalRequestId: request.requestId });
    }
    // This outbox is synthetic and in memory. No customer message is transmitted.
    const result = await this.outcome(tool, ticketId, { ok: true, code: 'REPLY_SENT_TO_FIXTURE', data: { ticketId, destination: 'synthetic in-memory outbox' } });
    this.outbox.push({ ticketId, reply: args.reply });
    return result;
  }
}
