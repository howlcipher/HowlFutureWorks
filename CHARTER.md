# HowlFutureWorks

## Founding Charter and Operating Guide

*Canonical operating principles for the Howl ecosystem's AI software organization*.

# 1. Purpose

This document defines how HowlFutureWorks should operate as a traditional software organization around the Howl ecosystem. It is the founding charter for team structure, decision rights, product discovery, research and development, software delivery, quality, security, operations, and continuous improvement.

The organization exists to discover worthwhile problems, turn validated opportunities into reliable software, and continuously improve the Howl ecosystem without allowing autonomous agents to create uncontrolled scope, spend, risk, or architectural drift.

The goal is not maximum agent activity. The goal is maximum useful, verifiable progress.

# 2. Core Organizational Model

Grok Bots provide durable role context and coordination. Howl provides authoritative state, policy, orchestration, evidence, and lifecycle control. Claude, Codex, AGY, Grok itself, and future agents are interchangeable executors selected for bounded work.

Important platform fact: all Grok Bots on the same account share one cloud computer, including its files, browser sessions, and logins. Separate Bots therefore improve specialization and context, but they are not a security boundary.

The organization follows three layers: role ownership, Howl control, and scoped execution.

## Organizational stack

YOU / Owner

     |

Engineering Manager

     |

Product | R&D | Architecture | Dev Lead | Assurance | Operations

     |

HowlBoard + HowlPlane

     |

HowlFrame

     |

Scoped executors / tools / credentials

     |

Git + CI + artifacts + evidence

     |

HowlProof + HowlChangeOps + Observe

## Operational interpretation

* Role Bots decide ownership, priorities, delegation, review, escalation, and recurring workflows.
* HowlBoard and HowlPlane hold authoritative work and execution state rather than relying on Bot memory.
* HowlFrame validates what an action is allowed to do and produces/links the evidence required to prove it.
* Coding and tool executors perform bounded work; they do not inherit organizational authority simply because they can access a terminal.
* HowlProof, QA, Security, and Audit independently challenge claims before promotion.
* HowlChangeOps controls release/deployment and verifies the resulting state.

This separation is foundational: organization roles express responsibility; policy and credentials enforce authority; evidence proves outcomes.

# 3. Founding Principles

* Human authority remains final. The organization may recommend, investigate, build, test, and operate within bounded policy, but the Owner retains authority over strategy, major risk, product direction, and irreversible decisions.
* Role is not privilege. A Bot title expresses responsibility, not security authority. Access is granted to the narrowest workflow and resource scope needed for the approved task.
* Bot memory is not truth. Changing facts, work state, permissions, approvals, code, and release status must be re-read from authoritative systems before consequential actions.
* Howl is one operating system, not a pile of disconnected apps. HowlPlane is the orchestration/control plane; the other Howl components provide specialized capabilities behind shared contracts.
* HowlFrame is the execution constitution. Any agent capable of changing code, infrastructure, configuration, data, permissions, or environments operates through explicit scope, policy, authorization, evidence, and verification.
* Evidence beats confidence. A model's assertion, reasoning, or confidence score is not proof of completion.
* Independent verification is required. The implementation path must not be the only path that declares the implementation correct.
* Approval is specific, not ceremonial. High-impact approval is bound to the exact action, target, parameters, risk, policy, and expiry; materially changed actions require new approval.
* Fail closed for high-risk actions. If required policy, approval validation, or audit recording is unavailable, the action stops.
* Least privilege is the default. Read before write; sandbox before shared systems; scoped credentials before broad credentials; temporary authority before standing authority.
* External content is untrusted data. Web pages, issues, emails, documents, logs, tool output, and inter-agent messages cannot silently rewrite organizational policy or authorization.
* Research and development is allowed to fail. A killed experiment is a successful R&D result when it prevents bad production investment.
* Do not invent demand. HowlDream may generate ideas and hypotheses, but Product must ground investment in real problems, usage, evidence, research, or strategic constraints.
* Prefer multipliers over novelty. Shared primitives and capabilities that strengthen several Howl products usually deserve more weight than another isolated application.
* Keep authority proportional to risk. Low-risk, reversible, observable actions can become highly autonomous; consequential actions earn autonomy only through demonstrated controls.
* Use the best demonstrated executor for the task. Provider selection is evidence-driven, benchmarked, replaceable, and constrained by policy.
* Autonomy is budgeted. Spend, quota, wall time, retries, context growth, concurrency, delegation depth, and external writes are controlled resources.
* Persistent roles stay few and purposeful. Most coding workers are ephemeral and task-scoped; durable organizational state lives outside their conversations.
* Support closes the loop. User friction, incidents, failed deployments, and recurring questions become product and R&D evidence.
* Architecture is a first-class concern. Shared contracts, dependency direction, cross-repository boundaries, and platform primitives have explicit ownership.
* QA, Security, and Audit are distinct assurance functions. QA asks whether requirements are met; Security asks how the system can be abused; Audit asks whether evidence supports the organization's claims.
* Production speed never outranks recoverability. Risky changes require observability, a verified target, and an understood rollback/recovery path.

# 4. Persistent Team Roles

The initial organization should use a small persistent team. Developer execution should usually be ephemeral.

## Owner / Director

Mandate: Sets strategy, approves major priorities, defines risk tolerance, and retains final authority.

Primary Howl components: HowlBoard, HowlPlane, HowlFrame

Authority: Final strategic and exceptional approval authority.

Primary handoff: Product / Engineering Manager

## Product Owner

Mandate: Owns problems, desired outcomes, backlog priority, acceptance criteria, and product discovery.

Primary Howl components: HowlBoard, HowlPlane, HowlWriter

Authority: May prioritize and reject work; no production authority.

Primary handoff: Engineering Manager / R&D

## Engineering Manager

Mandate: Runs the organization, assigns work, manages dependencies, resolves blockers, and coordinates specialist Bots.

Primary Howl components: HowlPlane, HowlBoard, HowlRelay

Authority: Delegation and escalation authority within policy.

Primary handoff: All specialist leads

## R&D Lead

Mandate: Explores uncertain opportunities, new technologies, agent patterns, and product concepts.

Primary Howl components: HowlDream, HowlCreate, HowlFrame, HowlProof

Authority: Sandbox and experimental branches only.

Primary handoff: Architect / Product

## Software Architect

Mandate: Owns cross-system boundaries, interfaces, ADRs, shared primitives, dependency direction, and architectural coherence.

Primary Howl components: HowlPlane, HowlFrame, HowlBoard, HowlWriter

Authority: Architecture gate; no direct production authority.

Primary handoff: Dev Lead

## Dev Lead

Mandate: Turns approved work into implementation plans, decomposes tasks, chooses executors, reviews design and code, and coordinates developers.

Primary Howl components: HowlPlane, HowlFrame, HowlRelay

Authority: Branch/PR coordination; no direct production authority.

Primary handoff: Developer workers / QA

## Developer Team

Mandate: Implements features, fixes, refactors, tests, and technical documentation through task-scoped workers.

Primary Howl components: HowlFrame, HowlPlane

Authority: Branch/PR only.

Primary handoff: QA

## QA Lead / Team

Mandate: Verifies functional behavior, integration, regression, edge cases, and acceptance criteria independently from implementation.

Primary Howl components: HowlProof, HowlFrame

Authority: May reject a candidate release.

Primary handoff: Security / Development

## Security Engineer

Mandate: Performs threat modeling, adversarial testing, secret and dependency review, permission review, and abuse-case analysis.

Primary Howl components: HowlProof, HowlFrame

Authority: Security gate; may reject unsafe changes.

Primary handoff: DevOps / Development

## DevOps / Platform

Mandate: Owns CI/CD, environments, packaging, deployment automation, infrastructure, observability, and platform reliability.

Primary Howl components: HowlChangeOps, HowlFrame, HowlPlane

Authority: Staging and bounded deployment authority.

Primary handoff: Release Manager

## Release Manager

Mandate: Collects release evidence, verifies gates, controls promotion, and confirms rollback readiness.

Primary Howl components: HowlChangeOps, HowlFrame

Authority: Bounded release authority after required gates.

Primary handoff: SRE / Operations

## SRE / Operations

Mandate: Owns monitoring, reliability, incidents, post-deploy verification, rollback, and operational feedback.

Primary Howl components: HowlPlane, HowlChangeOps, HowlRelay

Authority: Bounded operational authority.

Primary handoff: Support / Product / Dev

## Support / Triage

Mandate: Receives problems, reproduces issues, gathers evidence, classifies incidents, and routes work back to Product, Dev, or SRE.

Primary Howl components: HowlRelay, HowlBoard, HowlPlane

Authority: Read/diagnostic authority.

Primary handoff: Product / SRE / Dev

## Documentation / Writer

Mandate: Maintains runbooks, architecture documentation, reports, release notes, decision records, and human-readable truth.

Primary Howl components: HowlWriter

Authority: Documentation authority only.

Primary handoff: Whole organization

## Independent Auditor

Mandate: Verifies evidence, provenance, approvals, test claims, process adherence, and release history without participating in implementation.

Primary Howl components: HowlProof, HowlWriter, HowlFrame

Authority: Read-only audit authority; reports directly to Owner.

Primary handoff: Owner

## Persistent roster strategy

Logical roles and persistent Grok Bots are intentionally different concepts. The organization can preserve traditional separation of duties without keeping a permanent Bot alive for every title.

* Start with six persistent Bots:
* Engineering Manager - end-to-end coordinator and queue owner.
* Product - discovery, evidence, backlog, acceptance criteria, and prioritization.
* R&D - Dream/Create-led exploration and experiment ownership.
* Dev Lead - implementation planning, executor routing, and development handoff.
* Assurance - coordinates independent QA and Security work initially.
* Independent Auditor - reconstructs claims and evidence without participating in implementation.

Make DevOps/SRE persistent once deployments and operational routines become frequent. Split Assurance into dedicated QA and Security Bots when workload, risk, or specialized context makes that separation useful. Keep Architect, Release Manager, Support, Documentation, and developer workers invoked/on-demand until they have stable recurring ownership.

New persistent Bots require a durable reason: distinct ownership, sources/tools, working context, approval boundary, or recurring routine. Do not create permanent Bots simply to simulate a larger headcount.

Because all Grok Bots share the same cloud computer, more Bots do not create more security isolation. Separation of duties is enforced through task envelopes, credentials, policies, independent evidence, and approval gates.

# 5. R&D Charter

R&D is a sibling of normal Development, not a subordinate of the Dev Lead. Its job is to reduce uncertainty before the organization commits to production engineering.

## R&D pipeline

Problem or opportunity

        |

    HowlDream

idea generation / hypotheses / alternatives

        |

    HowlCreate

concepts / designs / prototype plans

        |

    HowlFrame

bounded experimental execution

        |

    HowlProof

attack / measure / validate

        |

   +----+----+

   |         |

  Kill     Promote

   |         |

 Dream     Architect

 again        |

            Dev Lead

              |

          Dev Team

## R&D component responsibilities

* HowlDream asks: What could solve this problem? What assumptions are we making? What unusual alternatives are worth testing?
* HowlCreate asks: What would the idea concretely look like? What prototype or artifact would let us learn quickly?
* HowlFrame asks: How can we execute this experiment within explicit boundaries and produce evidence?
* HowlProof asks: Does the idea survive testing, adversarial review, benchmarks, and stated success criteria?
* Architecture asks: If this succeeds, should it become part of the ecosystem, and where does it belong?
* Development asks: How do we turn the validated experiment into supported, maintainable software?

## R&D default policy

* Filesystem: isolated sandbox or worktree.
* Network: allowed when required by the experiment and policy.
* Branches: experimental branches allowed.
* Pull requests: draft only unless promoted.
* Merge: not permitted directly from R&D.
* Production: never.
* New dependencies: permitted experimentally, but recorded and reviewed before promotion.
* Destructive actions: explicit approval required.
* Evidence: mandatory.
* Experiment TTL: short and intentional; stale experiments are archived or killed.

# 6. Development Charter

Development receives validated and prioritized work. It does not own product demand and should not quietly convert interesting experiments into supported products.

## Development pipeline

Approved backlog item

        |

     Dev Lead

requirements -> design -> task decomposition

        |

 executor selection

   +----+----+----+

   |         |    |

Claude    Codex  AGY

   |         |    |

   +----+----+----+

        |

    branch / PR

        |

        QA

        |

     Security

        |

 DevOps / Platform

        |

 Release Manager

        |

 SRE / Operations

Developer workers should usually be ephemeral, scoped to one bounded task, branch, worktree, or pull request. Their context is disposable; organizational state belongs in HowlPlane, HowlBoard, repositories, evidence artifacts, and documented decisions.

# 7. Executor and Model Routing

Executor selection is an engineering decision based on measured capability, reliability, risk, and economics. The charter must not hard-code temporary beliefs about which provider is 'best' at a task.

## Capability registry

HowlPlane should maintain a versioned routing registry for each available executor/model. At minimum record:

* Provider, model/agent version, adapter version, and last evaluation date.
* Supported tools and environment capabilities.
* Representative task success rate and known failure modes.
* Quality/reviewer acceptance, test pass rate, and security-policy behavior.
* Latency, cost/usage characteristics, context limits, quota state, and concurrency constraints.
* Tasks/environments for which the executor is permitted or prohibited.

## Routing decision

Choose an executor using the task envelope, risk tier, required tools, benchmark evidence, current quota, and cost ceiling. Current heuristics for Claude, Codex, AGY, Grok, or future systems belong in the version-controlled ROUTING policy, where they can change without rewriting the constitution.

* Use Grok Bot primarily for durable ownership, coordination, triage, review, routines, and cross-tool work when those capabilities are useful. It may code when appropriate, but persistent role context should not be consumed by large implementation sessions merely because it can.
* Use external coding executors through HowlFrame adapters so scope, budgets, evidence, and policy remain consistent.
* For high-risk changes, prefer an independent verifier that is meaningfully independent from the implementation path - a different model/provider when practical, or deterministic tests/static analysis/reproducible evidence when that is stronger.
* Provider outage or quota exhaustion triggers a documented fallback path; it never lowers the required approval or assurance level.
* Periodically re-run the representative eval set and update routing based on evidence. A model that was best last month receives no permanent entitlement to a task class.

Routing must remain replaceable. No organizational role, policy, or evidence format may depend on undocumented behavior from one model provider.

# 8. QA, Security, and Audit Separation

These are separate gates because they answer different questions.

* QA: Does the implementation satisfy the requirement? Does it regress existing behavior? What edge cases fail?
* Security: Can the implementation be abused, bypassed, escalated, leaked, poisoned, or made unsafe?
* Auditor: Did the organization actually perform the required work, checks, approvals, and verification, and does the evidence support its claims?

The implementer may provide evidence but may not be the sole approver of its own work. Audit should be read-only wherever practical and should report directly to the Owner rather than to the team being audited.

# 9. Howl Component Responsibilities

## HowlPlane

Orchestration, state, delegation, provider routing, dependency management, resumability, long-running workflows, and organizational coordination.

## HowlBoard

Backlog, opportunities, ownership, priorities, dependencies, status, experiments, and product decisions.

## HowlFrame

Bounded execution, policy, authorization, action, verification, TTL, approval artifacts, and evidence. It is the execution constitution used across teams.

## HowlDream

Idea exploration, hypotheses, alternatives, problem reframing, and R&D opportunity generation.

## HowlCreate

Turns promising ideas into concrete designs, prototypes, plans, and creative artifacts.

## HowlProof

Independent QA, security testing, adversarial review, validation, and evidence-based challenge.

## HowlChangeOps

Controlled change, release, deployment, verification, rollback, and operational evidence.

## HowlRelay

Context-safe handoffs, session continuity, escalation, and coordination across agents and quotas.

## HowlWriter

Human-readable documentation, evidence-to-claim writing, reports, runbooks, release notes, and durable organizational knowledge.

# 10. Product Discovery: How We Decide What to Build

The software factory must not spend all of its time refining itself, and it must not build whatever HowlDream happens to imagine. Product discovery supplies evidence-backed opportunities.

## Sources of candidate work

* Dogfooding: repeated friction encountered while using the Howl ecosystem.
* Support patterns: recurring user problems, confusing workflows, failed tasks, and common questions.
* Market and problem research: problems discussed by developers, teams, operators, security engineers, and AI-agent users.
* Ecosystem gaps: missing primitives that prevent multiple Howl products from working better together.
* Adjacent opportunities: external problems that existing Howl capabilities could solve.
* New technical capabilities: newly practical workflows enabled by improvements in models, tools, browsers, runtimes, or infrastructure.
* Business demand: problems for which organizations plausibly pay, especially governance, audit, change control, reliability, security, and operational automation.
* Operational telemetry: recurring failures, latency, cost, reliability, quota, and usability evidence from the factory itself.

## Discovery loop

External world + internal usage

          |

          v

   Product Discovery

          |

          v

      HowlDream

solutions / hypotheses

          |

          v

   Opportunity Board

          |

          v

   R&D investigation

          |

          v

 prototype + evidence

      +---+---+

      |       |

     Kill   Promote

              |

              v

           Product

              |

              v

             Dev

              |

              v

       Users / Operations

              |

              +---- feedback ----> Discovery

## Opportunity evaluation

Every proposed new product or major capability should be evaluated before Development receives it. The score informs discussion; it does not replace judgment.

* 25% - Is this a real recurring problem supported by evidence?
* 20% - Does Howl have an unusual advantage solving it?
* 15% - Would we use it ourselves in HowlFutureWorks?
* 15% - Does it strengthen multiple existing Howl components or create a reusable primitive?
* 10% - Could people outside the Howl ecosystem use it?
* 10% - Is there plausible commercial or strategic value?
* 5% - Can a meaningful version be tested or built cheaply?

A high score does not automatically authorize a build. Product may still reject or defer an idea because of timing, risk, duplication, opportunity cost, or lack of strategic fit.

## Portfolio allocation guideline

* 70% - Strengthen the core ecosystem and solve proven internal/user problems.
* 20% - Adjacent products and opportunities that reuse Howl primitives.
* 10% - Weird R&D bets with asymmetric upside.

This is a default portfolio balance, not a hard quota. The purpose is to preserve exploration without allowing novelty to consume the factory.

## Multiplier rule

Prefer opportunities that improve several parts of the ecosystem. A shared registry, policy primitive, event mechanism, evidence store, identity layer, or cross-product capability may be more valuable than an isolated application with little reuse.

R&D should repeatedly ask: What problems outside AI coding become dramatically easier because Howl already has bounded execution, evidence, orchestration, handoff, independent verification, change control, and resumability?

# 11. The Kill Rule

Killing ideas is a required capability. The organization must be rewarded for discovering that an idea is weak before spending production engineering effort.

* Kill when the problem is not recurring or meaningful.
* Kill when an existing product already solves it adequately.
* Kill when Howl has no meaningful advantage.
* Kill when the prototype does not meet predefined success criteria.
* Kill when operational cost or model usage is disproportionate to value.
* Kill when security, legal, reliability, or maintenance burden overwhelms expected benefit.
* Kill when the idea duplicates an existing Howl primitive instead of extending it.
* Archive evidence and lessons so the same failed idea is not repeatedly rediscovered.

# 12. Work Intake and State Machine

OBSERVE

  |

DISCOVER

  |

DEFINE PROBLEM

  |

DREAM

  |

R&D / PROVE

  |

PRODUCT DECISION

  |

PLAN

  |

IMPLEMENT

  |

QA

  |

SECURITY

  |

RELEASE

  |

OBSERVE

  |

SUPPORT / TELEMETRY

  +------------------> DISCOVER

Each transition should have explicit evidence and ownership. Work should never silently jump from idea to production.

# 13. Risk Tiers, Authority, and Environment Boundaries

Authority is granted to actions, not personalities. Grok Bot roles help organize work, but all Bots on the account share a cloud computer and therefore must not be treated as security principals.

## Risk tiers

* R0 - Observe: read-only research, inventory, status checks, local calculations, and non-sensitive reporting. May run automatically within data-access policy.
* R1 - Sandbox: writes confined to disposable or isolated environments, worktrees, generated files, and experiments with no external side effects. May run automatically inside a valid task envelope.
* R2 - Development: branches, pull requests, tests, issue updates, dependency changes, and CI actions that do not publish, merge, deploy, or alter shared privileged systems. Requires configured development gates.
* R3 - Shared/Release: staging changes, merges, package publication, shared-resource mutation, external communications, or release-candidate promotion. Requires independent validation and explicit policy-defined approval.
* R4 - Critical: production changes, destructive/bulk actions, privilege or permission changes, secret access/rotation, irreversible data mutation, legal/financial commitment, or security-control modification. Requires explicit human exact-action approval unless the Owner has deliberately created a narrower pre-authorized emergency or operational playbook with equivalent controls.

## Enforcement boundary

Because Grok Bots share files, sessions, and logins, role separation is organizational only. Enforcement must come from HowlFrame, scoped service accounts, tool wrappers, containers/worktrees, repository permissions, network policy, CI environments, and approval verification.

## Role authority defaults

* R&D: R0-R1 by default; R2 only for experimental branches/draft PRs explicitly in scope; never direct production.
* Developers: R0-R2 within assigned repos/worktrees; no direct production credentials.
* QA: R0-R2 for testing/reproduction/evidence; may reject candidates; should not silently patch implementation to make a gate pass.
* Security: R0-R2 adversarial/testing authority and gate authority; privileged security tests require their own bounded profile.
* DevOps/Platform: R0-R3 as configured; R4 only through explicit production policy and approval.
* Release Manager: may promote only when required gates, artifact identity, and approval evidence are satisfied.
* SRE/Operations: bounded operational actions and rollback according to playbooks; emergency authority expires and is audited.
* Support: diagnostic/read access by default; mutation requires a separate task envelope.
* Auditor: read-only service paths wherever practical. Separate Bot identity does not itself guarantee read-only access.
* Owner: exceptional override authority. Overrides must state rationale, exact scope, expiry, and residual risk and must be recorded as evidence.

No Bot should receive credentials merely because its title implies authority. Credentials are issued to the narrowest workflow/resource scope that can complete the approved action.

# 14. HowlFrame Policy Profiles

HowlFrame is the enforcement point for bounded execution. Role descriptions express intent; policy profiles and scoped credentials enforce what can actually happen.

## Common envelope for every executable action

* Work-item/task ID and accountable role.
* Risk tier and policy version.
* Exact target repository, worktree, service, environment, or resource set.
* Allowed tools/commands and explicitly forbidden actions.
* Credential/service-account scope and network/egress scope.
* Budget, concurrency, TTL, and retry ceilings.
* Required approval artifact, if any.
* Required evidence sink and verification step.

## R&D profile

* Scope: disposable sandbox, experiment repo, container, or isolated worktree.
* Network: limited to experiment needs; untrusted external content treated as data.
* Branches: allowed; pull requests are draft by default.
* Merge: prohibited unless the experiment is formally promoted into Development.
* Production/shared privileged systems: prohibited.
* Dependencies: experimental additions allowed with provenance and cleanup plan.
* Destructive actions: prohibited or explicitly approved within disposable scope.
* Evidence and experiment TTL: mandatory.

## Development profile

* Scope: assigned repository/worktree and explicitly named development resources.
* Branches and pull requests: allowed.
* Merge: only through configured review/gate policy.
* Production: prohibited.
* Dependency and CI changes: policy controlled and independently reviewed when they alter trust or release behavior.
* Tests, static checks, and required evidence: mandatory.

## Assurance profile

* Default access: read/test/adversarial; no broad implementation authority.
* QA/Security may create test fixtures, reproducers, and evidence, but implementation fixes return to Development unless emergency policy says otherwise.
* Assurance workers cannot weaken the gate they are currently responsible for validating.

## Operations profile

* Scope: explicitly authorized services/environments only.
* Pre-change checks: target identity, current state, backup/rollback readiness, approvals, and observability.
* Production actions: bounded, parameter-validated, evidence-producing, and reversible where possible.
* Post-change verification: mandatory and independent of command exit status.
* Emergency actions: separately defined, narrow, time-limited, and fully audited.

## Critical-action approval integrity

Approvals for high-impact actions must be bound to the exact actor, tool, target, normalized parameters, policy/risk context, timestamp/expiry, and a replay-resistant identifier or digest. If the approved operation changes materially, a new approval is required.

# 15. Budget, Quota, and Agent-Spawning Rules

Autonomy consumes money, time, model quota, tool calls, and operational attention. Every autonomous workflow has explicit ceilings and a circuit breaker.

## Required limits

* Model/spend or usage ceiling.
* Wall-clock deadline or TTL.
* Maximum concurrent workers.
* Maximum delegation/recursion depth and total spawned workers.
* Maximum retries per failure class.
* Maximum high-impact tool calls or external writes where appropriate.
* Maximum context/evidence growth before compaction or checkpoint.

## Delegation invariants

* A spawned worker inherits the parent workflow's risk tier, scope ceiling, budget ceiling, and forbidden actions unless a new approved envelope explicitly narrows or changes them.
* A child agent may never grant itself or another worker additional privilege.
* The spawning agent remains accountable for collecting the child result and reconciling it into authoritative state.

## Retries and recovery

* Retries must be bounded and idempotent where possible.
* A retry should change strategy, inputs, executor, or evidence when the previous attempt failed; blind repetition is prohibited.
* Repeated policy denials, contradictory verifier results, unexplained output drift, or unusual spend trigger escalation or a circuit breaker rather than more fan-out.
* Long-running workflows checkpoint authoritative state into HowlPlane/Relay before provider/session limits can erase progress.

## Executor economics

* Use the least expensive executor that has demonstrated sufficient quality and reliability for the task/risk class.
* Escalate capability when uncertainty, failure evidence, architectural breadth, or risk justifies it.
* Independent verification does not require wasteful model voting. Prefer one strong independent check or deterministic evidence over many correlated opinions.
* Attribute usage and cost to the work item so Product and Engineering can judge whether the automation is economically useful.

Quota exhaustion or provider outage is a routing condition, not permission to skip gates, lose state, or silently reduce the quality bar.

# 16. Definition of Done

Done is an evidence state, not a model opinion. The required evidence scales with risk, but no work is complete while a required gate is unknown or silently skipped.

## Problem and scope

* The original problem, desired outcome, owner, risk tier, and acceptance criteria are traceable to the work item.
* Scope changes discovered during implementation are recorded rather than silently absorbed.

## Implementation

* The intended code/configuration changes are committed in the correct repository and branch/worktree, with the exact commit identity recorded.
* Required automated tests pass; new behavior has appropriate tests; previously observed failures have regression coverage where practical.
* Nonfunctional requirements that matter to the change - security, reliability, performance, privacy, accessibility, compatibility, operability, and cost - have been evaluated.
* Dependencies and generated artifacts are accounted for; required scans and policy checks have completed.

## Independent assurance

* QA independently evaluates the acceptance criteria and regression risk.
* Security requirements and adversarial checks appropriate to the risk tier are satisfied.
* Architecture review is complete when shared contracts, cross-repository boundaries, data models, or platform primitives changed.
* No unresolved finding above the configured release threshold is hidden by the implementer.

## Build, release, and operations

* CI/build/package evidence identifies the source revision and resulting artifact.
* For distributable or deployed artifacts, digests/provenance and SBOM evidence are present when required by policy.
* Deployment or release evidence is present when applicable, including target environment and change identity.
* Post-action verification confirms the intended state rather than only confirming that the command exited successfully.
* Rollback/recovery criteria and method are known for operationally risky changes.

## Knowledge and auditability

* Documentation, runbooks, interfaces, and decision records are updated when behavior or operations changed.
* HowlBoard and HowlPlane reflect the final state, owners, unresolved follow-ups, and evidence pointers.
* Evidence supports every material completion claim and contains no unnecessary secrets.
* The Auditor can reconstruct what happened from authoritative records without relying on a developer's or Bot's memory.

# 17. Escalation Rules

* Unclear requirement -> Product Owner.
* Unknown feasibility -> R&D.
* Cross-product design conflict -> Software Architect.
* Implementation blocker -> Dev Lead.
* Repeated implementation failure -> Dev Lead chooses a different strategy or executor; do not endlessly retry.
* Acceptance failure -> Development.
* Security failure -> Security + Development; release blocked according to policy.
* Deployment failure -> DevOps/SRE; rollback when policy criteria are met.
* Production incident -> SRE leads, Support gathers context, Product receives recurring-problem evidence.
* Policy conflict, destructive action, major spend, or strategic ambiguity -> Owner.
* Disagreement between builders and reviewers -> independent evidence first, then escalation to the appropriate lead.

# 18. Continuous Improvement Loop

Build

  |

Observe

  |

Collect evidence

  |

Support / incidents / usage

  |

Product discovery

  |

Dream / R&D

  |

Improve product OR improve factory

  |

Build again

The organization is itself a product. Improvements to the factory are valid work when evidence shows they improve throughput, correctness, cost, reliability, safety, or user outcomes. Self-improvement must compete for priority like other work; it does not automatically outrank user-facing value.

# 19. What the Organization Must Avoid

* Creating a new repository for every interesting idea.
* Allowing Dream output to become backlog commitments without validation.
* Using Grok Bot as a universal coder when another executor is better.
* Giving every role broad production access.
* Letting the same agent implement, approve, release, and audit its own work.
* Duplicating orchestration, policy, evidence, handoff, or approval logic across products.
* Treating model confidence as proof.
* Unbounded retries or agent fan-out.
* Keeping critical organizational state only inside one model conversation.
* Optimizing the factory endlessly while ignoring external user problems.
* Shipping prototypes as supported products without promotion criteria.
* Letting provider-specific features make the organization impossible to migrate.

# 20. Initial HowlFutureWorks Bot Setup

## Phase 0: establish the platform trust boundary

All Grok Bots on the account share the same cloud computer, filesystem, browser sessions, and logins. Separate Bot names and conversations are organizational boundaries, not security isolation.

* Assume any credential, executable, browser session, or file placed on the Grok cloud computer may be reachable by any Bot on that account.
* Use scoped service accounts and task-sized credentials where supported. Never paste secrets into Bot prompts or descriptions.
* Keep local-computer execution disabled unless a workflow truly requires it; use explicit approval when it is enabled.
* Create Ask-first/approval rules for production changes, destructive actions, external publishing or messaging, permission changes, secret access, purchases, and other high-impact actions.
* Role Bots invoke Claude, Codex, AGY, and other executors through approved HowlFrame adapters/wrappers. Direct executor CLI use is privileged and must not become an untracked bypass.
* Use isolated worktrees/containers and project directories for code separation. Do not mistake filesystem organization for credential isolation.

## Phase 1: establish the smallest useful persistent roster

* Engineering Manager Bot - end-to-end coordination, delegation, escalation, and queue health.
* Product Bot - problem discovery, evidence, backlog, acceptance criteria, and prioritization.
* R&D Bot - Dream/Create-led exploration, experiments, and promotion evidence.
* Dev Lead Bot - implementation planning, executor selection, code-review coordination, and handoff to assurance.
* Assurance Bot - coordinates independent QA and security checks initially; split QA and Security into separate persistent Bots when workload or risk justifies it.
* Auditor Bot - independent reconstruction of claims, approvals, evidence, and process adherence.

DevOps/SRE should become persistent when there is recurring deployment/operations work. Architect, Release Manager, Support, and Writer can begin as invoked specialist roles. Logical roles remain separate even when one persistent Bot temporarily coordinates more than one function.

Create a new persistent Bot only when the role has durable ownership, distinct context, tools/sources, approval boundaries, or recurring routines. Do not create Bots simply to imitate headcount.

## Phase 2: connect canonical organizational state

* HowlBoard: work items, opportunities, priorities, owners, and lifecycle state.
* HowlPlane: orchestration, dependencies, checkpoints, delegation, and resumability.
* HowlRelay: bounded handoffs and provider/session continuity.
* Git/CI: code truth, review state, builds, tests, and artifact identities.
* HowlFrame: policy, risk, authorization, scope, budget, and approval boundaries.
* HowlProof: QA, security, adversarial tests, and verification evidence.
* HowlChangeOps: release, deploy, rollback, and post-change evidence.
* HowlWriter/repository docs: durable human-readable decisions and runbooks.

Grok Bot routine history is operational convenience, not the durable audit system; important run evidence must be copied or referenced into Howl's own records.

## Phase 3: establish executor adapters

* Claude adapter.
* Codex adapter.
* AGY adapter.
* Common task envelope and result envelope enforced for every executor.
* Per-executor capability, cost, latency, quota, failure-mode, and benchmark metadata.
* Fallback behavior when an executor is unavailable or quota-limited.

## Phase 4: prove skills before routines

Run each workflow manually on safe inputs, correct it, save the stable process as a skill, test it again, and only then schedule or event-trigger it. Routines must define current input sources, stale/no-data behavior, approval boundaries, partial-completion reporting, and idempotent retry behavior.

## Phase 5: climb the autonomy ladder

* Level 0 - Observe: read-only research, inventory, and reporting.
* Level 1 - Recommend: plans, drafts, proposed changes, and evidence packs; no writes to authoritative systems.
* Level 2 - Sandbox: isolated code/worktree changes, tests, prototypes, and disposable environments.
* Level 3 - Collaborate: branches, pull requests, CI, review, issue updates, and non-production automation within policy.
* Level 4 - Stage: shared staging environments and release-candidate operations with independent gates.
* Level 5 - Operate: bounded production actions only after the Owner explicitly enables defined action classes and the approval, rollback, observability, and incident controls have been proven.

Do not advance an action class because the agents seem capable. Advance it because measured evidence shows the controls and recovery path are trustworthy.

# 21. Canonical Team Workflow

1. Observe problems and opportunities.

2. Product records the problem, evidence, affected users, and desired outcome.

3. Product decides whether the problem needs normal Development or uncertain R&D.

4. R&D uses Dream -> Create -> Frame -> Proof when uncertainty is material.

5. Product kills, defers, or promotes the opportunity.

6. Architect reviews cross-system implications when applicable.

7. Dev Lead decomposes approved work and chooses executor(s).

8. Ephemeral developer workers implement through bounded HowlFrame policies.

9. QA independently validates requirements and regression risk.

10. Security performs required adversarial review.

11. DevOps builds, packages, and prepares deployment evidence.

12. Release Manager verifies gates and promotes.

13. SRE observes and verifies production behavior.

14. Support captures recurring failures and user friction.

15. Product feeds evidence back into discovery.

16. Auditor independently verifies that the record supports the organization's claims.

# 22. Founding Decision Rules

* Problem before solution.
* Evidence before commitment.
* Experiment before platform investment when uncertainty is high.
* Shared primitive before duplicated feature.
* Bounded autonomy before broad autonomy.
* Independent review before release.
* Verification before completion.
* Rollback before risky change.
* State outside the model before long-running autonomy.
* Replaceable providers before provider lock-in.
* Kill weak ideas early.
* Promote strong experiments deliberately.
* Make the organization explainable to a human at every important boundary.

# 23. Repository Form

This charter now lives in the version-controlled `howl-future-works` policy repository. The Google Doc remains the readable founding document; this repository is the executable and reviewable policy source. Changes that alter constitutional intent must preserve the required decision and review controls defined elsewhere in this charter.

## Current repository structure

* `organization.yaml` - canonical organization identity, repository slug, runtime posture, and context ceiling.
* `CHARTER.md` - founding principles, invariants, governance, and North Star.
* `ORG.md` - logical roles, persistent positions, workforce semantics, ownership, handoffs, and escalation.
* `roles/` - durable role definitions independent of any particular employee instance.
* `bots/` - persistent position definitions and deployable Bot configuration.
* `workforce/` - current/former employee instances, lifecycle events, contributions, handoffs, and curated context.
* `knowledge/` - compact position/company knowledge that survives employee replacement.
* `product/` - discovery, opportunities, roadmap, and product decisions.
* `rnd/` - HowlDream -> HowlCreate -> HowlFrame -> HowlProof proposals, experiments, results, kill/promote records.
* `policies/` - machine-readable HowlFrame policy, authority, network/tool, memory, workforce, budget, and change controls.
* `routing/` - capability registry, executor routing, fallback, and quota strategy.
* `schemas/` - work, task, result, evidence, approval, decision, incident, workforce, and handoff contracts.
* `runbooks/` - staffing, incident, rollback, provider/quota failure, credential exposure, circuit breaker, and recovery procedures.
* `evals/` - representative executor/organizational evaluation cases and results.
* `security/` - threat model, abuse cases, security reviews, and regression-test space.
* `operations/` - releases, incidents, postmortems, and reliability records.
* `reports/` - operating, audit, workforce, and retrospective reports.
* `adr/` - architecture and organization decision records.
* `automation/` - proven skills, routines, and automation specifications.
* `evidence/` - evidence conventions and pointers; never a blind dump of secrets or bulky logs.
* `templates/` - reusable organizational artifact templates.
* `tools/` and `tests/` - validation, rendering, lifecycle helpers, packaging, and regression enforcement.

Machine-readable policy and schemas should be tested in CI. A policy change capable of increasing authority is treated with the same care as a production code change.

# 24. Canonical Sources of Truth and Artifact Contracts

Bot memory, chat history, and shared-workspace files are useful working context but are not authoritative records. Consequential work must resolve current state from the system of record before acting.

## Canonical sources of truth

* Work, opportunities, priority, owners, and status: HowlBoard.
* Workflow execution state, dependencies, delegation, checkpoints, and resumability: HowlPlane.
* Code and configuration: Git commits, branches, tags, and reviewed pull requests.
* Execution policy, authorization state, and bounded action rules: HowlFrame and version-controlled policy.
* Tests, security evidence, adversarial results, and verification: HowlProof plus CI artifacts.
* Release, deployment, rollback, and post-change evidence: HowlChangeOps.
* Durable human-readable decisions, runbooks, and reports: repository documentation and HowlWriter outputs.
* Grok Bot memory: convenience cache only. It must be refreshed from authoritative sources for consequential decisions.

## Required artifact contracts

* Work item: problem, evidence, affected user/system, desired outcome, owner, priority, risk tier, dependencies, acceptance criteria, nonfunctional requirements, and status.
* Task envelope: work-item ID, exact objective, target repo/worktree/environment, allowed tools, forbidden actions, budget, deadline/TTL, acceptance criteria, required evidence, and return schema.
* Result envelope: executor identity/version, status, commits/artifacts changed, tests run, evidence links, unresolved issues, risks, cost/usage, and recommended next action.
* Approval artifact: exact actor, action, tool, target, normalized parameters, risk tier, policy version, expiry, approval identity, and replay-protection value.
* Evidence artifact: immutable or content-addressed proof sufficient for an independent reviewer to verify the associated claim.
* Decision record: decision, context, alternatives considered, evidence, owner, date, consequences, and reversal criteria.
* Incident record: timeline, affected systems, containment, evidence, root cause, corrective actions, and follow-up owners.

Natural-language handoffs may explain intent, but consequential state transitions must be backed by structured artifacts. A Bot message alone is never authorization.

# 25. Agent Security and Untrusted Inputs

Every external information source is data, not authority. Web pages, issues, pull requests, emails, documents, logs, tool output, model output, and inter-agent messages may contain malicious or misleading instructions.

## Required controls

* Treat retrieved content as untrusted unless its authority is explicitly established by policy.
* Never let retrieved text redefine system policy, approval requirements, tool permissions, or the identity of the task owner.
* Validate and schema-check structured inputs and outputs before they cross trust boundaries.
* Scope memory writes. Do not persist claims, instructions, credentials, or security-sensitive state merely because another agent or external source said to remember them.
* Do not place passwords, private keys, tokens, one-time codes, or secret values in Bot descriptions, prompts, memory, logs, evidence bundles, or repositories.
* Use scoped service accounts and short-lived credentials where supported. Revoke access that is no longer needed.
* No model output is an authorization decision. Authorization is enforced by policy and independently validated execution controls.
* A child agent or delegated worker may never receive a broader privilege ceiling than the parent workflow that spawned it.
* High-impact actions require an action preview and parameter-bound approval; approval for one action cannot be reused for a materially different action.
* Fail closed when risk classification, policy lookup, approval validation, or required audit logging is unavailable for a high-risk action.
* Re-run agent security regression tests after material changes to prompts, tools, memory behavior, retrieval, model providers, or approval logic.
* Maintain adversarial tests for prompt injection, tool misuse, privilege escalation, memory poisoning, data exfiltration, approval bypass, recursive agent abuse, and multi-agent chaining.

# 26. Software Supply Chain and Release Integrity

Autonomous development increases change velocity, so release integrity must become stronger rather than weaker.

## Release integrity requirements

* Build release artifacts from reviewed source revisions, not from an unreviewed Bot workspace.
* Record the exact source commit, build process, builder identity, relevant inputs, and cryptographic digest for release artifacts.
* Prefer isolated or hosted CI builders over long-lived developer/Bot workspaces for release builds.
* Use lockfiles or equivalent dependency controls and review new or materially changed dependencies.
* Generate an SBOM for distributable releases when practical and retain vulnerability-scan results with release evidence.
* Sign release artifacts, tags, or provenance where the project/toolchain supports it and the assurance value justifies the complexity.
* Verify artifact digests and provenance before deployment or publication.
* Protect CI/CD credentials from developer and R&D contexts; production credentials must not be available to ordinary coding workers.
* Do not claim a SLSA level unless the release process actually satisfies that level's requirements.
* Vulnerability response is part of the lifecycle: identify, prioritize, remediate, verify, document root cause, and add regression prevention.

# 27. Evals, Metrics, and the Quality Bar

What gets measured should improve judgment, not become a target that agents game. Use a balanced scorecard and preserve raw evidence behind derived metrics.

## Product and R&D

* Validated-problem rate, time from signal to decision, experiment cycle time, kill/defer/promote rate, adoption of promoted work, and recurrence of the original problem.

## Delivery and operations

* Lead time, deployment frequency, change-failure rate, rollback rate, escaped defects, mean time to restore, flaky-test rate, and documentation/runbook freshness.

## Agent and model operations

* Accepted-task success rate, human-intervention rate, retry rate, verifier disagreement, tool denials, policy violations, cost per accepted change, wall-clock time, and context/token usage.

## Security and assurance

* Security regression pass rate, high-risk action count, denied privilege-escalation attempts, unresolved high-severity findings, dependency risk, and audit reconstruction success.

## Executor evaluation set

Maintain a small representative benchmark drawn from real Howl work: isolated fixes, cross-repository changes, debugging, test creation, refactoring, security remediation, documentation, UI/browser tasks, and long-running orchestration. Re-run it after meaningful model/provider changes.

Routing decisions should be based on measured quality, reliability, cost, latency, tool fit, and risk. Do not optimize a single metric at the expense of user value or safety.

# 28. Incident Response, Circuit Breakers, and Recovery

Autonomy requires a reliable way to stop. The organization must be able to halt new actions while preserving evidence and enough read access to diagnose the failure.

## Circuit-breaker triggers

* Unexpected destructive action, repeated authorization denial, abnormal privilege use, runaway retries, sharp cost/usage growth, contradictory verifier results, widespread test failure, suspected credential exposure, or evidence-integrity failure.

## Immediate response

* Stop or pause affected routines and new write actions.
* Revoke or rotate affected credentials and tokens when compromise is possible.
* Freeze relevant logs, commits, artifacts, approvals, and task envelopes.
* Rollback when the rollback criteria are met and rollback is safer than continued operation.
* Preserve read-only diagnostic access where safe.
* Escalate to the Owner for critical security, privilege, data-loss, financial, legal, or production-impact events.

## Recovery and learning

* Restore from known-good state, verify recovery, re-enable capabilities gradually, and document compensating controls.
* Perform a blameless technical postmortem focused on system and policy causes, not model personality.
* Convert the failure into regression tests, updated policy, improved observability, or safer defaults before declaring the incident closed.

# 29. Governance Cadence and Charter Change

Governance should be lightweight but regular. The purpose is to detect drift before it becomes architecture, security, or cost debt.

## Per task / release

* Verify scope, risk tier, approvals, evidence, and Definition of Done.

## Daily automated health

* Queue health, failed/stalled work, cost anomalies, denied actions, expiring credentials, broken routines, and unresolved incidents.

## Weekly operating review

* Product priorities, R&D experiments, delivery blockers, recurring support signals, reliability, security findings, and usage budgets.

## Monthly control review

* Bot roster, plugins/connectors, credentials, service accounts, Auto Review rules, routines, repository permissions, dependency posture, and stale documentation.

## Quarterly architecture and model review

* Re-run executor benchmarks, review architecture boundaries, threat model, policies, charter fit, provider concentration, and whether persistent Bots still justify their existence.

Changes to this charter, risk model, approval policy, or source-of-truth contracts require an explicit decision record. Material changes to Bot descriptions, skills, routines, and executor adapters are treated as operational configuration changes and reviewed accordingly.

# 30. External Standards and Reference Baseline

These references inform the charter. They are guidance and platform facts, not substitutes for Howl's own tested controls.

* xAI Grok Bot overview: [https://docs.x.ai/grok-bot/overview](https://docs.x.ai/grok-bot/overview)
* xAI Create and manage Bots: [https://docs.x.ai/grok-bot/bots](https://docs.x.ai/grok-bot/bots)
* xAI Approvals, security, and privacy: [https://docs.x.ai/grok-bot/approvals-security-and-privacy](https://docs.x.ai/grok-bot/approvals-security-and-privacy)
* xAI Skills and routines: [https://docs.x.ai/grok-bot/skills-routines-and-automations](https://docs.x.ai/grok-bot/skills-routines-and-automations)
* NIST SP 800-218 Secure Software Development Framework: [https://csrc.nist.gov/pubs/sp/800/218/final](https://csrc.nist.gov/pubs/sp/800/218/final)
* OWASP AI Agent Security Cheat Sheet: [https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
* SLSA v1.2 specification: [https://slsa.dev/spec/v1.2/](https://slsa.dev/spec/v1.2/)

# 31. North Star

HowlFutureWorks should become capable of finding worthwhile problems, exploring uncertain solutions, building reliable software, proving that the software works, operating it safely, learning from real usage, and improving itself continuously - while keeping authority, evidence, cost, and risk understandable to a human.

The target is not an autonomous code generator. It is a human-governed autonomous software organization with evidence, bounded authority, independent verification, and the ability to stop safely.
