# Data and Retention

## Never commit
- passwords, tokens, keys, one-time codes or secret values,
- full raw agent/browser session dumps by default,
- hidden chain-of-thought or private reasoning,
- bulky generated logs/artifacts when a digest/pointer is sufficient.

## Durable organizational records
Retain while the repository remains the organizational record unless a stronger deletion policy applies:

- charter/policy/ADRs,
- workforce lifecycle events,
- employee tenure summaries and curated context snapshots,
- contribution records and artifact/evidence references,
- compact position/company knowledge with evidence pointers,
- incident/postmortem/release records,
- significant product/R&D decisions.

A departed employee's record is not deleted merely because the live Bot was disabled. Corrections should preserve historical traceability.

## Context principle
Persist conclusions, decisions, known pitfalls, open work and source/evidence references. Re-read changing facts from authoritative systems. Do not preserve raw model reasoning merely to make a future Bot feel continuous.

Canonical behavioral rules for this are in `policies/memory.yaml`; canonical numeric checkpoint/handoff/knowledge budgets are in `policies/budgets.yaml` and `organization.yaml`.

## Reports
Prefer compact summaries and references. `reports/**/raw/` and `evidence/raw/` are ignored by Git by default.
