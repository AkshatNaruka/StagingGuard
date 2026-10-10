import assert from 'node:assert/strict';
import { test } from 'node:test';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createContext } from '../src/config.js';
import { RehearsalRuntime } from '../src/runtime.js';

async function withRuntime(run: (runtime: RehearsalRuntime, expire: () => void) => Promise<void>, env: NodeJS.ProcessEnv = {}) {
  const directory = await mkdtemp(join(tmpdir(), 'agntid-starter-'));
  let now = 1_000_000;
  const context = createContext(now, env);
  const runtime = await RehearsalRuntime.create(context, { directory, clock: () => now });
  try { await run(runtime, () => { now = context.expiresAt; }); }
  finally { await rm(directory, { recursive: true, force: true }); }
}

test('task scope denies same-tenant and cross-tenant tickets without leaking data', async () => {
  await withRuntime(async (runtime) => {
    assert.equal((await runtime.call('support_get_ticket', { ticketId: 'T100' })).ok, true);
    for (const ticketId of ['T101', 'T200', 'T999']) {
      const result = await runtime.call('support_get_ticket', { ticketId });
      assert.equal(result.code, 'RESOURCE_DENIED'); assert.equal(result.data, undefined);
    }
  });
});

test('tenant check still applies when a ticket is on the task allowlist', async () => {
  await withRuntime(async (runtime) => {
    assert.equal((await runtime.call('support_get_ticket', { ticketId: 'T200' })).code, 'RESOURCE_DENIED');
  }, { DEMO_TICKET_IDS: 'T100,T200' });
});

test('tool inputs cannot choose tenant, extend expiry, or approve their own writes', async () => {
  await withRuntime(async (runtime) => {
    for (const extra of [{ tenantId: 'zen' }, { expiresAt: 999999999 }, { approved: true }]) {
      assert.equal((await runtime.call('support_get_ticket', { ticketId: 'T100', ...extra })).code, 'INVALID_INPUT');
    }
    assert.equal((await runtime.call('approve', { ticketId: 'T100', reply: 'yes' })).code, 'TOOL_DENIED');
    assert.equal(runtime.outbox.length, 0);
  });
});

test('approval is bound to exact text and consumed once under concurrent retries', async () => {
  await withRuntime(async (runtime) => {
    const args = { ticketId: 'T100', reply: 'Use the reset link.' };
    const pending = await runtime.call('support_send_reply', args);
    assert.equal(pending.code, 'APPROVAL_REQUIRED'); assert.equal(runtime.outbox.length, 0);
    assert.ok(pending.approvalRequestId);
    await runtime.approvals.approve(pending.approvalRequestId, 1_000_000);
    assert.equal((await runtime.call('support_send_reply', { ...args, reply: 'Different reply.' })).code, 'APPROVAL_REQUIRED');
    const results = await Promise.all([runtime.call('support_send_reply', args), runtime.call('support_send_reply', args)]);
    assert.equal(results.filter((result) => result.ok).length, 1);
    assert.equal(runtime.outbox.length, 1);
    assert.equal((await runtime.call('support_send_reply', args)).code, 'APPROVAL_REQUIRED');
  });
});

test('lease expiry blocks reads and approved writes at the boundary', async () => {
  await withRuntime(async (runtime, expire) => {
    const args = { ticketId: 'T100', reply: 'Use the reset link.' };
    const pending = await runtime.call('support_send_reply', args); assert.ok(pending.approvalRequestId);
    await runtime.approvals.approve(pending.approvalRequestId, 1_000_000);
    expire();
    assert.equal((await runtime.call('support_get_ticket', { ticketId: 'T100' })).code, 'TASK_EXPIRED');
    assert.equal((await runtime.call('support_send_reply', args)).code, 'TASK_EXPIRED');
    assert.equal(runtime.outbox.length, 0);
  });
});

test('audit events include allow and deny outcomes while excluding reply contents', async () => {
  await withRuntime(async (runtime) => {
    await runtime.call('support_get_ticket', { ticketId: 'T100' });
    await runtime.call('support_send_reply', { ticketId: 'T100', reply: 'private-synthetic-body' });
    await runtime.call('support_get_ticket', { ticketId: 'T200' });
    assert.deepEqual(runtime.events.map((event) => event.outcome), ['allowed', 'approval_required', 'denied']);
    assert.ok(!JSON.stringify(runtime.events).includes('private-synthetic-body'));
  });
});
