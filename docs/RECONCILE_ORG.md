# Reconcile Desired and Deployed Organization

1. Read desired position state from `bots/manifest.yaml`.
2. Read staffing state from `workforce/roster.yaml` and employee records.
3. Inventory live Bots, platform IDs, descriptions, skills, routines, recent routine evidence, and relevant permissions. Remember that hiding does not pause routines and deletion removes routines.
4. Map live Bot instances to immutable employee IDs and record non-secret `deployment_ref` values in the roster when reconciled.
5. Compare normalized position fingerprints and deployment status.
6. Categorize drift: harmless metadata, config drift, workforce drift, authority drift, missing employee/Bot, extra live Bot, stale routine, residual shared-computer access/sign-ins, or stale credentials.
7. Auto-repair only changes permitted by current policy.
8. Use hire/separation/reassignment proposals for staffing drift rather than deleting history.
9. Produce proposals for authority/risk changes.
10. Update `deployment_status`, `deployment_ref`, and `deployed_fingerprint` only after verification; record a report under `reports/audits/` with before/after fingerprints and workforce event refs.

Never delete former employee records to make deployed state look clean.
