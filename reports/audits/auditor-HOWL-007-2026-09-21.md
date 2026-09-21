# Audit Report — HOWL-007 (Auditor)

Durable Git path (repo convention): `reports/audits/auditor-HOWL-007-2026-09-21.md` on **HowlFutureWorks** (prefer org repo for Auditor reports; howlboard does not hold org audit reports unless a separate convention says otherwise).  
Alternate under work-item folder: `reports/work-items/HOWL-007/auditor-report.md`

- Work item: HOWL-007 (HowlBoard informational mission `depends_on` visibility)
- Auditor: Heinrich Lunge (bot-auditor-0001)
- Supporting reconstruction: read-only investigation assist (did **not** implement; did **not** merge; did **not** rewrite Assurance as Auditor’s own; did **not** start HOWL-008)
- Report date: 2026-09-21 (America/Detroit)
- **Verdict: PASS WITH FINDINGS** (one **Medium** process/evidence finding; **no Critical**; Info residuals only otherwise)
- Product PR: https://github.com/howlcipher/howlboard/pull/7 (open, not draft, **not merged**)
- Product branch: `feat/howl-007-mission-dependencies`
- Product tip (audited): `eb86e95f40e7e794f338f33100814cb52967fe5c`
- Product base `main`: `8037dd878553ad4fd11ef18faf28eaa62e96d21d`
- Org evidence PR: https://github.com/howlcipher/HowlFutureWorks/pull/6 (open, not draft, **not merged**)
- Org evidence branch: `docs/howl-007-assurance`
- Org evidence tip (audited): `4f3a0f4aaa06cc7905e0c7a5765446e4a02bb6d5`
- Org base `main`: `008a259a7259c24a031b32940fb15c7900479990` (includes HOWL-006)
- Tip relationship: **reference-only** — org tip cites product SHA/PR; does **not** copy howlboard blobs (by design)
- Live CI @ product `eb86e95`: Build/Contract/Docs & SEO **SUCCESS**; `mergeable` MERGEABLE · `mergeStateStatus` **CLEAN**
- Live CI @ org `4f3a0f4`: validate (3.11) **SUCCESS**, validate (3.13) **SUCCESS**, distribution **SUCCESS**; `mergeable` MERGEABLE · `mergeStateStatus` **CLEAN** (was `unstable` at assignment; re-checked live — now clean)
- Owner-complete declared: **No** (`evidence/2026-09-21-HOWL-007-assurance.yaml` `owner_complete_declared: false`; PR bodies agree)
- Secrets scan (Auditor independent pattern scan of product changed files + org assurance tip files): **0 hits**; no contiguous PEM armor-header literal introduced in this draft
- Auditor did not implement: **Confirmed** (investigation + draft report only; parent lands; no product implementation; HOWL-008 not started)

## Scope

Independent reconstruction from Git/GitHub of whether HOWL-007 (informational `depends_on` on HowlBoard) claims are supported by Product/EM acceptance artifacts, SELF routing, implementation, Assurance QA+Security evidence, and live CI — **without** rewriting Engineering/Assurance findings as Auditor’s own, **without** product changes, **without** merge, **without** starting HOWL-008.

Git is authority. Chat claims disregarded where they conflict with SHAs/blobs/CI. Local unpushed objects are disclosed separately from remote tips.

## Claims evaluated (target questions)

| # | Claim / question | Auditor determination |
|---|---|---|
| 1 | Real documented product gap (`depends_on` unrendered)? | **Supported** — at base `8037dd8`, limitations/roadmap stated unrendered; create path and `mission_view.howl` lacked `depends_on`; domain_model Mission table omitted field |
| 2 | Product defined a bounded informational-only slice? | **Supported locally / Medium remote gap** — ACs 1–16 + non-goals exist at local unpushed `822d971`; **not** present on remote `main` or org PR #6 tip `4f3a0f4` |
| 3 | Task classification bounded/R2 reasonable? | **Supported (content) / Medium remote gap** — EM acceptance at local `822d971` classifies bounded/R2 with rationale; live `orgctl route` agrees; same remote-publish gap |
| 4 | SELF vs external routing evidence-based (SELF selected)? | **Supported (content + live route) / Medium remote gap** — decision record + EM selection table choose SELF; orgctl → `SELF_preferred_unless_expected_value`; decision record not on remote tip |
| 5 | Selected executor eligible / stayed in envelope? | **Supported** — SELF is always eligible under policy when sufficient; product tip is native howlboard HowlFrame/Go/docs edits within EM envelope; no external-executor invocation artifacts required |
| 6 | Astra treated as Codex alias (not fourth runtime)? | **Supported** — registry `runtime_alias_of: codex` (main/HOWL-006); EM/decision text treat Astra as alias; not used as implementer; decision record does not count Astra separately |
| 7 | Implementation stayed in scope (no ordering/authority/cycles/HowlPlane/gates/ChangeOps/graph)? | **Supported** — tip diff surface is create validator + mission_view render + fixtures/docs/tests; authority create defaults still `REQUIRE_APPROVAL` + empty gates; verification empty list; added lines only *deny* ordering/authority semantics in comments/copy |
| 8 | Assurance independently verified? | **Supported (product tip)** — independent go/docs/CI/secret/security pack on org tip `4f3a0f4` tip-locked to product `eb86e95`; Auditor re-ran go + docs + orgctl + CI. Routing reconstructability claim is weakened by Medium finding #1 (org Product/EM/routing docs not remote) |
| 9 | Security claims (`esc`, no handler-JS injection) supported? | **Supported** — `(call esc dep)` into HTML text; `TestDependsOnRender` XSS case; `TestDependsOnNeverInHandlerJS`; Assurance security companion agrees; Auditor re-ran DependsOn* PASS |
| 10 | Capability conclusions kept narrow (no permanent ranking from one task)? | **Supported** — no ranking/score keys introduced; selection-policy still forbids permanent_ranking / invent scores; decision notes “Not a ranking exercise”; no HOWL-007 permanent preference baked into howlboard |
| 11 | Context budgets not raised? | **Supported** — `policies/budgets.yaml` and all `budget_chars` identical on org main vs assurance tip (EM 18000 / DL 15000 / Assurance 14000 / Product 12000 / Auditor 14000). Local compaction `eb48dc7` moves always-load items only (**also unpushed**; limits unchanged) |
| 12 | Native publish preserved? | **Supported** — howlboard PR #7 is native git/gh publish (`feat/howl-007-mission-dependencies` @ `eb86e95`); org PR #6 references SHA/PR only (no product diff copy) |

### Additional mandated checks

| Check | Determination |
|---|---|
| Tip relationship product ↔ org evidence | **Supported (reference-only tip-lock)** — org tip `4f3a0f4` cites product `eb86e95` / PR #7; name-status vs main = 11 Assurance/evidence/security paths only |
| Live CI both PRs | **Supported** — product SUCCESS; org all three SUCCESS; both CLEAN/MERGEABLE on re-check |
| Owner-complete declared? | **No** |
| Secrets scan clean? | **Supported** — Assurance 0 hits; Auditor independent rescan 0 hits (product + org tip) |
| HOWL-008 started? | **No** — no HOWL-008 paths on product tip, org tip, or local feat branch |
| Field naming `depends` vs `depends_on` | **Supported** — persisted/API/docs field is `depends_on`; CSS `depends-*` / local `deps` presentation-only |

## Tips audited

| Tip | Full SHA | Role | Remote? |
|---|---|---|---|
| Product | `eb86e95f40e7e794f338f33100814cb52967fe5c` | howlboard HOWL-007 implementation (PR #7 head) | **Yes** |
| Product base | `8037dd878553ad4fd11ef18faf28eaa62e96d21d` | howlboard main at open | **Yes** |
| Org evidence / PR #6 head | `4f3a0f4aaa06cc7905e0c7a5765446e4a02bb6d5` | Assurance independent verification only | **Yes** |
| Org main | `008a259a7259c24a031b32940fb15c7900479990` | Includes HOWL-006 | **Yes** |
| Org Product+EM+routing (local only) | `822d97115491b0e0d71a7a5bafa86094b1d6f325` | product-definition / em-acceptance / decision-record / HOWL-007.json | **No** — not on GitHub |
| Org context compaction (local only) | `eb48dc766e319ec13823ba86ce8eababdbec731c` | always-load compaction; no budget raises | **No** — not on GitHub |

**Remote tip-lock (org evidence vs product):** org does not carry product blobs; pointer inventory at `evidence/2026-09-21-HOWL-007-assurance.yaml` + `evidence/howl-007-assurance-verify-eb86e95/SUMMARY.md`.

## Authoritative AC / acceptance source

- **Intended:** `reports/work-items/HOWL-007/product-definition.md`, `em-acceptance.md`, `routing/decision-records/HOWL-007.md`, `reports/work-items/HOWL-007.json`
- **Remote reality at audit time:** those four paths are **absent** from HowlFutureWorks `main` and from PR #6 tip `4f3a0f4`. They exist only as local Git objects under branch name `feat/howl-007-mission-dependencies` at `822d971` on the shared box (commit **not** reachable via `api.github.com` — 422 No commit found).
- Assurance pack on PR #6 **references** those paths for routing reconstructability — see Medium finding.

Product ACs as implemented were still independently checked against howlboard tip behavior + Assurance AC map (not trusted alone).

## Reconstruction answers (paths / SHAs)

### 1 — Real documented product gap

At howlboard base `8037dd8`:

| Evidence | Path / observation |
|---|---|
| Limitations gap | `docs/limitations.md`: `depends_on` “in the model but … neither populated nor rendered” |
| Roadmap gap | `docs/roadmap.md`: Dependencies — neither populated nor rendered |
| Create path | `backend/server.howl` — **no** `depends_on` at base |
| Shared view | `frontend/mission_view.howl` — **no** depends render at base |
| Domain table | `docs/domain_model.md` — Mission table **omitted** `depends_on` at base |

Tip `eb86e95` closes the documented gap for the informational slice (create + render + docs).

### 2 — Bounded informational-only Product slice

Local `822d971` `product-definition.md`: ACs 1–16; explicit non-goals (ordering, authority, cycles, HowlPlane, gates, ChangeOps, graph); no executor pre-pick; no budget raises. Matches shipped tip behavior.

**Caveat:** document not on remote org tip — Medium finding #1.

### 3 — Classification bounded / R2

Local `822d971` `em-acceptance.md`: task_class **bounded**, risk **R2**, tools coding/git, security note on escape. Reasonable for a scoped create+render+docs vertical that does not change authority/lifecycle.

Live Auditor probe at org tip:

```
python tools/orgctl.py route --task-class bounded --risk R2 --required-tool coding
→ decision: SELF_preferred_unless_expected_value
→ eligible: claude, codex, agy, astra (alias of codex)
```

### 4 — SELF selected (evidence-based)

Local decision record `routing/decision-records/HOWL-007.md`: `selected_executor: SELF`; reasons: bounded competence, SELF preferred when sufficient, no measured EV for specialist, quota unknown conservative, orgctl decision. EM selection table marks Claude/Codex/Astra/AGY eligible-not-selected.

Implementation consistency: howlboard PR #7 is ordinary product engineering (no external-runtime baseline/eval harness for this slice).

### 5 — Executor eligibility / envelope

SELF stayed in EM envelope: optional `depends_on` list; create validation fail-closed; round-trip; shared mission_view; DEMO fixture; esc; contract/render/docs tests; docs informational-only; native publish. No recursive external delegation; no budget raises; no HOWL-008.

### 6 — Astra = Codex alias

- `routing/capability-registry.yaml` (on org main / assurance tip): `astra.runtime_alias_of: codex`
- EM acceptance + decision record: Astra not a fourth runtime; not selected
- HOWL-007 did not invent a separate Astra install or ranking

### 7 — Scope held (non-goals)

Product tip file list (11 paths):

- `backend/server.howl`, `backend/contract_test.go`
- `frontend/mission_view.howl`, `frontend/render_harness.howl`
- `data/fixtures/missions.json`, `docs/missions.json`, `docs/demo.js`
- `docs/domain_model.md`, `docs/limitations.md`, `docs/roadmap.md`
- `scripts/test_docs.py`

Create path still seeds `authority` = `REQUIRE_APPROVAL` + empty `gates` and empty `verification` list (additive `depends_on` only). Spot-check of added lines: only comments/UI copy stating informational / non-ordering — no cycle/HowlPlane/ChangeOps/scheduler/graph enforcement.

### 8 — Assurance independent verification

Present on org tip `4f3a0f4`:

| Artifact | Path |
|---|---|
| Assurance report (PASS) | `reports/work-items/HOWL-007/assurance-report.md` |
| Commands / go / docs / CI / secret / files / routing | `reports/work-items/HOWL-007/assurance-*.txt|log` |
| Evidence SUMMARY | `evidence/howl-007-assurance-verify-eb86e95/SUMMARY.md` |
| Manifest | `evidence/2026-09-21-HOWL-007-assurance.yaml` |
| Security companion | `security/reviews/HOWL-007-assurance-2026-09-21.md` |

Auditor did **not** treat Assurance as sole truth: re-ran `go test ./...` → PASS; DependsOn* verbose PASS; `python3 scripts/test_docs.py` → PASS; `orgctl route` bounded/R2; live GitHub check-runs both PRs; secret pattern rescan 0; tip SHAs match assignment.

### 9 — Security (`esc` / no handler-JS)

- `frontend/mission_view.howl`: dependency IDs via `(call esc dep)` inside `<code>` HTML text; comment forbids handler JS
- `TestDependsOnRender` includes `<script>alert(1)</script>` case + onclick guard
- `TestDependsOnNeverInHandlerJS` source scan
- Fail-closed `INVALID_DEPENDS_ON` for non-list / non-string elements (contract cases)
- Assurance security review PASS; residual risk disclosed (free-form IDs; no existence check — by design)

### 10 — Narrow capability conclusions

No permanent ranking, no invented scores, no “HOWL-007 proves executor X preferred.” Org selection-policy forbids permanent_ranking / invent_capability_scores. Decision record: “Not a ranking exercise.”

### 11 — Context budgets

| Check | Result |
|---|---|
| `git diff main..4f3a0f4 -- policies/budgets.yaml` | empty |
| `budget_chars` on assurance tip vs main | identical |
| Local `eb48dc7` | always-load compaction only; message “No budget increases”; `budget_chars` still 18000/15000 |

### 12 — Native publish

howlboard PR #7 authored/committed on product branch via normal git; org assurance PR references tip SHA without copying product diff — matches EM publish envelope.

## Live CI (authoritative for merge posture)

| Check | Product tip `eb86e95` (PR #7) | Org tip `4f3a0f4` (PR #6) |
|---|---|---|
| Build, Contract Tests, Docs & SEO | **SUCCESS** | — |
| validate (3.11) | — | **SUCCESS** |
| validate (3.13) | — | **SUCCESS** |
| distribution | — | **SUCCESS** |
| mergeable / mergeStateStatus | MERGEABLE / **CLEAN** | MERGEABLE / **CLEAN** (was unstable at assignment; cleared on re-check ~12:51 EDT) |

## Findings

1. **Medium — Org Product/EM/routing evidence not on remote GitHub.**  
   Commits `822d971` (Product AC + EM acceptance + SELF routing decision + `HOWL-007.json`) and `eb48dc7` (always-load compaction) exist only on the shared-box local branch `feat/howl-007-mission-dependencies`. Remote refs: only `docs/howl-007-assurance` @ `4f3a0f4` (Assurance pack) and `main` @ `008a259`. GitHub API returns 422 for `822d971`. Assurance routing reconstructability therefore **cannot** be verified from the claimed remote org tip alone.  
   **Remediation for parent (do not treat as Auditor implement):** land `822d971` (and optionally `eb48dc7`) onto HowlFutureWorks (e.g. onto `docs/howl-007-assurance` or a sibling docs PR) so Product → EM → routing → Assurance → Auditor is reconstructable from remote Git before Owner-complete.

2. **Info — Tip relationship is reference-only by design.** Org evidence tip does not embed howlboard blobs; product logic locked to `eb86e95`. Acceptable; merge review should keep product and org tips paired by SHA.

3. **Info — Assignment-time org `mergeable_state: unstable` cleared.** Re-check shows CLEAN with all three checks SUCCESS.

4. **Info — Assurance residual notes (not re-owned):** demo.js UTF-8 em-dash mojibake in source view; `frontend/app.js` gitignored build output. Docs/render tests green; non-blocking.

5. **Info — Shared-box hygiene:** local HowlFutureWorks had dirty/stashed `HOWL-007.json` overlays and an unpushed feat branch. Tip verification for remote PR #6 used `docs/howl-007-assurance` @ `4f3a0f4`. Do not trust dirty working-tree overlays.

6. **Info — Land path preference:** primary Auditor report belongs on HowlFutureWorks (`reports/audits/...` + work-item copy). howlboard should not become the org audit home unless convention explicitly changes.

**Blocking findings:** none that invalidate the product tip’s informational `depends_on` delivery or green CI. Medium finding blocks **process completeness** of remote org reconstructability until Product/EM/routing docs are published.

## Exceptions

None requested.

## Unresolved risks (residual, non-blocking)

- Dependency IDs are free-form informational strings (no existence/cycle checks) — by design for this slice; operators must not treat UI as authority/ordering control.
- Org Product/EM/routing docs remain unpublished on GitHub until parent lands them (Medium finding).
- Secret-literal CI risk: avoid contiguous PEM armor-header substrings when landing this report (same hygiene as HOWL-004/006).

## Secrets-literal CI risks (note for landers)

- Do **not** paste contiguous PEM armor headers into evidence prose.
- Auditor high-signal rescan of product changed files and org assurance tip: **NONE**.

## Evidence paths inspected

| Path | Role |
|---|---|
| howlboard PR #7 metadata / check-runs / files | Product tip, CI, mergeability |
| HowlFutureWorks PR #6 metadata / check-runs / files | Org Assurance tip, CI, mergeability |
| howlboard `8037dd8..eb86e95` | Gap close + scope |
| `backend/server.howl`, `frontend/mission_view.howl`, fixtures, docs, tests | Implementation |
| Org tip Assurance pack + security review | Independent verification inventory |
| Local `822d971` Product/EM/routing (disclosed unpushed) | Classification / SELF selection content |
| `routing/capability-registry.yaml`, `selection-policy.yaml` | Astra alias + ranking forbids |
| Live `orgctl route`, `go test`, `test_docs.py` | Auditor re-run |
| `policies/budgets.yaml`, `bots/*/context.yaml` | Budget non-raise |

## Explicit declarations

| Item | Status |
|---|---|
| Owner-complete declared? | **No** (must remain false until Owner declares) |
| Auditor implemented product changes? | **No** |
| Auditor merged either PR? | **No** |
| HOWL-008 started? | **No** |
| Assurance findings rewritten as Auditor’s own? | **No** — independent reconstruction; Assurance used as pointer inventory |
| This supporting pass pushed to GitHub? | **No** — parent lands the report |
| Remote Product/EM/routing docs present on org tip? | **No** — Medium finding |

## Reconstruction result

**PASS WITH FINDINGS** (Medium #1 + Info residuals).

HowlBoard HOWL-007 informational `depends_on` reconstructs cleanly at product tip `eb86e95f40e7e794f338f33100814cb52967fe5c` (PR #7): real documented gap closed; create/API round-trip + fail-closed validation; shared mission_view render via `esc`; DEMO `HP-207` → `HF-412`; docs/tests updated; non-goals held; CI SUCCESS/CLEAN. Org Assurance tip `4f3a0f4aaa06cc7905e0c7a5765446e4a02bb6d5` tip-locks that product SHA with independent go/docs/CI/secret/security evidence and CI SUCCESS/CLEAN on re-check. SELF routing rationale is coherent and matches live orgctl, but Product definition / EM acceptance / decision record remain **unpushed local-only** (`822d971`) — parent should land those org docs onto the assurance branch (or equivalent) so remote Git reconstructability matches Assurance’s claim. Owner-complete **not** declared. Budgets not raised. Astra remains Codex alias. No permanent ranking. Native publish preserved. HOWL-008 not started.

### Durable Git path (for parent land)

- Primary: `reports/audits/auditor-HOWL-007-2026-09-21.md` on HowlFutureWorks branch `docs/howl-007-assurance` (org evidence PR #6)
- Also: `reports/work-items/HOWL-007/auditor-report.md`
- Prefer org repo; howlboard is not the home for org Auditor reports unless convention says otherwise
- **Also land (related Medium remediation, not this draft’s body alone):** unpublished `822d971` Product/EM/routing artifacts onto remote HowlFutureWorks

### Draft absolute paths (this supporting pass)

- `/workspace/audit-reports/HOWL-007/auditor-HOWL-007-2026-09-21.md`
- `/tmp/howl007-auditor/auditor-HOWL-007-2026-09-21.md`

— End of HOWL-007 audit report —

### Land note

Landed by Auditor on HowlFutureWorks branch `docs/howl-007-assurance` via native `git` push (Auditor report only). Product/EM/routing artifacts cited as local-only remain **unpublished** on remote tip at land time — Medium finding stands for Engineering/EM to push; Auditor did not author or rewrite those Product/EM documents.

— End of HOWL-007 audit report —
