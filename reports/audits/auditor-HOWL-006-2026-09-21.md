# Audit Report — HOWL-006 (Auditor)

Durable Git path (repo convention): `reports/audits/auditor-HOWL-006-2026-09-21.md`  
Alternate under work-item folder if EM prefers: `reports/work-items/HOWL-006/auditor-report.md`

- Work item: HOWL-006 (Activate and baseline external executors)
- Auditor: Heinrich Lunge (bot-auditor-0001)
- Supporting reconstruction: read-only investigation assist (did **not** implement; did **not** merge; did **not** rewrite Assurance as Auditor’s own; did **not** start HOWL-007)
- Report date: 2026-09-21 (America/Detroit)
- **Verdict: PASS WITH FINDINGS** (Info residuals only; **no Critical / Medium**)
- PR: https://github.com/howlcipher/HowlFutureWorks/pull/5 (open, not draft, **not merged**)
- Branch: `feat/howl-006-executor-baseline`
- Product tip (Assurance-verified / claimed): `65ac49e0c3c91183d3768b424a98eb1859d3c6dd`
- Assurance evidence tip / current PR head (audited): `ceabc1b1771902cc4d8d91d67621085f91d5d556`
- Base `main`: `1fb67757fb1ec3068b38f05e50480d5d0755c538` (includes HOWL-005)
- Tip-lock: **OK** — product blobs identical across tips; head adds Assurance evidence/security paths only
- Live CI @ `ceabc1b` (PR head): validate (3.11) **SUCCESS**, validate (3.13) **SUCCESS**, distribution **SUCCESS**
- Live CI @ `65ac49e` (product tip): validate (3.11) **SUCCESS**, validate (3.13) **SUCCESS**, distribution **SUCCESS**
- `mergeable`: MERGEABLE · `mergeStateStatus`: **CLEAN** (observed 2026-09-21 ~11:33 EDT)
- Owner-complete declared: **No** (confirmed in Git: `evidence/2026-09-21-HOWL-006-assurance.yaml` `owner_complete_declared: false`)
- Auditor did not implement: **Confirmed** (investigation + draft report only; parent lands; no product implementation)

## Scope

Independent reconstruction from Git/GitHub of whether HOWL-006 (executor runtime inventory + Owner-controlled auth + minimal EVAL-A..E + compact capability-registry updates) claims are supported by Product/EM acceptance artifacts, implementation, eval evidence, Assurance QA+Security evidence, and live CI — **without** rewriting Engineering/Assurance findings as Auditor’s own, **without** product changes, **without** merge, **without** starting HOWL-007.

Git is authority. Chat claims disregarded where they conflict with SHAs/blobs/CI.

## Claims evaluated (target questions)

| # | Claim / question | Auditor determination |
|---|---|---|
| 1 | Which executors actually configured/authenticated? | **Supported** — Claude, Codex, AGY authenticated; Astra authenticated **via Codex alias** (not a distinct binary) |
| 2 | Auth without secrets in Git/evidence? | **Supported** — status enums only; Auditor high-signal rescan **NONE** |
| 3 | Exact baseline tasks run (EVAL-A..E)? | **Supported** — A isolated-fix, B debugging, C security-remediation, D cross-cut-edit, E orchestration-smoke |
| 4 | Evidence supporting each registry claim? | **Supported** — inventory + `evals/howl-006/*/result.json` + `evidence_ref` |
| 5 | Failed/blocked results retained honestly? | **Supported** — pre-auth `blocked:*` retained at `fcb08fc`; tip supersedes with post-auth outcomes (history intact) |
| 6 | Assurance independently verified? | **Supported** — tip-locked pack + Auditor local re-run |
| 7 | Any permanent rankings introduced? (must not) | **Supported (none)** — policy forbid + labels + no score/rank keys |
| 8 | Router still prefers SELF for trivial/simple? | **Supported** — live `orgctl route` → `SELF` |
| 9 | Quota/scarcity honesty? | **Supported** — one combined run/runtime; Astra no extra burn; unknowns disclosed |
| 10 | Context budgets bounded (esp. EM / Dev Lead always-load)? | **Supported with Info finding** — limits **not** raised; Dev Lead headroom **84**; EM **172** |
| 11 | Install/auth ≠ authority expansion? | **Supported** — AVAILABLE≠preferred; install≠invoke; SELF still default |
| 12 | Claims limited by sample size (INITIAL BASELINE / LOW SAMPLE)? | **Supported** — labels on README + all `result.json` |
| 13 | Astra correctly represented as Codex alias (Owner clarification)? | **Supported** — `runtime_alias_of: codex`; Owner clarification in work item + inventory |

### Additional mandated checks

| Check | Determination |
|---|---|
| Tip-lock product vs evidence tip | **Supported** — `git diff --name-only 65ac49e ceabc1b` = 11 Assurance/evidence/security paths only; spot-checked product blobs identical |
| Live CI on current head | **Supported** — all three checks SUCCESS on `ceabc1b` and on product tip `65ac49e` |
| Owner-complete declared? | **No** |
| No inflated capability beyond baseline sample | **Supported** — `baseline-evaluated` + LOW SAMPLE labels; long-horizon unknowns disclosed |
| HowlFrame / routing invariants from HOWL-005 intact | **Supported** — `howlframe_bypass: forbidden`; child privilege false; recursive default off; permanent_ranking/invent scores forbidden; tool-access unchanged vs main |
| HOWL-007 started? | **No** — no `HOWL-007` paths at tip |

## Tips audited

| Tip | Full SHA | Role |
|---|---|---|
| Product | `65ac49e0c3c91183d3768b424a98eb1859d3c6dd` | Owner Astra=Codex clarification on work item (after authenticated inventory/evals `44cabd7`) |
| Evidence / PR head | `ceabc1b1771902cc4d8d91d67621085f91d5d556` | Assurance independent verification evidence only |
| Auth/evals product land | `44cabd7a40b25e1564d222dcb1ecbc0df190882e` | Authenticated inventory + EVAL results + registry |
| Pre-auth honest blocked | `fcb08fc573944b2094062eea4bfa99c1efb7bde5` | Inventory/evals with `not_authenticated` / `blocked:not_installed` |
| Base main | `1fb67757fb1ec3068b38f05e50480d5d0755c538` | Merge of HOWL-005 |

**Tip-lock verification:** `git diff --name-only 65ac49e0c3c91183d3768b424a98eb1859d3c6dd ceabc1b1771902cc4d8d91d67621085f91d5d556` lists only:

- `evidence/2026-09-21-HOWL-006-assurance.yaml`
- `evidence/howl-006-assurance-verify-65ac49e/SUMMARY.md`
- `reports/work-items/HOWL-006/assurance-*` (8 files)
- `security/reviews/HOWL-006-assurance-2026-09-21.md`

Spot-checked identical blobs at both tips for: `routing/capability-registry.yaml`, `routing/selection-policy.yaml`, `policies/budgets.yaml`, `policies/tool-access.yaml`, `evals/howl-006/EVAL-A/result.json`, `reports/work-items/HOWL-006/runtime-inventory.md`.

## Authoritative AC / acceptance source

- `reports/work-items/HOWL-006/em-acceptance.md` (EM ACCEPTED; Owner AC themes 1–11)
- `reports/work-items/HOWL-006/product-definition.md`
- Committed tip `reports/work-items/HOWL-006.json` (phase `baseline-evaluation` at tip; **do not trust dirty working-tree overlays** on shared boxes — local dirty phase/assignee overlay observed, **not** on tip)

## Reconstruction answers (paths / SHAs)

### 1 — Executors configured / authenticated

| Executor | Install | Auth (tip `65ac49e`) | Evidence |
|---|---|---|---|
| SELF | n/a (orgctl) | n/a | `reports/work-items/HOWL-006/runtime-inventory.md` |
| Claude | installed 2.1.278 | **authenticated** (`claude.ai`) | inventory + registry `auth_status: authenticated` |
| Codex | installed 0.155.1 | **authenticated** (ChatGPT) | same |
| AGY | installed 1.2.7 | **authenticated** (`agy models` listable) | same |
| Astra | same as Codex | **authenticated via Codex** | `runtime_alias_of: codex`; Owner clarification in `HOWL-006.json` `owner_clarifications` |

Pre-auth honesty at `fcb08fc`: Claude/Codex/AGY `not_authenticated`; Astra `installation_status: blocked` (official path unclear) — later corrected by Owner “Astra is Codex” clarification, not by improvising a third-party install.

### 2 — Auth without secrets

- Probe rule documented: only `authenticated` \| `not_authenticated` \| `blocked` \| `unknown`.
- Dev Lead scan: `reports/work-items/HOWL-006/evidence/secret-scan.txt`
- Assurance scan: `reports/work-items/HOWL-006/assurance-secret-scan.txt` (0 hits)
- Auditor independent high-signal rescan of HOWL-006 reports/evals/registry/assurance evidence/security review: **NONE**
- No contiguous PEM private-key armor header literals introduced in this draft (CI-sensitive pattern).

### 3 — Exact baseline tasks (EVAL-A..E)

| Eval | Kind | Path |
|---|---|---|
| EVAL-A | isolated-fix | `evals/howl-006/EVAL-A/` |
| EVAL-B | debugging | `evals/howl-006/EVAL-B/` |
| EVAL-C | security-remediation | `evals/howl-006/EVAL-C/` |
| EVAL-D | cross-cut-edit | `evals/howl-006/EVAL-D/` |
| EVAL-E | orchestration-smoke | `evals/howl-006/EVAL-E/` |

Harness README: `evals/howl-006/README.md`. Mode: **one combined isolated session per authenticated runtime** (Claude, Codex, AGY); Astra shares Codex. Compact summary: `reports/work-items/HOWL-006/evidence/eval-run-summary.md`.

### 4 — Registry claims ↔ evidence

At tip `65ac49e` / head `ceabc1b`, `routing/capability-registry.yaml`:

- Each of claude/codex/agy/astra: `status: available-if-configured`, `install_status: installed`, `auth_status: authenticated`, `benchmark_status: baseline-evaluated`, `evidence_ref: reports/work-items/HOWL-006/runtime-inventory.md`
- Astra: `runtime_alias_of: codex` + Owner clarification notes
- Header: “AVAILABLE ≠ preferred. No rankings/scores.”
- Per-eval outcomes: `evals/howl-006/EVAL-{A..E}/result.json` (`outcome: pass` for claude/codex/agy; astra `status: mapped_to_codex`)
- EVAL-B `fix_note` differs per executor (supports separate real runs, not copy-paste identical fabrications)

### 5 — Failed/blocked retained honestly

- Tip results are all post-auth **pass** (expected after Owner login).
- Git history at `fcb08fc` retains honest blocked eval JSON (`blocked:not_authenticated` / `blocked:not_installed`) and blocked registry `benchmark_status: blocked` / Astra `install_status: blocked`.
- No silent rewrite that erases pre-auth failure from history. Tip supersession is chronological, not denial.

### 6 — Assurance independent verification

Pack present (tip `ceabc1b`):

| Artifact | Path |
|---|---|
| Assurance report | `reports/work-items/HOWL-006/assurance-report.md` (verdict PASS WITH FINDINGS; tip `65ac49e`) |
| Commands / route / pytest / validate / secret / files / CI | `reports/work-items/HOWL-006/assurance-*.txt|log` |
| Evidence SUMMARY | `evidence/howl-006-assurance-verify-65ac49e/SUMMARY.md` |
| Manifest | `evidence/2026-09-21-HOWL-006-assurance.yaml` |
| Security companion | `security/reviews/HOWL-006-assurance-2026-09-21.md` (distinct from Dev Lead `reports/work-items/HOWL-006/security-review.md`) |

Auditor did **not** treat Assurance as sole truth: re-ran `orgctl validate` → VALIDATION PASSED; `pytest -q` → **99 passed**; `orgctl route` matrix; tip-lock; CI via GitHub check-runs; secret rescan.

### 7 — Permanent rankings (must not)

- `routing/selection-policy.yaml`: `permanent_ranking: forbidden`, `provider_loyalty: forbidden`, `invent_capability_scores: forbidden`
- All EVAL `result.json`: `scores_invented: false`; labels include **NOT PERMANENT RANKING**
- Registry: no numeric score/rank/preference keys on executor entries
- Route rationales: “choose by measured fit not loyalty/rankings”

### 8 — Router prefers SELF for trivial/simple

Auditor live re-run at head `ceabc1b`:

| Task / risk | `decision` | `model_invoke` |
|---|---|---|
| trivial / R0 | **SELF** | false |
| simple / R1 | **SELF** | false |
| bounded / R2 | SELF_preferred_unless_expected_value | false |
| complex / R3 | eligible_profile_by_measured_fit | false |
| critical / R4 | eligible_profile_by_measured_fit; `independent_verification: required` | false |

Committed proofs: `reports/work-items/HOWL-006/evidence/route-proofs.md`; Assurance capture: `assurance-orgctl-route.txt`.

### 9 — Quota / scarcity honesty

- One combined A..E session per authenticated runtime; Astra shares Codex (**no extra burn**)
- Inventory + security reviews disclose long-horizon quota/cost/reliability **unknown**
- Selection policy retains scarce/unknown quota conservatism from HOWL-005
- Fixtures tiny (~136K tree; fixture sources ~few KB)

### 10 — Context budgets bounded

- `policies/budgets.yaml` and all `bots/*/context.yaml` `budget_chars` **identical to main** (`git diff 1fb6775..ceabc1b -- policies/budgets.yaml` empty; Assurance blob-same check)
- Measured rendered always-load (Auditor reproduced via `build/bots/*.md` sizes matching Assurance log):
  - engineering-manager: used **17828** / 18000 → headroom **172**
  - dev-lead: used **14916** / 15000 → headroom **84** (registry growth 727→1715 bytes on always-load path)
- Limits **not** raised to “fix” headroom. **Info finding** below.

### 11 — Install/auth ≠ authority expansion

- Route rationale still includes “merely having an executor installed is not a reason to invoke it”
- Registry `status` remains `available-if-configured` (not “preferred”)
- Trivial/simple still SELF despite authenticated externals
- HowlFrame / child privilege / recursive defaults unchanged vs HOWL-005

### 12 — Sample-size limited claims

Every EVAL README + `result.json` carries labels: **INITIAL BASELINE**, **LOW SAMPLE**, **NOT PERMANENT RANKING**. Gaps section discloses MCP catalogs incomplete and long-horizon unknowns. No production-ranking or permanent-preference language in registry.

### 13 — Astra = Codex alias (Owner clarification)

- `routing/capability-registry.yaml` `astra.runtime_alias_of: codex`
- `reports/work-items/HOWL-006/runtime-inventory.md` Astra mapping section
- `reports/work-items/HOWL-006.json` `owner_clarifications` + `auth_state_verified.astra: alias_of_codex` (tip `65ac49e`)
- EVAL results: astra `status: mapped_to_codex` sharing Codex `fix_note` on EVAL-B
- Pre-auth blocked-install stance at `fcb08fc` correctly retired only after Owner clarification — no improvised DataStax/Open-Astra install

## Live CI (authoritative for merge posture)

| Check | Tip `65ac49e` (product) | Tip `ceabc1b` (PR head) |
|---|---|---|
| validate (3.11) | SUCCESS | SUCCESS |
| validate (3.13) | SUCCESS | SUCCESS |
| distribution | SUCCESS (~11:27 EDT on product tip run) | SUCCESS (completed ~11:32 EDT / 15:32Z) |
| mergeable_state | — | **CLEAN** / MERGEABLE |

Assurance at handoff claimed green on product tip — **confirmed**. Current head also green (Assurance evidence commit re-triggered checks; all SUCCESS).

## Findings

1. **Info — Tip-lock by design:** Assurance verified product tip `65ac49e`; PR head `ceabc1b` is evidence-land only. Product blobs unchanged. Acceptable pattern; merge review should treat product logic as locked to `65ac49e`.
2. **Info — Dev Lead always-load headroom compressed to 84** after `routing/capability-registry.yaml` growth (727→1715 bytes) while registry remains in online always-load. Still within 15000; **limits not raised**. Prefer future compaction / moving verbose notes out of always-load over raising budgets (same residual Assurance recorded).
3. **Info — EM headroom 172 vs earlier Dev Lead handoff claim 194** in work-item preflight / dirty overlay — minor delta; both within budget. Do not trust dirty `HOWL-006.json` alone.
4. **Info — Doc lag:** `docs/EXECUTOR_ROUTING.md` still narrates `needs-local-eval` while registry is now `baseline-evaluated` — cosmetic; policy/HowlFrame intact.
5. **Info — Shared-box hygiene:** Local worktree had **uncommitted** edits to `reports/work-items/HOWL-006.json` (not on tip). Tip verification unaffected. Parent should ignore dirty overlay.
6. **Info — Preferred worktree** `/workspace/HowlFutureWorks-howl006` was absent for Assurance; verification used shared `/workspace/HowlFutureWorks` @ tip (Assurance finding; reconstructable; non-blocking).
7. **Info — Raw `/tmp/howl-006-runs/{claude,codex,agy}` disposable:** still present on this box at audit time as corroboration; durable attribution rests on committed `result.json` (+ differing EVAL-B fix notes). Absolute proof of every CLI token interaction is not in Git (expected for quota discipline).

**Blocking findings:** none.

## Exceptions

None.

## Unresolved risks (residual, non-blocking)

- Low-sample baseline only — long-horizon reliability, quota_state trends, and cost curves remain unknown.
- MCP plugin catalogs not exhaustively enumerated.
- Operators must still apply hard constraints (tools/risk/privilege/HowlFrame/quota) against task envelopes — `orgctl route` documents filter as operator-applied.
- Always-load headroom on Dev Lead (84) is operationally tight for future always-load additions.
- Secret-literal CI risk: prior HOWL-004 failure mode was contiguous PEM armor-header substrings in evidence prose. This Auditor draft avoids contiguous PEM armor-header literals. Do not reintroduce them when landing.

## Secrets-literal CI risks (note for landers)

- Repo test asserts absence of contiguous PEM armor header form in tracked text.
- HOWL-006 evidence currently **clean** of that contiguous form and of high-signal token patterns (Auditor rescan: **NONE**).
- When landing this report: do **not** paste contiguous PEM armor headers; refer to “PEM armor header” or split tokens as the test does.

## Evidence paths inspected

| Path | Role |
|---|---|
| PR #5 metadata / commits / check-runs | Head SHA, mergeability, CI |
| `reports/work-items/HOWL-006/em-acceptance.md` | EM acceptance / Owner AC themes |
| `reports/work-items/HOWL-006/product-definition.md` | Problem / non-goals |
| `reports/work-items/HOWL-006.json` | Work item (committed tip content) |
| `reports/work-items/HOWL-006/runtime-inventory.md` | Non-secret install/auth inventory |
| `evals/howl-006/**` | EVAL-A..E fixtures + `result.json` |
| `reports/work-items/HOWL-006/evidence/*` | Eval summary, route proofs, secret scan |
| `routing/capability-registry.yaml` | Compact registry claims |
| `routing/selection-policy.yaml`, `docs/EXECUTOR_ROUTING.md` | HOWL-005 invariants |
| `policies/tool-access.yaml`, `policies/budgets.yaml`, `bots/*/context.yaml` | HowlFrame / budgets |
| `tools/orgctl.py`, `tests/test_executor_routing.py` | Route + regression |
| `reports/work-items/HOWL-006/assurance-*` | Assurance pack |
| `evidence/howl-006-assurance-verify-65ac49e/SUMMARY.md` | Tip lock pointer |
| `evidence/2026-09-21-HOWL-006-assurance.yaml` | Manifest (`owner_complete_declared: false`) |
| `security/reviews/HOWL-006-assurance-2026-09-21.md` | Assurance Security companion |
| `reports/work-items/HOWL-006/security-review.md` | Dev Lead security write-up (not sole trust) |
| Git history `fcb08fc` | Pre-auth blocked honesty |
| Local Auditor re-run | validate PASS; pytest 99; route matrix; tip-lock; CI |

## Explicit declarations

| Item | Status |
|---|---|
| Owner-complete declared? | **No** (must remain false until Owner declares) |
| Auditor implemented product changes? | **No** |
| Auditor merged PR? | **No** |
| HOWL-007 started? | **No** |
| Assurance findings rewritten as Auditor’s own? | **No** — independent reconstruction; Assurance used as pointer inventory |
| This supporting pass pushed to GitHub? | **No** — parent lands the report |

## Reconstruction result

**PASS WITH FINDINGS** (Info only).

HOWL-006’s authenticated executor baseline reconstructs from Git at product tip `65ac49e0c3c91183d3768b424a98eb1859d3c6dd`, with tip-locked Assurance evidence on `ceabc1b1771902cc4d8d91d67621085f91d5d556`. Claude/Codex/AGY authenticated with enum-only auth evidence; Astra correctly aliased to Codex per Owner clarification; EVAL-A..E labeled INITIAL BASELINE / LOW SAMPLE / NOT PERMANENT RANKING with no invented scores or permanent rankings; SELF still preferred for trivial/simple; HowlFrame/privilege/recursive/secrets controls from HOWL-005 intact; budgets not raised (tight Dev Lead headroom acknowledged); live validate+distribution green on product tip and PR head; Owner-complete **not** declared. Ready for Owner merge decision subject to Info residuals above.

### Durable Git path (for parent land)

- Primary: `reports/audits/auditor-HOWL-006-2026-09-21.md`
- Also note: `reports/work-items/HOWL-006/auditor-report.md`

### Draft absolute paths (this supporting pass)

- `/workspace/audit-reports/HOWL-006/auditor-HOWL-006-2026-09-21.md`
- `/tmp/howl006-auditor/auditor-HOWL-006-2026-09-21.md`

— End of HOWL-006 audit report —

### Land note

Landed by Auditor on PR branch `feat/howl-006-executor-baseline` via native `git` push. Duplicate at `reports/work-items/HOWL-006/auditor-report.md` per EM path request.

— End of HOWL-006 audit report —
