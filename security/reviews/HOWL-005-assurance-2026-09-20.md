# Security Review — HOWL-005 (Assurance Security lane)

**Date:** 2026-09-20 23:34 EDT (America/Detroit)  
**Branch:** `feat/howl-005-executor-routing`  
**Tip:** `069c73ba5f7f2da26ea1f9d7a2eef3beb8c6103b`  
**Reviewer role:** Assurance Security (independent)  
**Note:** This file is **Assurance-authored**. It does **not** overwrite the Dev Lead review at `security/reviews/HOWL-005-2026-09-20.md` or `reports/work-items/HOWL-005/security-review.md`. Dev Lead materials were used only as a challenge inventory.

## Scope
Policy + deterministic tooling only (no executor authentication). Independent re-verification of Owner security challenges against YAML policy, `orgctl validate` rules, regression tests, route inspection, and secret scan.

## Challenge re-verification

| Challenge | Independent finding |
|-----------|---------------------|
| Prompt injection of selection | Selection is version-controlled YAML; `orgctl route` sets `model_invoke: false` / `deterministic: true`; `model_output_untrusted_until_validated: true`. |
| Privilege escalate via child | `selection-policy.security.child_privilege_may_exceed_parent: false`; `policies/tool-access.yaml` `child_worker_may_exceed_parent_scope: false`; validate + `test_privilege_howlframe_recursive_defaults` / weaken tests. |
| Risk downgrade for cheaper executor | `complexity_does_not_override_risk: true`; fallback preserves risk tier and assurance; `quota_outage_may_lower_assurance: false`. |
| Recursive spawn | `recursive_delegation.default: off`; validate fails if set `on`; tests cover detection. |
| Secrets in routing evidence | `secrets_in_routing_config: forbidden`; decision-record template forbids secrets; high-signal secret scan of changed files + `routing/` found **no** credential literals or PEM private-key armor headers. |
| Unsafe quota fallback | Quota states include conservative `unknown`/`exhausted`; `fallback_may_lower_assurance: false`; `blind_retry: forbidden`; `max_retries_per_failure_class: 2`. |
| Builder self-verify as independent | `builder_not_sole_verifier: true`; `different_provider_not_proof_of_independence: true`; critical class `independent_verification: required`. |
| Untrusted text rewriting rules | Model/provider output untrusted until validated; routing policy authoritative. |
| Multi-model fan-out | `multi_model_fan_out: not_normalized` in selection and fallback. |
| HowlFrame bypass | `howlframe_bypass: forbidden` and tool-access `direct_executor_cli_bypass_of_howlframe: forbidden`; validate detects weakening. |

## HowlFrame / privilege / recursive (spot-check commands)
- Read `routing/selection-policy.yaml` security + recursive_delegation blocks
- Read `policies/tool-access.yaml` rules
- pytest: `test_privilege_howlframe_recursive_defaults`, `test_validate_detects_howlframe_bypass_weakened`, `test_validate_detects_recursive_default_on`

## Residual risk
Low for this change set. Residual operational risk: capability registry remains `needs-local-eval` until evidence-backed evals (HOWL-006 territory). Cold-start correctly returns `evidence-insufficient` for complex/critical rather than inventing scores.

## Verdict
**PASS** — no HowlFrame, approvals, privilege, or secret-handling regressions observed. Independent of Dev Lead conclusion, evidence supports the same security outcome for policy/tooling scope.
