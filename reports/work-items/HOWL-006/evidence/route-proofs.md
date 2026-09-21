# HOWL-006 — orgctl route proofs

**Captured:** 2026-09-21 00:01 EDT  
**Command:** `python tools/orgctl.py route …` (deterministic; `model_invoke: false`)  
**Registry:** post-HOWL-006 compact facts (`benchmark_status: blocked` for all external profiles)

## SELF is real

1. `tools/orgctl.py route` returns `decision: SELF` for trivial/simple with rationale that defaults to SELF and forbids install-as-reason.
2. Route inspection never invokes a model (`deterministic: true`, `model_invoke: false`).
3. SELF denotes the **persistent-member** path (Grok Bots / orgctl / ordinary workflow), not a stub executor ID in the capability registry.
4. `python tools/orgctl.py validate` and pytest exercise the same deterministic tooling path used when SELF is selected.

orgctl present: `True`

## Captured outputs

### trivial / R0

Must select SELF; proves SELF is a real decision (deterministic, no model invoke).

```json
{
  "command": "route",
  "deterministic": true,
  "model_invoke": false,
  "task_class": "trivial",
  "risk_tier": "R0",
  "required_tools": [],
  "objective": null,
  "result": "selected",
  "decision": "SELF",
  "rationale": [
    "trivial defaults to SELF",
    "external delegation requires expected value",
    "merely having an executor installed is not a reason to invoke it"
  ],
  "selection_steps": [
    {
      "step": "classify_task_class_and_risk",
      "task_class": "trivial",
      "risk_tier": "R0"
    },
    {
      "step": "decide_self_vs_delegate",
      "decision": "SELF"
    },
    {
      "step": "record_rationale_or_evidence_insufficient"
    }
  ],
  "independent_verification": "not_required",
  "uncertainty": null
}
```
### simple / R1

Must select SELF.

```json
{
  "command": "route",
  "deterministic": true,
  "model_invoke": false,
  "task_class": "simple",
  "risk_tier": "R1",
  "required_tools": [],
  "objective": null,
  "result": "selected",
  "decision": "SELF",
  "rationale": [
    "simple defaults to SELF",
    "external delegation requires expected value",
    "merely having an executor installed is not a reason to invoke it"
  ],
  "selection_steps": [
    {
      "step": "classify_task_class_and_risk",
      "task_class": "simple",
      "risk_tier": "R1"
    },
    {
      "step": "decide_self_vs_delegate",
      "decision": "SELF"
    },
    {
      "step": "record_rationale_or_evidence_insufficient"
    }
  ],
  "independent_verification": "not_required",
  "uncertainty": null
}
```
### bounded / R2

Cold-start: SELF_or_owner_configured_known_capable; profiles uncertain/blocked — no specialist invented.

```json
{
  "command": "route",
  "deterministic": true,
  "model_invoke": false,
  "task_class": "bounded",
  "risk_tier": "R2",
  "required_tools": [],
  "objective": null,
  "result": "selected",
  "decision": "SELF_or_owner_configured_known_capable",
  "rationale": [
    "no fabricated capability scores",
    "registry profiles lack local eval evidence",
    "cold_start guidance: trivial/simple\u2192SELF; bounded may use Owner-configured path with incomplete evidence marked",
    "owner_configured_path_with_incomplete_evidence_marked"
  ],
  "eligible_profiles": [
    {
      "id": "claude",
      "status": "available-if-configured",
      "benchmark_status": "blocked",
      "eligible": "uncertain",
      "reason": "blocked"
    },
    {
      "id": "codex",
      "status": "available-if-configured",
      "benchmark_status": "blocked",
      "eligible": "uncertain",
      "reason": "blocked"
    },
    {
      "id": "agy",
      "status": "available-if-configured",
      "benchmark_status": "blocked",
      "eligible": "uncertain",
      "reason": "blocked"
    },
    {
      "id": "astra",
      "status": "available-if-configured",
      "benchmark_status": "blocked",
      "eligible": "uncertain",
      "reason": "blocked"
    }
  ],
  "selection_steps": [
    {
      "step": "classify_task_class_and_risk",
      "task_class": "bounded",
      "risk_tier": "R2"
    },
    {
      "step": "filter_hard_constraints",
      "note": "tools/risk/privilege/howlframe/quota applied by operator against task envelope"
    },
    {
      "step": "assess_measured_fit",
      "profiles": [
        {
          "id": "claude",
          "status": "available-if-configured",
          "benchmark_status": "blocked",
          "eligible": "uncertain",
          "reason": "blocked"
        },
        {
          "id": "codex",
          "status": "available-if-configured",
          "benchmark_status": "blocked",
          "eligible": "uncertain",
          "reason": "blocked"
        },
        {
          "id": "agy",
          "status": "available-if-configured",
          "benchmark_status": "blocked",
          "eligible": "uncertain",
          "reason": "blocked"
        },
        {
          "id": "astra",
          "status": "available-if-configured",
          "benchmark_status": "blocked",
          "eligible": "uncertain",
          "reason": "blocked"
        }
      ]
    },
    {
      "step": "prefer_least_resource_intensive_sufficient",
      "skipped": true,
      "reason": "evidence-insufficient"
    },
    {
      "step": "apply_quality_over_cost_when_failure_material"
    },
    {
      "step": "require_independent_verification_if_critical",
      "required": false
    },
    {
      "step": "record_rationale_or_evidence_insufficient"
    }
  ],
  "independent_verification": "not_required",
  "uncertainty": "visible: missing benchmark data; never invent scores",
  "external_requires_expected_value": true,
  "recursive_delegation_default": "off"
}
```
### complex / R2 (dry)

evidence-insufficient; no auto specialist.

```json
{
  "command": "route",
  "deterministic": true,
  "model_invoke": false,
  "task_class": "complex",
  "risk_tier": "R2",
  "required_tools": [],
  "objective": "dry-run complex",
  "result": "evidence-insufficient",
  "decision": "evidence-insufficient",
  "rationale": [
    "no fabricated capability scores",
    "registry profiles lack local eval evidence",
    "cold_start guidance: trivial/simple\u2192SELF; bounded may use Owner-configured path with incomplete evidence marked",
    "complex/critical require stronger justification + verification before external pick"
  ],
  "eligible_profiles": [
    {
      "id": "claude",
      "status": "available-if-configured",
      "benchmark_status": "blocked",
      "eligible": "uncertain",
      "reason": "blocked"
    },
    {
      "id": "codex",
      "status": "available-if-configured",
      "benchmark_status": "blocked",
      "eligible": "uncertain",
      "reason": "blocked"
    },
    {
      "id": "agy",
      "status": "available-if-configured",
      "benchmark_status": "blocked",
      "eligible": "uncertain",
      "reason": "blocked"
    },
    {
      "id": "astra",
      "status": "available-if-configured",
      "benchmark_status": "blocked",
      "eligible": "uncertain",
      "reason": "blocked"
    }
  ],
  "selection_steps": [
    {
      "step": "classify_task_class_and_risk",
      "task_class": "complex",
      "risk_tier": "R2"
    },
    {
      "step": "filter_hard_constraints",
      "note": "tools/risk/privilege/howlframe/quota applied by operator against task envelope"
    },
    {
      "step": "assess_measured_fit",
      "profiles": [
        {
          "id": "claude",
          "status": "available-if-configured",
          "benchmark_status": "blocked",
          "eligible": "uncertain",
          "reason": "blocked"
        },
        {
          "id": "codex",
          "status": "available-if-configured",
          "benchmark_status": "blocked",
          "eligible": "uncertain",
          "reason": "blocked"
        },
        {
          "id": "agy",
          "status": "available-if-configured",
          "benchmark_status": "blocked",
          "eligible": "uncertain",
          "reason": "blocked"
        },
        {
          "id": "astra",
          "status": "available-if-configured",
          "benchmark_status": "blocked",
          "eligible": "uncertain",
          "reason": "blocked"
        }
      ]
    },
    {
      "step": "prefer_least_resource_intensive_sufficient",
      "skipped": true,
      "reason": "evidence-insufficient"
    },
    {
      "step": "apply_quality_over_cost_when_failure_material"
    },
    {
      "step": "require_independent_verification_if_critical",
      "required": false
    },
    {
      "step": "record_rationale_or_evidence_insufficient"
    }
  ],
  "independent_verification": "preferred",
  "uncertainty": "visible: missing benchmark data; never invent scores",
  "external_requires_expected_value": true,
  "recursive_delegation_default": "off"
}
```
### critical / R3

evidence-insufficient; independent verification required; risk not lowered.

```json
{
  "command": "route",
  "deterministic": true,
  "model_invoke": false,
  "task_class": "critical",
  "risk_tier": "R3",
  "required_tools": [],
  "objective": null,
  "result": "evidence-insufficient",
  "decision": "evidence-insufficient",
  "rationale": [
    "no fabricated capability scores",
    "registry profiles lack local eval evidence",
    "cold_start guidance: trivial/simple\u2192SELF; bounded may use Owner-configured path with incomplete evidence marked",
    "complex/critical require stronger justification + verification before external pick"
  ],
  "eligible_profiles": [
    {
      "id": "claude",
      "status": "available-if-configured",
      "benchmark_status": "blocked",
      "eligible": "uncertain",
      "reason": "blocked"
    },
    {
      "id": "codex",
      "status": "available-if-configured",
      "benchmark_status": "blocked",
      "eligible": "uncertain",
      "reason": "blocked"
    },
    {
      "id": "agy",
      "status": "available-if-configured",
      "benchmark_status": "blocked",
      "eligible": "uncertain",
      "reason": "blocked"
    },
    {
      "id": "astra",
      "status": "available-if-configured",
      "benchmark_status": "blocked",
      "eligible": "uncertain",
      "reason": "blocked"
    }
  ],
  "selection_steps": [
    {
      "step": "classify_task_class_and_risk",
      "task_class": "critical",
      "risk_tier": "R3"
    },
    {
      "step": "filter_hard_constraints",
      "note": "tools/risk/privilege/howlframe/quota applied by operator against task envelope"
    },
    {
      "step": "assess_measured_fit",
      "profiles": [
        {
          "id": "claude",
          "status": "available-if-configured",
          "benchmark_status": "blocked",
          "eligible": "uncertain",
          "reason": "blocked"
        },
        {
          "id": "codex",
          "status": "available-if-configured",
          "benchmark_status": "blocked",
          "eligible": "uncertain",
          "reason": "blocked"
        },
        {
          "id": "agy",
          "status": "available-if-configured",
          "benchmark_status": "blocked",
          "eligible": "uncertain",
          "reason": "blocked"
        },
        {
          "id": "astra",
          "status": "available-if-configured",
          "benchmark_status": "blocked",
          "eligible": "uncertain",
          "reason": "blocked"
        }
      ]
    },
    {
      "step": "prefer_least_resource_intensive_sufficient",
      "skipped": true,
      "reason": "evidence-insufficient"
    },
    {
      "step": "apply_quality_over_cost_when_failure_material"
    },
    {
      "step": "require_independent_verification_if_critical",
      "required": true
    },
    {
      "step": "record_rationale_or_evidence_insufficient"
    }
  ],
  "independent_verification": "required",
  "uncertainty": "visible: missing benchmark data; never invent scores",
  "external_requires_expected_value": true,
  "recursive_delegation_default": "off"
}
```


## Summary table

| Task class | Risk | result | decision |
|---|---|---|---|
| trivial | R0 | selected | SELF |
| simple | R1 | selected | SELF |
| bounded | R2 | selected | SELF_or_owner_configured_known_capable |
| complex | R2 | evidence-insufficient | evidence-insufficient |
| critical | R3 | evidence-insufficient | evidence-insufficient |

Policy holds: AVAILABLE ≠ preferred; blocked/auth gaps → no fabricated specialist ranking.
