# Provider Outage

## Trigger
Executor/provider unavailable or materially degraded.

## Procedure
1. Checkpoint task, branch/worktree, evidence and orchestration state before switching.
2. Preserve the task risk tier, approval requirements and acceptance criteria.
3. Consult routing fallback policy and capability registry; verify the fallback is allowed for this task class.
4. Record the executor/model/adapter change in the result/handoff.
5. Do not lower assurance because the preferred provider is unavailable.
6. If no approved fallback exists, pause and escalate rather than improvising privilege.

## Required record
Link work item/incident, actors or employee IDs, timestamps, policy/risk context, evidence pointers, actions, verification and follow-ups.

## Exit criteria
- Fallback resumes from authoritative state and the change of executor is auditable.
