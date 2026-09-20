# Rollback

## Trigger
Configured rollback criteria are met or Owner/SRE authorizes rollback.

## Procedure
1. Confirm exact target and last known-good artifact/state.
2. Verify rollback authority and required approvals.
3. Preserve pre-rollback evidence.
4. Execute the smallest bounded rollback.
5. Verify service/data state after rollback.
6. Record whether forward remediation is still required.

## Required record
Link work item/incident, actors or employee IDs, timestamps, policy/risk context, evidence pointers, actions, verification and follow-ups.

## Exit criteria
- Known-good or explicitly accepted state is restored and verified.
