# Bot / Position Factory

The factory creates or changes **persistent positions/configurations**, not disposable employee history. The Engineering Manager / Organizer owns the controlled workflow.

## Position pipeline

signal → roster evaluation → position proposal → instructions/context/boundaries → validation → review → manifest activation → live deployment → drift/audit report

`orgctl scaffold-bot` requires an explicit durable purpose, writes candidates to `bots/proposals/`, and intentionally does not grant authority or staff the position.

## Staffing after position approval

Once a position exists, use `runbooks/hire-worker.md` and the `workforce/` layer to create an employee instance. Replacements receive new employee IDs and curated predecessor handoffs.

## Continuous tuning

Stable lessons can graduate into role/position instructions or skills. Task-specific history remains in work items/reports/contribution records. Do not make a live Bot conversation the institutional memory layer.
