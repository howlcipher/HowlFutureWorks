# Persistent Bot Desired State

This directory defines persistent **positions and Bot configuration** as code. Individual employee/worker history lives under `workforce/`.

`manifest.yaml` is the active desired position catalog. `workforce/roster.yaml` records who occupies each position now and who occupied it previously. Each active Bot has a directory containing its role instructions, minimal context manifest, capability declaration, boundaries, skills and routines.

## Organizer ownership

The Engineering Manager / Organizer owns roster maintenance. It may:

- identify a durable need for a new Bot,
- scaffold a proposal under `bots/proposals/`,
- refine a Bot's instructions/context/skills/routines,
- reconcile live Bot configuration to reviewed desired state,
- propose retirement or consolidation.

It may not use roster maintenance to widen its own authority, weaken approvals, or grant another Bot permissions outside approved policy.

## Position lifecycle

Firing/replacing an employee does not remove the position. Use the workforce lifecycle for staffing changes.

1. `python tools/orgctl.py scaffold-bot ...` creates a proposal.
2. Review the roster-change proposal and boundaries.
3. When approved, move the candidate to `bots/<id>/` and add it to `manifest.yaml`.
4. Validate and render.
5. Reconcile deployed Grok state.
6. Record the change and deployment fingerprint.

A normal CLI AI should be able to do all repository work by reading `AGENTS.md`; no giant bootstrap prompt is required.
