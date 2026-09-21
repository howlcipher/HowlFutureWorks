# Security Review — HOWL-005 (Intelligent Executor Routing)

**Date:** 2026-09-20 (America/Detroit)  
**Branch:** `feat/howl-005-executor-routing`  
**Reviewer role:** Dev Lead (implementation security write-up)  
**Scope:** Policy + deterministic tooling only (no executor auth)

## Change summary

Adds task classes, selection/fallback policy, Astra registry entry, routing docs,
decision-record convention, `orgctl route` inspection, and validate/tests. Does not
authenticate Claude/Codex/AGY/Astra or fabricate benchmarks.

## Owner challenge coverage

| Challenge | Mitigation in HOWL-005 |
|-----------|------------------------|
| Prompt injection of selection | Selection rules live in version-controlled YAML; untrusted model/provider text must not rewrite class, risk, or approvals (`selection-policy.security.model_output_untrusted_until_validated`). Route inspection is deterministic and does not invoke models. |
| Privilege escalate via child | `child_privilege_may_exceed_parent: false`; aligned with `policies/tool-access.yaml` and agent-spawning inheritance. Validate fails if weakened. |
| Risk downgrade for cheaper executor | Complexity ≠ risk; `complexity_does_not_override_risk`; fallback preserves risk tier and may not lower assurance. |
| Recursive spawn | `recursive_delegation.default: off`; if ever permitted, child authority/risk/budget ≤ parent. Validate enforces default off. |
| Secrets in routing evidence | `secrets_in_routing_config: forbidden`; decision-record template forbids secrets; AGENTS.md secret invariant retained. |
| Unsafe quota fallback | Quota/outage must not lower assurance (`quota_outage_may_lower_assurance: false`, `fallback_may_lower_assurance: false`). `unknown`/`exhausted` are conservative. |
| Builder self-verify as independent | `builder_not_sole_verifier`; different provider ≠ proof of independence; prefer deterministic evidence. Critical requires independent verification. |
| Untrusted text rewriting rules | Model output untrusted until validated; routing policy files are authoritative over executor suggestions. |
| Multi-model fan-out | `multi_model_fan_out: not_normalized` in selection and fallback; fallback is classify → bounded retry → alternative/escalate. |
| HowlFrame bypass | `howlframe_bypass: forbidden`; `policies/tool-access.yaml` retains `direct_executor_cli_bypass_of_howlframe: forbidden`. Validate checks both. |

## Residual risk

Low for this change set. Residual risk is operational: future registry population must remain evidence-backed (HOWL-006 territory). Cold-start still requires human judgment for complex/critical without evals.

## Verdict

**PASS** for policy/tooling scope — no HowlFrame/approvals/privilege weakening observed in the delivered artifacts.
