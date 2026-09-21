# HOWL-006 — EVAL run summary (compact)

**Captured:** 2026-09-21 11:22 EDT  
**LABELS:** INITIAL BASELINE · LOW SAMPLE · NOT PERMANENT RANKING

| Runtime | Mode | A | B | C | D | E | Notes |
|---|---|---|---|---|---|---|---|
| claude | one combined isolated session | pass | pass | pass | pass | pass | Claude Code 2.1.278 |
| codex | one combined isolated session | pass | pass | pass | pass | pass | codex-cli 0.155.1 |
| agy | one combined isolated session | pass | pass | pass | pass | pass | agy 1.2.7; model gemini-3.8-flash-low |
| astra | **mapped to Codex** (no separate run) | pass* | pass* | pass* | pass* | pass* | *shares Codex outcomes |

Workspaces under `/tmp/howl-006-runs/{claude,codex,agy}` — disposable; **not** committed. No cross-executor fallback. No permanent ranking.
