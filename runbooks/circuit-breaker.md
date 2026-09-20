# Circuit Breaker

## Trigger
Any configured safety/operational threshold is crossed.

## Procedure
1. Pause new write actions for the affected scope.
2. Preserve read-only diagnostics where safe.
3. Record trigger, affected tasks/workers, time and evidence refs.
4. Escalate based on risk tier.
5. Require an explicit recovery decision before re-enabling capability.
6. Re-enable gradually and verify monitoring.

## Required record
Link work item/incident, actors or employee IDs, timestamps, policy/risk context, evidence pointers, actions, verification and follow-ups.

## Exit criteria
- Trigger cause is resolved or accepted with compensating controls and writes are deliberately re-enabled.
