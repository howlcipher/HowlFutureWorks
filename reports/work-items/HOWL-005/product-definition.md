# HOWL-005 — Product definition (lightweight)

Status: Product definition for EM acceptance  
Author: bot-product-0001 (Quatre Raberba Winner)  
Work item: `reports/work-items/HOWL-005.json`  
Baseline main: `a5554ea`  
Risk: R2  
Scope: organizational infrastructure (not product feature development)

## Problem

HowlFutureWorks knows external executor families exist (Claude, Codex, AGY; Astra not yet registered) but lacks a complete **deterministic** routing layer for:

- self vs delegate decisions
- machine-readable task classes
- capability sufficiency without invented scores
- quota / cost / latency / context constraints
- fallback and cold-start uncertainty
- independent verification (builder must not be sole verifier)

Current `routing/` has a thin capability registry + high-level rules; `task-classes.yaml`, `selection-policy.yaml`, and `docs/EXECUTOR_ROUTING.md` are absent. Members cannot reliably answer routing questions from policy alone.

## Impact

Without this policy and tooling, persistent Bots may:

- overuse expensive external models
- delegate trivial/simple work
- choose inconsistently or encode provider loyalty / permanent rankings
- exhaust quota without conservative handling
- treat the implementer/builder as sole verifier on consequential work

## Desired outcome

A persistent member (or deterministic `orgctl` route inspection, if implemented cleanly) can answer, from version-controlled policy + registry state:

1. Should I do this myself (SELF) or delegate?
2. What capabilities does the task require?
3. Which executor profiles are eligible under hard constraints?
4. Why was this profile selected (explainable factors — no invented rankings)?
5. Is independent verification required?
6. Is evidence insufficient / cold-start uncertain — and what is the fail-closed behavior?

HOWL-005 delivers **policy + deterministic tooling only**. It does **not** authenticate external executors or run large benchmarks (that is HOWL-006 territory).

Governing principles (Owner):

- Persistent members handle ordinary work themselves; external executors only when expected benefit materially justifies delegation.
- Choice follows measured capability, tools, risk, reliability, quota, cost/usage, latency, and context — not provider loyalty or permanent rankings.

## Acceptance criteria

**Authoritative source:** Owner HOWL-005 brief ACs **1–36** (self/delegate, task classes, executors incl. Astra, selection neutrality, capability sufficiency, verification, security, uncertainty). Product does not invent demand beyond that brief.

Distilled themes for implementers (must satisfy Owner ACs 1–36 in full):

1. **Self vs delegate** — Trivial and simple work default to SELF; external delegation requires expected value / material benefit.
2. **Task classes** — Machine-readable classes at least: trivial, simple, bounded, complex, critical; complexity does **not** override risk tier.
3. **Executors** — Claude, Codex, AGY remain registered; **Astra added** with honest `needs-local-eval` (or equivalent) state; no fabricated capability scores.
4. **Selection neutrality** — Forbid provider loyalty and permanent rankings; consider measured evidence, tools, risk, reliability, quota, cost/usage, latency, context, known failure modes.
5. **Capability sufficiency** — Prefer least-resource-intensive sufficiently capable executor; quality over cost when failure cost is material.
6. **Verification** — Critical/consequential work requires independent verification; builder/implementer is not sole verifier.
7. **Security** — Task envelopes; child privilege ≤ parent; HowlFrame bypass forbidden; recursive delegation off by default; no secrets in routing config; provider/model output remains untrusted until validated.
8. **Uncertainty / quota / cold-start** — Missing benchmarks → visible uncertainty (never invent scores); quota states healthy / constrained / scarce / exhausted / unknown with conservative semantics; cold-start and fallback/retry documented; multi-model fan-out not normalized; fallback must not lower assurance/approvals.
9. **Artifacts / validation** — `docs/EXECUTOR_ROUTING.md`; selection/task-class policy files as needed; schemas + validation + tests; optional `orgctl route` inspection if clean; context budgets pass; CI gates (validate, pytest, audit, dist/verify-dist) remain enforced — no convenience waivers.
10. **Auth out of scope** — No Claude/Codex/AGY/Astra authentication in HOWL-005.

If the durable Owner brief text with numbered ACs 1–36 is attached in Git later, that document remains the AC checklist of record; this file is the Product distillation for routing/implementation.

## Explicit non-goals

- Authenticate or login to Claude / Codex / AGY / Astra
- Large external-model benchmarks or fabricated capability scores
- HowlBoard / HowlPlane implementation
- Product feature development (Howl app features)
- Weakening HowlFrame, approvals, privilege model, or assurance gates
- Permanent provider rankings
- Starting HOWL-006 automatically

## Baseline (verified at assignment)

| Item | State at `a5554ea` |
|---|---|
| Claude / Codex / AGY in capability-registry | present |
| Astra | absent |
| `routing/task-classes.yaml` | absent |
| `routing/selection-policy.yaml` | absent |
| `docs/EXECUTOR_ROUTING.md` | absent |
| Native GitHub publish | operational |

## Non-goals note on discovery hold

Owner discovery hold for open product discovery remains unchanged. HOWL-005 is Owner-authorized **organizational infrastructure** only.
