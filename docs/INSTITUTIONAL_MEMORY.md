# Institutional Memory

The organization should remember **what matters**, not preserve every conversation.

## Promotion ladder

`task evidence -> employee context -> position knowledge -> company knowledge -> ADR/policy/runbook`

- Task-specific facts stay with the work/evidence.
- A worker's useful continuity facts can be captured in a curated context snapshot or handoff.
- Repeated, durable role lessons move to `knowledge/positions/<position>.md`.
- Cross-role lessons move to `knowledge/company/`.
- Normative rules move to policy, ADRs or runbooks.

## Successor context

A successor should receive the current role/position bundle, compact position knowledge, current authoritative work references and the predecessor's exit handoff. It should not recursively load all historical employees or conversations.

## Context hygiene

Position knowledge must be periodically compacted and revalidated. Keep evidence pointers rather than copied raw logs. Changing facts must be re-read from authoritative systems. Secrets and private reasoning are never institutional memory.

See also `docs/KNOWLEDGE_RETENTION.md` for when and how to checkpoint (`orgctl.py checkpoint`) and the governing `policies/memory.yaml` principle.
