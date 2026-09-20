# Context Strategy

The repo reduces token waste by separating durable knowledge from task-local context.

## Load order
1. `AGENTS.md`.
2. Current role/position context manifest.
3. Current employee curated context/handoff only when relevant.
4. Task/work-item state from authoritative systems.
5. Additional policy/runbook/charter sections on demand.

## Never preload by default
- whole repository,
- full charter when not needed,
- raw chat transcripts,
- predecessor conversation history,
- bulky evidence/logs.

## Institutional memory
`workforce/people/<employee-id>/context/`, handoffs, ADRs, reports, contributions and decisions preserve the useful part of prior work. Store outcomes and source references, not chain-of-thought.

## Employee continuity bundles

Rendered employee continuity bundles are capped by `organization.yaml: employee_continuity_budget_chars`. If a successor needs more history than fits the cap, promote stable lessons into position/company knowledge and retrieve older evidence on demand rather than raising the budget casually.
