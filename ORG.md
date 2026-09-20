# HowlFutureWorks Organization Model

`organization.yaml` is the canonical identity record for the organization and repository.

## Durable organization

Owner → Engineering Manager → Product / R&D / Architecture / Development / Assurance / Operations.

Logical roles remain separate even when one persistent Bot coordinates multiple functions.

## Roles, positions and employees

- `roles/` defines jobs/responsibilities.
- `bots/` defines persistent positions and deployable Bot configuration.
- `workforce/` records the individual worker instances occupying those positions.
- work products/evidence belong to the organization and survive staffing changes.
- `knowledge/positions/` contains compact role knowledge that is inherited by successors; `knowledge/company/` contains cross-role institutional lessons.

**Roles and positions outlive employees.** A worker can be fired/replaced without deleting its contributions, context snapshots, decisions or handoffs. See `docs/WORKFORCE_LIFECYCLE.md`.

## Initial persistent positions

| Position | Durable ownership | Risk ceiling | Notes |
|---|---|---|---|
| Engineering Manager | roster, coordination, delegation, drift | R2 by default | cannot self-escalate |
| Product | discovery, problem definition, prioritization | R1 | no production authority |
| R&D | uncertain ideas and experiments | R1, bounded R2 drafts | sandbox-first |
| Dev Lead | implementation planning and executor routing | R2 | no direct production |
| Assurance | coordinates separate QA and Security evidence | R2 | cannot weaken its gates |
| Auditor | independent evidence reconstruction | R0 | read-only wherever practical |

## Invoked specialist roles

Software Architect, Developer, QA, Security, DevOps, Release Manager, SRE, Support, Writer.

A persistent position is justified only by durable ownership, recurring workflows, specialized context/tools, a distinct approval boundary, or repeated handoff patterns.

## Position lifecycle

`proposed → approved → active → deprecated → retired`

The Organizer owns position proposals/maintenance within policy. Authority expansion follows approval policy.

## Employee lifecycle

`candidate → hired → active ↔ suspended → departed`

Departed types include `terminated`, `retired`, `laid_off`, `replaced`, and `provider_retired`. Departed workers remain in `workforce/roster.yaml` and `workforce/people/` for institutional memory.

## Separation of duties

Implementation, QA/Security verification, release authorization, and audit are separate decisions even when one persistent position coordinates more than one logical function.
