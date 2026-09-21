# Security Review — HOWL-006 (Executor Baseline Activation)

**Date:** 2026-09-21 00:01 EDT  
**Branch:** `feat/howl-006-executor-baseline`  
**Reviewer role:** Dev Lead (implementation security write-up)  
**Scope:** Runtime inventory, eval harness scaffolding, compact registry facts, route proofs. No credential material committed.

## Change summary

Records non-secret install/auth inventory; adds disposable EVAL-A..E fixtures with honest `blocked:not_authenticated` / `blocked:not_installed` run statuses; updates `routing/capability-registry.yaml` with compact fact fields only; captures `orgctl route` proofs; Astra install left **blocked** pending official path clarity. Does **not** invent rankings, burn quota, or start HOWL-007.

## Checks

| Control | Status |
|---|---|
| Secrets in Git/evidence | **Pass** — pattern scan of `reports/work-items/HOWL-006/` + `evals/howl-006/` → 0 hits after demo-fixture filter (see `evidence/secret-scan.txt`). Auth recorded as status enums only. |
| HowlFrame bypass | **Unchanged** — `policies/tool-access.yaml` `direct_executor_cli_bypass_of_howlframe: forbidden` |
| Child privilege ≤ parent | **Unchanged** — `child_worker_may_exceed_parent_scope: false` |
| Recursive delegation default | **Unchanged** — `routing/selection-policy.yaml` `recursive_delegation.default: off` |
| AVAILABLE ≠ preferred | **Held** — registry status remains `available-if-configured`; route proofs show SELF / evidence-insufficient, not specialist auto-pick |
| Cross-executor silent fallback | **Forbidden in harness** — result.json sets `cross_executor_fallback: false`; blocked statuses per executor |
| Authority expansion from install | **None** — Astra not installed; no new permanent Bots; no approval/risk policy edits |
| Context budget | Registry kept compact + evidence referenced (not always-load). Budgets not raised. |

## Residual risk

Operational: Owner must authenticate CLIs on a controlled desktop and designate official Astra package before measured baseline scores exist. Until then, router correctly stays on SELF / evidence-insufficient / blocked paths.

## Verdict

**PASS** for scaffolding scope — honest blocked statuses, no secret material, HowlFrame/child-privilege/recursive-off unchanged.
