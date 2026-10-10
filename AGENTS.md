# AgntID Hackathon workspace

Read README.md and docs/STATUS.md before changing the integration. Use Node.js,
TypeScript strict mode, the official MCP v2 SDK, and npm with package-lock.json.

## Boundaries

- This is pre-event preparation and a reusable starter. Do not present it as a
  completed hackathon entry or claim live AgntID enforcement without evidence.
- `src/runtime.ts` is a local permission rehearsal. `policies/rehearsal.json`
  belongs to this app, not to AgntID. Do not invent AgntID SDK names or API paths.
- Never read, print, commit, or return `.env`, auth values, OAuth storage, or
  invitation links. Use `.env.example` for documented setting names.
- Keep approval authority outside the MCP tool surface. A tool caller must never
  grant itself approval, choose its trusted tenant, or extend its lease.
- In live mode route every agent tool call through the platform-issued AgntID
  proxy. Direct backend access is only for local rehearsal and diagnosis.
- Do not publish, submit to Devfolio, upload screenshots, message organizers,
  spend credits, or deploy until the user authorizes that action.
- Preserve existing user configuration. Read status through supported CLIs;
  update only the named MCP entry.

## Verification and documentation

Run `npm run check`, `npm run demo`, and `npm run probe:local` for backend changes.
Update docs/STATUS.md with what was actually verified and remaining login steps.
Keep event claims linked to sources. Separate synthetic data and local evidence
from platform audit records. Generated artifacts stay in ignored artifacts/.

The schema skill concerns public JSON-LD. This repo has no public event or
product webpage. Follow docs/SCHEMA.md if one is later added; never invent a
venue, reviews, offers, price, or official affiliation.
