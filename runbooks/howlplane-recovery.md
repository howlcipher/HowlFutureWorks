# HowlPlane recovery

Machine rules: `routing/execution-substrate.yaml`. Executor failover stays in `routing/fallback-policy.yaml` and is not an orchestration bypass.

HowlPlane failure does not bypass HowlFrame, risk ceilings, approvals, credential boundaries, task scope, evidence, independent verification, bounded retries, or production controls.

## Non-colocated Grok roles

Persistent Grok Bots are usually **not** on the Factory host. Missing `howlplane` on the Grok PATH is expected. Do **not** install a second Factory in the Grok cloud.

Interim observe/dispatch: `runbooks/howlplane-remote-observation.md`. Capability gap: HOWL-011.

## Classify before calling it a Plane defect

Record the class in HowlPlane state, a HowlBoard work item, or a Git report. A Grok conversation is not the record.

| Class | Typical response |
|---|---|
| `provider_authentication`, `quota_capacity`, `configuration` | Fix the external condition. Do not modify HowlPlane. |
| `task_specific_failure`, `executor_failure` | Bounded executor retry/failover (`max_retries_per_failure_class: 2`). Not a Plane defect. |
| `routing_defect`, `orchestration_defect`, `state_recovery_defect`, `howlplane_software_defect` | One tracked repair, after the class is confirmed. |

## Health, then the still-working entrypoint

Commands below were taken from `howlplane` 0.1.0 help. Re-check `--help` if the CLI has moved.

1. `howlplane doctor`
2. `howlplane factory doctor`
3. `howlplane factory status`
4. `howlplane agents doctor`

If Factory will not start and `howlplane work` or `howlplane orchestrate` still runs, use that governed entrypoint for the original task. Do not switch to a raw provider CLI.

Within Plane, existing recovery commands are `howlplane factory resume`, `howlplane factory retry`, and `howlplane resume`.

## When no governed entrypoint works

Checkpoint evidence (`python tools/orgctl.py checkpoint`), stop, and escalate to the Owner.

There is no raw Codex/Claude/AGY path that still enforces HowlFrame. Do not invent one during an outage.

## One repair, then stop

```text
classified Plane defect
→ one tracked work item targeting HowlPlane
→ repair through a functioning governed path (factory --target self when that path still works)
→ verify
→ resume the original work only if that is still safe
```

If that repair path also fails: checkpoint, stop, escalate. Do not open a repair of the repair mechanism.

`--target` accepts `repo`, `self`, and `ecosystem` (`howlplane factory run --help`). `self` is how Plane is an eligible repair target. `ecosystem` is for evidence-backed improvement of other Howl components, under normal prioritization, not as an automatic response to one failure.
