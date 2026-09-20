# HowlFutureWorks Repository Map

This is a semantic map, not a generated file listing. Use `git ls-files` when an exact current file inventory is required.

## Identity and constitution

- `organization.yaml` — canonical machine-readable identity and repository slug.
- `CHARTER.md` — constitutional principles and organizational operating model.
- `ORG.md` — roles, positions, workforce relationships and separation of duties.
- `AGENTS.md` — entrypoint and invariants for normal CLI AI agents.
- `README.md` — human quick start.

## People and organization

- `roles/` — durable job definitions independent of any worker.
- `bots/` — persistent position definitions and deployable Bot configuration.
- `workforce/` — employee instances, current roster, lifecycle events, proposals, contributions, handoffs and tenure records.
- `knowledge/` — compact position/company knowledge that survives worker replacement.

## Governance and execution control

- `policies/` — machine-readable risk, approvals, credentials, access, budgets, workforce and change policy.
- `schemas/` — JSON Schema contracts plus validated examples.
- `routing/` — executor capability registry, routing and fallback policy.
- `runbooks/` — repeatable operational, security, staffing and recovery procedures.
- `security/` — threat model, abuse-case, regression-test and review areas.

## Work lifecycle

- `product/` — discovery, opportunities, roadmap and decisions.
- `rnd/` — proposals, experiments, results, killed and promoted work.
- `operations/` — releases, incidents, postmortems and reliability records.
- `reports/` — daily/weekly/monthly, audit, retrospective and workforce reports.
- `evidence/` — evidence conventions/manifests; not a raw secret/log dump.
- `adr/` — architecture and organizational decision records.

## Automation and evaluation

- `automation/` — reusable skills, routines and scripts.
- `evals/` — benchmark suite, results and routing recommendations.
- `templates/` — reusable forms for work, audits, staffing and incidents.

## Tooling and repository controls

- `tools/orgctl.py` — validate, inspect, render and propose controlled organizational changes.
- `tools/package_release.py` — clean-room ZIP/Git-bundle build and verification.
- `tests/` — structural and governance regression tests.
- `.github/` — CI, Dependabot and repository collaboration scaffolding.
- `docs/` — bootstrap, platform, reconciliation, identity, context and audit documentation.

## Durable-state rule

Do not move authoritative work state into this map or into Bot memory. Git is desired organizational state; HowlBoard/HowlPlane own changing work/execution state; HowlFrame enforces bounded execution; evidence and work systems remain authoritative for their respective claims.
