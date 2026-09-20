# Runaway Agent

## Trigger
Abnormal retries, fan-out, spend, tool calls, writes or policy denials.

## Procedure
1. Trigger the circuit breaker for new writes/spawns.
2. Checkpoint and preserve authoritative task/evidence state.
3. Revoke temporary high-risk credentials if continued execution could cause harm.
4. Identify the parent workflow and all spawned workers.
5. Stop duplicate/recursive work without deleting evidence.
6. Diagnose root cause: retry policy, task ambiguity, provider behavior, prompt/tool injection, or orchestration bug.
7. Require evidence-based approval before resuming write capability.

## Required record
Link work item/incident, actors or employee IDs, timestamps, policy/risk context, evidence pointers, actions, verification and follow-ups.

## Exit criteria
- No uncontrolled workers remain and corrective policy/test exists.
