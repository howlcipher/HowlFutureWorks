# Context Strategy (Runtime Context v2)

Persistent members run on **compact standing contract + retrieval index + task-local context**, not on concatenated policy bundles plus a growing conversation. Efficiency comes from compilation, deduplication, selective retrieval, delegation, checkpointing, bounded retries and concise communication. It never comes from weakening approvals, verification, evidence or risk ceilings.

## Five kinds of context

| Layer | What it is | Where it lives | When it is loaded |
|---|---|---|---|
| 1. Standing runtime contract | Compiled, provider-neutral projection of identity, risk ceiling, canonical state, invariants, authority, role rules, execution profile, lifecycle, communication rules and retrieval triggers | `build/bots/<id>.md`, compiled by `orgctl render-bot` from `policies/runtime-contract.yaml`, `policies/budgets.yaml` (`agent_runtime`), `bots/<id>/` and the `## Durable lessons` of `knowledge/positions/<id>.md` | Always (every work item) |
| 2. Task-local retrieved context | The specific policy, runbook, routing or work-item sources a task needs | Canonical files in Git and live state in HowlBoard/HowlPlane | Only when a `retrieve_when` trigger applies |
| 3. Durable institutional memory | Decisions, conclusions, open work, evidence refs, known pitfalls, position/company lessons | `knowledge/`, `workforce/people/<id>/context/`, ADRs, reports, evidence | Retrieved by trigger (e.g. `knowledge_checkpoint`) or written at checkpoint |
| 4. Employee continuity / onboarding | A worker's roster record, tenure, recent snapshots and predecessor handoffs | `orgctl render-employee <employee-id>` → `build/workforce/<id>.md` (capped by `employee_continuity_budget_chars`) | Only for onboarding, replacement, provider transition, explicit handoff or continuity recovery |
| 5. Raw conversation history | Disposable working context | The provider's conversation | Never carried into unrelated work; never committed |

Layer 1 is never a copy of layer 2 sources. Validation forbids retrieval triggers from pointing into `workforce/people/` or `build/`, so layer 4 cannot leak into routine context. If a successor needs more history than the continuity cap allows, promote stable lessons into position or company knowledge rather than raising the budget.

## Standing contract

`bots/<id>/context.yaml` (schema `schemas/position-context.schema.json`, `schema_version: 2`) declares:

- `standing_budget_chars`: this position's ceiling, ≤ `agent_runtime.standing_context_max_chars`
- `execution_profile`: `coordinator` (Engineering Manager), `implementer` (Dev Lead), `verifier` (Assurance), `auditor`, or `advisor` (Product, R&D)
- `position_knowledge`: whose `## Durable lessons` section is compiled in
- `retrieve_when`: trigger → extra sources. Each trigger also contributes the `required_sources` defined in `policies/runtime-contract.yaml`.

The v1 keys `always_load`, `load_on_demand` and `budget_chars` are rejected by `validate`, so there is one mechanism.

`orgctl validate` checks structure, not English sentences:

- Every required invariant ID is present with an existing source.
- Required triggers are present for every position, plus capability-coupled triggers: workforce management needs `staffing_change`, delegation needs `executor_selection`, and Bot-definition authority needs `bot_definition_change`.
- Core triggers carry their minimum sources (`authority_question` → CHARTER + approvals, `knowledge_checkpoint` → memory + budgets, and so on).
- The compiled contract keeps no-self-escalation, fail-closed and non-authoritative memory, and forbids chain-of-thought.
- Every compiled contract fits its budget.

## Retrieval triggers

Triggers name *when* to read *which* authoritative source: `authority_question`, `risk_classification`, `knowledge_checkpoint`, `evidence_verification`, `external_action`, `staffing_change`, `executor_selection`, `bot_definition_change`, `production_change`, `security_review`, `incident_response`, `role_detail`, `domain_reference`. Retrieval is conservative. When unsure whether a trigger applies to a consequential action, retrieve. A missing required policy or approval fails closed.

## Checkpoint-and-reset lifecycle

```text
work item starts
→ compact runtime contract loaded
→ task-local context retrieved per trigger
→ work performed or delegated
→ result verified (independently when consequential)
→ durable discoveries checkpointed (orgctl checkpoint / work-item records)
→ task-local disposable history discarded
```

Persist decisions, conclusions, open work, evidence refs, known pitfalls and handoff state. Never persist chain-of-thought, raw transcripts or secrets. A completed work item does not carry its transcript into unrelated future work. See `docs/KNOWLEDGE_RETENTION.md`.

## Communication

Progress narration is exceptions-only. Report proactively when an owner decision or approval is required, policy blocks action, execution is materially blocked, the plan changes materially, significant unexpected risk appears, or work completes.

## Measuring

`python tools/orgctl.py context-report [--json]` prints standing chars, bytes, approximate tokens (`ceil(chars / agent_runtime.token_estimate_chars_per_token)`, a documented approximation that needs no provider API), budget, and percent used per position. Run-time signals are recorded in the optional `efficiency` object of the result envelope; see `METRICS.md`.

## Never preload by default

The whole repository, the full charter, whole policy files, raw chat transcripts, predecessor conversation history, or bulky evidence/logs.
