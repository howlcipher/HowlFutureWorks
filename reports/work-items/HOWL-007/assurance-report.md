# HOWL-007 — Assurance report (dual QA + Security)

**Verdict:** PASS  
**Owner-complete:** NOT declared  
**Product tip:** `eb86e95f40e7e794f338f33100814cb52967fe5c` (`howlcipher/howlboard`)  
**Product PR:** https://github.com/howlcipher/howlboard/pull/7 (open; **not merged** by Assurance)  
**Product branch:** `feat/howl-007-mission-dependencies` (base `8037dd8`)  
**Org context:** HowlFutureWorks `reports/work-items/HOWL-007/{product-definition,em-acceptance}.md` + `routing/decision-records/HOWL-007.md`  
**Verified:** 2026-09-21 12:47:43 EDT  
**Worktree:** `/workspace/howlboard` clean @ tip (no dirty WT; worktree unnecessary)  
**Independence:** Product ACs and Dev Lead implementation cross-checked against tip diffs + real tests + CI; not trusted alone. HOWL-008 not started.

## Verdict summary

Independent verification of informational `depends_on` on HowlBoard tip `eb86e95` supports **PASS**. Product ACs 1–16 map clean. Non-goals held. Authority/verification create defaults unchanged aside from additive `depends_on`. Field name is consistently `depends_on` (no `depends` field drift). Local `go test ./...` and `python3 scripts/test_docs.py` exit 0. CI check on PR #7 is SUCCESS on the same tip OID. Secrets scan of changed files: 0 hits. Routing SELF reconstructable; budgets not raised for this slice.

## AC map (Product 1–16)

| AC | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | Optional `depends_on` list of mission ID strings; empty/omitted = none | **PASS** | `validate_depends_on` + create stores `("depends_on" deps)`; contract: omitted/empty → `[]` |
| 2 | Supported create/input path (not hand-edit store) | **PASS** | `/api/missions/create` reads `body.depends_on` (`backend/server.howl`) |
| 3 | Round-trip create → API read used by UI | **PASS** | `TestMissionAPIContract/depends_on_create_round-trips_through_get` PASS |
| 4 | Invalid input fail-closed, clear error | **PASS** | Non-list / non-string → 400 `INVALID_DEPENDS_ON`; contract cases cover string/object/int/bool elements |
| 5 | Shared `mission_view.howl` renders IDs when non-empty | **PASS** | Renders `depends-block` + escaped `<code>` IDs; `TestDependsOnRender` PASS |
| 6 | Missing/empty → no dependency block | **PASS** | Empty/`""` branches no-op; harness checks undefined/`[]`/null/`""` omit block |
| 7 | Same shared view for app + published demo | **PASS** | `frontend/app.howl` and `docs/demo.howl` both `(use ... mission_view.howl)`; docs test “published demo shares the application's renderer” |
| 8 | Informational-only UI/docs copy | **PASS** | Mission view copy + limitations/roadmap/domain_model state informational; non-ordering |
| 9 | Non-goals remain true (ordering/authority/cycles/HowlPlane/gates/ChangeOps/graph) | **PASS** | No new ordering/cycle/scheduler/graph/gate logic in create or view; comments/docs explicitly exclude; authority dict default unchanged |
| 10 | DEMO fixture with non-empty `depends_on` | **PASS** | `HP-207` provenance `DEMO`, `depends_on: ["HF-412"]` in `data/fixtures/missions.json` and `docs/missions.json`; contract DEMO test PASS |
| 11 | HTML escape; no handler-JS injection | **PASS** | `(call esc dep)` into HTML text; `TestDependsOnRender` XSS case + `TestDependsOnNeverInHandlerJS`; source has no `onclick`+depends |
| 12 | Backend contract create/fetch round-trip (incl empty/absent) | **PASS** | Subtests listed in `assurance-go-test.txt` |
| 13 | Frontend/render tests present/absent block | **PASS** | `TestDependsOnRender` via `frontend/render_harness.howl` + Node DOM stub |
| 14 | Docs: limitations/roadmap no longer “unrendered”; informational + non-goals | **PASS** | `scripts/test_docs.py` checks PASS; tip text reviewed |
| 15 | `docs/domain_model.md` documents `depends_on` consistent with shipped semantics | **PASS** | Mission table row + docs test |
| 16 | No HowlFutureWorks context-budget raises; org routing did not pre-pick in Product def | **PASS** | `policies/budgets.yaml` identical to main; all `budget_chars` unchanged (EM 18000 / DL 15000 / Assurance 14000 / Product 12000 / Auditor 14000). Product def deferred executor; EM selected SELF after AC. Compact chore `eb48dc7` moved always-load items — **no limit raises**. |

## Non-goals held

Confirmed absent from HOWL-007 implementation surface (create validator + mission_view render + fixtures/docs/tests only):

- Automatic execution ordering
- Cross-mission authority enforcement
- Cycle detection / graph algorithms
- HowlPlane scheduling
- Dependency completion gates
- ChangeOps approval propagation
- Full dependency graph visualization

Spot-check: create path still seeds `authority` as `REQUIRE_APPROVAL` + empty gates and `verification` as empty list — same as base; `can_transition` not semantically altered (line-shift only from inserted validator).

## Field naming

- **Data field / API / fixtures / docs / tests:** consistently `depends_on`.
- **No** alternate persisted field named `depends`.
- UI CSS classes `depends-block` / `depends-label` / `depends-list` and local var `deps` are presentation/locals only — not schema drift.
- **Note:** PASS — no `depends` vs `depends_on` field-name drift.

## Tests (real artifacts)

| Command | Exit | Artifact |
|---|---|---|
| `cd backend && go test ./...` | **0** | `assurance-go-test.txt` (`ok howlboard/backend`; DependsOn* PASS) |
| `python3 scripts/test_docs.py` | **0** | `assurance-docs-test.txt` (all docs checks passed incl HOWL-007) |

## CI

`gh pr checks 7 -R howlcipher/howlboard`: **pass** — `Build, Contract Tests, Docs & SEO Verification` (SUCCESS). PR head OID matches tip `eb86e95f40e7e794f338f33100814cb52967fe5c`. See `assurance-ci.txt`.

## Secrets

Independent scan of files changed vs `8037dd8`: **0 hits** (split PEM private-key armor fragments; AKIA; bearer/api_key patterns). Contiguous PEM armor header literal **not** written. See `assurance-secret-scan.txt`.

## Routing (SELF)

Reconstructable from org docs without re-picking: Product deferred → EM bounded/R2 → orgctl SELF_preferred_unless_expected_value → SELF selected (no EV for specialist; quota unknown conservative) → decision-record `selected_executor: SELF`. Implementation is native howlboard publish (PR #7); stayed SELF. See `assurance-routing-review.txt`.

## Budgets

Org `policies/budgets.yaml` and bot `budget_chars` **not raised** attributable to HOWL-007. Org also holds docs/routing records for this product slice (expected). Context compaction commit exists but does not increase limits.

## Security (Assurance dual hat)

| Item | Result |
|---|---|
| Untrusted dependency ID strings | Escaped to HTML text only via existing `esc` |
| Handler JS interpolation | Guarded by source test + render harness |
| Authority / lifecycle semantics | Unchanged (additive field only) |
| Secrets in tip diff | Clean |
| Fail-closed validation | `INVALID_DEPENDS_ON` on bad types |

## Findings

None blocking. Informational notes only:

1. Compiled `docs/demo.js` shows UTF-8 em-dash as mojibake in source view (`â` sequence) — typical of HowlFrame JS emit; escaped ID path and informational string still present; docs/render tests green.
2. `frontend/app.js` is gitignored build output (present locally with `depends_on`); published path is `docs/demo.js` — consistent with Makefile.

## Explicit non-actions

- Did **not** merge howlboard PR #7
- Did **not** start HOWL-008
- Did **not** print secrets
- Did **not** re-pick executor
- Did **not** copy full product diff into HowlFutureWorks
- Did **not** declare Owner-complete

## Artifact index

- `reports/work-items/HOWL-007/assurance-report.md` (this file)
- `reports/work-items/HOWL-007/assurance-commands.log`
- `reports/work-items/HOWL-007/assurance-go-test.txt`
- `reports/work-items/HOWL-007/assurance-docs-test.txt`
- `reports/work-items/HOWL-007/assurance-ci.txt`
- `reports/work-items/HOWL-007/assurance-secret-scan.txt`
- `reports/work-items/HOWL-007/assurance-files-changed.txt`
- `reports/work-items/HOWL-007/assurance-routing-review.txt`
- `evidence/howl-007-assurance-verify-eb86e95/SUMMARY.md`
- `evidence/2026-09-21-HOWL-007-assurance.yaml`
- `security/reviews/HOWL-007-assurance-2026-09-21.md`
