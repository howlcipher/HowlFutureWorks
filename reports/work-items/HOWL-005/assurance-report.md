# HOWL-005 Assurance Report — Independent verification

**Work item:** HOWL-005 (Intelligent Executor Routing)  
**PR:** https://github.com/howlcipher/HowlFutureWorks/pull/4  
**Branch:** `feat/howl-005-executor-routing`  
**Tip verified:** `069c73ba5f7f2da26ea1f9d7a2eef3beb8c6103b`  
**Base:** `main` `a5554eab36425f5496cd1059a9312cef1bd9463a`  
**Worktree:** `/workspace/HowlFutureWorks-howl005` @ tip  
**Date:** 2026-09-20 23:34 EDT (America/Detroit)  
**Reviewer lane:** Assurance (QA + Security) — **independent of Dev Lead**  
**Owner-complete:** **NOT declared**  
**Merge:** **NOT performed**  
**HOWL-006:** **NOT started**

## Overall verdict

# **PASS**

No blocking findings. Owner ACs 1–36 independently spot-checked against policy YAML, `orgctl validate`, `orgctl route` examples, pytest (98 passed), secret scan, and context budgets. Dev Lead `security-review.md` / `security/reviews/HOWL-005-2026-09-20.md` were read for challenge inventory but **not trusted alone** — each challenge was re-verified in policy + validate rules + tests.

Blocking findings: **none**.

---

## QA section (Assurance QA lane)

### Scope exercised
- Authoritative ACs: `em-acceptance.md` (1–36), `product-definition.md`
- Diff vs main: 20 paths (see `assurance-files-changed.txt`); no HOWL-006
- `python tools/orgctl.py validate` → VALIDATION PASSED
- Full `pytest` → 98 passed
- `orgctl route` examples (trivial/R0 → SELF; critical/R4 → evidence-insufficient)
- `orgctl render-all` → all bots within budget; budget_chars unchanged vs main
- Registry honesty: all four executors `needs-local-eval`; no numeric capability scores
- Docs present: `docs/EXECUTOR_ROUTING.md`, EVALS.md pointers, decision-record convention

### Route inspection results (deterministic; no model invoke)
| Input | result | decision | notes |
|-------|--------|----------|-------|
| trivial / R0 | selected | SELF | AC 1 |
| simple / R2 | selected | SELF | AC 2 |
| bounded / R2 | selected | SELF_or_owner_configured_known_capable | uncertainty visible |
| complex / R3 | evidence-insufficient | evidence-insufficient | specialist-expected cold-start |
| critical / R4 | evidence-insufficient | evidence-insufficient | independent_verification=required |

### Budgets
- `policies/budgets.yaml`: **unchanged** vs main
- All role `budget_chars` **unchanged** vs main (assurance 14000, auditor 14000, dev-lead 15000, eng-mgr 18000, product 12000, rnd 12000)
- Only change: `bots/dev-lead/context.yaml` **load_on_demand** additions (routing docs) — not always-load bloat; render-all still passes
- **Budgets not raised**

### CI note
PR #4 Actions at tip: `validate (3.11)` SUCCESS, `validate (3.13)` SUCCESS, `distribution` SUCCESS (parent also observed validate+distribution PASS).

---

## Security section (Assurance Security lane)

**Distinct from Dev Lead write-up.** See also `security/reviews/HOWL-005-assurance-2026-09-20.md`.

### Independent challenge spot-check
| Owner challenge | Independent evidence | Status |
|-----------------|----------------------|--------|
| Prompt injection of selection | YAML-only selection; route has `model_invoke: false`; `model_output_untrusted_until_validated: true` | Covered |
| Privilege escalate via child | `child_privilege_may_exceed_parent: false`; tool-access `child_worker_may_exceed_parent_scope: false`; validate + tests | Covered |
| Risk downgrade for cheaper executor | `complexity_does_not_override_risk`; fallback preserves risk/assurance; `quota_outage_may_lower_assurance: false` | Covered |
| Recursive spawn | `recursive_delegation.default: off`; validate rejects `on`; tests | Covered |
| Secrets in routing evidence | `secrets_in_routing_config: forbidden`; TEMPLATE prohibition; high-signal secret scan NONE | Covered |
| Unsafe quota fallback | quota semantics conservative; `fallback_may_lower_assurance: false`; blind_retry forbidden | Covered |
| Builder self-verify as independent | `builder_not_sole_verifier`; `different_provider_not_proof_of_independence`; critical requires independent | Covered |
| Untrusted text rewriting rules | model_output_untrusted; policy authoritative | Covered |
| Multi-model fan-out | `multi_model_fan_out: not_normalized` in selection + fallback | Covered |
| HowlFrame bypass | selection `howlframe_bypass: forbidden`; tool-access `direct_executor_cli_bypass_of_howlframe: forbidden`; validate detects weaken | Covered |

### Secret scan
High-signal credential / PEM private-key armor header patterns: **NONE** in changed files and `routing/`. See `assurance-secret-scan.txt`.

### Residual risk (Assurance)
Low / operational only: registry remains `needs-local-eval` until HOWL-006 (or later) evals populate measured fields. Cold-start correctly fail-closes for complex/critical. No privilege or HowlFrame weakening observed.

**Assurance Security verdict:** PASS

---

## Owner AC checklist (1–36) — mapped evidence

| AC | Statement (short) | Evidence | Result |
|----|-------------------|----------|--------|
| 1 | Trivial → SELF | task-classes.yaml; route trivial; test_trivial_and_simple; test_route_trivial | PASS |
| 2 | Simple → SELF | task-classes.yaml; route simple; tests | PASS |
| 3 | External needs expected value | selection + task-classes `external_requires_expected_value`; route rationale | PASS |
| 4 | Installed ≠ invoke | route rationale; AGENTS.md invariant | PASS |
| 5 | Deterministic ops avoid AI | self_preferred; docs EXECUTOR_ROUTING; route no model_invoke | PASS |
| 6 | Task classes defined | task-classes.yaml: trivial/simple/bounded/complex/critical | PASS |
| 7 | Complexity ≠ risk | complexity_does_not_override_risk true; risk-tiers source | PASS |
| 8 | Claude registered | capability-registry.yaml | PASS |
| 9 | Codex registered | capability-registry.yaml | PASS |
| 10 | AGY registered | capability-registry.yaml | PASS |
| 11 | Astra added | capability-registry; validate requires astra; tests | PASS |
| 12 | Future profiles w/o constitutional rewrite | fields_to_maintain; registry list pattern; docs | PASS |
| 13 | Permanent ranking forbidden | selection + routing-policy; validate; tests | PASS |
| 14 | Provider loyalty forbidden | selection + routing-policy; validate; tests | PASS |
| 15 | Measured evidence | measured_fit_factors includes evidence; route uncertainty | PASS |
| 16 | Tool compatibility | measured_fit_factors: tools; fields tool_support | PASS |
| 17 | Risk compatibility | measured_fit_factors: risk; allowed_risk_classes field | PASS |
| 18 | Reliability | measured_fit_factors + fields_to_maintain | PASS |
| 19 | Quota/cost/usage | quota_states/semantics; quota_cost factor; cost_or_usage field | PASS |
| 20 | Latency | measured_fit_factors + fields | PASS |
| 21 | Context capacity | measured_fit_factors: context; context_capacity field | PASS |
| 22 | Known failure modes | measured_fit_factors: failure_modes; known_failure_modes field | PASS |
| 23 | Least-resource sufficient | least_resource_intensive_sufficient; selection steps | PASS |
| 24 | Quality over cost when failure material | quality_over_cost_when_failure_material | PASS |
| 25 | Scarce high-capability reserved | quota_semantics.scarce | PASS |
| 26 | Critical independent verification | verification.critical_requires_independent; critical class required; route | PASS |
| 27 | Builder not sole verifier | builder_not_sole_verifier; tests | PASS |
| 28 | Different provider ≠ independence proof | different_provider_not_proof_of_independence | PASS |
| 29 | Prefer deterministic evidence | prefer_deterministic_evidence; orgctl route deterministic | PASS |
| 30 | Task envelopes | task_envelope_required; fallback preserve_task_envelope | PASS |
| 31 | Child privilege ≤ parent | child_privilege_may_exceed_parent false; tool-access; recursive if_permitted | PASS |
| 32 | HowlFrame bypass forbidden | howlframe_bypass; tool-access; validate+tests | PASS |
| 33 | Recursive delegation default off | recursive_delegation.default off; validate+tests | PASS |
| 34 | Secrets never in routing config | secrets_in_routing_config forbidden; secret scan clean | PASS |
| 35 | Missing benchmarks → visible uncertainty | route uncertainty string; cold_start; invent forbidden | PASS |
| 36 | Never invent capability scores | invent_capability_scores forbidden; no numeric scores in registry; tests | PASS |

**AC failures/gaps:** none.

---

## Verification themes A–K (cross-check)

| Theme | Verdict |
|-------|---------|
| A Task-class defaults | PASS |
| B Self vs delegate / expected-value | PASS |
| C Provider neutrality + registry membership | PASS |
| D No fabricated benchmarks/scores | PASS |
| E Quota / risk / fallback / recursive off | PASS |
| F HowlFrame + child privilege | PASS |
| G Independent verification / builder not sole | PASS |
| H Context budgets unchanged & pass | PASS |
| I validate + pytest + route examples | PASS |
| J No secrets in routing artifacts | PASS |
| K Security review challenges addressed (independent) | PASS |

---

## Artifacts produced (this Assurance pass)

Under `reports/work-items/HOWL-005/`:
- `assurance-report.md` (this file)
- `assurance-commands.log`
- `assurance-orgctl-route.txt`
- `assurance-pytest.txt`
- `assurance-validate.txt`
- `assurance-secret-scan.txt`
- `assurance-files-changed.txt`

Also:
- `evidence/howl-005-assurance-verify-069c73b/SUMMARY.md`
- `evidence/2026-09-20-HOWL-005-assurance.yaml`
- `security/reviews/HOWL-005-assurance-2026-09-20.md` (Assurance Security; does not overwrite Dev Lead review)

## Explicit non-declarations
- Owner-complete: **NOT** declared
- Merge: **NOT** performed
- HOWL-006: **NOT** started
