# Hire a Bot Employee

## Trigger
A persistent position is vacant/newly required, or an approved staffing decision calls for a replacement/additional seat.

## Procedure
1. Confirm the position exists and is approved in `bots/manifest.yaml`.
2. Check `seat_limit` and current active occupants in `workforce/roster.yaml`.
3. Create a hire proposal from `templates/hire.md`.
4. Assign a new immutable employee ID for a new worker instance.
5. Identify predecessor/handoff material if this is a replacement.
6. Build the onboarding context from role + compact position knowledge + curated predecessor handoff + current authoritative work refs.
7. Confirm no secrets or predecessor credentials are copied.
8. Obtain required staffing/authority approval.
9. Add the employee record and hire event; then reconcile the live platform.
10. Verify the deployed platform reference/fingerprint and record deployment status.

## Exit criteria
The employee can perform its bounded role, authoritative state is reachable, required gates work, and a rollback/disable path exists.
