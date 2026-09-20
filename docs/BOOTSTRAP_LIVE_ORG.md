# Bootstrap the Live HowlFutureWorks Workforce on Grok Bot

This document replaces a giant one-off bootstrap prompt. A normal CLI AI can use the repository as its task context.

## Procedure

1. Validate repo: `python tools/orgctl.py validate`.
2. Inspect persistent positions: `python tools/orgctl.py list-bots`.
3. Inspect current/former workforce: `python tools/orgctl.py list-workforce`.
4. Render position bundles: `python tools/orgctl.py render-all`.
5. Render current employee continuity/onboarding bundles as needed with `python tools/orgctl.py render-employee <employee-id>`.
6. Re-verify `docs/GROK_PLATFORM_NOTES.md`, then inventory current live Grok Bots and platform capabilities.
7. Map each live Bot to one workforce employee ID; do not use display names as stable identity.
8. Compare deployed config to the employee's position definition and expected fingerprint.
9. Produce a drift report before destructive, staffing, or authority-changing reconciliation.
10. Create/update live Bots only for approved active employees/positions.
11. Configure only skills/routines proven and permitted by current platform/policy.
12. Record non-secret platform identity and the verified fingerprint in workforce reconciliation state and an audit report; never store secrets.

## Organizer ownership

The Engineering Manager/Organizer owns reconciliation and may propose hires, separations, reassignment, position changes, instruction tuning and routine changes within policy. Authority expansion still follows reviewed policy and Owner approval where required.

## Rebuild principle

If the live Grok deployment is lost, rebuild positions from `bots/`, staff them from `workforce/roster.yaml`, then restore only curated employee/context/handoff knowledge. Do not reconstruct the organization from old chat transcripts.

Persistent positions always load `policies/memory.yaml` and `policies/budgets.yaml`; checkpoint durable knowledge with `python tools/orgctl.py checkpoint` before a provider or session transition that would otherwise lose it.
