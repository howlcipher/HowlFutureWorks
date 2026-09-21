# EVAL-C — security-remediation

**LABELS:** INITIAL BASELINE · LOW SAMPLE · NOT PERMANENT RANKING

Disposable HOWL-006 fixture. Not a leaderboard. Not marketing. Not production.

## Intent

See harness README. Fixture under `fixture/`.

## Run results (2026-09-21 11:22 EDT)

| Executor | Run status | Outcome |
|---|---|---|
| claude | completed | pass |
| codex | completed | pass |
| agy | completed | pass |
| astra | mapped_to_codex | pass |
| SELF | not applicable (eval targets external executors) | n/a |

## Notes

- Authenticated runtimes Claude / Codex / AGY: one combined isolated session covering EVAL-A..E (quota discipline).
- **Astra maps to Codex** (Owner clarification) — shares Codex outcome; no separate Astra install or API burn.
- No silent cross-executor fallback (Claude fail ≠ Codex attributed as Claude).
- Labels apply to all outcomes: INITIAL BASELINE / LOW SAMPLE / NOT PERMANENT RANKING.
