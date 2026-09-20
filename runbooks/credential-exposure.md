# Credential Exposure

## Trigger
Credential may have been copied, logged, leaked, or used outside intended scope.

## Procedure
1. Stop actions using the affected credential.
2. Revoke/rotate it through the proper secret system without copying the value into the repo/report.
3. Determine scope, permissions, systems and time window.
4. Preserve references to evidence without storing the secret.
5. Review access/audit logs where available.
6. Assess downstream impact and rotate dependent credentials if required.
7. Add a regression/prevention control.

## Required record
Link work item/incident, actors or employee IDs, timestamps, policy/risk context, evidence pointers, actions, verification and follow-ups.

## Exit criteria
- Credential is invalidated/re-scoped, impact is understood, and no secret value was added to organizational history.
