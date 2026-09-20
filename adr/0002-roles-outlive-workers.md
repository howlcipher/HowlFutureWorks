# ADR 0002: Roles and Positions Outlive Workers

- Status: Accepted
- Date: 2026-09-19

## Decision
Separate durable roles, deployable persistent positions, and individual employee/Bot instances. Preserve employee tenure, contributions, curated context, handoffs and lifecycle events after departure.

## Why
Treating a live Bot as both job and institutional memory makes replacement expensive, encourages context bloat, and loses history when a Bot is removed. A workforce layer permits hiring/firing/reassignment while keeping the organization reconstructable.

## Consequences
- New worker instances receive immutable employee IDs.
- Staffing changes do not delete role/position configuration or historical records.
- Successors inherit curated handoff/context, not raw conversations or credentials.
- Position retirement and employee termination are separate changes.
