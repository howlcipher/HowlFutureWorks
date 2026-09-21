# HOWL-006 — Product definition (lightweight)

Status: Product definition for EM acceptance  
Author: bot-product-0001 (Quatre Raberba Winner)  
Work item: `reports/work-items/HOWL-006.json`  
Baseline main: `1fb6775`  
Risk: R2  
Scope: activation / calibration of external executors (organizational infrastructure — **not** product feature work)

Predecessor: HOWL-005 (routing policy + deterministic tooling). HOWL-006 supplies **factual baseline evidence** so routing can distinguish specialists without inventing scores.

## Problem

After HOWL-005, Claude / Codex / AGY / Astra are registered as `available-if-configured` with `needs-local-eval`. Routing can correctly return **SELF** or **evidence-insufficient**, but it cannot yet make **evidence-based distinctions among specialists** because the registry lacks measured install/auth/tool/task evidence.

## Impact

Members cannot justify specialist delegation from facts. Risk of treating “available” as “preferred,” stalling on perpetual evidence-insufficient, or inventing capability folklore / rankings to unblock work.

## Desired outcome

Accurately know, from Owner-controlled observation and compact registry updates:

1. Which CLIs are installed and authenticated (human-controlled auth only)
2. Which tools each executor supports
3. Whether each can complete representative **bounded** tasks
4. Basic reliability signals from those runs
5. Latency / usage category if observable without quota burn
6. Known failure modes
7. What remains **unknown** (honest gaps)

Populate a **compact** capability registry from factual evidence (raw evidence referenced, not embedded in always-load context). Prove routing still chooses **SELF** when appropriate and can justify a specialist **only** when measured value supports it.

## Acceptance criteria

**Authoritative source:** Owner HOWL-006 brief (AC of record). Product does not invent demand beyond that brief.

Distilled themes for implementers:

1. **Runtime inventory** — Deterministic inventory of install/auth/tool presence for Claude, Codex, AGY, Astra (and SELF path). Report unknowns explicitly.
2. **Owner-controlled auth** — Human-controlled login/configure only; **no secrets** in chat, Git, evidence packs, memory, or logs.
3. **AVAILABLE ≠ preferred** — Registry `available-if-configured` / similar must not imply ranking or default specialist choice.
4. **Minimal EVAL-A..E baseline** — Small representative bounded evals only; label results **INITIAL BASELINE / LOW SAMPLE / NOT PERMANENT RANKING**. No full leaderboard; no marketing rankings.
5. **Raw evidence ≠ registry** — Keep detailed logs/artifacts out of always-load context; registry stays compact; reference evidence paths. Respect context-budget preflight (EM ~194 chars headroom — do **not** raise budgets as first fix; no new always-load eval docs).
6. **Quota discipline** — No quota burn / exhaustion campaigns; fail closed or skip with honest blocked when quota/auth insufficient.
7. **orgctl route proofs** — Demonstrate: trivial/simple → SELF; bounded may remain evidence-insufficient until baseline exists; critical preserves risk / does not lower assurance via executor choice.
8. **Independence** — Assurance independently verifies; Auditor can reconstruct claims from Git evidence.
9. **Honest failure OK** — Blocked/failed/unavailable executors reported honestly; do not invent scores to fill gaps.
10. **Publish path** — Native branch/PR path (HOWL-004); CloudAgent fallback only if publish blocked.
11. **Routing integrity** — SELF still preferred when appropriate; specialist only when measured value supports it; no permanent best-model declaration.

## Explicit non-goals

- Permanent “best model” declaration or permanent rankings
- Quota exhaustion / large leaderboards / marketing rankings
- Production or destructive tests
- Risk-policy changes or HowlFrame weakening
- Product feature development
- Credential broadening beyond Owner-controlled auth for eval inventory
- New permanent Bots
- Inventing capability scores
- Raising context budgets as the first fix
- Starting HOWL-007 automatically
- HowlBoard / HowlPlane implementation

## Baseline (at assignment)

| Item | State at `1fb6775` |
|---|---|
| Claude / Codex / AGY / Astra in registry | present (`available-if-configured`, `needs-local-eval`) |
| HOWL-005 routing artifacts | present (`task-classes`, `selection-policy`, `docs/EXECUTOR_ROUTING.md`, etc.) |
| Measured specialist distinctions | absent (needs-local-eval) |
| Context budget constraint | EM ~194 chars headroom; registry compact; raw evidence referenced not embedded |

## Discovery hold

Owner open-discovery hold remains unchanged. HOWL-006 is Owner-authorized **activation/calibration** only.
