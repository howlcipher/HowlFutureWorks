# HOWL-006 — Assurance report (dual QA + Security)

**Verdict:** PASS WITH FINDINGS  
**Owner-complete:** NOT declared  
**Tip:** `65ac49e0c3c91183d3768b424a98eb1859d3c6dd`  
**PR:** https://github.com/howlcipher/HowlFutureWorks/pull/5 (open; **not merged** by Assurance)  
**Branch:** `feat/howl-006-executor-baseline`  
**Verified:** 2026-09-21 11:30:20 EDT  
**Worktree:** preferred `/workspace/HowlFutureWorks-howl006` absent; used `/workspace/HowlFutureWorks` @ tip  
**Venv:** `/workspace/.venv-hfw`  
**Independence:** Dev Lead claims cross-checked; not trusted alone. HOWL-007 not started.

## Verdict summary

Independent checks 1–11 support acceptance of the HOWL-006 baseline **with findings**. No blockers for the stated AC. Residual gaps are honest unknowns / headroom compression / minor doc lag — not fabricated rankings, secrets, HowlFrame weakenings, or budget-limit raises.

## Checks 1–11

| # | Check | Result | Notes |
|---|---|---|---|
| 1 | Runtime inventory accurate | **PASS** | Independent probes: Claude 2.1.278 authenticated (`loggedIn: true`, `authMethod: claude.ai`); Codex 0.155.1 authenticated (ChatGPT); AGY 1.2.7 authenticated (`agy models` lists); Astra = no distinct binary, `runtime_alias_of: codex`. Inventory md matches registry yaml. |
| 2 | Auth evidence contains NO secrets | **PASS** | Independent pattern scan of inventory/evidence/evals/registry: **0 hits** after demo-fixture filter. Auth recorded as status enums only. No live tokens/cookies/OTP in Git evidence. (PEM private-key armor checked by descriptive pattern name; no contiguous armor header literal written.) |
| 3 | EVAL-A..E real, bounded, labeled | **PASS** | README + all `result.json` carry INITIAL BASELINE / LOW SAMPLE / NOT PERMANENT RANKING. Fixtures tiny (~15 KB total under `evals/howl-006`). One combined isolated session per runtime; `/tmp/howl-006-runs/{claude,codex,agy}` still present with per-eval dirs. |
| 4 | No silent cross-executor fallback | **PASS** | Each `result.json` attributes claude/codex/agy separately; `cross_executor_fallback: false`. Astra `status: mapped_to_codex` with explicit `runtime_alias_of` — alias share, not silent failover. EVAL-B `fix_note` differs per executor (supports real separate runs). |
| 5 | Registry claims match evidence | **PASS** | Registry: install/auth/cli_version/benchmark_status=`baseline-evaluated` + evidence_ref; astra notes Owner clarification. No fabricated scores/rankings/permanent ordering. `scores_invented: false` in all results. |
| 6 | AVAILABLE ≠ preferred; install ≠ authority | **PASS** | Registry header + `status: available-if-configured`; selection-policy forbids permanent ranking / inventing scores; docs: “Merely having an executor installed is not a reason to invoke it”; profiles are not authority. |
| 7 | orgctl route proofs | **PASS** | Independently captured (`--risk`, not `--risk-tier`): trivial/R0→SELF; simple/R1→SELF; bounded/R2→SELF_preferred_unless_expected_value; complex/R3→eligible_profile_by_measured_fit (IV preferred); critical/R4→eligible_profile_by_measured_fit (IV **required**). `model_invoke: false`. SELF is a real decision. See `assurance-orgctl-route.txt`. |
| 8 | Quota/cost honest | **PASS** | Low-sample discipline documented; long-horizon quota/cost/reliability unknowns disclosed in inventory + security-review; selection-policy `quota_states` includes `unknown`→conservative; Astra shares Codex (no extra burn). |
| 9 | HowlFrame intact; child ≤ parent; recursive off | **PASS** | `recursive_delegation.default: off`; `child_privilege_may_exceed_parent: false`; `howlframe_bypass: forbidden`; pytest `test_privilege_howlframe_recursive_defaults` + validate detectors present; 99 passed. |
| 10 | Context budgets still pass | **PASS WITH FINDING** | `policies/budgets.yaml` and all `bots/*/context.yaml` `budget_chars` **identical** to main (not raised). `orgctl render-all` OK. Measured headroom: EM **172**/18000; online **84**/15000 (registry always-load grew 727→1715 bytes). EM headroom not “fixed” by raising limit. See Findings. |
| 11 | validate + pytest + secret scan + GHA | **PASS** | Local: `orgctl validate` → VALIDATION PASSED; `pytest -q` → **99 passed**; secret scan 0 hits. GHA on tip: `validate (3.11)` success, `validate (3.13)` success, `distribution` success (completed ~11:27 EDT). |

## Findings (non-blocking)

1. **Dev-lead always-load headroom compressed to 84 chars** after registry growth while `routing/capability-registry.yaml` remains in online always-load. Still within 15000 limit; limit not raised. Recommend future compaction or moving detailed notes out of always-load path (do **not** raise budget as first fix).
2. **EM measured headroom 172** vs Dev Lead handoff claim `em_headroom: 194` in local dirty `HOWL-006.json` — minor delta; both within budget. Do not trust DL alone.
3. **Preferred worktree** `/workspace/HowlFutureWorks-howl006` was absent; verification used `/workspace/HowlFutureWorks` @ tip `65ac49e0c3c91183d3768b424a98eb1859d3c6dd` (matches PR head).
4. **Doc lag:** `docs/EXECUTOR_ROUTING.md` still narrates `needs-local-eval until local evals exist` while registry is now `baseline-evaluated` — cosmetic; not a policy/HowlFrame issue.
5. **Local dirty file:** `reports/work-items/HOWL-006.json` modified in worktree (phase→assurance, assignee→bot-assurance-0001) but **not** on tip commit; tip verification unaffected. Assurance did not commit/merge.

## Gaps / residuals (honest)

- Long-horizon reliability, quota_state trends, cost curves unknown (low-sample only).
- MCP plugin catalogs not exhaustively enumerated.
- Raw `/tmp` run workspaces are disposable (not committed) — attribution rests on result.json + still-present `/tmp` dirs + differing EVAL-B fix notes.
- Owner-complete **not** declared by Assurance.

## Security (Assurance dual hat)

| Item | Result |
|---|---|
| Secrets in evidence/registry/evals | Clean (0 hits) |
| HowlFrame / privilege / recursive | Intact; defaults enforced by validate+tests |
| Auth handling | Enums only in Git; Owner-controlled |
| Astra mapping | Explicit Codex alias; no improvised third-party install |
| Rankings / scores | Forbidden labels honored; none invented |
| Authority expansion from install/auth | Not observed |

## Explicit non-actions

- Did **not** merge PR #5
- Did **not** start HOWL-007
- Did **not** print secrets/tokens/cookies/OTP
- Did **not** declare Owner-complete

## Artifact index

- `reports/work-items/HOWL-006/assurance-report.md` (this file)
- `reports/work-items/HOWL-006/assurance-commands.log`
- `reports/work-items/HOWL-006/assurance-orgctl-route.txt`
- `reports/work-items/HOWL-006/assurance-pytest.txt`
- `reports/work-items/HOWL-006/assurance-validate.txt`
- `reports/work-items/HOWL-006/assurance-secret-scan.txt`
- `reports/work-items/HOWL-006/assurance-files-changed.txt`
- `reports/work-items/HOWL-006/assurance-ci.txt`
- `evidence/howl-006-assurance-verify-65ac49e/SUMMARY.md`
- `evidence/2026-09-21-HOWL-006-assurance.yaml`
- `security/reviews/HOWL-006-assurance-2026-09-21.md`
