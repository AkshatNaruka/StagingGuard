# Troubleshooting

## Docker is unavailable

Open OrbStack or Docker Desktop, then run `docker info` and
`docker compose version`. Starting the installed engine can resume other
projects' containers; leave them alone. Run Compose commands inside `runtime/`
so they use this workspace's files and selected ports.

## Port already allocated

The first setup attempt found 8080 occupied by an existing container. This
workspace uses `RUNTIME_PORT=18080` and `MCP_PORT=18082` in `runtime/.env`.
If those are also occupied, choose free local ports, update the runtime UI and
MCP URLs in your client/settings, then run `docker compose up -d` again.
Do not stop an unrelated service merely to claim its port.

## Parser startup or health is slow

```sh
cd runtime
docker compose ps
docker compose logs --tail=80 achr-intent-parser
```

The first model download is about 900 MB. Check outbound network and disk
space, and allow several extra minutes. Inspect logs locally; review and redact
them before sharing. Avoid automatic disk cleanup that removes other projects.

## Healthy but UNPROVISIONED

Docker health confirms the process runs; it does not establish account trust.
Generate a fresh one-time token in your signed-in portal and enter it directly
in the local runtime UI. Confirm Operational / Connected before client tests.
Expired or already-consumed tokens require a fresh token through the portal.

## Connected but tools missing

Check Setup, protection profile review, tool classifications/review, individual
enabled state, MCP server Applied sync, and OAuth role grants if active. A tool
can be correctly hidden by the profile. Do not loosen permissions to force it
into the list without understanding the action.

## AgntID smoke fails

Use [AGNTID.md](AGNTID.md), verify the `demo.add_numbers` policy and runtime
address, and inspect Reporting. The smoke suppresses raw errors to avoid leaking
credentials. Confirm the actual user/agent context before adapting it to a
production application. The model-free smoke uses SDK source version 0.2.0;
run `npm run setup:sdk` if the environment is missing.

## Local fixture task expires

The default rehearsal lease is 300 seconds, measured from server startup.
`TASK_EXPIRED` is an expected denial. Start a new legitimate local task/server;
approvals from a previous lease cannot be reused. `npm run demo` uses a fresh
deterministic lease and advances its clock without waiting five minutes.

## Local approval cannot be used

Review its current ID, exact text, ticket, tenant, lease, and expiry. A changed
reply needs a new request. Only one of concurrent sends can consume the same
approval. A consumed approval cannot replay. The synthetic outbox is in memory,
so a server restart does not retain sent replies.

## MCP transport issues

- Keep stdout clean for stdio; server messages go to stderr.
- The HTTP path is `/mcp`; `/health` is only a local status endpoint.
- Host and Origin guards intentionally reject untrusted browser origins.
- Docker `localhost` means the current container; see AGNTID.md for backend networking.
- The latest official TypeScript SDK uses split v2 packages. Do not mix v1
  import paths from older examples into this starter.

`npm run probe:local` tests the actual SDK transport. The tests use `node:http`
for the hostile Host check because newer Node fetch normalizes that header.

## Devfolio MCP shows not connected

Check `codex mcp get devfolio`, then `codex mcp login devfolio` if authorization
is missing. Reconnect the editor and make a read-only MCP call. A dashboard card
or config entry alone does not prove authentication. Event eligibility and
submission-opening rules can affect dashboard shortcuts.

## Stop this runtime

```sh
cd runtime
docker compose stop
# Later:
docker compose start
```

This preserves the runtime volumes and model cache. Do not use `down -v`, prune
Docker globally, or delete stored credentials as routine cleanup.
