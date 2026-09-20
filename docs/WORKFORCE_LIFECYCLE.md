# Workforce Lifecycle

The organization is intentionally staffable like a real software organization while preserving machine-verifiable continuity.

## Why the layer exists

Roles must outlive individual Bot instances. A weak or obsolete Bot can be replaced without erasing the decisions and work it helped produce. Conversely, preserving a Bot's conversation forever is not institutional memory; it is expensive, stale, and hard to audit.

## State model

`candidate -> hired -> active -> suspended -> active`

An active employee may also transition to a terminal state:

`active|suspended -> terminated | retired | laid_off | replaced | provider_retired`

Terminal employees remain documented. The position may remain active and be filled by a successor.

## Hire

A hire packet includes:

- employee ID,
- position and logical role,
- manager,
- provider/deployment kind,
- risk ceiling inherited from the position,
- required always-load context,
- predecessor handoff when relevant,
- current work references,
- onboarding verification.

Do not clone raw conversation history into a new employee. Start with clean role context plus curated organizational knowledge.

## Performance and fit

Evaluate workers using evidence: task acceptance, verifier disagreement, retries, cost, reliability, policy behavior, tool fit, and role-specific outcomes. Reviews are inputs to staffing decisions, not permission to bypass policy.

Possible outcomes include coaching/instruction adjustment, narrower scope, model/provider change, reassignment, suspension, replacement, or separation.

## Separation / firing

A normal termination is controlled offboarding, not file deletion.

Required sequence:

1. Freeze new work for the employee.
2. Identify active tasks, routines, owned queues and temporary credentials.
3. Produce an exit handoff and context snapshot.
4. Reassign unfinished work.
5. Record final contributions and unresolved risks.
6. Revoke or rotate employee-scoped access as applicable.
7. Disable/suspend the live Bot or routines.
8. Record the separation event and update roster status.
9. Verify that the durable record remains readable.
10. Fill or retire the position separately.

For suspected compromise, use emergency suspension before normal offboarding.

## Succession

A replacement receives:

- current role/position files,
- the predecessor's **curated** exit handoff,
- current authoritative work references,
- stable lessons and ADRs,
- required policies/runbooks.

It does not inherit the predecessor's credentials or unverified memory. Stable lessons that should survive multiple generations are promoted into `knowledge/positions/<position>.md`, so successor context does not grow as a chain of old handoffs.

## Rehire

Use the same employee ID only when intentionally restoring the same employee identity. A newly generated Bot/model instance filling the same position is normally a new employee generation.

## Position retirement

Retiring a persistent Bot position is different from firing an employee. A position retirement changes `bots/manifest.yaml` and may affect organizational design; all former employee records remain.
