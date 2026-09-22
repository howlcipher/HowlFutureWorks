# HOWL-008 — Assurance report (dual QA + Security)

**Verdict:** PASS  
**Owner-complete:** NOT declared  
**Product tip:** `41a91af6a6432e0df4eeec03f0a93acdb09e3794` (`howlcipher/howlboard`)  
**Product PR:** https://github.com/howlcipher/howlboard/pull/8 (open; **not merged** by Assurance)  
**Product branch:** `feat/howl-008-dependency-navigation` (base `cab020c`)  
**Org context:** HowlFutureWorks `reports/work-items/HOWL-008/{product-definition,em-acceptance,dev-lead-implementation}.md` + `routing/decision-records/HOWL-008.md`  
**Verified:** 2026-09-21 13:23:45 EDT  
**Worktree:** `/workspace/howlboard` clean @ tip (no dirty WT; worktree unnecessary)  
**Independence:** Product ACs and Dev Lead implementation cross-checked against tip diffs + real tests + CI; not trusted alone. HOWL-009 not started. Executor not re-picked.

## Verdict summary

Independent verification of navigable informational `depends_on` on HowlBoard tip `41a91af` supports **PASS**. Product ACs 1–17 map clean. Non-goals held. HOWL-007 create/round-trip/empty-block contracts still green. No mission ID interpolated into JS handler source; hostile ID coverage present. App `open_mission` get body uses `encode_json`. Demo remains read-only and shares `mission_view.howl`. Local `go test ./...` and `python3 scripts/test_docs.py` exit 0. CI check on PR #8 is SUCCESS on the same tip OID. Secrets scan of changed files: 0 hits. Routing SELF reconstructable as evidence-based (not preference); budgets not raised for this slice.

## AC map (Product 1–17)

| AC | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | Non-empty `depends_on` IDs as activatable controls (not inert `<code>`-only) | **PASS** | `mission_view.howl` emits `<button class="depends-link" …>`; inert `<li><code>` path removed; `TestDependsOnControlUsesDataAttrPattern` PASS |
| 2 | Controls in shared `frontend/mission_view.howl` (app + published demo) | **PASS** | App + `docs/demo.howl` both `(use … mission_view.howl)`; docs test “published demo shares the application's renderer” PASS |
| 3 | Activation calls existing `window.open_mission` / `open_mission` | **PASS** | Constant `onclick="window.open_mission(this.dataset.missionId)"` on depends controls (same as rows) |
| 4 | Mission ID in `data-mission-id` via `esc` | **PASS** | `(call esc dep)` into `data-mission-id`; render harness asserts escaped XSS ID in attribute |
| 5 | Handler source is a **constant** string (no ID→JS concat) | **PASS** | Constant onclick only; `TestDependsOnRender` rejects ID in onclick; `TestDependsOnNeverInHandlerJS` PASS |
| 6 | App `open_mission` get body via `encode_json` (not string-concat JSON) | **PASS** | `(encode_json (dict ("id" id)))`; `TestOpenMissionUsesEncodeJSON` PASS; old `{\"id\":\"` concat gone |
| 7 | Hostile / quote-bearing IDs cannot break out / inject | **PASS** | XSS + quote/`O'Brien` cases in `TestDependsOnRender`; esc of `<>"'` |
| 8 | Opening existing dependency loads that mission detail (app + demo paths) | **PASS** | App: existing `open_mission` → `/api/missions/get` + `render_detail`; demo: fixture lookup + `view/render_detail` |
| 9 | Missing target fails honestly (not silent no-op) | **PASS** | App: `Mission not found` + detail placeholder; demo: `Mission not found: …`; tests `TestOpenMissionUsesEncodeJSON` / `TestDemoOpenMissionReportsMissing` |
| 10 | Empty/missing `depends_on` → no dependency block | **PASS** | HOWL-007 empty branches preserved; harness checks undefined/`[]`/null/`""` omit block |
| 11 | UI/docs state informational only | **PASS** | Mission view copy + limitations/roadmap/domain_model; docs tests PASS |
| 12 | Non-goals remain true | **PASS** | See Non-goals section; tip diff has no ordering/blocking/cycles/authority/ChangeOps/HowlPlane/dispatch/graph logic |
| 13 | HOWL-007 backend `depends_on` contract compatible | **PASS** | `backend/server.howl` unchanged in tip; create/round-trip/empty/DEMO/INVALID_DEPENDS_ON still PASS |
| 14 | Tests cover navigation, absent, hostile, encode_json, docs drift | **PASS** | Extended `TestDependsOnRender` + new encode_json/demo/control tests + `scripts/test_docs.py` HOWL-008 checks |
| 15 | No HowlFutureWorks budget raises; no broad request-serialization refactor | **PASS** | `policies/budgets.yaml` + bots `budget_chars` identical to main; only `open_mission` get-body hardened |
| 16 | Product definition published early on HOWL-008 org branch | **PASS** | `product-definition.md` on `feat/howl-008-dependency-navigation` (af14374+) |
| 17 | Do not pre-pick executor in Product definition | **PASS** | Product AC17 + routing note defer to EM; EM selected SELF after AC |

## Non-goals held

Confirmed absent from HOWL-008 implementation surface (mission_view navigation + open_mission harden + demo missing-target + tests/docs/CSS only):

- Execution ordering
- Blocking / satisfaction semantics
- Cycle detection
- Authority / ChangeOps propagation
- HowlPlane scheduling
- Automatic dispatch
- Graph visualization
- Broad API request serialization refactor
- Context budget increases
- HOWL-009 auto-start
- Executor pre-selection / Assurance preference re-pick

Non-goal mentions in tip appear only as **exclusions** in limitations/roadmap wording (preserved).

## HOWL-007 contracts still green

| Contract | Result |
|---|---|
| `depends_on` create round-trips through get | **PASS** |
| omitted / empty list → no dependencies (`[]`) | **PASS** |
| DEMO fixture carries informational `depends_on` | **PASS** |
| INVALID_DEPENDS_ON fail-closed cases | **PASS** (under create_validates_input) |
| Empty/missing → no dependency block (render) | **PASS** (`TestDependsOnRender`) |
| No depends values in handler JS | **PASS** (`TestDependsOnNeverInHandlerJS`) |

`backend/server.howl` / `server.hfbc` **not** modified in this tip (navigation/UX + secure open path only).

## Security (Assurance dual hat)

| Item | Result |
|---|---|
| Untrusted dependency ID → `data-mission-id` via `esc` | **Pass** |
| Constant onclick; no ID interpolated into handler source | **Pass** |
| Hostile script / quote-bearing IDs covered by tests | **Pass** |
| App get body `encode_json` (no string-concat JSON) | **Pass** |
| Missing target honest failure (app + demo) | **Pass** |
| Demo remains read-only (no approve/reject/advance in demo) | **Pass** (docs tests) |
| Secrets in tip diff | **Pass** (0 hits) |
| CI green on tip | **Pass** (PR #8 SUCCESS; headOid matches) |

## Tests (real artifacts)

| Command | Exit | Artifact |
|---|---|---|
| `cd backend && go test ./...` | **0** | `assurance-go-test.txt` (`ok howlboard/backend`; all HOWL-007/008 DependsOn* + OpenMission* PASS) |
| `python3 scripts/test_docs.py` | **0** | `assurance-docs-test.txt` (20 checks incl HOWL-008 navigable/encode_json) |

## CI

`gh pr checks 8 -R howlcipher/howlboard`: **pass** — `Build, Contract Tests, Docs & SEO Verification` (SUCCESS, ~41s). PR head OID matches tip `41a91af6a6432e0df4eeec03f0a93acdb09e3794`. See `assurance-ci.txt`.

## Secrets

Independent scan of files changed vs `cab020c`: **0 hits** (split private-key armor fragments; AKIA; bearer/token patterns). Contiguous PEM armor header literal **not** written. See `assurance-secret-scan.txt`.

## Routing (SELF)

Reconstructable from org docs without preference re-pick: Product deferred (AC17) → EM bounded/R2 → orgctl SELF_preferred_unless_expected_value → SELF selected with fresh sufficiency rationale (in-repo row pattern; HOWL-007 = evidence not standing rule; no specialist EV; quota constrained) → decision-record `selected_executor: SELF`. Implementation is native howlboard publish (PR #8); stayed SELF. See `assurance-routing-review.txt`.

## Budgets

Org `policies/budgets.yaml` and bot `budget_chars` **identical to origin/main** for this branch. HOWL-008.json `context_budget_preflight.budgets_raised: false`. Limits remain EM 18000 / DL 15000 / Assurance 14000 / Product 12000 / Auditor 14000.

## Findings

None blocking. Informational notes only:

1. `docs/demo.js` is a large compiled artifact (expected HowlFrame emit churn); source of truth is `docs/demo.howl` + shared `mission_view.howl`; docs test confirms compiled demo shares renderer and offers no mutating actions.
2. CSS `.depends-link` added in both `frontend/styles.css` and `docs/style.css` for app + demo presentation — not schema drift.
3. Owner-complete not declared by implementer; Assurance does not declare it.

## Explicit non-actions

- Did **not** merge howlboard PR #8
- Did **not** start HOWL-009
- Did **not** print secrets
- Did **not** re-pick executor for preference
- Did **not** copy full product diff into HowlFutureWorks
- Did **not** declare Owner-complete

## Artifact index

- `reports/work-items/HOWL-008/assurance-report.md` (this file)
- `reports/work-items/HOWL-008/assurance-commands.log`
- `reports/work-items/HOWL-008/assurance-go-test.txt`
- `reports/work-items/HOWL-008/assurance-docs-test.txt`
- `reports/work-items/HOWL-008/assurance-ci.txt`
- `reports/work-items/HOWL-008/assurance-secret-scan.txt`
- `reports/work-items/HOWL-008/assurance-files-changed.txt`
- `reports/work-items/HOWL-008/assurance-routing-review.txt`
- `evidence/howl-008-assurance-verify-41a91af/SUMMARY.md`
- `evidence/2026-09-21-HOWL-008-assurance.yaml`
- `security/reviews/HOWL-008-assurance-2026-09-21.md`
