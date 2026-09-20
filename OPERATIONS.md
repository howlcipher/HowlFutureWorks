# Operations

Operational changes follow risk classification, explicit target verification, bounded authority, post-action verification, and rollback/recovery readiness.

## Known procedures

Use `runbooks/` for provider failure, quota exhaustion, failed deployment, rollback, credential exposure, runaway agents, circuit breakers, security incidents and recovery.

Workforce operations are also runbook-driven:

- `runbooks/hire-worker.md`
- `runbooks/fire-worker.md`
- `runbooks/suspend-worker.md`
- `runbooks/reassign-worker.md`
- `runbooks/succession.md`
- `runbooks/performance-review.md`
- `runbooks/retire-position.md`
- `runbooks/rehire-worker.md`

A staffing action changes who is allowed to receive work; it does not erase historical work product. Emergency suspension stops new work before investigation when safety is uncertain.
