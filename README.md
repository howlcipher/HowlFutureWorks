# HowlFutureWorks

Version-controlled operating system for **HowlFutureWorks**, the human-governed autonomous software organization for the Howl ecosystem.

The repository is **desired organizational state**. Live Grok Bots are a deployed representation of that state. Bot memory is never the source of truth.

**Documentation:** https://howlcipher.github.io/HowlFutureWorks/

## Start here

1. Read `organization.yaml` for canonical organization identity and repository naming.
2. Read `AGENTS.md` if you are a CLI coding/automation agent.
3. Read `CHARTER.md` for constitutional rules.
4. Run `python tools/orgctl.py about` to confirm organization identity, then `python tools/orgctl.py validate`.
5. Run `python tools/orgctl.py render-all` to build compact position context bundles under `build/bots/`.
6. Run `python tools/orgctl.py org-status` to see filled/vacant positions and current staff.
7. Run `python tools/orgctl.py list-workforce` to inspect current staff and preserved alumni.
8. Use `python tools/orgctl.py employee-history <employee-id>` when investigating a worker's tenure.
9. Use `docs/BOOTSTRAP_LIVE_ORG.md` to create or reconcile the live HowlFutureWorks workforce on Grok Bot.

## Persistent Bot roster

- Engineering Manager / Organizer
- Product
- R&D
- Dev Lead
- Assurance
- Independent Auditor

Other functions are logical roles or invoked specialists until recurring workload justifies a persistent Bot.

## Core rule

The Organizer may create, tune, reconcile, or retire persistent positions/configurations, and maintain skills and routines **within policy**. It may not expand its own authority, weaken approval rules, redefine critical risk downward, or grant another Bot broader authority without an approved policy change.

## Repository map

- `organization.yaml` — canonical organization identity, repository slug, and provider-neutral operating identity.
- `roles/` — durable human-readable role definitions.
- `bots/` — source-controlled persistent positions/Bot definitions.
- `workforce/` — current/former employee instances, tenure, contributions, context snapshots, handoffs, and lifecycle events.
- `knowledge/` — compact position/company knowledge that survives employee replacement without replaying old chats.
- `policies/` — machine-readable organizational policy.
- `routing/` — executor capability registry and selection rules.
- `schemas/` — structured contracts for tasks, results, approvals, evidence, incidents, etc.
- `runbooks/` — repeatable operating and recovery procedures.
- `product/` — discovery, opportunities, roadmap, and decisions.
- `rnd/` — proposals, experiments, killed/deferred/promoted work.
- `evals/` — benchmark definitions and results.
- `security/` — threat model, agent-security tests, reviews.
- `operations/` — release, incident, postmortem, and reliability records.
- `reports/` — operating reports; generated reports are retained according to `DATA.md`.
- `adr/` — architecture/organization decision records.
- `templates/` — reusable work templates.
- `automation/` — skills, routines, and automation specifications.
- `evidence/` — evidence conventions and manifests, not secret/raw-log dumping.
- `tools/` — local CLI utilities for validation and rendering.

## Staffing model

Persistent positions are not individual employees. Workers can be hired, suspended, reassigned, replaced, or fired while their documented contributions/context remain in `workforce/`. Replacements get a new employee ID and curated predecessor handoff rather than raw conversation history.

## Distribution

Run `make audit` for the local validation/test/compile/whitespace gate. After committing, run `make dist` to produce reproducible source ZIP and Git bundle artifacts under `dist/`; run `make verify-dist` to test both in clean rooms.
