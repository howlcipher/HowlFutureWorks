# ADR 0005: Runtime Context v2 (Compiled Runtime Contracts)

- Status: Accepted
- Date: 2026-09-28

## Context

Each persistent position's standing context was built by concatenating every `always_load` file with its instructions, capabilities and boundaries. As a result the same invariants appeared in AGENTS.md, ORG.md, roles, instructions, boundaries and several policies. Standing context ran from about 9,400 to 14,700 characters per position (EM largest) before any task-local context or conversation history was added.

## Decision

Replace concatenation with compilation:

- `policies/runtime-contract.yaml` defines shared provider-neutral inputs once: canonical state rules, invariants (each with ID and source), execution profiles, the task lifecycle, communication rules, the retrieval-trigger vocabulary with minimum sources, required triggers, and continuity rules.
- `policies/budgets.yaml` adds `agent_runtime` efficiency limits. They are escalation points, not hard stops.
- `bots/<id>/context.yaml` moves to `schema_version: 2` (`standing_budget_chars`, `execution_profile`, `position_knowledge`, `retrieve_when`). v1 keys are rejected.
- `orgctl render-bot` compiles a deterministic runtime contract. `orgctl validate` checks it structurally, and `orgctl context-report` measures it.

Alternatives considered: hand-written per-Bot runtime files, which re-duplicate invariants and drift from policy; and trimming `always_load`, which is still concatenation and cannot reach the Engineering Manager target without dropping required policies.

## Consequences

- Standing context shrinks to about 3,970 to 5,800 characters per position. Every previously loaded source stays reachable through a trigger.
- Canonical policy, role, charter and knowledge documents are unchanged and remain authoritative.
- Governance is validated by invariant and trigger IDs rather than by matching English sentences. Required triggers and their minimum sources are fixed in `orgctl` and cannot be removed by editing policy alone.
- Employee continuity (`render-employee`) is separate from routine standing context and cannot be reached through retrieval triggers.
- This supersedes ADR 0004's "every persistent position always loads memory/budgets". Those sources are now mandatory in the `knowledge_checkpoint` trigger of every position.
