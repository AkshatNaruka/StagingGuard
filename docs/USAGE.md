# Local usage

## Commands

Run commands from the repository root unless stated otherwise.

| Command | Behavior |
| --- | --- |
| `npm ci` | Install the locked Node dependencies |
| `npm run setup` | Create missing `.env` files and local directories |
| `npm run doctor` | Report prerequisite/configuration status without printing credentials |
| `npm run check` | Typecheck, execute seven tests, build JavaScript |
| `npm run dev` | Start the fixture MCP server on 127.0.0.1:8787 |
| `npm start` | Run the compiled fixture server; build first |
| `npm run demo` | Run nine deterministic local permission scenarios |
| `npm run probe:local` | Start an ephemeral HTTP MCP server and verify real client calls |
| `npm run approve -- ID` | Show the exact pending synthetic reply to a local reviewer |
| `npm run approve -- ID --yes` | Approve that request once, before its lease expires |
| `npm run setup:sdk` | Install the reviewed official Python SDK in `.local/` |
| `npm run probe:agntid` | Test live MCP discovery; does not prove enforcement |
| `npm run smoke:agntid -- --allow-deny` | Call the documented demo tool using the official task lifecycle |

Root `.env` settings are automatically loaded by these npm commands. Review
[.env.example](../.env.example) for setting names; keep actual values local.

## The fixture tools

| Tool | Example arguments | Local behavior |
| --- | --- | --- |
| `support_get_ticket` | `{"ticketId":"T100"}` | Return a synthetic ticket in the trusted task scope |
| `support_draft_reply` | `{"ticketId":"T100","reply":"Use the reset link."}` | Return unsent text |
| `support_send_reply` | `{"ticketId":"T100","reply":"Use the reset link."}` | Require reviewer approval, then append to an in-memory synthetic outbox |

All inputs reject extra fields. An agent cannot supply its own tenant, approval,
agent ID, task ID, or expiry. Trusted context comes from server configuration.
The default task allows only tenant `acme`, ticket `T100`, for 300 seconds.
`T101` is outside the task; `T200` belongs to another tenant.

The task lease starts once per server process. HTTP request recreation does not
extend it. Restarting the process creates a new lease and invalidates approvals
from its previous instance. This process-wide model is for a single-user
rehearsal, not an authenticated multi-user service.

## Manual approval rehearsal

1. Start `npm run dev` in one terminal and connect an MCP client to
   `http://127.0.0.1:8787/mcp`.
2. Read T100, draft a response, then call `support_send_reply` with the exact text.
3. The tool returns `APPROVAL_REQUIRED` and an `approvalRequestId`. No reply has
   been sent, even to the synthetic outbox.
4. In a separate reviewer terminal, run `npm run approve -- <ID>`. Inspect the
   ticket, task, tenant, reply text, and expiry.
5. Approve with `npm run approve -- <ID> --yes`.
6. Retry the exact send arguments before expiry. The response is
   `REPLY_SENT_TO_FIXTURE`. Changed text needs a new approval, and the consumed
   approval cannot execute twice.

The reviewer command is outside MCP. In a real application, the agent process
must not have shell access to the reviewer store. This local same-user filesystem
workflow is not a secure boundary against arbitrary host access.

## Error codes

| Code | Meaning and next step |
| --- | --- |
| `INVALID_INPUT` | Use the documented fields and reply length of 1–2000 characters |
| `RESOURCE_DENIED` | Resource is outside the task/tenant or unavailable; do not broaden the task automatically |
| `TOOL_DENIED` | Tool is not allowed by the local policy |
| `APPROVAL_REQUIRED` | A separate reviewer must inspect the exact request |
| `TASK_EXPIRED` | Start a new legitimate task; existing approvals are invalid |
| `UNSAFE_LOCAL_POLICY` | Keep the fixture write tool approval-gated |

## Audit and artifacts

The running fixture server appends local outcomes to `.local/audit.jsonl`. Each
entry has an event ID, timestamp, tool, ticket ID, task ID, agent ID, outcome,
and error code. Reply contents and credentials are excluded. Pending approval
files contain synthetic reply text and stay under ignored `.local/approvals/`.

`npm run demo` creates:

- `artifacts/local-rehearsal.json`: expected outcomes for all nine scenarios.
- `artifacts/local-audit.jsonl`: the corresponding local audit events.

Every record identifies `local-rehearsal-only`. These files are not AgntID audit
records. The outbox is in memory and resets when the process exits.

## Add your project's tools

Keep tool registration in `src/tools.ts`, domain behavior behind a small
service boundary, and schemas near the behavior they validate. Use actual API
authorization and resource ownership checks in the service. The fixture tools
are examples; replace their synthetic storage when you choose the project.

Register the final backend with AgntID using its portal-generated configuration.
Give the model only task-shortlisted business tools and route calls through the
official SDK wrapper or protected MCP client. Keep lifecycle/approval controls
outside the model's tool list. See [architecture](ARCHITECTURE.md).
