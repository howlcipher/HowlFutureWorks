# Audit Report — HOWL-005 (Auditor)

Durable Git path: `reports/audits/auditor-HOWL-005-2026-09-20.md`  
(Alternate under work-item folder if EM prefers: `reports/work-items/HOWL-005/auditor-report.md` — **repo convention for prior HOWL audits is `reports/audits/`**.)

- Work item: HOWL-005 (Intelligent Executor Routing)
- Auditor: Heinrich Lunge (bot-auditor-0001)
- Supporting reconstruction: read-only investigation assist (did not implement; did not merge; did not start HOWL-006)
- Report date: 2026-09-20 (America/Detroit)
- **Verdict: PASS WITH FINDINGS** (Info residuals only; **no Critical / Medium**)
- PR: https://github.com/howlcipher/HowlFutureWorks/pull/4 (open, not draft)
- Branch: `feat/howl-005-executor-routing`
- Product tip (Assurance-verified / claimed): `069c73ba5f7f2da26ea1f9d7a2eef3beb8c6103b`
- Assurance evidence tip / current PR head (audited): `df6148ac3b5ebd1b7ea31df66257e26f422e54d9`
- Base `main`: `a5554eab36425f5496cd1059a9312cef1bd9463a` (includes HOWL-004)
- Tip-lock: **OK** — product blobs identical across tips; head adds Assurance evidence only
- Live CI @ `df6148a`: validate (3.11) **SUCCESS**, validate (3.13) **SUCCESS**, distribution **SUCCESS**
- `mergeable`: MERGEABLE · `mergeStateStatus`: **CLEAN** (observed 2026-09-20 ~23:37 EDT)
- Owner-complete declared: **No** (confirmed in Git)
- Auditor did not implement: **Confirmed** (investigation + durable report land; no product implementation)

## Scope

Independent reconstruction from Git/GitHub of whether HOWL-005 (deterministic executor routing policy + tooling) claims are supported by Product/EM acceptance artifacts, implementation, tests, Assurance QA+Security evidence, and live CI — **without** rewriting Engineering/Assurance findings as Auditor’s own, **without** product changes, **without** merge, **without** starting HOWL-006.

Git is authority. Chat claims disregarded where they conflict with SHAs/blobs/CI.

## Claims evaluated (target questions)

| # | Claim | Auditor determination |
|---|---|---|
| 1 | Why the routing system exists is clear and justified | **Supported** |
| 2 | Product criteria (Owner ACs 1–36) were met | **Supported** (mapped below) |
| 3 | Implementation does **not** encode permanent provider preferences | **Supported** |
| 4 | Self-handling is truly the default for ordinary/trivial/simple work | **Supported** |
| 5 | Capability uncertainty is represented honestly (no invented scores) | **Supported** |
| 6 | Higher-cost executors can still be selected when warranted | **Supported** (policy + code path; cold-start Info residual) |
| 7 | Risk controls override cost optimization | **Supported** |
| 8 | Assurance independently tested (evidence in Git); tip lock; CI live | **Supported** |
| 9 | Native GitHub governance preserved (no CloudAgent for publish) | **Supported** with Info absolute-proof limit |

### Additional mandated checks

| Check | Determination |
|---|---|
| HowlFrame intact | **Supported** (`howlframe_bypass: forbidden`; `policies/tool-access.yaml` `direct_executor_cli_bypass_of_howlframe: forbidden` unchanged vs `a5554ea`) |
| Child privilege bounded | **Supported** (`child_privilege_may_exceed_parent: false`; tool-access `child_worker_may_exceed_parent_scope: false`) |
| Recursive delegation default off | **Supported** (`recursive_delegation.default: off`; validate rejects `on`; tests) |
| No secrets in routing | **Supported** (policy forbid + Auditor high-signal scan NONE on routing/HOWL-005 evidence) |
| Builder not sole verifier for critical work | **Supported** (`builder_not_sole_verifier`; critical `independent_verification: required`; different provider ≠ independence) |

## Tips audited

| Tip | Full SHA | Role |
|---|---|---|
| Product | `069c73ba5f7f2da26ea1f9d7a2eef3beb8c6103b` | `feat(HOWL-005): deterministic executor routing policy and tooling` — 20 paths vs main |
| Evidence / PR head | `df6148ac3b5ebd1b7ea31df66257e26f422e54d9` | `docs(HOWL-005): add Assurance independent verification evidence` — +10 evidence/security paths only |
| Base main | `a5554eab36425f5496cd1059a9312cef1bd9463a` | Merge of HOWL-004 |

**Tip-lock verification:** `git diff --name-only 069c73b df6148a` lists only Assurance/evidence/security-review paths. Spot-checked blobs identical at both tips for `routing/selection-policy.yaml`, `routing/capability-registry.yaml`, `tools/orgctl.py`, `tests/test_executor_routing.py`, `reports/work-items/HOWL-005/em-acceptance.md`.

## Authoritative AC source

Owner ACs **1–36** listed in full in:

- `reports/work-items/HOWL-005/em-acceptance.md` (AC checklist of record)
- Distilled in `reports/work-items/HOWL-005/product-definition.md`
- Theme list also in committed `reports/work-items/HOWL-005.json` (phase `implementation` at tip; **do not trust dirty working-tree overlays** on shared boxes)

## Claims table / AC mapping summary (independent)

Auditor re-verified against policy YAML + `orgctl route` + validate rules + tests at tip `df6148a` (product logic = `069c73b`). Assurance pack was read for pointer inventory, then each claim was reconstructed from product/policy/code — **not** copied as Auditor verdict.

| AC | Short statement | Independent evidence | Result |
|----|-----------------|----------------------|--------|
| 1 | Trivial → SELF | `routing/task-classes.yaml` `default_executor: SELF`; `orgctl route --task-class trivial` → `decision: SELF`; `tests/test_executor_routing.py::test_trivial_and_simple_default_to_self`, `test_route_trivial_selects_self` | PASS |
| 2 | Simple → SELF | Same files; route simple/R2 → SELF; tests | PASS |
| 3 | External needs expected value | `selection-policy.yaml` `external_requires_expected_value: true`; task-classes `external_delegation: requires_expected_value`; route rationale | PASS |
| 4 | Installed ≠ invoke | Route rationale string; `AGENTS.md` Executor routing invariant; docs | PASS |
| 5 | Deterministic ops avoid AI | `route_inspect` `model_invoke: false`; self_preferred; docs | PASS |
| 6 | Task classes defined | `task-classes.yaml`: trivial/simple/bounded/complex/critical | PASS |
| 7 | Complexity ≠ risk | `complexity_does_not_override_risk: true`; risk source `policies/risk-tiers.yaml`; routing-policy echo | PASS |
| 8–10 | Claude/Codex/AGY registered | `capability-registry.yaml` ids present (baseline on main retained) | PASS |
| 11 | Astra added | Registry id `astra`; `REQUIRED_EXECUTORS` in `orgctl.py`; tests require Astra | PASS |
| 12 | Future profiles w/o constitutional rewrite | `fields_to_maintain`; list-of-executors pattern; docs | PASS |
| 13 | Permanent ranking forbidden | selection + routing-policy `permanent_ranking: forbidden`; validate; tests | PASS |
| 14 | Provider loyalty forbidden | selection + routing-policy; validate; tests | PASS |
| 15–22 | Measured fit factors | `measured_fit_factors` + `fields_to_maintain` cover evidence/tools/risk/reliability/quota_cost/latency/context/failure_modes | PASS |
| 23 | Least-resource sufficient | `least_resource_intensive_sufficient: true`; selection_steps | PASS |
| 24 | Quality over cost when failure material | `quality_over_cost_when_failure_material: true`; docs § Selection step 6; code path when measured evidence present | PASS |
| 25 | Scarce high-capability reserved | `quota_semantics.scarce: reserve_high_capability_for_material_outcome` | PASS |
| 26 | Critical independent verification | critical class `independent_verification: required`; verification block; route critical → required | PASS |
| 27 | Builder not sole verifier | `builder_not_sole_verifier: true`; validate + tests | PASS |
| 28 | Different provider ≠ independence | `different_provider_not_proof_of_independence: true` | PASS |
| 29 | Prefer deterministic evidence | `prefer_deterministic_evidence: true`; orgctl route deterministic | PASS |
| 30 | Task envelopes | `task_envelope_required: true`; fallback `preserve_task_envelope` | PASS |
| 31 | Child privilege ≤ parent | `child_privilege_may_exceed_parent: false`; tool-access child scope false | PASS |
| 32 | HowlFrame bypass forbidden | selection + tool-access; validate detect weaken; tests | PASS |
| 33 | Recursive delegation default off | `recursive_delegation.default: off`; validate; tests | PASS |
| 34 | Secrets never in routing config | `secrets_in_routing_config: forbidden`; TEMPLATE note; Auditor scan clean | PASS |
| 35 | Missing benchmarks → visible uncertainty | route `uncertainty: visible: missing benchmark data…` for bounded/complex/critical cold-start | PASS |
| 36 | Never invent capability scores | `invent_capability_scores: forbidden`; registry has no numeric score fields; tests fail on unexpected numerics | PASS |

**AC failures/gaps:** none observed for HOWL-005 scope (policy + deterministic tooling; auth/benchmarks explicitly out of scope).

## Determination (narrative)

### 1 — Problem / justification — **Supported**

`product-definition.md` and `HOWL-005.json` state the org knew Claude/Codex/AGY existed but lacked deterministic self-vs-delegate, task classes, honest capability sufficiency, quota/cost, fallback, independent verification, and cold-start uncertainty. Impact (overuse expensive models, delegate trivial work, loyalty/rankings, builder-as-sole-verifier) matches Owner brief themes. Non-goals correctly exclude auth, large benchmarks, HowlBoard, and HOWL-006 auto-start.

### 2 — ACs 1–36 — **Supported**

EM acceptance file is the numbered checklist of record. Implementation delivers `task-classes.yaml`, `selection-policy.yaml`, Astra registry entry, docs, `orgctl route`/`validate`, and regression tests. Auditor local re-run at head: `VALIDATION PASSED`; **98 passed** pytest; route matrix matches Assurance samples.

### 3 — No permanent provider preferences — **Supported**

All four executors share `status: available-if-configured` and `benchmark_status: needs-local-eval`. No ranking scores, no “prefer Claude/Codex/…” hard-codes in routing YAML. Loyalty/ranking explicitly `forbidden` and enforced by validate.

### 4 — Self default for trivial/simple — **Supported**

Defaults and live route: trivial/R0 and simple/R2 → `SELF` with expected-value rationale. Cold-start also maps trivial/simple → SELF.

### 5 — Honest uncertainty — **Supported**

With all profiles `needs-local-eval`, complex/critical routes return `evidence-insufficient` with visible uncertainty; no fabricated scores. Bounded returns `SELF_or_owner_configured_known_capable` with incomplete-evidence marked.

### 6 — Higher-cost still selectable when warranted — **Supported** (Info residual)

Policy encodes `quality_over_cost_when_failure_material` and scarce reservation of high-capability capacity. When any registry profile has measured evidence (`eligible: True`), `route_inspect` takes the measured-fit branch and records quality-over-cost / least-resource steps (`tools/orgctl.py` ~313–340). **Today’s cold-start** correctly refuses to auto-pick expensive externals without evidence (`never_auto_pick_most_expensive_when_evidence_missing`). Live selection of a higher-cost profile therefore awaits future measured fields (HOWL-006 territory) — not a HOWL-005 AC failure.

### 7 — Risk overrides cost — **Supported**

`complexity_does_not_override_risk`; `fallback_may_lower_assurance: false`; `quota_outage_may_lower_assurance: false`; fallback preserves risk tier / assurance / approvals; quality-over-cost when failure material.

### 8 — Assurance independence + tip lock + CI — **Supported**

Pack present under `reports/work-items/HOWL-005/assurance-*.md|txt`, `evidence/howl-005-assurance-verify-069c73b/SUMMARY.md`, `evidence/2026-09-20-HOWL-005-assurance.yaml`, `security/reviews/HOWL-005-assurance-2026-09-20.md` (distinct from Dev Lead `security/reviews/HOWL-005-2026-09-20.md`). Tip lock to product `069c73b` reconstructable. Auditor reproduced validate/pytest/route locally. Live GHA on `df6148a`: validate×2 + distribution **SUCCESS**; product tip `069c73b` likewise all SUCCESS.

### 9 — Native GitHub publish — **Supported** with Info limit

Both PR commits authored/committed as `howlcipher`; no CloudAgent / Cursor Agent co-author trailers in commit bodies. Absolute negative proof of transport tooling unavailable from Git alone (same limit as HOWL-004).

## Live CI (authoritative for merge posture)

| Check | Tip `069c73b` | Tip `df6148a` (PR head) |
|---|---|---|
| validate (3.11) | SUCCESS | SUCCESS |
| validate (3.13) | SUCCESS | SUCCESS |
| distribution | SUCCESS | SUCCESS (completed ~23:37 EDT / 03:37Z) |
| mergeable_state | — | **CLEAN** / MERGEABLE |

## Findings

1. **Info — Tip-lock by design:** Assurance verified product tip `069c73b`; PR head `df6148a` is evidence-land only. Product blobs unchanged. Acceptable pattern; merge review should treat product logic as locked to `069c73b`.
2. **Info — Cold-start / higher-cost path not live-exercised:** All executors remain `needs-local-eval`. Higher-cost-when-warranted is encoded and reachable after measured evidence exists; until then routes correctly fail-closed. Residual operational risk owned by future evals (not HOWL-005 scope).
3. **Info — Native-without-CloudAgent absolute proof limited** to authorship + PR claims + tip presence (same limit Assurance/prior audits recorded).
4. **Info — Shared-box hygiene:** At audit start, local worktree had **uncommitted** edits to `reports/work-items/HOWL-005.json` claiming `phase: audit` / fabricated CI+assurance fields. **Not present in tip SHAs.** Restored to tip content for investigation. Parent should ignore any dirty overlay.

**Blocking findings:** none.

## Exceptions

None.

## Unresolved risks (residual, non-blocking)

- Registry remains unevaluated until future local evals populate `fields_to_maintain` (explicit HOWL-005 non-goal / HOWL-006 territory).
- Operators must still apply hard constraints (tools/risk/privilege/HowlFrame/quota) against task envelopes — `orgctl route` documents that filter as operator-applied, not fully automated envelope enforcement.
- Secret-literal CI risk: prior HOWL-004 failure mode was contiguous PEM armor-header substrings in evidence prose. HOWL-005 Assurance scan text deliberately avoids contiguous armor headers. **This Auditor draft likewise avoids contiguous PEM armor-header literals.** Do not reintroduce them when landing.

## Secrets-literal CI risks (note for landers)

- Repo test asserts absence of contiguous PEM armor header form (`BEGIN` + space + `PRIVATE KEY`) in tracked text (`tests/test_structure.py`).
- HOWL-005 evidence currently **clean** of that contiguous form and of high-signal token patterns (Auditor rescan of routing/ + HOWL-005 reports/evidence/security reviews: **NONE**).
- When landing this report: do **not** paste contiguous PEM armor headers; refer to “PEM armor header” or split tokens as the test does.

## Evidence paths inspected

| Path | Role |
|---|---|
| PR #4 metadata / commits / check-runs | Head SHA, mergeability, CI |
| `reports/work-items/HOWL-005/em-acceptance.md` | Owner ACs 1–36 |
| `reports/work-items/HOWL-005/product-definition.md` | Problem / non-goals |
| `reports/work-items/HOWL-005.json` | Work item (committed tip content) |
| `routing/*.yaml`, `routing/decision-records/*` | Policy truth |
| `docs/EXECUTOR_ROUTING.md`, `AGENTS.md`, `EVALS.md` | Docs / invariant |
| `tools/orgctl.py` (`validate_routing` / `route_inspect`) | Deterministic tooling |
| `tests/test_executor_routing.py` | Regression coverage |
| `policies/tool-access.yaml`, `policies/agent-spawning.yaml`, `policies/risk-tiers.yaml` | HowlFrame / privilege / risk |
| `bots/*/context.yaml`, `policies/budgets.yaml` | Budgets unchanged (`budget_chars` not raised; only dev-lead load_on_demand additions) |
| `reports/work-items/HOWL-005/assurance-*` | Assurance pack |
| `evidence/howl-005-assurance-verify-069c73b/SUMMARY.md` | Tip lock pointer |
| `evidence/2026-09-20-HOWL-005-assurance.yaml` | Manifest (`owner_complete_declared: false`) |
| `security/reviews/HOWL-005-2026-09-20.md` | Dev Lead security write-up (not sole trust) |
| `security/reviews/HOWL-005-assurance-2026-09-20.md` | Assurance Security companion |
| `reports/work-items/HOWL-005/security-review.md` | Dev Lead challenge inventory |
| Local Auditor re-run logs | `/tmp/howl005-auditor-validate.txt`, `...-route.txt`, `...-pytest.txt` |

## Explicit declarations

| Item | Status |
|---|---|
| Owner-complete declared? | **No** (must remain false until Owner declares) |
| Auditor implemented product changes? | **No** |
| Auditor merged PR? | **No** |
| HOWL-006 started? | **No** (no work-item path; mentioned only as future eval territory) |
| Assurance findings rewritten as Auditor’s own? | **No** — independent reconstruction; Assurance used as pointer inventory |

## Reconstruction result

**PASS WITH FINDINGS** (Info only).

HOWL-005’s deterministic routing policy and tooling reconstruct from Git at product tip `069c73ba5f7f2da26ea1f9d7a2eef3beb8c6103b`, with tip-locked Assurance evidence on `df6148ac3b5ebd1b7ea31df66257e26f422e54d9`, Owner ACs 1–36 independently mapped PASS, HowlFrame/privilege/recursive/secrets/builder-verifier controls intact, live validate+distribution green, mergeable CLEAN. Owner-complete **not** declared. Ready for Owner merge decision subject to Info residuals above.

### Durable Git path

`reports/audits/auditor-HOWL-005-2026-09-20.md` (land by parent Auditor — this supporting pass does not push)

— End of HOWL-005 audit report —

### Land note

Landed by Auditor on PR branch `feat/howl-005-executor-routing` via native `git` push (no CloudAgent). Duplicate copy at `reports/work-items/HOWL-005/auditor-report.md` per EM path request.

— End of HOWL-005 audit report —
