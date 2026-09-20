# Quota Exhaustion

## Trigger
A provider/model/session quota blocks continued work.

## Procedure
1. Checkpoint authoritative state and current evidence.
2. Record quota condition; do not treat it as task failure or permission to skip gates.
3. Use approved fallback routing only if task/risk/tool requirements remain satisfied.
4. Prevent duplicate work by marking the original execution attempt paused.
5. Resume with a new executor/session using the task envelope and curated handoff, not a full transcript dump.

## Required record
Link work item/incident, actors or employee IDs, timestamps, policy/risk context, evidence pointers, actions, verification and follow-ups.

## Exit criteria
- One execution path owns the task and all gates remain intact.
