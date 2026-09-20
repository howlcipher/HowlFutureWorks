# Failed Deployment

## Trigger
Deployment fails, post-change verification fails, or resulting state is ambiguous.

## Procedure
1. Stop additional rollout/fan-out.
2. Capture target, artifact/commit identity, command/output summary and health evidence.
3. Determine whether rollback criteria are met; rollback when safer than continued operation.
4. Preserve failed-deployment evidence and open/attach an incident when impact warrants it.
5. Do not "fix forward" by unreviewed production edits outside the task/change envelope.
6. Verify recovered state independently from command exit status.

## Required record
Link work item/incident, actors or employee IDs, timestamps, policy/risk context, evidence pointers, actions, verification and follow-ups.

## Exit criteria
- Service is stable, desired/current state are known, and follow-up work has owners.
