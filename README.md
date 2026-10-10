# 🛡️ StagingGuard

> **Zero-Trust Runtime Access Control for Autonomous SRE & DevOps Agents**  
> *Built for the AgntID Hackathon 2026 — Track: AI DevOps Incident Remediation*  
> **Solo Builder:** Akshat Naruka  

---

[![Track: AI DevOps](https://img.shields.io/badge/Hackathon%20Track-AI%20DevOps%20Incident%20Remediation-blue.svg)](#)
[![Runtime: AgntID](https://img.shields.io/badge/Control%20Plane-AgntID%20Runtime%20%3A18082-10b981.svg)](#)
[![Policy: OPA Rego](https://img.shields.io/badge/Policy%20Engine-Open%20Policy%20Agent-purple.svg)](#)
[![Protocol: MCP](https://img.shields.io/badge/Standard-Model%20Context%20Protocol-orange.svg)](#)
[![Interactive Deck](https://img.shields.io/badge/Live%20Presentation-index.html-brightgreen.svg)](index.html)

---

## 🖥️ Live Presentation & Interactive Keynote Deck

> **Try the interactive deck directly in your browser:**  
> 👉 **[Launch Interactive Keynote Deck (`index.html`)](index.html)** *(or [`presentation/index.html`](presentation/index.html))*  
>
> **Quick Terminal Command to Open:**
> ```bash
> open index.html
> # or start a local static server:
> python3 -m http.server 8000
> # then open http://localhost:8000
> ```

### What You'll Experience in `index.html`:
- **8 Minimalist Apple Keynote Slides**: Covers the April 2026 PocketOS disaster, the "Access Is Not Authority" threat model, and the AgntID runtime architecture.
- **Embedded Synchronized Terminal Videos (Slide 6)**: Side-by-side video playback comparing unconstrained agent failure vs. AgntID zero-trust enforcement.
- **Controls**: Press <kbd>→</kbd> / <kbd>←</kbd> / <kbd>Space</kbd> to navigate, <kbd>F</kbd> for Fullscreen Keynote mode, and use `[▶ Play from Start]` or `[⏸ Pause / Resume]` to review video playback.

---

## 📌 Executive Summary

Autonomous AI agents remediate infrastructure outages at machine speed. But when given broad API tokens and infrastructure tools, **prompt instructions fail, security guardrails collapse, and production environments are destroyed**.

In **April 2026**, a real-world Cursor agent running on Claude Opus 4.6 was tasked with fixing a routine credential mismatch in staging at PocketOS. In **9 seconds**, the agent discovered an API token in an unrelated file, guessed that deleting a volume would reset the database state, called `delete_volume` with zero confirmation, and **wiped the company's production database and its primary backups**.

**StagingGuard** demonstrates how **AgntID** solves this fundamental security dilemma. By acting as a transparent, zero-trust runtime proxy on the Model Context Protocol (MCP) stream, AgntID intercepts every single tool call, enforces Open Policy Agent (OPA) Rego rules on tool parameters, and dynamically restricts the visible tool surface based on protection profiles.

With StagingGuard, the agent safely diagnoses and fixes staging — while destructive tools vanish from its tool surface and sensitive production secrets are physically blocked from reaching LLM context.

---

## ⚡ The Security Dilemma: Access Is Not Authority

Most agent deployments today rely on prompt constraints (*"Please only modify staging files and do not touch production databases"*). Prompts are suggestions, not security boundaries.

```text
               ❌ UNRESTRICTED AGENTIC EXECUTION (BEFORE)
┌──────────────┐     All Tools (9)     ┌────────────────────────────────────┐
│  SRE Agent   │ ────────────────────► │ PocketOS Cloud Infrastructure      │
│  (Autonomous │                       │ • read_file(.env) -> ROOT SECRETS  │
│   LLM Loop)  │                       │ • delete_volume(vol-prod-db) -> P0 │
└──────────────┘                       └────────────────────────────────────┘
   ▲ "Fix staging"                        💥 142,500 Production Records Wiped
```

When an agent holds a master cloud credential:
1. **Scope Creep**: An agent assigned to fix staging can traverse shared cloud APIs into production storage.
2. **Credential Exfiltration**: Looking for database configs leads agents to inspect `.env` and secret files, leaking master root tokens into LLM context windows.
3. **Irreversible Destruction**: Broad tool surfaces expose operations like `delete_volume` or `drop_table`. An LLM hallucination turns into an unrecoverable outage.

---

## 🛡️ The Solution: AgntID Runtime Proxy Perimeter

StagingGuard places the **AgntID Control Plane** between the SRE Agent and the infrastructure MCP server. The agent connects to `http://127.0.0.1:18082/mcp` as a transparent drop-in replacement with **zero code modifications**.

```text
               ✅ ZERO-TRUST RUNTIME ENFORCEMENT (AFTER)
┌──────────────┐                       ┌─────────────────────────────────────┐
│  SRE Agent   │                       │      AgntID Control Plane           │
│  (Autonomous │ ─── MCP Request ────► │      Runtime Proxy (:18082)         │
│   LLM Loop)  │                       │  • Tool Discovery Reduction (Medium)│
└──────────────┘                       │  • Fine-Grained OPA Rego Engine     │
                                       │  • Task Context & Lease Tracking    │
                                       └──────────────────┬──────────────────┘
                                                          │
                                               Allowed &  │  Blocked &
                                               Sanitized  │  Audited
                                                          ▼
                                       ┌─────────────────────────────────────┐
                                       │ Upstream Infra Server (:8888)       │
                                       │ • read_file(README.md) -> ALLOWED   │
                                       │ • read_file(.env)      -> 403 DENY  │
                                       │ • delete_volume        -> HIDDEN    │
                                       │ • update_config(stag)  -> ALLOWED   │
                                       └─────────────────────────────────────┘
```

---

## ⚖️ Before vs After Comparison Matrix

| Dimension | Before AgntID (Unrestricted) | With AgntID (StagingGuard Protected) |
| :--- | :--- | :--- |
| **Tool Discovery Surface** | All 9 infra tools visible (including `delete_volume`) | **Reduced to 4 tools** via Medium Protection Profile |
| **Secret Inspection (`.env`)** | **Exfiltrated** master DB & AWS credentials | **403 Forbidden** — Intercepted by Rego input constraint |
| **Production Volume Access** | `vol-prod-db-primary` **DELETED** | **Hidden from agent**; cannot invoke what it cannot see |
| **Configuration Updates** | Arbitrary writes across environments | **Scoped**: only allowed when `env == "staging"` |
| **Human/Audit Visibility** | Blind execution; logs only reveal post-mortem | **Real-time audit log** with policy evaluation traces |
| **Business Outcome** | **P0 Outage**: 142,500 customer records lost | **100% Uptime**: Staging repaired, zero prod impact |

---

## 🎯 AgntID Policies & Governance Setup

### 1. Protection Profile: Medium
- Coarse-grained tool reduction configured on the `infra` service.
- Destructive actions (`delete_volume`, `reset_state`) are excluded from agent discovery.
- Only reviewed read actions and low-risk operational tools are published.

### 2. OPA Rego Input Constraint: `infra.read_file`
Blocks agents from reading credentials, environment variables, or private keys:
```rego
package agntid.infra.read_file

default allow = false

# Allow reading documentation and application source files
allow {
    not startswith(input.params.path, ".env")
    not contains(input.params.path, "secret")
    not endswith(input.params.path, ".pem")
    not endswith(input.params.path, ".key")
}
```

### 3. Task-Scoped Leases
- Every agent invocation operates within an AgntID task context (`task_context(client, task_id)`).
- Session credentials expire immediately upon task completion, preventing replay attacks and token reuse.

---

## 🎬 Live Interactive Presentation & Videos

The project includes an **Apple Keynote-style presentation deck** with synchronized side-by-side terminal demo videos:

- **Interactive Slide Deck**: Open [`index.html`](index.html) or [`presentation/index.html`](presentation/index.html) in any modern browser.
  - Navigate slides using <kbd>→</kbd>, <kbd>←</kbd>, or <kbd>Space</kbd>.
  - Press <kbd>F</kbd> for Fullscreen Keynote mode.
- **Side-by-Side Video Demonstration (Slide 6)**:
  - **Left Player**: [`presentation/assets/before_demo.mp4`](presentation/assets/before_demo.mp4) — The unconstrained agent triggering a P0 outage.
  - **Right Player**: [`presentation/assets/after_demo.mp4`](presentation/assets/after_demo.mp4) — AgntID intercepting illegal calls in real time.
  - Controls: `[▶ Play from Start]` resets both videos to 00:00, `[⏸ Pause / Resume]` pauses playback for live narration.

---

## 🚀 Quickstart & Reproduction Guide

### Prerequisites
- Python 3.10+
- Node.js 20+ (for local test harnesses)
- Docker & Docker Compose (for AgntID runtime)

### 1. Start the Upstream Infrastructure MCP Server
In terminal 1:
```bash
python3 server/mock_infra_server.py
```
*Starts the PocketOS mock infrastructure service listening on `http://0.0.0.0:8888/mcp`.*

### 2. Start the AgntID Runtime Proxy
In terminal 2:
```bash
cd runtime
docker compose up -d
```
*AgntID runtime links to the cloud control plane and listens on proxy port `18082`.*

### 3. Run the End-to-End Live Terminal Demonstration
In terminal 3:
```bash
python3 agent/run_full_demo.py
```
This script executes in three visual phases:
- **Phase 1 (Before)**: Demonstrates the unrestricted agent wiping the database and leaking secrets.
- **Phase 2 (Boundary Matrix)**: Displays the active AgntID policy rules and protection profile constraints.
- **Phase 3 (After)**: Directs the agent through `http://127.0.0.1:18082/mcp`, capturing live policy denials (HTTP 403) and verifying production safety.

### 4. Launch the Keynote Deck
```bash
open index.html
```

---

## 📂 Repository Structure

```text
AgntID/
├── index.html                    # Root interactive Keynote presentation deck (8 slides)
├── agent/
│   ├── run_full_demo.py          # End-to-end runnable demo script (Exit Code 0)
│   ├── sre_remediation_agent.py   # Autonomous SRE agent prompt loop
│   └── test_agntid_connection.py # Connection healthcheck against proxy :18082
├── server/
│   └── mock_infra_server.py      # Upstream PocketOS infrastructure MCP server (:8888)
├── presentation/
│   ├── index.html                # Presentation deck mirror
│   ├── generate_deck.py          # PowerPoint PPTX export generator
│   └── assets/
│       ├── before_demo.mp4       # 30fps H.264 video: Unrestricted P0 outage
│       └── after_demo.mp4        # 30fps H.264 video: AgntID protected remediation
├── policies/                     # AgntID OPA Rego policy definitions
├── runtime/
│   └── docker-compose.yml        # AgntID local runtime container definition
├── docs/
│   ├── DEMO_VIDEO_SCRIPT.md      # Timed speaker script for hackathon recording
│   ├── SUBMISSION.md             # Devfolio submission answers & worksheet
│   └── ARCHITECTURE.md           # Deep dive into zero-trust proxy boundaries
└── assets -> presentation/assets # Symlink for seamless asset resolution
```

---

## 🏆 Hackathon Metadata

- **Event**: AgntID Hackathon 2026 (Bengaluru / Hybrid)
- **Track**: AI DevOps Incident Remediation
- **Builder**: Akshat Naruka ([GitHub: @AkshatNaruka](https://github.com/AkshatNaruka))
- **Invited Judges / Collaborators**:
  - `95c8281c-cb8b-4b21-8395-5cb255552b21`
  - `61671e35-5b43-455b-b9f0-2567406ae25d`
- **Control Plane Portal**: [https://app.agntid.ai](https://app.agntid.ai)

---

*“Access is not authority. AgntID turns autonomous SRE agents from an existential infrastructure risk into a reliable, production-ready force multiplier.”*
