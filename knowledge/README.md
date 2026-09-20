# Institutional Knowledge

This directory stores **curated organizational knowledge that outlives individual workers**. It is not a transcript archive.

## Memory layers

1. **Task evidence** — work items, commits, tests, reports and other authoritative artifacts.
2. **Employee continuity** — `workforce/people/<employee>/context/` and handoffs. These preserve a worker's useful tenure knowledge.
3. **Position knowledge** — `knowledge/positions/<position>.md`. Stable lessons that every future occupant of that position should know.
4. **Company knowledge** — `knowledge/company/`. Cross-role lessons that should survive any staffing or provider change.
5. **ADRs/policy** — normative decisions. If a lesson becomes a rule, move it into the appropriate ADR/policy rather than leaving it as folklore.

## Promotion rule

Promote knowledge upward only when it is useful beyond one task, supported by evidence, safe to retain, and unlikely to become misleading quickly. Do not promote secrets, raw chats, chain-of-thought, transient quota state, or unverified model claims.

## Succession rule

A successor loads the current position knowledge plus a curated predecessor handoff. It should **not** replay every former employee's history. Position knowledge is periodically compacted so context cost does not grow without bound.
