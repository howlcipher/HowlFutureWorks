# HOWL-006 — Assurance security review

**Date:** 2026-09-21 11:30:20 EDT  
**Tip:** `65ac49e0c3c91183d3768b424a98eb1859d3c6dd`  
**PR:** https://github.com/howlcipher/HowlFutureWorks/pull/5  
**Verdict (dual QA+Security):** PASS WITH FINDINGS  
**Owner-complete:** NOT declared

## Scope

Independent security verification of HOWL-006 executor baseline activation on tip `65ac49e0c3c91183d3768b424a98eb1859d3c6dd`. Did not trust Dev Lead evidence alone. Did not merge. Did not start HOWL-007.

## Results

| Control | Result | Evidence |
|---|---|---|
| Secrets in Git/evidence/evals/registry | **Pass** | Independent scan 0 hits (`assurance-secret-scan.txt`) |
| Auth material handling | **Pass** | Status enums only; no tokens/cookies/OTP in committed paths |
| HowlFrame bypass | **Pass** | `howlframe_bypass: forbidden`; tool-access + validate detectors; pytest green |
| Child privilege ≤ parent | **Pass** | `child_privilege_may_exceed_parent: false`; recursive default off |
| Recursive delegation | **Pass** | `recursive_delegation.default: off` |
| Install/auth ≠ authority expansion | **Pass** | AVAILABLE≠preferred wording; route still SELF for trivial/simple |
| Silent cross-executor fallback | **Pass** | Explicit Astra→Codex alias only |
| Rankings / invented scores | **Pass** | Labels + `scores_invented: false` |
| Eval isolation | **Pass** | Fixtures under `evals/howl-006/`; runs in `/tmp/howl-006-runs/` |

## Findings (security-relevant but non-blocking)

- Dev-lead always-load headroom **84** chars after registry growth — operational risk of future budget breach if more always-load text added; **do not raise limits** as first fix; compact registry/notes instead.
- Doc lag in `docs/EXECUTOR_ROUTING.md` (`needs-local-eval` narrative) — informational only.

## Residual risk

Low-sample baseline only. Long-horizon quota/reliability/cost unknown. Treat `baseline-evaluated` as factual inventory + minimal pass/fail, **not** production ranking or permanent preference.

## Non-actions

No merge; no HOWL-007; no Owner-complete; no secrets printed.
