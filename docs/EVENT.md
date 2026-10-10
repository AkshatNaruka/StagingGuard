# Event brief

Source check: **9 October 2026**. Event slug: `agntid`.

| Item | Current evidence |
| --- | --- |
| Date | 10 October 2026 |
| City | Bengaluru, India |
| Devfolio event window | 11:00–16:00 IST (`05:30–10:30 UTC`) |
| Public schedule | Check-in begins at 10:00 IST |
| Venue returned by Devfolio | 2586Labs, Indiranagar, Bengaluru; confirm in your registration |
| Account application | Submitted application found through authenticated MCP |
| Prize | Organizer description names a MacBook Neo for the winning team |
| Prize-track API | Returned an empty list; no track UUIDs can be selected from it |

Sources: [Luma event](https://luma.com/ca02ch66), [Devfolio event](https://agntid.devfolio.co/),
and the authenticated Devfolio MCP snapshot in [devfolio-event.json](references/devfolio-event.json).
The referral query token is deliberately omitted from these saved links.

## What the project must demonstrate

- A useful working AI agent or agentic workflow.
- At least one external tool.
- Permitted and restricted actions.
- AgntID enforcing the boundary during execution.
- A clear before-and-after demonstration.

Identify the agent's actions, tool/API access, allowed resources and parameters,
approval needs, user/task/environment differences, and required audit evidence.
You need only the controls that fit the workflow. Local fixture permissions
alone do not satisfy the live AgntID requirement.

## Schedule discrepancies

The public Luma page lists hacking ending at **16:00**, judging **16:00–16:30**,
demos **16:30–17:30**, and closing **17:30**. The Devfolio description lists
**15:00 demos** and **16:30 closing**. Its structured event window is
**11:00–16:00**. It also reports `is_online: true`, while the registration and
Luma page describe a Bengaluru venue. Team metadata says size **1**, while the
description speaks of teams. These are conflicting organizer records.

Use your confirmation email and the opening briefing for the final logistics,
submission deadline, attendance mode, and team rule. Keep a working demo ready
before 15:00 until the organizer confirms otherwise. This is a planning choice,
not a claimed official deadline.

## Suggested event work plan

| Time, IST | Work |
| --- | --- |
| Before the event | Finish provisioning and the documented allow/deny test; read the conduct rules |
| 10:00–11:00 | Check in and confirm venue, team rules, schedule, and preparation-code policy |
| 11:15 walkthrough | Confirm real policy and approval capabilities with AgntID support |
| 12:00–12:30 | Choose one useful workflow, external tool, and measurable boundary |
| 12:30–13:30 | Implement the smallest complete agent path through AgntID |
| 13:30–14:15 | Exercise allow/deny cases, confirm no blocked side effect, inspect Reporting |
| 14:15–14:45 | Capture real screenshots, rehearse, complete the submission worksheet |
| After 14:45 | Keep a stable demo ready; follow the confirmed organizer schedule |

## Links

- [AgntID Quick Start](https://docs.agntid.ai/quick-start/)
- [AgntID portal](https://app.agntid.ai/)
- [Devfolio dashboard](https://agntid.devfolio.co/dashboard)
- [Devfolio MCP guide](https://guide.devfolio.co/docs/guide/devfolio-mcp)
- [Code of Conduct](https://devfolio.co/code-of-conduct)
- [Devfolio terms](https://devfolio.co/terms-and-conditions)

No invitation token, bootstrap token, personal application answer, or credential
is stored in this brief.
