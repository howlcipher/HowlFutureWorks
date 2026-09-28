# HOWL-009: Implementation report

Status: implementation complete; awaiting independent Assurance verification
Implementer: Claude Code (external executor, Owner-requested)
Branch: `feat/runtime-context-v2`, base `439f823`
Risk: R2 (organizational configuration and tooling; no authority, credential or production change)

Implementer evidence only. This is not independent verification, and Owner completion is not declared.

## Summary

Runtime Context v2 replaces concatenated standing Bot bundles with a compiled, provider-neutral runtime contract (ADR 0005, `docs/CONTEXT_STRATEGY.md`).

## Standing context (chars, rendered `build/bots/<id>.md`)

| Position | Before | After | Target |
|---|---|---|---|
| engineering-manager | 15,370 | 5,803 | 6,000 |
| product | 9,939 | 3,913 | 5,000 |
| rnd | 10,049 | 4,006 | 5,000 |
| dev-lead | 10,331 | 4,989 | 5,000 |
| assurance | 10,784 | 4,379 | 5,500 |
| auditor | 10,515 | 3,970 | 5,500 |

Tokens are approximately chars / 4 (`agent_runtime.token_estimate_chars_per_token`).

## Commands run (final working tree)

- `python tools/orgctl.py validate`: VALIDATION PASSED
- `python tools/orgctl.py render-all`: all six positions rendered within budget
- `python tools/orgctl.py context-report`: table above
- `python tools/orgctl.py render-employee bot-engmgr-0001`: 7,971 chars against a 24,000 budget
- `make audit`: validate, 149 tests passed (113 before), compileall, `git diff --check`
- `make dist && make verify-dist`: passed in a throwaway committed copy, because dist refuses a dirty tree

## Test Impact Assessment

- Behavior changed: standing-context rendering, `context.yaml` schema, validation of context and runtime policy, and the `context` and `context-report` CLI commands.
- New tests in `tests/test_runtime_context.py` cover:
  - generation, coverage, size targets and determinism
  - required governance fields
  - missing invariants, policy references, triggers and paths
  - capability-coupled triggers and legacy keys
  - malformed config, oversized contracts and the budget ceiling
  - retry cap, chain-of-thought prohibition, continuity isolation and report math
- Updated tests: five v1 `always_load` tests in `tests/test_structure.py` and `tests/test_checkpoint.py` were moved to v2 with equal or stronger checks. One of them would otherwise have passed without testing anything.
- Not covered: live Grok deployment behavior and runtime efficiency telemetry (non-goals).

## Governance preservation

No approval, risk-tier, capability, boundary or routing policy value changed. Required invariant IDs and minimum trigger sources are fixed in `orgctl`. Canonical policy, role, charter and knowledge documents are unchanged apart from additive pointers.

## Needed next

- Independent Assurance verification of this branch
- Owner review and merge decision
