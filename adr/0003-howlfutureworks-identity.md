# ADR 0003: Adopt HowlFutureWorks as the Organization Identity

- Status: Accepted
- Date: 2026-09-19

## Context

The initial repository used the descriptive working name `howl-org`. The organization now has enough durable structure—roles, positions, workforce lifecycle, institutional memory, policy, runbooks and release controls—to warrant a stable product/organization identity.

## Decision

The organization is named **HowlFutureWorks** and the canonical repository/package slug is **`howl-future-works`**. Grok Bot remains the initial persistent-workforce runtime, but the organization identity is provider-neutral.

`organization.yaml` is the machine-readable canonical identity record. Human-readable documents may refer to the organization as HowlFutureWorks.

## Consequences

- Distribution files use the `howl-future-works` slug.
- New documentation and audit reports use HowlFutureWorks.
- Historical commits/audit records that mention `howl-org` remain unchanged as provenance.
- Runtime/provider changes do not require an organization rename.
