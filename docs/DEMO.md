# Demo runbook

## Setup rehearsal

```sh
npm run check
npm run demo
npm run probe:local
```

The local script shows nine verified scenarios: T100 read allowed; T101 and
T200 reads denied; drafting allowed; send awaiting approval; changed reply
awaiting new approval; exact approved send executed in the fixture outbox;
approval replay stopped; expired task stopped. Label this as a local rehearsal.

## Prove the platform setup

1. Show both official containers Healthy and the local runtime Operational /
   Connected.
2. Show Setup 5 of 5, Medium profile reviewed, and Applied sync.
3. Show the actual `demo.add_numbers` input policy.
4. Run `npm run smoke:agntid -- --allow-deny`.
5. Confirm result 32 for `(11, 21)` and denial for `(50, 21)`.
6. Open Reporting and correlate the two outcomes to the policy and tasks.

The smoke test needs no model key. Simulator is an additional native UI
demonstration after a healthy model credential and cost authorization exist.

## Final project demo: about three minutes

| Segment | Show |
| --- | --- |
| 0:00–0:30 | User problem and one concrete task |
| 0:30–1:10 | Useful agent completing an allowed action using a real external tool |
| 1:10–1:50 | The same agent attempting a restricted action; AgntID stops it |
| 1:50–2:20 | Backend state proving the blocked operation did not happen |
| 2:20–2:50 | Actual profile/policy and matching Reporting event |
| 2:50–3:00 | Why the boundary helps this user; state remaining limits |

For a before-and-after baseline, use disposable synthetic data. Capture what
an unrestricted test agent could do, then run the identical operation through
the governed path. Do not create broad production permissions for comparison.

## Evidence checklist

- [ ] Working agent or agentic workflow, not just a policy library.
- [ ] At least one actual external tool in the final project.
- [ ] AgntID-governed path visible in architecture and configuration.
- [ ] Allowed result and denied request with clear input/resource boundary.
- [ ] Independent backend state check for the denied side effect.
- [ ] AgntID Reporting events matched to the request and applied policy.
- [ ] Approval shown only if a real configured approval flow was tested.
- [ ] Credential scope/expiry claims backed by real platform evidence.
- [ ] Real running-project screenshots for Devfolio.
- [ ] Tokens, keys, private customer data, and unrelated logs excluded from captures.

Use [SUBMISSION.md](SUBMISSION.md) to turn that evidence into an accurate entry.
