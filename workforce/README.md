# Workforce and Institutional Memory

The workforce layer models **who currently occupies a position** without confusing an employee instance with the durable role or Bot configuration.

## Four separate concepts

1. **Role** (`roles/`) — durable job description and decision responsibility.
2. **Position/Bot definition** (`bots/`) — deployable configuration for a persistent seat such as Product or Dev Lead.
3. **Employee instance** (`workforce/`) — one specific Bot occupant with an immutable employee ID and tenure history.
4. **Work product** — commits, ADRs, reports, evidence, decisions, experiments, incidents and other artifacts that belong to the organization, not to the employee's memory.

A position can be vacant, filled, split, consolidated, or retired. An employee can be hired, activated, reassigned, suspended, reinstated, terminated, retired, laid off, replaced, or rehired. **Separating an employee never deletes its historical record.**

## Current-state source

`workforce/roster.yaml` is the current workforce roster. `bots/manifest.yaml` defines persistent positions/configurations.

## Historical source

- `workforce/events/` — append-only lifecycle events.
- `workforce/people/<employee-id>/` — durable profile, tenure summary, curated context, reviews, and handoffs.
- `workforce/contributions/` — attributable contribution records pointing to real artifacts/evidence.

Git history is additional evidence but is not the only workforce record.

## Hiring

Hiring creates a **new immutable employee ID** unless the exact same employee identity is intentionally being rehired. A replacement for a departed Bot normally gets a new employee ID and may point to a predecessor.

Before activation, validate the position, risk ceiling, manager, context packet, and required approvals. Deployment credentials are not stored here.

## Separation / firing

User-facing language may say "fire"; the recorded lifecycle event is normally `terminated`. Separation must:

1. stop new assignments,
2. preserve active-work state,
3. capture a curated context snapshot and exit handoff,
4. record contributions and unresolved risks,
5. revoke runtime access/routines as applicable,
6. mark the employee departed without deleting its record,
7. leave the position vacant or hire a successor.

Emergency security cases use `suspended` first so writes can stop immediately while evidence is preserved.

## Context retention rule

Keep **durable knowledge**, not raw model reasoning. Store conclusions, decisions, source/evidence references, known pitfalls, open work, and handoff notes. Do not store hidden chain-of-thought, secrets, full chat dumps, or stale claims that can be re-read from authoritative systems.

A successor should load the role/position definition plus the predecessor's curated handoff/context only when relevant. It should verify changing facts against canonical sources before acting.

## Live deployment mapping

`workforce/roster.yaml` may store a non-secret provider/platform `deployment_ref` and last verified `deployed_fingerprint`. These are reconciliation metadata, not credentials or authority.
