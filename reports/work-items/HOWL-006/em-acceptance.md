# HOWL-006 — EM acceptance

Status: **ACCEPTED** for implementation  
Author: bot-engmgr-0001 (Rintaro Okabe)  
Product definition: `reports/work-items/HOWL-006/product-definition.md` — accepted  
Implementation assignee: bot-devlead-0001 (Motoko Kusanagi)  
Branch: `feat/howl-006-executor-baseline`  
Risk: R2  
Publish: native `git`/`gh` (CloudAgent only if native fails; record why)

## Classification

Organizational activation/calibration — not product feature work. R&D not required unless a genuine unresolved experimental question appears.

## Context-budget constraint (binding)

| Bot | Used | Limit | Headroom |
|---|---:|---:|---:|
| engineering-manager | 17806 | 18000 | **194** |
| dev-lead | 13926 | 15000 | 1074 |
| assurance | 10896 | 14000 | 3104 |
| auditor | 10627 | 14000 | 3373 |
| product | 10051 | 12000 | 1949 |
| rnd | 10161 | 12000 | 1839 |

Rules:
- Do **not** raise budgets to fit HOWL-006.
- Do **not** add raw eval transcripts or large docs to always-load manifests.
- Capability registry must stay compact; evidence lives under `evals/` or `reports/work-items/HOWL-006/evidence/` and is **referenced**.
- After registry update, re-run `orgctl render-all` and confirm all bots still within budget — especially EM.

## Pre-inventory (EM, non-secret)

| Executor | Installed | Version | Auth (safe status) |
|---|---|---|---|
| Claude | yes | Claude Code 2.1.278 | not logged in |
| Codex | yes | codex-cli 0.155.1 | not logged in |
| AGY | yes | 1.2.7 | sign-in required (`agy models` asks to launch CLI to sign in) |
| Astra | **no** | — | n/a |

AVAILABLE ≠ preferred. Installed ≠ eligible for all risk classes.

## Owner AC themes (of record)

1. Runtime inventory (install/auth/tools/unknowns)
2. Owner-controlled auth — no secrets in chat/Git/evidence/memory
3. AVAILABLE ≠ preferred
4. Minimal EVAL-A..E — INITIAL BASELINE / LOW SAMPLE / NOT PERMANENT RANKING
5. Raw evidence ≠ registry; compact registry; on-demand refs
6. Quota discipline — no burn campaigns
7. `orgctl route` proofs: trivial/simple → SELF; bounded may stay evidence-insufficient; critical preserves risk
8. Assurance independent verify; Auditor reconstructable
9. Honest blocked/failed OK
10. Native PR path
11. SELF still preferred when appropriate

## Implementation envelope (Dev Lead)

1. **Branch** from current `main` (`1fb6775` or newer tip): `feat/howl-006-executor-baseline`
2. **Eval fixtures** — isolated disposable dirs/worktrees under e.g. `evals/howl-006/`; never mutate `main` solely for evals
3. **EVAL-A..E** — one (or very few) representative run(s) per available authenticated executor; label INITIAL BASELINE / LOW SAMPLE / NOT A PERMANENT RANKING
4. **Auth** — initiate official login flows; stop for Owner desktop takeover; record only `authenticated` / `not_authenticated` / `blocked` / `unknown`. Never paste keys/tokens/cookies/OTP into chat or Git.
5. **Astra** — official install only; if official path cannot be established confidently → `installation_status: blocked` with reason; do not improvise mirrors
6. **No cross-executor silent fallback** during baseline (Claude fail ≠ hand to Codex and mark Claude pass)
7. **Registry update** — compact fields only; `benchmark_status` → `baseline-evaluated` / `partially-evaluated` / `blocked` as justified; no global scores or permanent ordering
8. **Route proofs** — capture `orgctl route` for trivial, simple, bounded coding, complex (dry), critical — show SELF and evidence-insufficient/specialist-justified only if evidence supports
9. **Security** — scan evidence for secrets; HowlFrame intact; recursive delegation default off; no authority expansion from install
10. **Publish** — native push + PR; then hand Assurance

## Non-goals

No permanent rankings; no quota burn; no prod/destructive tests; no risk-policy change; no product features; no credential broadening; no new permanent Bots; no invented scores; no budget raises as first fix; do not start HOWL-007.

## Merge gates (do not waive)

Product AC · Dev Lead complete · Assurance PASS/PASS WITH FINDINGS · Auditor evidence in Git · orgctl validate · pytest · audit · dist · context budgets · GHA green · secret checks
