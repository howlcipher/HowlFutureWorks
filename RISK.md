# Risk Model

Canonical machine-readable policy: `policies/risk-tiers.yaml`.

- **R0 Observe** — read-only and reporting.
- **R1 Sandbox** — isolated/disposable writes.
- **R2 Development** — branches, PRs, tests, CI, development resources.
- **R3 Shared / Release** — merges, staging/shared mutation, publication, release promotion, external communications.
- **R4 Critical** — production, destructive/bulk, privilege/secret/security-control changes, irreversible data, financial/legal commitment.

Risk is attached to the **action**, not the Bot title.
