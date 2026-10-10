# AgntID setup and integration

This guide follows the authenticated [Quick Start](https://docs.agntid.ai/quick-start/)
and the official SDK source reviewed on 9 October 2026. The full vendor
reference is saved locally at `docs/vendor/agntid-context.md`.

## Runtime installation

The official file is checked into `runtime/docker-compose.yml` without
modification. `runtime/compose.override.yml` restricts both published ports to
loopback. `runtime/.env` selects ports 18080/18082 because another project uses
8080. The installed Docker engine is OrbStack.

```sh
npm run setup
cd runtime
docker compose config --quiet
docker compose up -d --wait --wait-timeout 180
docker compose ps
```

Expect `achr-runtime` and `achr-intent-parser` to be **healthy**. Allow extra time
for the parser's first model download. The vendor recommends about 4 GB RAM
and 5 GB disk. Do not prune unrelated Docker resources to make space.

The vendor Compose tracks `:main` images. The exact installed digests, SDK
commit, Compose checksum, and downloaded-doc checksum are in
[setup-provenance.json](references/setup-provenance.json). If reproducible
image versions are needed, set `ACHR_RUNTIME_IMAGE` and
`ACHR_INTENT_PARSER_IMAGE` to those digest references in `runtime/.env` before
starting a fresh instance. Update them only after reviewing the new release.

## Link the runtime to your account

1. Open [Runtimes](https://app.agntid.ai/runtimes) in the signed-in browser.
2. Select **Add Runtime → Generate Bootstrap Token**.
3. Copy the token directly into the **Bootstrap Token** field at
   **http://127.0.0.1:18080** and select **Connect to Control Plane**.
4. Confirm the local UI shows **Operational** and **Connected**.
5. Return to Runtimes and open the new runtime. Give it a clear hackathon name
   if the UI supports renaming.

The token is one-time and time-limited. Keep it out of chat, `.env`, source
control, command history, logs, and screenshots. Once provisioned, the runtime
persists its configuration in Docker volumes. A restart normally preserves the
connection; `docker compose down -v` destroys that state and should not be used
as routine troubleshooting.

## Review setup and policy

1. In the runtime's **Setup** tab, confirm Runtime Registered, Runtime Healthy,
   MCP Support, CLI Enforcement, and Protection Profile checks.
2. Keep optional CLI enforcement off for the Quick Start. Review
   **Medium / READ_WRITE** and mark the profile reviewed.
3. Wait for **5 of 5** and **Runtime sync: Applied**.
4. Open **Operations → MCP → Servers**. Confirm the built-in `demo` server is
   enabled, connected, and exposes `demo.add_numbers`.
5. Open **Access Control → Access Policies → demo → demo.add_numbers → Baseline
   Allow Policy**. Add these inclusive input constraints and save:

| Input | Minimum | Maximum |
| --- | --- | --- |
| `first_number` | 10 | 20 |
| `second_number` | 20 | 30 |

Wait for Applied before testing. These are the vendor's Quick Start constraints;
`policies/rehearsal.json` is a separate local application policy and cannot be
uploaded as AgntID policy syntax.

## Verify without buying model calls

The official Python SDK is installed in `.local/agntid-venv` from source commit
`f4fcd2fe476f0c4dcf800e498530b7042b830f6b`, version 0.2.0. The docs recommend the
source checkout while its framework APIs are not yet available in the published
wheel. `npm run setup:sdk` recreates that isolated installation.

```sh
# Root .env: AGNTID_MCP_URL=http://127.0.0.1:18082/mcp
npm run probe:agntid
npm run smoke:agntid -- --allow-deny
```

The TypeScript probe initializes MCP and discovers tools. The Python smoke
test uses the documented task lifecycle, shortlists tools for the prompt, calls
`demo_add_numbers` through `wrap_client`, and closes every task. It expects
`(11, 21)` to return 32 and `(50, 21)` to be denied. It prints only selected
non-secret results, not raw transport errors or internal metadata.

In **Reporting**, verify the allowed tool execution and denied attempt, their
task correlation, input policy, reason, and task-close events. A failed smoke
is not an enforcement pass. A successful tool list is only connectivity.

## Simulator and Inspector

Simulator needs a Healthy AI model credential, **Simulation System** enabled
under **Operations → Configuration**, and Applied synchronization. Model calls
may cost money; use them after choosing and authorizing that provider.

After connection, compare:

```text
Use demo.add_numbers to add 11 and 21.
Use demo.add_numbers to add 50 and 21.
```

Expected outcomes are Success / result 32, and Execution Denied. Inspect the
corresponding Reporting groups. Simulator is unavailable while OAuth client
access is required; use the actual client to test that authenticated path.

Inspector can test raw MCP without a model: select the runtime, create a link,
open Inspector, choose **Direct** if needed, Connect, List Tools, and call
`demo_add_numbers`. Direct here refers to the secure AgntID runtime tunnel, not
bypassing AgntID for the raw backend. Inspector success does not validate an
external client's OAuth flow.

## Connect Codex and OpenCode

In **Runtimes → runtime → Operations → MCP → Clients**, choose Codex and **Same
machine**. Confirm the generated MCP URL uses the actual published port
**18082**, not the vendor default 8082. Merge only the generated `agntid` entry
into the existing client configuration.

For an open loopback runtime, the equivalent Codex registration is:

```sh
codex mcp add agntid --url "http://127.0.0.1:18082/mcp"
codex mcp get agntid
```

This local entry is already registered on this machine. Confirm it against the
generated configuration after provisioning rather than adding a duplicate.

If the generated configuration requires OAuth, use it exactly and run
`codex mcp login agntid`. OAuth credentials are separate from the bootstrap
token. The portal login cookie is not an MCP access token.

OpenCode remote entry shape, after confirming the portal settings:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "agntid": {
      "type": "remote",
      "url": "http://127.0.0.1:18082/mcp",
      "enabled": true
    }
  }
}
```

List tools, execute an allowed and denied call, and inspect Reporting from the
actual editor before calling its integration verified.

## Connect a project backend

Use **Operations → MCP → Servers → Add MCP**. Follow
[Add an MCP Server](https://docs.agntid.ai/mcp/attach-server/) for the supported
HTTP or local process mode, credentials, testing, discovery, classification,
and review. Docker `localhost` means the runtime container, not this Mac.

The fixture HTTP server binds only to 127.0.0.1. A runtime container cannot
reach that host service by using its own `localhost:8787`. For a real backend,
place both services on a private Docker network, or use a reviewed host route
with appropriate listener/auth settings. Do not broaden the fixture listener
or publish the runtime to the Internet merely to get a demo working. The
built-in demo tool is sufficient for initial platform setup.

After choosing the project, make its tenant/user/resource authorization real,
keep the service credentials behind AgntID, and deny alternate direct agent
routes. Approval and ephemeral credential features should be demonstrated only
after their actual configured behavior is verified. The local rehearsal's
approval/lease implementation is not evidence of those platform capabilities.
