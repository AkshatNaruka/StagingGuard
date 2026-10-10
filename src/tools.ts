import { McpServer } from '@modelcontextprotocol/server';
import type { CallToolResult } from '@modelcontextprotocol/server';
import { z } from 'zod';
import { RehearsalRuntime, ticketInput, replyInput } from './runtime.js';

const outputSchema = z.object({
  ok: z.boolean(), enforcement: z.literal('local-rehearsal-only'), code: z.string(),
  data: z.record(z.string(), z.unknown()).optional(), approvalRequestId: z.string().optional(),
});

export function createToolServer(runtime: RehearsalRuntime): McpServer {
  const server = new McpServer({ name: 'support-rehearsal-mcp-server', version: '0.1.0' });
  const definitions = [
    { name: 'support_get_ticket', title: 'Read support ticket', description: 'Read a synthetic support ticket within this server task tenant and ticket scope. Returns ticket details or a denial.', schema: ticketInput, readOnly: true },
    { name: 'support_draft_reply', title: 'Draft support reply', description: 'Prepare a reply for a permitted synthetic support ticket. Returns the unsent text; nothing is transmitted.', schema: replyInput, readOnly: true },
    { name: 'support_send_reply', title: 'Send reply to fixture outbox', description: 'Add an approved reply to the synthetic in-memory outbox. Requires separate local reviewer approval of the exact text. No real messages are sent.', schema: replyInput, readOnly: false },
  ];
  for (const definition of definitions) {
    server.registerTool(definition.name, {
      title: definition.title, description: definition.description, inputSchema: definition.schema, outputSchema,
      annotations: { readOnlyHint: definition.readOnly, destructiveHint: false, idempotentHint: definition.readOnly, openWorldHint: false },
    }, async (args): Promise<CallToolResult> => {
      try {
        const result = await runtime.call(definition.name, args);
        return { content: [{ type: 'text', text: JSON.stringify(result) }], structuredContent: { ...result }, isError: !result.ok };
      } catch {
        return { content: [{ type: 'text', text: 'Local tool failed. Inspect local storage permissions and restart the rehearsal.' }], isError: true };
      }
    });
  }
  return server;
}
