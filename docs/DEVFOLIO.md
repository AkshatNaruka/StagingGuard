# Devfolio MCP and submissions

Devfolio MCP is registered globally in Codex as `devfolio` at
`https://mcp.devfolio.co/mcp`. OAuth completed successfully and authenticated
MCP calls fetched this account's submitted `agntid` application, event details,
tracks, and submission guide on 9 October 2026.

## Codex

```sh
codex mcp get devfolio
```

For another machine or missing configuration:

```sh
codex mcp add devfolio --url "https://mcp.devfolio.co/mcp"
codex mcp login devfolio
```

Authorize the client in the browser if prompted. Restart/reconnect the editor's
MCP session if the tools do not appear after registration. The supported setup
is documented in the [Devfolio MCP guide](https://guide.devfolio.co/docs/guide/devfolio-mcp).
Existing OAuth storage belongs to Codex; do not copy or inspect it to build this
project.

## OpenCode

Merge [opencode.example.json](../configs/opencode.example.json) into your
existing project or user config. Keep other MCP entries and settings. This
workspace stores an example; it does not overwrite any installed OpenCode
configuration.

## Useful read-only prompts

```text
Read my AgntID Hackathon application and event requirements. Do not modify them.
Fetch the submission guide for hackathon slug agntid and check this repository against it.
Review the local submission worksheet and identify missing evidence. Do not publish.
Read the current prize tracks and explain eligibility using returned track IDs.
```

Tool ordering: resolve the actual event from your account, read its details,
then load `getProjectSubmissionGuide` and `getHackathonTracksAndPrizes` before
creating or updating any project. This event's tracks API currently returns an
empty list; the prize appears in the event description. Do not invent a track
or reuse a prize UUID as a track ID.

## Current submission contract

See the exact source snapshot at [submission-guide.json](references/submission-guide.json).
Re-fetch it before submitting because organizers can change requirements.

| Field | Current rule |
| --- | --- |
| Name | 2–50 characters to publish; needed for a draft |
| Tagline | 2–50 characters to publish; needed for a draft |
| Technologies / `hashtags` | 1–10 to publish |
| Screenshots / `pictures` | 1–6 real screenshots to publish |
| Links | Up to 5; include repository when available |
| Platforms | Up to 5 |
| Commit message, if supplied | 2–50 characters to publish |
| Demo video, logo, cover | Optional; use real project assets |
| Organizer answers | Both required fields below must be answered to publish |

Required organizer fields:

1. **The problem it solves** — UUID `95c8281c6a904f6eb0e177f75307f4a4`.
   Describe the workflow, real AgntID controls, where they apply, and a
   before-and-after example.
2. **Challenges we ran into** — UUID `61671edfc8ca422aab34acb24586e5d2`.
   State the actual hurdle, fix, and any remaining limitation.

Devfolio explicitly requires screenshots of the running project, not generated
stand-ins. Drafts may omit publish-only fields, but supplied values still must
respect formats and maximum lengths. The locally saved worksheet is not a
Devfolio draft or submission.

## Drafting and publishing

Prepare [SUBMISSION.md](SUBMISSION.md) with facts from the finished build. Check
the final payload against the freshly fetched guide and verify URLs/assets.
Create a remote draft or publish only when the user asks for that action.
The setup request authorizes the connection and local preparation, not a
public project submission.

Manage/revoke client authorization through **Account Settings → MCP → Connected
clients**. Registration does not automatically subscribe to announcements,
change the application, invite teammates, or RSVP to another event.
