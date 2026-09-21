# HOWL-005 — EM acceptance

Status: **ACCEPTED** for implementation  
Author: bot-engmgr-0001 (Rintaro Okabe)  
Product definition: `reports/work-items/HOWL-005/product-definition.md` — accepted  
Implementation assignee: bot-devlead-0001 (Motoko Kusanagi)  
Branch: `feat/howl-005-executor-routing`  
Risk: R2  
Publish: native `git`/`gh` (CloudAgent only if native fails; record why)

## Classification

Organizational infrastructure — routing policy + deterministic tooling. Not product feature development. R&D not required unless a genuine unresolved experimental question appears.

## Owner AC checklist of record (1–36)

### Self vs delegate
1. Trivial work defaults to SELF.
2. Simple work defaults to SELF.
3. External delegation requires expected value.
4. Merely having an executor installed is not a reason to invoke it.
5. Deterministic operations should not unnecessarily invoke an AI executor.

### Task classes
6. Define machine-readable task classes: trivial, simple, bounded, complex, critical.
7. Task complexity does not override risk policy.

### Executors
8. Claude remains registered.
9. Codex remains registered.
10. AGY remains registered.
11. Astra is added.
12. Future executor profiles can be added without rewriting constitutional policy.

### Selection
13. Permanent provider ranking is forbidden.
14. Provider loyalty is forbidden.
15. Routing considers current measured evidence.
16. Tool compatibility is considered.
17. Risk compatibility is considered.
18. Reliability is considered.
19. quota/cost/usage is considered.
20. latency is considered.
21. context capacity is considered.
22. known failure modes are considered.

### Capability sufficiency
23. Prefer the least resource-intensive executor that has sufficient measured capability.
24. Do not optimize cost when expected failure cost materially outweighs the savings.
25. Scarce high-capability capacity may be reserved for tasks where it changes expected outcome.

### Verification
26. Critical/consequential work requires independent verification according to existing policy.
27. The implementation executor should not normally be its only verifier.
28. A different provider is useful where appropriate but is not itself proof of independence.
29. Deterministic evidence is preferred where available.

### Security
30. External executors stay inside task envelopes.
31. Child privilege may not exceed parent privilege.
32. Direct executor bypass of HowlFrame remains forbidden.
33. Recursive executor delegation is forbidden by default.
34. Secrets never enter routing configuration.

### Uncertainty
35. Missing benchmark data must produce visible uncertainty.
36. The router must never invent capability scores.

## Implementation envelope (Dev Lead)

Canonical files under `routing/` (extend existing; avoid unnecessary fragmentation):

- `README.md` — update
- `capability-registry.yaml` — keep Claude, Codex, AGY; **add Astra** with honest `needs-local-eval` / `available-if-configured`; no fabricated scores; preserve `fields_to_maintain`; allow future profiles without constitutional rewrite
- `task-classes.yaml` — **new** (trivial/simple/bounded/complex/critical + defaults; complexity ≠ risk)
- `selection-policy.yaml` — **new** (self_preferred_when_sufficient, external_requires_expected_value, provider_loyalty forbidden, permanent_ranking forbidden, least_resource_intensive_sufficient, quality_over_cost_when_failure_material; ordered explainable selection steps)
- Keep `routing-policy.yaml` / `fallback-policy.yaml` or fold cleanly into selection/fallback without breaking readers

Also deliver:

1. Concise global invariant in `AGENTS.md` (Owner wording; do not bloat into routing docs)
2. `docs/EXECUTOR_ROUTING.md` — full explanation (persistent vs ephemeral; self vs delegate; classes; risk vs complexity; registry; selection; quota; profiles; fallback; recursive delegation; independent verification; cold-start; evaluation process; credential separation)
3. Compact routing decision record convention for **significant delegated** work only (not trivial/self)
4. Evaluation framework pointers in docs / EVALS.md — how future evals populate registry; **do not run large benchmarks**
5. `python tools/orgctl.py route ...` deterministic inspection if it fits cleanly (no model invoke; evidence-insufficient is a valid result)
6. Extend `orgctl validate` for meaningful routing checks (duplicate executor IDs, missing Astra, unknown task class/risk refs, invalid quota state, loyalty/ranking enabled, self-preferred/expected-value absent, critical independent verification absent, HowlFrame bypass weakened, child privilege expansion, recursive default off)
7. Regression tests covering Owner minimum list (registry membership, defaults, neutrality, exclusions, uncertainty honesty, privilege/HowlFrame/recursive)
8. After change: `orgctl render-all` (or equivalent); **context budgets must still pass** — do not raise budgets to fit docs; keep always-load minimal (global invariant + compact selection for roles that route)
9. Explicit security review of Owner challenges (prompt injection of selection, privilege escalate, risk downgrade for cheaper executor, recursive spawn, secrets in routing evidence, unsafe quota fallback, builder self-verify as independent, untrusted text rewriting rules, multi-model fan-out)

Quota states: `healthy` | `constrained` | `scarce` | `exhausted` | `unknown` (conservative; no invented usage %).

Cold-start: trivial/simple → self; bounded may use Owner-configured known-capable path with incomplete evidence marked; complex/critical need stronger justification + verification; never auto-pick most expensive when evidence missing.

Fallback: classify failure → bounded retry (align `max_retries_per_failure_class: 2`; blind retry forbidden) → eligible alternative or escalate. Do not spray the same prompt across every provider.

Recursive delegation: off by default; if ever permitted, child authority/risk/budget ≤ parent; preserve evidence lineage.

Role notes: reference canonical routing files — do not duplicate full policy into each Bot.

## Non-goals

No Claude/Codex/AGY/Astra authentication; no fabricated benchmarks; no HowlBoard; no product feature work; no weakening HowlFrame/approvals; do not start HOWL-006.

## Merge gates (do not waive)

Product AC · Dev Lead complete · Assurance PASS · Auditor evidence in Git · `orgctl validate` · pytest · `make audit` · dist/verify-dist · context budgets · GitHub Actions green
