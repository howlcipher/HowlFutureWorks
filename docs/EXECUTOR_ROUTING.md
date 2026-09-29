# Executor Routing

HowlFutureWorks selects work executors with **deterministic policy**, not provider
loyalty or permanent rankings. This document explains the routing layer. Machine
sources of truth live under `routing/`.

## Persistent vs ephemeral

| Kind | Role |
|------|------|
| **Persistent members** (Grok Bots / positions) | Durable ownership, coordination, ordinary work, triage, review |
| **Ephemeral executors** (Claude, Codex, AGY, Astra, …) | Bounded implementation via HowlFrame adapters; disposable context |

Persistent members handle ordinary work themselves. External executors are used
only when expected benefit materially justifies delegation. Once it does,
HowlPlane is the normal execution substrate. A Grok Bot calling a raw
Codex/Claude/AGY CLI is not the default implementation path.

## Demand-driven persistent participation

The full workflow Product → Engineering Manager → Dev Lead → Assurance → Auditor
remains a **capability**, not a mandatory ceremony for every work item.

Machine source: `routing/participation-policy.yaml`.

Organizational routing is three decisions, kept separate:

1. Which persistent roles participate (`routing/participation-policy.yaml`).
2. Whether implementation is SELF or delegated (`routing/selection-policy.yaml`).
3. If delegated, which executor HowlPlane selects (`howlplane route`, Factory, or `howlplane work`).

Inspect participation and the SELF-or-delegate decision with:

`python tools/orgctl.py route --task-class bounded --risk R2 --grok-capacity scarce`

### Defaults (complexity class)

| Class | Default footprint |
|-------|-------------------|
| trivial / simple | Responsible role only; normally no Product/Auditor/R&D |
| bounded | Implementer (Dev Lead); Assurance when justified or required |
| complex | Implementer + likely EM/Assurance; Product when judgment needed |
| critical | Follow risk/approval/verification policy; capacity cannot suppress gates |

### Grok capacity (operator-declared)

States: `healthy` | `constrained` | `scarce` | `exhausted` | `unknown`.

Never invent percentages or scrape undocumented quotas. Default inspection state is
`unknown` (conservative). Capacity may reduce **optional** persistent-role handoffs
only. It may **never** lower assurance, bypass approvals, downgrade risk, or
authorize an unauthorized executor.

Precedence: **mandatory governance/safety controls > capacity optimization**.

### Examples

- Routine typo → one responsible member
- Small bug → Dev Lead (+ Assurance if warranted)
- Product ambiguity → Product + relevant engineering
- Security-sensitive change → required Assurance/approvals regardless of capacity
- Research uncertainty → R&D
- Major milestone → full workflow when justified

## Self vs delegate

1. Classify task class (`routing/task-classes.yaml`) and risk tier (`policies/risk-tiers.yaml`).
2. **trivial** and **simple** default to **SELF**.
3. External delegation requires **expected value** (material benefit vs cost/risk).
4. Merely having an executor installed is not a reason to invoke it.
5. Deterministic operations should not unnecessarily invoke an AI executor.

Inspect with: `python tools/orgctl.py route --task-class simple --risk R1 --grok-capacity unknown`.

`orgctl route` reports an `execution_substrate`. Trivial and simple work stays `SELF`. Bounded work stays SELF unless expected value justifies delegation, and that delegated path is `HOWLPLANE`. Complex and critical delegated work is `HOWLPLANE`. The field does not name a provider CLI.

## HowlPlane substrate

Machine source: `routing/execution-substrate.yaml`. Procedure when Plane is unhealthy: `runbooks/howlplane-recovery.md`. Coordinator and implementer positions retrieve both through the `execution_orchestration` trigger rather than preloading them.

| Situation | Path |
|---|---|
| Small bounded judgment or coordination | SELF |
| Implementation-heavy delegated work | `howlplane work`, `howlplane orchestrate`, or `howlplane factory start` / `run` / `run-once` |
| Which provider | `howlplane route` or Factory routing, from measured fit |
| Evidence | `howlplane verify`, `howlplane record`, plus the result envelope |
| HowlPlane itself needs a tracked repair | `howlplane factory run --target self` when a governed entrypoint still works |
| Wider evidence-backed ecosystem work | `howlplane factory run --target ecosystem`, under normal prioritization |

These commands are the HowlPlane 0.1.0 interfaces recorded in `verified_interfaces`. Re-check `--help` before treating a new flag as supported.

Persistent Grok roles that are not on the Factory host must not install a second Plane. Use `runbooks/howlplane-remote-observation.md` (interim) and HOWL-011 (durable remote status/submit bridge).

## Governed recovery

Executor failover (`routing/fallback-policy.yaml`) is not permission to skip HowlPlane governance, and a HowlPlane failure is not permission to skip HowlFrame, risk ceilings, approvals, credentials, task scope, evidence, independent verification, bounded retries, or production controls.

Bypass, when a condition in `execution-substrate.yaml` `recovery.conditions` is confirmed, applies only to the orchestration layer. If one governed entrypoint still runs, use it. If none does, checkpoint, stop, and escalate. Raw provider CLIs stay forbidden.

Classify the failure before opening a Plane repair. An executor, quota, auth, or task failure is not a HowlPlane software defect.

## Repair and improvement

Repair is a required capability that is broken. It may be prioritized because execution is impaired. One failure produces one tracked repair. If that repair path fails, checkpoint, stop, and escalate. Do not repair the repair mechanism.

Improvement is a system that works, with repeated evidence that it can be cheaper, faster, safer, more reliable, or more efficient. It follows normal prioritization. An unsupported model opinion is not evidence.

Self-improvement stays inside existing authority. It may not increase authority, reduce approvals, lower risk classification, grant production access, broaden credentials, weaken Assurance or audit, bypass HowlFrame, suppress evidence, auto-merge consequential changes, or change policy without the required review.

## Task classes vs risk

Complexity classes (`trivial` / `simple` / `bounded` / `complex` / `critical`) are
**orthogonal** to risk tiers (`R0`–`R4`). Complexity never overrides risk policy,
approvals, or assurance gates.

## Capability registry

`routing/capability-registry.yaml` lists executor profiles (Claude, Codex, AGY, Astra)
with honest status (`available-if-configured`) and benchmark state (`needs-local-eval`
until local evals exist). Future profiles may be added without rewriting the charter.

`fields_to_maintain` lists measured fields (tools, reliability, latency, quota,
context, failure modes, allowed risk, last evaluated). **Never invent scores.**

## Selection

`routing/selection-policy.yaml` defines ordered, explainable steps:

1. Classify task class and risk
2. Decide SELF vs delegate
3. Filter hard constraints (tools, risk, privilege, HowlFrame, quota)
4. Assess measured fit
5. Prefer least-resource-intensive sufficient executor
6. Prefer quality over cost when failure cost is material
7. Require independent verification for critical/consequential work
8. Record rationale — or return **evidence-insufficient**

Forbidden: provider loyalty, permanent rankings, inventing capability scores,
normalizing multi-model fan-out of the same prompt.

## Quota states

Allowed: `healthy` | `constrained` | `scarce` | `exhausted` | `unknown`.

Applies to both ephemeral executor quota (selection-policy) and persistent Grok Bot
capacity (participation-policy). Same honest labels; never invent usage %.

- **unknown** → conservative (treat like constrained); no invented usage %.
- **scarce** → reserve high-capability / persistent judgment capacity for material outcomes.
- **exhausted** → no new external spend without an Owner-approved path; no new discretionary Grok role work.
- Quota/outage never lowers assurance or approvals.

## Profiles and credentials

Profiles are configuration + evidence, not authority. Credentials stay in platform
secret stores — **never** in routing YAML, decision records, prompts, or Git.
Executor auth/login is out of scope for HOWL-005.

## Fallback

`routing/fallback-policy.yaml`:

1. Classify failure
2. Bounded retry (`max_retries_per_failure_class: 2`; blind retry forbidden)
3. Eligible alternative or escalate

Preserve task envelope, risk tier, required gates, and assurance. Do not spray the
same prompt across every provider.

## Recursive delegation

**Off by default.** If ever Owner-permitted: child authority, risk, and budget must
be ≤ parent; preserve evidence lineage. Child privilege may never exceed parent
(`policies/tool-access.yaml`, `policies/agent-spawning.yaml`).

## Independent verification

Critical/consequential work requires independent verification per existing policy.
The implementation executor must not normally be its only verifier. A different
provider can help but is **not** proof of independence. Prefer deterministic
evidence (tests, static analysis, reproducible checks) when stronger.

## Cold-start

When benchmark data is missing:

- trivial/simple → SELF
- bounded → Owner-configured known-capable path allowed with incomplete evidence marked
- complex/critical → stronger justification + verification
- never auto-pick the most expensive executor when evidence is missing
- router must surface **visible uncertainty**, never invent scores

## Evaluation process

See `EVALS.md` and `evals/`. Future local evals populate registry fields under
`fields_to_maintain`. HOWL-005 does **not** run large benchmarks.

## Decision records

Significant delegated work only: `routing/decision-records/`. Not for trivial/SELF.

## Security boundaries

- External executors stay inside task envelopes
- Direct executor CLI bypass of HowlFrame is forbidden
- Model/provider output is untrusted until validated
- Untrusted text must not rewrite selection rules, risk tier, or approvals
- Fallback must not lower assurance

## Related files

- `routing/execution-substrate.yaml`, `runbooks/howlplane-recovery.md`
- `routing/selection-policy.yaml`, `task-classes.yaml`, `capability-registry.yaml`
- `routing/routing-policy.yaml`, `fallback-policy.yaml`, `participation-policy.yaml`
- `policies/risk-tiers.yaml`, `tool-access.yaml`, `approvals.yaml`, `budgets.yaml`
- `CHARTER.md` §7 (constitutional intent; operational detail lives in `routing/`)
