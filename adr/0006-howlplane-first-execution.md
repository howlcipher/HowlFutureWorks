# ADR 0006: HowlPlane-first execution and governed self-improvement

- Status: Accepted
- Date: 2026-09-28

## Context

Runtime Context v2 (ADR 0005) made persistent positions cheap to stand up. Implementation-heavy work was still easy to describe as a Grok Bot calling a raw provider CLI. HowlPlane already runs Factory, `work`, `orchestrate`, routing, failover, evidence, authority profiles, and `--target self|repo|ecosystem`.

## Decision

Keep three decisions separate: which roles participate, whether work is SELF or delegated, and which executor HowlPlane selects once delegation is justified.

- Small bounded work stays SELF when orchestration would cost more than the work.
- Delegated implementation uses the existing HowlPlane CLI. Raw provider CLIs are not a normal path.
- A HowlPlane failure may skip only the orchestration layer, and only for a listed condition. It does not bypass HowlFrame, risk, approvals, credentials, scope, evidence, verification, retries, or production controls.
- If no governed entrypoint still runs, checkpoint, stop, and escalate.
- A confirmed Plane defect opens one tracked repair. If that path fails, stop. Executor failures are not Plane defects.
- Improvement of HowlPlane or other Howl components requires repeated evidence and normal prioritization. Self-improvement cannot expand authority.
- Durable execution state stays in HowlPlane, HowlBoard, or Git.
- The rules live in `routing/execution-substrate.yaml` and are retrieved by the `execution_orchestration` trigger. Standing contracts were not used as the place to store them, and efficiency budgets were not raised.

HowlPlane itself was not modified. The 0.1.0 CLI already exposed the entrypoints this policy names.

## Consequences

- `orgctl route` reports an execution substrate alongside the existing SELF-or-delegate decision.
- `orgctl validate` rejects a governance bypass, unbounded repair, opinion-only improvement, authority expansion, and a normalized raw CLI.
- Engineering Manager standing context grows by a short trigger line and stays under 6,000 characters. Dev Lead stays under 5,000. Other positions are unchanged.
- There is still no second runner that enforces HowlFrame when every HowlPlane entrypoint is down. That case escalates.
