# HOWL-006 — orgctl route proofs

**Captured:** 2026-09-21 11:22 EDT  
**Command:** `python tools/orgctl.py route …` (deterministic; `model_invoke: false`)  
**Registry:** post-auth baseline (`benchmark_status: baseline-evaluated` for claude/codex/agy/astra; astra `runtime_alias_of: codex`)

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

With baseline-evaluated profiles present, bounded prefers SELF unless expected value supports external; not a ranking.

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
  "decision": "SELF_preferred_unless_expected_value",
  "rationale": [
    "choose by measured fit not loyalty/rankings",
    "prefer least-resource-intensive sufficient executor",
    "quality over cost when failure material"
  ],
  "eligible_profiles": [
    {
      "id": "claude",
      "status": "available-if-configured",
      "benchmark_status": "baseline-evaluated",
      "eligible": true,
      "reason": "measured evidence present"
    },
    {
      "id": "codex",
      "status": "available-if-configured",
      "benchmark_status": "baseline-evaluated",
      "eligible": true,
      "reason": "measured evidence present"
    },
    {
      "id": "agy",
      "status": "available-if-configured",
      "benchmark_status": "baseline-evaluated",
      "eligible": true,
      "reason": "measured evidence present"
    },
    {
      "id": "astra",
      "status": "available-if-configured",
      "benchmark_status": "baseline-evaluated",
      "eligible": true,
      "reason": "measured evidence present"
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
          "benchmark_status": "baseline-evaluated",
          "eligible": true,
          "reason": "measured evidence present"
        },
        {
          "id": "codex",
          "status": "available-if-configured",
          "benchmark_status": "baseline-evaluated",
          "eligible": true,
          "reason": "measured evidence present"
        },
        {
          "id": "agy",
          "status": "available-if-configured",
          "benchmark_status": "baseline-evaluated",
          "eligible": true,
          "reason": "measured evidence present"
        },
        {
          "id": "astra",
          "status": "available-if-configured",
          "benchmark_status": "baseline-evaluated",
          "eligible": true,
          "reason": "measured evidence present"
        }
      ]
    },
    {
      "step": "prefer_least_resource_intensive_sufficient",
      "policy": true
    },
    {
      "step": "apply_quality_over_cost_when_failure_material",
      "policy": true
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
  "uncertainty": null,
  "external_requires_expected_value": true
}
```

### complex / R3

Complex may use measured-fit among baseline-evaluated profiles; independent verification / expected-value still apply. Not a ranking.

```json
{
  "command": "route",
  "deterministic": true,
  "model_invoke": false,
  "task_class": "complex",
  "risk_tier": "R3",
  "required_tools": [],
  "objective": null,
  "result": "selected",
  "decision": "eligible_profile_by_measured_fit",
  "rationale": [
    "choose by measured fit not loyalty/rankings",
    "prefer least-resource-intensive sufficient executor",
    "quality over cost when failure material"
  ],
  "eligible_profiles": [
    {
      "id": "claude",
      "status": "available-if-configured",
      "benchmark_status": "baseline-evaluated",
      "eligible": true,
      "reason": "measured evidence present"
    },
    {
      "id": "codex",
      "status": "available-if-configured",
      "benchmark_status": "baseline-evaluated",
      "eligible": true,
      "reason": "measured evidence present"
    },
    {
      "id": "agy",
      "status": "available-if-configured",
      "benchmark_status": "baseline-evaluated",
      "eligible": true,
      "reason": "measured evidence present"
    },
    {
      "id": "astra",
      "status": "available-if-configured",
      "benchmark_status": "baseline-evaluated",
      "eligible": true,
      "reason": "measured evidence present"
    }
  ],
  "selection_steps": [
    {
      "step": "classify_task_class_and_risk",
      "task_class": "complex",
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
          "benchmark_status": "baseline-evaluated",
          "eligible": true,
          "reason": "measured evidence present"
        },
        {
          "id": "codex",
          "status": "available-if-configured",
          "benchmark_status": "baseline-evaluated",
          "eligible": true,
          "reason": "measured evidence present"
        },
        {
          "id": "agy",
          "status": "available-if-configured",
          "benchmark_status": "baseline-evaluated",
          "eligible": true,
          "reason": "measured evidence present"
        },
        {
          "id": "astra",
          "status": "available-if-configured",
          "benchmark_status": "baseline-evaluated",
          "eligible": true,
          "reason": "measured evidence present"
        }
      ]
    },
    {
      "step": "prefer_least_resource_intensive_sufficient",
      "policy": true
    },
    {
      "step": "apply_quality_over_cost_when_failure_material",
      "policy": true
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
  "uncertainty": null,
  "external_requires_expected_value": true
}
```

### critical / R4

Critical preserves risk/assurance; measured-fit eligibility ≠ preference ranking. Independent verification required.

```json
{
  "command": "route",
  "deterministic": true,
  "model_invoke": false,
  "task_class": "critical",
  "risk_tier": "R4",
  "required_tools": [],
  "objective": null,
  "result": "selected",
  "decision": "eligible_profile_by_measured_fit",
  "rationale": [
    "choose by measured fit not loyalty/rankings",
    "prefer least-resource-intensive sufficient executor",
    "quality over cost when failure material"
  ],
  "eligible_profiles": [
    {
      "id": "claude",
      "status": "available-if-configured",
      "benchmark_status": "baseline-evaluated",
      "eligible": true,
      "reason": "measured evidence present"
    },
    {
      "id": "codex",
      "status": "available-if-configured",
      "benchmark_status": "baseline-evaluated",
      "eligible": true,
      "reason": "measured evidence present"
    },
    {
      "id": "agy",
      "status": "available-if-configured",
      "benchmark_status": "baseline-evaluated",
      "eligible": true,
      "reason": "measured evidence present"
    },
    {
      "id": "astra",
      "status": "available-if-configured",
      "benchmark_status": "baseline-evaluated",
      "eligible": true,
      "reason": "measured evidence present"
    }
  ],
  "selection_steps": [
    {
      "step": "classify_task_class_and_risk",
      "task_class": "critical",
      "risk_tier": "R4"
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
          "benchmark_status": "baseline-evaluated",
          "eligible": true,
          "reason": "measured evidence present"
        },
        {
          "id": "codex",
          "status": "available-if-configured",
          "benchmark_status": "baseline-evaluated",
          "eligible": true,
          "reason": "measured evidence present"
        },
        {
          "id": "agy",
          "status": "available-if-configured",
          "benchmark_status": "baseline-evaluated",
          "eligible": true,
          "reason": "measured evidence present"
        },
        {
          "id": "astra",
          "status": "available-if-configured",
          "benchmark_status": "baseline-evaluated",
          "eligible": true,
          "reason": "measured evidence present"
        }
      ]
    },
    {
      "step": "prefer_least_resource_intensive_sufficient",
      "policy": true
    },
    {
      "step": "apply_quality_over_cost_when_failure_material",
      "policy": true
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
  "uncertainty": null,
  "external_requires_expected_value": true
}
```

## Astra representation note

Registry entry `astra` uses `runtime_alias_of: codex` (Owner clarification 2026-09-21). Route proofs do not invent a distinct Astra binary; Astra eligibility follows Codex baseline evidence.
