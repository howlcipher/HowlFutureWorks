# EVAL-B — debugging

**LABELS:** INITIAL BASELINE · LOW SAMPLE · NOT PERMANENT RANKING

Disposable HOWL-006 fixture. Not a leaderboard. Not marketing. Not production.

## Intent

Locate and explain a planted bug in a tiny disposable module.

## Fixture

- `fixture/` — minimal disposable inputs (safe to delete/regenerate)
- No network-required secrets; no production paths

## Run results (2026-09-21 00:01 EDT)

| Executor | Run status | Score |
|---|---|---|
| claude | blocked:not_authenticated | n/a (not run) |
| codex | blocked:not_authenticated | n/a (not run) |
| agy | blocked:not_authenticated | n/a (not run) |
| astra | blocked:not_installed | n/a (not run) |
| SELF | not applicable (eval targets external executors) | n/a |


## Notes

- Auth missing → honest `blocked:not_authenticated` (no fabricated pass/fail scores).
- No silent cross-executor fallback (Claude fail ≠ Codex attributed as Claude).
- Re-run after Owner-controlled auth; keep sample size minimal (quota discipline).
