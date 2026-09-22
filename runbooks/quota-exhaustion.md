# Quota Exhaustion

## Trigger
A provider/model/session quota blocks continued work.

## Procedure
1. Checkpoint authoritative state and current evidence.
2. Record quota condition; do not treat it as task failure or permission to skip gates.
3. Classify whether the exhausted resource is **persistent Grok Bot capacity** or an **external executor** quota.
4. For persistent Grok capacity: reduce discretionary role handoffs per `routing/participation-policy.yaml`; keep mandatory Assurance/Auditor/approvals/verification. Prefer SELF or configured external executors for bounded implementation when routing permits.
5. Use approved fallback routing only if task/risk/tool requirements remain satisfied.
6. Prevent duplicate work by marking the original execution attempt paused.
7. Resume with a new executor/session using the task envelope and curated handoff, not a full transcript dump.

## Required record
Link work item/incident, actors or employee IDs, timestamps, policy/risk context, evidence pointers, actions, verification and follow-ups. Record the operator-declared capacity state (`healthy|constrained|scarce|exhausted|unknown`) without inventing usage percentages.

## Exit criteria
- One execution path owns the task and all gates remain intact.
- Capacity optimization did not override risk, approval, verification, or HowlFrame controls.
