# ADR 0004: Durable Knowledge and Context Checkpointing

- Status: Accepted
- Date: 2026-09-20

## Context

Bot conversations are disposable; the repository is the durable organizational record (ADR-0001). Sessions, providers and context windows are frequently replaced, but conclusions, decisions, open work and risks discovered mid-session were previously only as durable as whoever remembered to write a handoff by hand. Nothing forced a consistent moment or format to capture that knowledge before it was lost, and nothing bounded how large a captured snapshot could grow.

## Decision

Adopt an explicit, machine-checked checkpoint operation: `python tools/orgctl.py checkpoint`. It writes a schema-validated `workforce/people/<employee-id>/context/<snapshot-id>.yaml` snapshot, never overwrites an existing snapshot, always sets `contains_raw_chain_of_thought: false`, and refuses to write a snapshot that exceeds `policies/budgets.yaml`'s `knowledge_artifacts.checkpoint_chars`. `policies/memory.yaml` states the governing principle — use conversations for disposable working context, use durable repository records for knowledge another session/provider/worker would otherwise have to rediscover ("write once, retrieve many") — and every persistent position always loads it and `policies/budgets.yaml`. `schemas/context-snapshot.schema.json`'s `reason` enum is extended to name the moments that should trigger a checkpoint: task completion, approaching the context budget, a provider switch, session end, and material decisions/discoveries, in addition to the existing lifecycle reasons.

## Consequences

- A checkpoint is either a complete, schema-valid, size-bounded record, or it does not exist; there is no silent partial or oversized write.
- Checkpoint triggers and numeric budgets are discoverable in policy rather than left to individual Bot judgment.
- `orgctl.py validate` extends to catch missing policy loading, out-of-range budgets, and oversized knowledge artifacts, the same way it already catches other structural drift.
- This is additive: existing context snapshots, handoffs and the employee continuity budget are unaffected; no prior `reason` value is removed.
