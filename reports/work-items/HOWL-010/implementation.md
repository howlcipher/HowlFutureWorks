# HOWL-010: Implementation report

Status: implementation complete; awaiting independent Assurance verification
Implementer: Cursor agent on `feat/howlplane-first-execution`, base `d44525a` (HOWL-009 merged as PR #11)
Risk: R2 (routing and retrieval; no authority, credential, or production change)

Implementer evidence only. This is not independent verification.

## Summary

Delegated implementation now has an explicit substrate: HowlPlane. Persistent roles still do small bounded work themselves. Plane failure skips orchestration only, and only after classification. It does not skip HowlFrame or the existing policy controls. Repair is one tracked objective. Improvement requires repeated evidence and cannot expand authority.

HowlPlane was inspected (`howlplane` 0.1.0 help) and not modified. Factory, `work`, `orchestrate`, `route`, doctor, verify, record, authority, and `--target self|repo|ecosystem` already cover the path.

## Architecture

| Path | What happens |
|---|---|
| SELF | Small bounded work when orchestration costs more than doing it |
| Normal implementation | Expected value justifies delegation, then HowlPlane |
| HowlPlane execution | `howlplane work`, `howlplane orchestrate`, or `howlplane factory start` / `run` / `run-once` |
| Executor selection | `howlplane route` or Factory routing from measured fit |
| HowlPlane failure | Classify. Use a still-working governed entrypoint. If none exists, checkpoint, stop, escalate |
| HowlPlane repair | One tracked work item. `howlplane factory run --target self` when a governed path still works |
| Ecosystem improvement | Repeated evidence, normal prioritization, then a tracked work item (`--target ecosystem` when Factory is the implementation path) |

## Standing context (chars)

| Position | Before HOWL-010 | After | Budget | Headroom |
|---|---:|---:|---:|---:|
| engineering-manager | 5,803 | 5,924 | 6,000 | 76 |
| product | 3,913 | 3,913 | 5,000 | 1,087 |
| rnd | 4,006 | 4,006 | 5,000 | 994 |
| dev-lead | 4,989 | 4,968 | 5,000 | 32 |
| assurance | 4,379 | 4,379 | 5,500 | 1,121 |
| auditor | 3,970 | 3,970 | 5,500 | 1,530 |

Budgets were not raised. The 5,000/6,000 figures remain efficiency targets. The hard safety ceiling (`agent_runtime.standing_context_max_chars` 6,000, plus fail-closed validation) is unchanged. Dev Lead's target is close, so the new rules are a retrieval trigger, not standing prose. The long delegation list stays on the Engineering Manager contract, where it still fits, and in `policies/budgets.yaml` for everyone else.

Approximate tokens are chars / 4. Engineering Manager 1,451 → 1,481. Dev Lead 1,248 → 1,242.

## Commands

`python` is not on this machine's PATH. The same entrypoints were run with `python3`:

- `python3 tools/orgctl.py validate`: VALIDATION PASSED
- `python3 tools/orgctl.py render-all`: six positions within budget
- `python3 tools/orgctl.py context-report`: table above
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q`: 166 passed
- `python3 -m compileall -q tools tests` and `git diff --check`: clean

`make audit` calls `python`, so it was not invoked by that name. The audit steps above are the Makefile body.

HowlPlane tests were not run. No HowlPlane file changed.

## Governance preservation

Unchanged and checked by `orgctl validate`: Owner authority, no self-escalation, fail-closed approvals, exact R3/R4 binding, risk ceilings, HowlFrame bypass forbidden, independent verification, evidence, bounded retries (`max_retries_per_failure_class` 2, blind retry forbidden). `self_improvement.may_not` is an exact set. A Plane failure cannot set `howlplane_failure_is_governance_bypass`.

## Remaining gap

When every HowlPlane entrypoint is down, there is still no second runner that enforces HowlFrame. The policy checkpoints, stops, and escalates. That is intentional. The recorded CLI list is an observation of howlplane 0.1.0 on 2026-09-28, not a live probe in CI.
