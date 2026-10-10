# StagingGuard: Devfolio Submission Worksheet

Event: **AgntID Hackathon**, Saturday 10 October 2026, Bengaluru  
Builder: **Akshat Naruka** (Solo Builder)  
Project Name: **StagingGuard**  
Tagline: **Runtime access control keeping SRE and DevOps agents inside staging and away from production disaster.**

---

## Identity and links

| Field | Value |
| :--- | :--- |
| **Project Name** | StagingGuard |
| **Tagline** | Runtime access control keeping SRE agents inside staging and away from prod disaster. |
| **Technologies** | AgntID Runtime Proxy, MCP (Model Context Protocol), FastMCP, Python 3.11, Docker, OrbStack |
| **Public Repository** | https://github.com/akshatnaruka/StagingGuard (or current repo URL) |
| **Demo / Video Link** | [Demo Recording / Backup Video] |
| **Platform** | macOS / Linux / Docker / Cloud |

---

## 1. The problem it solves
**Organizer Field UUID:** `95c8281c6a904f6eb0e177f75307f4a4` (Required to publish)

In real-world DevOps environments, engineering teams increasingly deploy autonomous AI agents (powered by Claude or Cursor) to diagnose staging deployment failures, parse logs, and remediate service outages. However, granting autonomous agents access to infrastructure tools (Model Context Protocol servers) creates catastrophic security and operational risks. Because agents operate dynamically, a prompt injection, hallucination, or over-broad credential exposure can cause the agent to step outside staging boundaries and execute irreversible destructive actions in production.

This scenario directly replays the April 2026 PocketOS incident: a coding agent tasked with fixing a routine staging deploy hit an authentication failure, parsed a repository `.env` file containing over-broad cloud tokens, and executed a volume deletion against the production database cluster (`vol-prod-db-primary`), wiping 142,500 customer records and automated snapshot backups.

**How StagingGuard Solves It:**
StagingGuard inserts AgntID as a customer-hosted runtime MCP proxy between the DevOps agent and the infrastructure MCP server. Instead of static coarse-grained API keys, AgntID intercepts and evaluates every individual tool execution at runtime:
1. **Visibility Filtering (Protection Profile):** Only tools relevant to routine operations are surfaced to the agent; dangerous unapproved primitives are hidden or cataloged.
2. **Parameter-Level Boundary Enforcement:** Parameter policies guarantee that write and modification tools (`update_config`, `delete_volume`) can only execute when `env == "staging"`. Any attempt to target `prod` is denied at the proxy layer before the tool executes.
3. **Secret Protection:** Read policies block access to files matching `.env` or credential paths, preventing token leakage.
4. **Human-in-the-Loop Escalation:** Sensitive actions like `restart_service` require human operator approval before execution resumes.
5. **Auditable Attribution:** Every allowed call and denied violation is recorded in AgntID Reporting with task correlation IDs and policy details.

The result: The agent successfully diagnoses and remediates the staging deploy without touching production infrastructure or exposing master credentials.

---

## 2. Challenges we ran into
**Organizer Field UUID:** `61671edfc8ca422aab34acb24586e5d2` (Required to publish)

1. **Docker Container Loopback Networking with Remote MCP Servers:**
   The customer-hosted AgntID runtime (`achr-runtime`) runs inside a Docker container. When registering the mock infrastructure MCP server running on the macOS host, specifying `localhost:8888` failed because `localhost` resolved inside the container namespace. We resolved this by binding the mock server to `0.0.0.0:8888` and using the host gateway address `http://host.docker.internal:8888/sse`. We verified end-to-end HTTP/SSE streaming reachability from inside the runtime container via `curl -I http://host.docker.internal:8888/sse`.

2. **Port Conflict on Port 8080:**
   The default AgntID compose specification binds to `8080` (Runtime UI) and `8082` (MCP endpoint), which conflicted with an existing local service. We adapted the Docker Compose mapping to loopback ports `127.0.0.1:18080` and `127.0.0.1:18082`, ensuring isolated, secure communication.

3. **Runtime Policy Synchronization:**
   Changes made in the AgntID Portal require synchronization across the control plane to the local runtime. We incorporated checks for `Runtime sync: Applied` and implemented structured `DenialResult` handling in our Python agent loop using `agntid.wrap_client` and `getattr(result, 'denied', False)`, allowing the agent to gracefully adapt its plan after a policy denial rather than crashing.

---

## 3. Screenshots Checklist (1 to 6)

| # | Screenshot Content | Where to Capture |
| :--- | :--- | :--- |
| **1** | Terminal output of the **Before Run** showing unconstrained agent wiping prod volume (142,500 records erased) | Run `agent/replay_before_after.py` |
| **2** | Terminal output of the **After Run** showing AgntID intercepting the destructive call (`Execution Denied`) and allowing staging fix | Run `agent/replay_before_after.py` or `agent/live_agntid_test.py` |
| **3** | AgntID Portal **Runtimes** tab showing runtime status **Operational / Connected** (5 of 5 checks green) | `app.agntid.ai` $\to$ Runtimes |
| **4** | AgntID Portal **Operations → MCP → Servers** showing `stagingguard` attached and applied | `app.agntid.ai` $\to$ MCP Servers |
| **5** | AgntID Portal **Reporting Dashboard** showing the live audit trail of allowed staging calls and intercepted production denials | `app.agntid.ai` $\to$ Reporting |
| **6** | AgntID Portal **Access Control → Policies** showing parameter rule `env == "staging"` | `app.agntid.ai` $\to$ Access Control |
