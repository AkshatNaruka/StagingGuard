# 🎬 StagingGuard: 3-Minute Demo Video Recording Script & Guide

This document gives you the **exact, word-for-word presenter script** and **screen-recording storyboard** for presenting **StagingGuard** at the **AgntID Hackathon 2026**.

---

## 📋 Pre-Recording Setup Checklist (Takes 1 Minute)

1. **Launch Recordly**:
   - Recordly is already opened (or open it with `open /Applications/Recordly.app`).
   - Select **Screen Recording** (Full Screen or Browser Window).
   - Ensure your microphone is enabled.

2. **Open the Pitch Deck in your browser**:
   ```bash
   open presentation/index.html
   ```
   *(Press `F` to enter full-screen presentation mode)*

3. **Open AgntID Portal in a second browser tab**:
   - `https://app.agntid.ai`
   - Navigate to: **Access Policies** $\to$ click on `agntid.tools.infra.read_file` (Rego Editor).
   - Have the **Reporting** tab ready to show live audit logs.

4. **Have your terminal ready in another window**:
   - Run the presentation runner:
   ```bash
   PYTHONPATH=. .local/agntid-venv/bin/python3 agent/run_full_demo.py
   ```

---

## ⏱️ Video Storyboard & Word-for-Word Script (Target: 2 min 45 sec)

### 🔹 Scene 1: Introduction & The Core Problem (0:00 - 0:35)
**Screen to Show:** Pitch Deck (`presentation/index.html`) — **Slide 1 & Slide 2**

> **Presenter Script:**
> *"Hi everyone, I'm Akshat, and this is **StagingGuard** — zero-trust runtime access control for autonomous AI DevOps agents, built for the AgntID Hackathon.*
> 
> *Today, autonomous SRE agents are given powerful infrastructure tools over MCP to diagnose errors and fix services. But the reality is: LLM agents are unpredictable. When an agent is given raw tool credentials without runtime boundaries, prompt engineering alone cannot stop multi-step reasoning drift or prompt injection. A simple instruction to fix staging can quickly escalate into inspecting sensitive files, exposing master keys, or wiping production databases."*

---

### 🔹 Scene 2: Part 1 — The Catastrophic "Before" Run (0:35 - 1:15)
**Screen to Show:** Pitch Deck — **Slide 3** (or Terminal running Part 1)

> **Presenter Script:**
> *"Let's look at our first requirement: **What the agent could do before AgntID**.*
> 
> *Here, our agent was given a standard prompt: 'Staging deploy is failing. Find the cause and fix it.'*
> 
> *First, it inspected the staging logs and found a credential error. Looking for credentials, it autonomously called `read_file` on `.env`. Without any runtime policy, it immediately extracted master AWS keys and production database tokens.*
> 
> *Then, believing it needed to clean up disk space, it called `delete_volume` on our production database `vol-prod-db-primary`. In seconds, 142,500 customer records were wiped out, creating a catastrophic production outage — while staging remained completely broken."*

---

### 🔹 Scene 3: Part 2 — The Intended Boundary Matrix (1:15 - 1:40)
**Screen to Show:** Pitch Deck — **Slide 4 & Slide 5** (or AgntID Portal Policy Editor)

> **Presenter Script:**
> *"Here is **what the agent should actually be allowed to do**.*
> 
> *Under the principle of least privilege, our SRE agent should only have read access to staging diagnostics, documentation files, and config updates strictly scoped to the staging environment.*
> 
> *It should **never** be able to read credential files like `.env`, and destructive actions like `delete_volume` should not even be visible in its tool catalog.*
> 
> *To enforce this, we placed AgntID as a transparent runtime proxy between the agent and our infrastructure MCP server."*

---

### 🔹 Scene 4: Part 3 — AgntID Live Runtime Interception (1:40 - 2:25)
**Screen to Show:** Browser showing **AgntID Web Portal** (`https://app.agntid.ai`) + Live Terminal / Deck Slide 6

> **Presenter Script:**
> *(Switch to AgntID Web Portal tab)*
> *"Here in the AgntID Control Plane, we configured two critical layers:*
> *1. A **Medium Protection Profile**, which automatically hides unreviewed, high-risk tools like `delete_volume` so the agent cannot hallucinate or invoke them.*
> *2. A custom **OPA Rego Access Policy** on `infra.read_file` that denies any path containing `.env`, `secret`, or SSH keys.*
> 
> *(Switch to Terminal or Deck Slide 6)*
> *Now, watch what happens when the exact same agent runs through the AgntID Runtime Proxy:*
> 
> *The agent starts by reading staging logs — **ALLOWED** under the Medium profile.*
> *Next, it attempts to read `.env`. Immediately, AgntID intercepts and **DENIES** the call with an OPA Rego policy violation. The secret never enters the LLM's context!*
> *Next, when the agent queries its tool list to delete volumes, `delete_volume` is completely hidden from its tool catalog.*
> *Finally, the agent applies the config fix exclusively to `staging` — which AgntID **ALLOWS**. Staging is restored to healthy, and production was 100% protected!"*

---

### 🔹 Scene 5: Results Scorecard & Conclusion (2:25 - 2:45)
**Screen to Show:** Pitch Deck — **Slide 7 & Slide 8** (Before vs After Scorecard)

> **Presenter Script:**
> *"To summarize the transformation:*
> - *Production Uptime went from **CATASTROPHIC OUTAGE** to **100% OPERATIONAL**.*
> - *Customer records lost went from **142,500 ERASED** to **ZERO**.*
> - *Secrets went from **LEAKED** to **PROTECTED**.*
> - *And every single allow and deny decision is captured with full audit evidence in the AgntID dashboard.*
> 
> *Both hackathon organizer UUIDs have been invited as collaborators in the AgntID portal. Thank you!"*

---

## 🖥️ How to Run Everything Right Now

1. **Launch the presentation deck**:
   ```bash
   open /Users/akshatnaruka/Desktop/AgntID/presentation/index.html
   ```

2. **Open the PPTX file (if you prefer Keynote/PowerPoint)**:
   ```bash
   open /Users/akshatnaruka/Desktop/AgntID/presentation/StagingGuard_AgntID_Pitch.pptx
   ```

3. **Run the interactive live demo in terminal**:
   ```bash
   PYTHONPATH=. .local/agntid-venv/bin/python3 agent/run_full_demo.py
   ```

4. **Record your screen with Recordly**:
   - Hit Record in Recordly.
   - Walk through the slides and tabs using the script above.
   - Stop recording and save the `.mp4` video.
