# Setup status

Checked on **9 October 2026** in `/Users/akshatnaruka/Desktop/AgntID`.

## Latest readiness recheck

- Both Docker containers remain **Healthy**, and `npm run doctor` passes its
  infrastructure checks.
- Local UI remains **OPERATIONAL / Connected**, with mTLS **Active** and
  policy sync **Success** (1 policy loaded).
- Fresh MCP discovery succeeds with **6 visible tools**. The earlier count of
  11 below is historical, before account provisioning completed.
- A fresh `npm run smoke:agntid` **fails** after discovering those 6 tools.
  Successful protected execution has therefore not been established.
- The runtime UI's live-updates WebSocket reports HTTP 404 and **Offline**;
  the control-plane connection remains Connected.

The development base is ready for the event; the live integration is not yet
fully verified. Complete the checks below before relying on a protected demo.

## Verified

- Empty workspace initialized as a local Git repository on `main`; no remote or
  publication was created.
- TypeScript starter with pinned MCP v2 dependencies installed; npm reported
  zero dependency vulnerabilities at installation time.
- Typecheck, **7 tests**, JavaScript build, **9 local rehearsal scenarios**, and
  a real MCP client initialize/discovery/allow/deny probe passed.
- Codex `devfolio` MCP registered; OAuth reported **Successfully logged in**.
  Authenticated event/application/track/submission-guide reads succeeded.
- AgntID portal and docs read through the existing authenticated Chrome session.
- Official AI-ready documentation downloaded locally with checksum recorded.
- OrbStack started, official AgntID Compose pulled, parser model initialized;
  **both containers are Healthy**.
- Runtime UI at **http://127.0.0.1:18080**; MCP port **18082**. Both published
  ports restricted to 127.0.0.1. Port 8080 conflict was resolved without stopping
  the existing container.
- Official Python SDK **0.2.0**, reviewed source commit
  `f4fcd2fe476f0c4dcf800e498530b7042b830f6b`, installed in an isolated Python
  **3.11.16** environment. Import and required task API checks passed.
- Model-free official SDK smoke client created and syntax-checked.
- Local `agntid` MCP registered in Codex at
  `http://127.0.0.1:18082/mcp`. A real MCP discovery returned **11 visible tools**.
- Account linking completed with the approved one-time bootstrap token entered
  directly into the local UI. The runtime displays **OPERATIONAL**, **Connected**,
  and mTLS **Active**. No bootstrap token was saved in chat or repository files.
- Portal confirms runtime `f8076e02-b582-4644-8817-f0237f21d873` is
  **Active / Healthy**; Setup currently reports **4 of 5** steps complete.
- The official SDK smoke reached the runtime and attempted `(11, 21)`;
  it returned **denied** while the runtime was unprovisioned. This is a failed
  readiness test, not the desired allowed/denied policy demonstration.

## Account-dependent steps pending

- Review Medium / READ_WRITE, confirm Setup 5 of 5 and Applied synchronization.
- Add the documented numeric input policy to `demo.add_numbers`.
- Verify allowed/denied calls and matching AgntID Reporting records.
- Copy the runtime's generated editor client configuration and test that editor
  path, including OAuth if configured.

The local UI is **OPERATIONAL / Connected**. At the last portal inspection,
the protection profile review remained pending and the portal reported
**No MCP connected**, despite the local UI showing the built-in demo as Healthy.
The portal's current setup progress has not been rechecked. Resolve any remaining
readiness mismatch and verify the policy demonstration before claiming live
AgntID enforcement.

## Project and submission work

This is a base setup. No finished event project, live external-tool integration,
paid model call, published site, remote Devfolio draft, screenshot upload, or
submission has been created. The support workflow is a synthetic fixture
example. Choose the final project and verify organizer preparation-code rules
at the event.

Luma and Devfolio schedules differ; attendance/team metadata also conflicts.
See EVENT.md and confirm logistics with the organizer. The tracks API returned
no configured prize tracks.

## Repeat verification

```sh
npm run setup
npm run check
npm run demo
npm run probe:local
npm run doctor
cd runtime
docker compose ps
```

After provisioning and policy synchronization:

```sh
npm run probe:agntid
npm run smoke:agntid -- --allow-deny
```

Compare the result to the matching platform Reporting records before recording
the AgntID allow/deny demonstration as verified.
