# Knowledge Retention

## Why this exists

Conversations end. Sessions expire. Providers get swapped. Context windows fill up. None of that should cost the organization knowledge that another session, provider, or worker would otherwise have to rediscover from scratch. See `policies/memory.yaml` for the governing principle and `docs/INSTITUTIONAL_MEMORY.md` for the promotion ladder this doc assumes.

**Use conversations for disposable working context. Use durable repository records for knowledge another session/provider/worker would otherwise need to rediscover. Write once, retrieve many.**

## Disposable vs durable

Disposable (stays in the conversation, never committed): exploration, false starts, chain-of-thought, intermediate tool output, anything easily re-derived by re-reading authoritative systems.

Durable (belongs in the repository): conclusions, decisions and their rationale, open work and its owner, known pitfalls/risks backed by evidence, source/evidence references (pointers, not copies).

## Checkpoint triggers

Checkpoint durable knowledge with `python tools/orgctl.py checkpoint <employee-id> --reason <reason> ...` at any of:

- task completion (`task_complete`),
- approaching the context budget — see the 75% rule below (`context_budget`),
- a provider or session switch (`provider_switch`, `session_end`),
- a decision or discovery material enough that losing it would cost real rework (`material_decision`, `material_discovery`),
- the existing workforce lifecycle moments: `handoff`, `separation`, `reassignment`, `incident`, `periodic`, `manual`.

## The 75% rule

`policies/budgets.yaml`'s `defaults.context_checkpoint_threshold_percent` (currently 75) is the point at which a worker should stop accumulating more working context and checkpoint durable conclusions before the window fills and forces an uncontrolled loss. Don't wait for 100%.

## Knowledge hierarchy and promotion

See `docs/INSTITUTIONAL_MEMORY.md` for the full promotion ladder and successor-context rules; the short version: task evidence stays with the work, a worker's own useful facts go in its curated context/handoff, repeated durable lessons move to `knowledge/positions/<position>.md`, cross-role lessons to `knowledge/company/`, and normative rules become policy/ADR/runbook. Promoted knowledge should **replace** duplicated lower-level prose with a reference, not sit alongside it.

## Write once, retrieve many

A checkpoint, position-knowledge entry, or ADR is written once and read by every future session/worker that needs it. Do not re-derive or re-explain something already recorded — reference it (`ADR-000N`, `knowledge/positions/<id>.md`, a commit or report path) instead of restating it.

## Numeric budgets

Canonical numeric limits live in `policies/budgets.yaml` (`knowledge_artifacts.*`, `guidance.*`, `defaults.context_checkpoint_threshold_percent`) and in `organization.yaml` (`employee_continuity_budget_chars`). This document does not restate those numbers — read the policy files for current values.

## Evidence over transcripts

Point to evidence (a commit SHA, a report path, an ADR number, a test run) instead of pasting logs or transcripts. `orgctl.py checkpoint` always sets `contains_raw_chain_of_thought: false` and rejects a snapshot that doesn't fit the checkpoint budget — that's a forcing function to summarize, not a suggestion.

## Successor behavior

A successor loads current position/company knowledge plus the predecessor's curated handoff — never a chain of every predecessor's raw history. See `docs/CONTEXT_STRATEGY.md` for the full load order.

## Example

**Good:** "Deployment verification failed silently because the executor treated a non-zero exit status as success when stdout still contained partial output. Fix and regression test in commit `<sha>`; see `ADR-000N` for the exit-status contract this created." — one sentence of durable lesson, a pointer to the fix, a pointer to the rule it produced.

**Bad:** pasting the full deploy log, the full back-and-forth debugging transcript, and every intermediate hypothesis that turned out wrong. None of that is retrievable-once-written knowledge; it's disposable working context that happened to get committed.
