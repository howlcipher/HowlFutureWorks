#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import argparse, json, sys, hashlib, re

ROOT=Path(__file__).resolve().parents[1]
RISKS={"R0","R1","R2","R3","R4"}
ACTIVE_WORKFORCE={"candidate","hired","active","suspended"}
TERMINAL_WORKFORCE={"terminated","retired","laid_off","replaced","provider_retired"}
SEPARATION_TYPES=TERMINAL_WORKFORCE


def load_yaml(path):
    try:
        import yaml
    except Exception:
        raise SystemExit("PyYAML required: python -m pip install -r requirements-dev.txt")
    return yaml.safe_load(path.read_text())


def dump_yaml(data,path):
    try:
        import yaml
    except Exception:
        raise SystemExit("PyYAML required: python -m pip install -r requirements-dev.txt")
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))


def load_json(path): return json.loads(path.read_text())

def validate_instance(data,schema_path,label,errors):
    try:
        import jsonschema
        schema=load_json(schema_path)
        jsonschema.Draft202012Validator.check_schema(schema)
        validator=jsonschema.Draft202012Validator(schema,format_checker=jsonschema.FormatChecker())
        validator.validate(data)
    except Exception as e:
        errors.append(f"invalid {label}: {e}")


def organization(): return load_yaml(ROOT/"organization.yaml") or {}
def manifest(): return load_yaml(ROOT/"bots/manifest.yaml") or {"bots":[]}
def workforce(): return load_yaml(ROOT/"workforce/roster.yaml") or {"employees":[]}



REQUIRED_EXECUTORS = ("claude", "codex", "agy", "astra")
TASK_CLASS_IDS = ("trivial", "simple", "bounded", "complex", "critical")
QUOTA_STATES = ("healthy", "constrained", "scarce", "exhausted", "unknown")
PARTICIPATION_ROLE_KEYS = (
    "responsible",
    "implementer",
    "product",
    "engineering_manager",
    "assurance",
    "auditor",
    "rnd",
)
# Statuses that capacity may defer (never "required").
OPTIONAL_PARTICIPATION_STATUSES = frozenset({"conditional", "likely", "optional", "as_applicable"})


def validate_routing(errors):
    """Meaningful routing policy checks (HOWL-005)."""
    reg_path = ROOT / "routing/capability-registry.yaml"
    sel_path = ROOT / "routing/selection-policy.yaml"
    tc_path = ROOT / "routing/task-classes.yaml"
    rp_path = ROOT / "routing/routing-policy.yaml"
    fb_path = ROOT / "routing/fallback-policy.yaml"
    for rel in (
        "routing/capability-registry.yaml",
        "routing/selection-policy.yaml",
        "routing/task-classes.yaml",
        "routing/routing-policy.yaml",
        "routing/fallback-policy.yaml",
        "routing/participation-policy.yaml",
        "routing/execution-substrate.yaml",
    ):
        if not (ROOT / rel).exists():
            errors.append(f"missing {rel}")
            return

    try:
        registry = load_yaml(reg_path) or {}
        selection = load_yaml(sel_path) or {}
        classes = load_yaml(tc_path) or {}
        routing = load_yaml(rp_path) or {}
        fallback = load_yaml(fb_path) or {}
        tool_access = load_yaml(ROOT / "policies/tool-access.yaml") or {}
        risk_tiers = load_yaml(ROOT / "policies/risk-tiers.yaml") or {}
    except Exception as e:
        errors.append(f"routing load: {e}")
        return

    executors = registry.get("executors") or []
    ids = [e.get("id") for e in executors if isinstance(e, dict)]
    if len(ids) != len(set(ids)):
        errors.append("routing: duplicate executor IDs in capability-registry")
    for req in REQUIRED_EXECUTORS:
        if req not in ids:
            errors.append(f"routing: capability-registry missing required executor {req}")

    class_map = classes.get("classes") or {}
    for cid in TASK_CLASS_IDS:
        if cid not in class_map:
            errors.append(f"routing: task-classes missing class {cid}")
    if classes.get("rules", {}).get("complexity_does_not_override_risk") is not True:
        errors.append("routing: complexity_does_not_override_risk must be true")
    risk_src = classes.get("rules", {}).get("risk_policy_source")
    if risk_src and not (ROOT / risk_src).exists():
        errors.append(f"routing: unknown risk_policy_source {risk_src}")
    known_risks = set((risk_tiers.get("tiers") or {}).keys()) | RISKS
    for cid, meta in class_map.items():
        if not isinstance(meta, dict):
            continue
        for key in ("allowed_risk_tiers", "risk_refs"):
            for r in meta.get(key) or []:
                if r not in known_risks:
                    errors.append(f"routing: task class {cid} references unknown risk {r}")

    for default_cls in ("trivial", "simple"):
        d = (class_map.get(default_cls) or {}).get("default_executor")
        if d != "SELF":
            errors.append(f"routing: {default_cls} must default to SELF, got {d}")

    crit = class_map.get("critical") or {}
    if crit.get("independent_verification") != "required":
        errors.append("routing: critical class must require independent verification")

    principles = selection.get("principles") or {}
    for key, expected in (
        ("self_preferred_when_sufficient", True),
        ("external_requires_expected_value", True),
        ("provider_loyalty", "forbidden"),
        ("permanent_ranking", "forbidden"),
        ("least_resource_intensive_sufficient", True),
        ("quality_over_cost_when_failure_material", True),
        ("invent_capability_scores", "forbidden"),
    ):
        if key not in principles:
            errors.append(f"routing: selection-policy principles missing {key}")
        elif principles.get(key) != expected:
            errors.append(f"routing: selection-policy principles.{key} must be {expected!r}")

    qstates = selection.get("quota_states") or []
    if set(qstates) != set(QUOTA_STATES):
        errors.append(f"routing: quota_states must be exactly {list(QUOTA_STATES)}")
    for st in qstates:
        if st not in QUOTA_STATES:
            errors.append(f"routing: invalid quota state {st}")

    rec = selection.get("recursive_delegation") or {}
    if rec.get("default") not in (False, "off"):
        errors.append("routing: recursive_delegation.default must be off")

    ver = selection.get("verification") or {}
    if ver.get("critical_requires_independent") is not True:
        errors.append("routing: critical_requires_independent must be true")
    if ver.get("builder_not_sole_verifier") is not True:
        errors.append("routing: builder_not_sole_verifier must be true")

    sec = selection.get("security") or {}
    if sec.get("howlframe_bypass") != "forbidden":
        errors.append("routing: howlframe_bypass must be forbidden")
    if sec.get("child_privilege_may_exceed_parent") is not False:
        errors.append("routing: child_privilege_may_exceed_parent must be false")
    if sec.get("secrets_in_routing_config") != "forbidden":
        errors.append("routing: secrets_in_routing_config must be forbidden")
    if sec.get("fallback_may_lower_assurance") is not False:
        errors.append("routing: fallback_may_lower_assurance must be false")

    rr = routing.get("rules") or {}
    if rr.get("provider_loyalty") != "forbidden":
        errors.append("routing: routing-policy provider_loyalty must be forbidden")
    if rr.get("permanent_ranking") not in (None, "forbidden") and rr.get("permanent_ranking") is not False:
        # allow absent only if forbidden elsewhere; prefer explicit
        if rr.get("permanent_ranking") != "forbidden":
            errors.append("routing: routing-policy permanent_ranking must be forbidden")
    if rr.get("quota_outage_may_lower_assurance") is not False:
        errors.append("routing: quota_outage_may_lower_assurance must be false")
    if rr.get("self_preferred_when_sufficient") is not True:
        errors.append("routing: routing-policy self_preferred_when_sufficient must be true")
    if rr.get("external_requires_expected_value") is not True:
        errors.append("routing: routing-policy external_requires_expected_value must be true")

    validate_participation(errors, routing=routing)

    fb = fallback.get("fallback_behavior") or {}
    if fb.get("blind_retry") != "forbidden":
        errors.append("routing: fallback blind_retry must be forbidden")
    if fb.get("multi_model_fan_out") != "not_normalized":
        errors.append("routing: fallback multi_model_fan_out must be not_normalized")
    if fb.get("preserve_assurance_and_approvals") is not True:
        errors.append("routing: fallback must preserve assurance and approvals")
    retries = fb.get("max_retries_per_failure_class")
    if retries != 2:
        errors.append(f"routing: max_retries_per_failure_class must be 2, got {retries}")

    ta = tool_access.get("rules") or {}
    if ta.get("direct_executor_cli_bypass_of_howlframe") != "forbidden":
        errors.append("routing: tool-access HowlFrame bypass must remain forbidden")
    if ta.get("child_worker_may_exceed_parent_scope") is not False:
        errors.append("routing: tool-access child_worker_may_exceed_parent_scope must be false")

    validate_execution_substrate(errors, routing=routing, selection=selection, fallback=fallback)

    # No secrets-looking keys in routing YAML values (heuristic).
    import re as _re
    secretish = _re.compile(r"(?i)(api[_-]?key|secret|password|token|begin\s+private)")
    for p in (ROOT / "routing").rglob("*.yaml"):
        raw = p.read_text()
        if secretish.search(raw):
            # allow the word in policy forbidding secrets
            if "secrets_in_routing_config" in raw and raw.count("secret") <= 3:
                continue
            if "forbidden" in raw and "secret" in raw.lower():
                continue
            errors.append(f"routing: possible secret material in {p.relative_to(ROOT)}")


# Structural execution-substrate requirements (HOWL-010). English wording is not the check.
REQUIRED_EXECUTION_DECISIONS = (
    "persistent_role_participation",
    "self_or_delegated_implementation",
    "executor_selected_by_howlplane",
)
REQUIRED_RECOVERY_CONDITIONS = (
    "howlplane_unavailable",
    "factory_will_not_start",
    "confirmed_howlplane_software_defect",
    "corrupted_unrecoverable_orchestration_state",
    "missing_required_howlplane_capability",
    "bootstrap_or_recovery_of_howlplane",
)
REQUIRED_RECOVERY_PRESERVE = (
    "howlframe",
    "risk_ceilings",
    "approvals",
    "credential_boundaries",
    "task_scope",
    "evidence",
    "independent_verification",
    "bounded_retries",
    "production_controls",
)
REQUIRED_FAILURE_CLASSES = (
    "provider_authentication",
    "quota_capacity",
    "configuration",
    "task_specific_failure",
    "executor_failure",
    "routing_defect",
    "orchestration_defect",
    "state_recovery_defect",
    "howlplane_software_defect",
)
REQUIRED_SELF_IMPROVEMENT_DENIALS = (
    "increase_authority",
    "reduce_approvals",
    "lower_risk_classification",
    "grant_production_access",
    "broaden_credentials",
    "weaken_assurance",
    "weaken_audit",
    "bypass_howlframe",
    "suppress_evidence",
    "consequential_auto_merge",
    "change_policy_without_required_review",
)
REQUIRED_PLANE_COMMANDS = (
    "howlplane factory start",
    "howlplane factory run",
    "howlplane factory run-once",
    "howlplane factory status",
    "howlplane work",
    "howlplane route",
)


def validate_execution_substrate(errors, routing=None, selection=None, fallback=None):
    """HowlPlane-first execution without treating Plane failure as a governance bypass."""
    path = ROOT / "routing/execution-substrate.yaml"
    if not path.exists():
        errors.append("missing routing/execution-substrate.yaml")
        return
    sub = load_yaml(path) or {}
    rules = sub.get("rules") or {}
    routing = routing if routing is not None else (load_yaml(ROOT / "routing/routing-policy.yaml") or {})
    selection = selection if selection is not None else (load_yaml(ROOT / "routing/selection-policy.yaml") or {})
    fallback = fallback if fallback is not None else (load_yaml(ROOT / "routing/fallback-policy.yaml") or {})

    if list(sub.get("decisions") or []) != list(REQUIRED_EXECUTION_DECISIONS):
        errors.append("execution-substrate: decisions must be participation, SELF-or-delegate, then HowlPlane executor selection")
    for key, expected in (
        ("self_preferred_when_sufficient", True),
        ("external_requires_expected_value", True),
        ("delegated_implementation_substrate", "howlplane"),
        ("raw_executor_cli", "not_normalized"),
        ("howlplane_failure_is_governance_bypass", False),
        ("executor_failure_is_plane_defect", False),
        ("unsupported_model_opinion_is_improvement_evidence", False),
    ):
        if rules.get(key) != expected:
            errors.append(f"execution-substrate: rules.{key} must be {expected!r}")

    rr = routing.get("rules") or {}
    for key, expected in (
        ("delegated_implementation_substrate", "howlplane"),
        ("raw_executor_cli", "not_normalized"),
        ("howlplane_failure_is_governance_bypass", False),
    ):
        if rr.get(key) != expected:
            errors.append(f"routing-policy: rules.{key} must be {expected!r}")
    if (routing.get("canonical") or {}).get("execution_substrate") != "routing/execution-substrate.yaml":
        errors.append("routing-policy: canonical.execution_substrate must point at routing/execution-substrate.yaml")
    principles = selection.get("principles") or {}
    if principles.get("delegated_substrate") != "howlplane":
        errors.append("selection-policy: principles.delegated_substrate must be howlplane")
    if principles.get("raw_executor_cli") != "not_normalized":
        errors.append("selection-policy: principles.raw_executor_cli must be not_normalized")
    delegation = ((load_yaml(ROOT / "policies/budgets.yaml") or {}).get("agent_runtime") or {}).get("delegation") or {}
    if delegation.get("delegated_substrate") != "howlplane":
        errors.append("budgets: agent_runtime.delegation.delegated_substrate must be howlplane")
    if delegation.get("raw_executor_cli") != "not_normalized":
        errors.append("budgets: agent_runtime.delegation.raw_executor_cli must be not_normalized")
    orch = fallback.get("orchestration_failure") or {}
    if orch.get("executor_fallback_is_orchestration_bypass") is not False:
        errors.append("fallback: executor fallback must not be an orchestration bypass")
    if orch.get("howlplane_failure_is_governance_bypass") is not False:
        errors.append("fallback: howlplane failure must not be a governance bypass")

    recovery = sub.get("recovery") or {}
    if recovery.get("applies_to") != "orchestration_layer_only":
        errors.append("execution-substrate: recovery.applies_to must be orchestration_layer_only")
    if set(recovery.get("conditions") or []) != set(REQUIRED_RECOVERY_CONDITIONS):
        errors.append("execution-substrate: recovery.conditions drifted from the required set")
    if set(recovery.get("must_preserve") or []) != set(REQUIRED_RECOVERY_PRESERVE):
        errors.append("execution-substrate: recovery.must_preserve drifted from the required set")
    if recovery.get("howlplane_failure_is_governance_bypass") is not False:
        errors.append("execution-substrate: recovery must not treat Plane failure as a governance bypass")
    if recovery.get("raw_executor_cli") != "forbidden":
        errors.append("execution-substrate: recovery raw_executor_cli must be forbidden")
    if recovery.get("when_no_governed_entrypoint_works") != "checkpoint_stop_escalate":
        errors.append("execution-substrate: recovery without a governed entrypoint must checkpoint, stop, and escalate")
    runbook = recovery.get("runbook")
    if not runbook or not (ROOT / runbook).exists():
        errors.append(f"execution-substrate: recovery runbook missing {runbook}")

    if set(sub.get("failure_classes") or []) != set(REQUIRED_FAILURE_CLASSES):
        errors.append("execution-substrate: failure_classes drifted from the required set")
    if sub.get("executor_failure_is_plane_defect") is not False:
        errors.append("execution-substrate: executor_failure_is_plane_defect must be false")

    repair = sub.get("repair") or {}
    rec = repair.get("recursion") or {}
    if "howlplane" not in (repair.get("eligible_targets") or []):
        errors.append("execution-substrate: repair.eligible_targets must include howlplane")
    if repair.get("mechanism") != "one_tracked_work_item":
        errors.append("execution-substrate: repair.mechanism must be one_tracked_work_item")
    if rec.get("max_repair_objectives_per_failure") != 1:
        errors.append("execution-substrate: repair recursion must allow only one objective per failure")
    if rec.get("unbounded_recursive_repair") != "forbidden":
        errors.append("execution-substrate: unbounded_recursive_repair must be forbidden")
    if rec.get("if_governed_repair_path_fails") != "checkpoint_stop_escalate":
        errors.append("execution-substrate: a failed repair path must checkpoint, stop, and escalate")

    improvement = sub.get("improvement") or {}
    if improvement.get("requires_evidence") is not True:
        errors.append("execution-substrate: improvement.requires_evidence must be true")
    if improvement.get("unsupported_model_opinion") != "insufficient":
        errors.append("execution-substrate: unsupported model opinion must be insufficient for improvement")
    if improvement.get("follows_normal_prioritization") is not True:
        errors.append("execution-substrate: improvement must follow normal prioritization")
    if "howlplane" not in (improvement.get("eligible_targets") or []):
        errors.append("execution-substrate: improvement.eligible_targets must include howlplane")
    loop = improvement.get("loop") or []
    for step in ("observation", "evidence", "tracked_work_item", "verification", "measure"):
        if step not in loop:
            errors.append(f"execution-substrate: improvement.loop missing {step}")

    denial = set((sub.get("self_improvement") or {}).get("may_not") or [])
    if set(REQUIRED_SELF_IMPROVEMENT_DENIALS) != denial:
        errors.append("execution-substrate: self_improvement.may_not drifted from the required set")
    if (sub.get("self_improvement") or {}).get("within_existing_authority") is not True:
        errors.append("execution-substrate: self_improvement must stay within existing authority")

    work = sub.get("work_state") or {}
    for key, expected in (
        ("git", "desired_organizational_and_product_state"),
        ("howlboard", "authoritative_work_state"),
        ("howlplane", "authoritative_execution_state"),
        ("grok_conversation", "disposable_working_context"),
    ):
        if work.get(key) != expected:
            errors.append(f"execution-substrate: work_state.{key} must be {expected}")

    interfaces = sub.get("verified_interfaces") or {}
    commands = set(interfaces.get("commands") or [])
    for cmd in REQUIRED_PLANE_COMMANDS:
        if cmd not in commands:
            errors.append(f"execution-substrate: verified_interfaces.commands missing {cmd}")
    defaults = interfaces.get("default_delegated_commands") or []
    if any(cmd.split()[0] != "howlplane" for cmd in defaults):
        errors.append("execution-substrate: default delegated commands must be howlplane entrypoints")
    if "raw_provider_cli" in defaults or interfaces.get("not_a_default_path") != "raw_provider_cli":
        errors.append("execution-substrate: raw provider CLI must not be a default delegated path")
    if "self" not in (interfaces.get("factory_target_values") or []):
        errors.append("execution-substrate: factory target values must include self")


def execution_substrate_for(task_class, decision):
    """Execution path for a routing decision. Does not select a provider CLI."""
    sub = load_yaml(ROOT / "routing/execution-substrate.yaml") or {}
    rules = sub.get("rules") or {}
    view = {
        "decisions": list(sub.get("decisions") or []),
        "raw_executor_cli": rules.get("raw_executor_cli", "not_normalized"),
        "howlplane_failure_is_governance_bypass": rules.get("howlplane_failure_is_governance_bypass", False),
    }
    if task_class in ("trivial", "simple") or decision == "SELF":
        view.update({"path": "SELF", "orchestration": "none"})
        return view
    if decision in ("SELF_preferred_unless_expected_value", "SELF_or_owner_configured_known_capable"):
        view.update({"path": "SELF_unless_delegated", "when_delegated": "HOWLPLANE", "orchestration": "howlplane"})
        return view
    view.update({
        "path": "HOWLPLANE",
        "when_delegated": "HOWLPLANE",
        "orchestration": "howlplane",
        "executor_selection": "howlplane",
    })
    return view


def _map_participation_token(token):
    """Normalize policy tokens to explainable participation statuses."""
    if token in (None,):
        return "not_required"
    if token is True or token == "required":
        return "required"
    if token in ("not_required", "not_default", "not_required_for_ordinary_steps"):
        return "not_required"
    if token in (
        "when_justified_or_required",
        "when_policy_or_security_boundary",
        "when_requirements_need_judgment",
        "when_governance_or_risk_requires",
        "when_genuine_uncertainty",
        "optional_lightweight_when_valuable",
        "as_applicable",
        "required_when_policy_requires_verification",
        "when_verification_or_security_boundary",
        "when_governance_or_consequential",
        "conditional",
    ):
        return "conditional"
    if token == "likely":
        return "likely"
    if token == "optional":
        return "optional"
    return "conditional"


def participation_inspect(task_class, risk, grok_capacity="unknown", class_meta=None, participation=None):
    """Deterministic persistent-role participation. Never invokes a model or scrapes quota."""
    if grok_capacity not in QUOTA_STATES:
        return {
            "result": "invalid-input",
            "errors": [f"unknown grok capacity state {grok_capacity}"],
            "capacity_overrode_safety": False,
        }
    participation = participation if participation is not None else (
        load_yaml(ROOT / "routing/participation-policy.yaml") or {}
    )
    classes = load_yaml(ROOT / "routing/task-classes.yaml") or {}
    class_meta = class_meta if class_meta is not None else (
        (classes.get("classes") or {}).get(task_class) or {}
    )
    defaults = (participation.get("task_defaults") or {}).get(task_class) or {}
    overlays = participation.get("risk_overlays") or {}
    capacity_cfg = participation.get("grok_capacity") or {}
    semantics = (capacity_cfg.get("semantics") or {}).get(grok_capacity, "conservative")

    roles = {}
    rationale = [
        f"task_class={task_class}",
        f"risk_tier={risk}",
        "demand-driven participation; full workflow is a capability not a ceremony",
        "mandatory governance/safety controls outrank capacity optimization",
    ]

    if task_class in ("trivial", "simple"):
        roles["responsible"] = "required"
        roles["implementer"] = "not_required"
        roles["product"] = _map_participation_token(defaults.get("product", "not_required"))
        roles["engineering_manager"] = _map_participation_token(
            defaults.get("engineering_manager", "not_required")
        )
        roles["assurance"] = _map_participation_token(defaults.get("assurance", "conditional"))
        roles["auditor"] = _map_participation_token(defaults.get("auditor", "not_required"))
        roles["rnd"] = _map_participation_token(defaults.get("rnd", "not_required"))
        rationale.append(f"{task_class}: responsible role only by default")
    elif task_class == "bounded":
        roles["responsible"] = "not_required"
        roles["implementer"] = "required"
        roles["product"] = _map_participation_token(defaults.get("product", "conditional"))
        roles["engineering_manager"] = _map_participation_token(
            defaults.get("engineering_manager", "not_required")
        )
        roles["assurance"] = _map_participation_token(defaults.get("assurance", "conditional"))
        roles["auditor"] = _map_participation_token(defaults.get("auditor", "not_required"))
        roles["rnd"] = _map_participation_token(defaults.get("rnd", "not_required"))
        rationale.append("bounded: implementer required; Assurance/Product conditional")
    elif task_class == "complex":
        roles["responsible"] = "not_required"
        roles["implementer"] = "required"
        roles["product"] = _map_participation_token(defaults.get("product", "conditional"))
        roles["engineering_manager"] = _map_participation_token(
            defaults.get("engineering_manager", "likely")
        )
        roles["assurance"] = _map_participation_token(defaults.get("assurance", "likely"))
        roles["auditor"] = _map_participation_token(defaults.get("auditor", "conditional"))
        roles["rnd"] = _map_participation_token(defaults.get("rnd", "conditional"))
        rationale.append("complex: additional participation allowed when it adds value")
    else:  # critical
        roles["responsible"] = "not_required"
        roles["implementer"] = "required"
        roles["product"] = _map_participation_token(defaults.get("product", "conditional"))
        roles["engineering_manager"] = _map_participation_token(
            defaults.get("engineering_manager", "conditional")
        )
        roles["assurance"] = "required"
        roles["auditor"] = _map_participation_token(defaults.get("auditor", "conditional"))
        roles["rnd"] = _map_participation_token(defaults.get("rnd", "conditional"))
        rationale.append("critical: follow risk policy; mandatory controls retained")

    # Risk / verification overlays (fail closed — may only raise, never lower required).
    risk_meta = overlays.get(risk) or {}
    if risk_meta.get("assurance") == "required" or risk == "R4":
        roles["assurance"] = "required"
        rationale.append(f"risk overlay {risk}: Assurance required")
    elif risk_meta.get("assurance") and roles.get("assurance") == "not_required":
        roles["assurance"] = "conditional"
        rationale.append(f"risk overlay {risk}: Assurance conditional")
    if risk in ("R3", "R4"):
        rationale.append(f"risk {risk}: human approval required per policies/approvals.yaml")
    if class_meta.get("independent_verification") == "required":
        roles["assurance"] = "required"
        rationale.append("independent_verification required → Assurance required")
    if task_class == "critical" and risk == "R4":
        if roles.get("auditor") == "not_required":
            roles["auditor"] = "conditional"
        rationale.append("critical/R4: Auditor when governance or consequential work requires it")

    # Capacity may defer optional participation only.
    deferred = []
    if grok_capacity in ("constrained", "scarce", "exhausted", "unknown"):
        for role, status in list(roles.items()):
            if status in OPTIONAL_PARTICIPATION_STATUSES:
                # Keep Assurance/Auditor conditional markers when policy already elevated them
                # to required; only defer truly optional/likely discretionary roles.
                if status == "conditional" and role in ("assurance", "auditor") and risk in ("R3", "R4"):
                    continue
                if status == "conditional" and role == "assurance" and class_meta.get(
                    "independent_verification"
                ) in ("required", "preferred") and task_class in ("complex", "critical"):
                    # preferred verification on complex stays conditional under capacity pressure
                    # unless required; do not silently drop required paths.
                    if class_meta.get("independent_verification") == "required":
                        continue
                if grok_capacity == "exhausted" or (
                    grok_capacity in ("scarce", "constrained", "unknown")
                    and status in ("likely", "optional", "as_applicable")
                ):
                    roles[role] = "deferred_optional"
                    deferred.append(role)
                elif grok_capacity in ("scarce",) and status == "conditional" and role in (
                    "product",
                    "rnd",
                    "engineering_manager",
                    "auditor",
                ):
                    # Scarce: defer discretionary ceremony roles; keep Assurance conditional.
                    if role != "assurance":
                        roles[role] = "deferred_optional"
                        deferred.append(role)
        if deferred:
            rationale.append(
                f"grok_capacity={grok_capacity} deferred optional roles: {', '.join(deferred)}"
            )
        rationale.append(f"grok_capacity semantics: {semantics}")
    else:
        rationale.append("grok_capacity=healthy: normal demand-driven participation")

    # Exhausted: note external/SELF still eligible for execution; no new discretionary Grok.
    execution_note = None
    if grok_capacity == "exhausted":
        execution_note = (
            "no new discretionary Grok Bot work; use SELF or configured external executors "
            "where routing policy permits; mandatory persistent roles still apply"
        )
        rationale.append(execution_note)

    return {
        "result": "selected",
        "persistent_participation": roles,
        "grok_capacity": grok_capacity,
        "grok_capacity_semantics": semantics,
        "deferred_optional_roles": deferred,
        "capacity_overrode_safety": False,
        "capacity_affects": "optional_participation_only",
        "execution_capacity_note": execution_note,
        "rationale": rationale,
        "implementer_default": defaults.get("implementer", "dev-lead" if task_class not in ("trivial", "simple") else "responsible"),
    }


def route_inspect(task_class, risk, required_tools=None, objective=None, grok_capacity="unknown"):
    """Deterministic routing inspection. Never invokes a model."""
    required_tools = required_tools or []
    out = {
        "command": "route",
        "deterministic": True,
        "model_invoke": False,
        "task_class": task_class,
        "risk_tier": risk,
        "required_tools": required_tools,
        "objective": objective,
        "grok_capacity": grok_capacity,
    }
    if task_class not in TASK_CLASS_IDS:
        out["result"] = "invalid-input"
        out["errors"] = [f"unknown task class {task_class}"]
        return out
    if risk not in RISKS:
        out["result"] = "invalid-input"
        out["errors"] = [f"unknown risk tier {risk}"]
        return out
    if grok_capacity not in QUOTA_STATES:
        out["result"] = "invalid-input"
        out["errors"] = [f"unknown grok capacity state {grok_capacity}"]
        return out

    classes = load_yaml(ROOT / "routing/task-classes.yaml") or {}
    selection = load_yaml(ROOT / "routing/selection-policy.yaml") or {}
    registry = load_yaml(ROOT / "routing/capability-registry.yaml") or {}
    participation_pol = load_yaml(ROOT / "routing/participation-policy.yaml") or {}
    class_meta = (classes.get("classes") or {}).get(task_class) or {}
    principles = selection.get("principles") or {}

    part = participation_inspect(
        task_class, risk, grok_capacity=grok_capacity,
        class_meta=class_meta, participation=participation_pol,
    )
    out["persistent_participation"] = part.get("persistent_participation")
    out["participation_rationale"] = part.get("rationale")
    out["capacity_overrode_safety"] = False
    out["deferred_optional_roles"] = part.get("deferred_optional_roles") or []
    out["grok_capacity_semantics"] = part.get("grok_capacity_semantics")
    if part.get("execution_capacity_note"):
        out["execution_capacity_note"] = part["execution_capacity_note"]

    steps = []
    steps.append({"step": "classify_task_class_and_risk", "task_class": task_class, "risk_tier": risk})
    steps.append({
        "step": "select_persistent_participation",
        "demand_driven": True,
        "capacity_overrode_safety": False,
        "roles": part.get("persistent_participation"),
    })

    default = class_meta.get("default_executor", "SELF")
    self_preferred = principles.get("self_preferred_when_sufficient") is True
    external_requires_ev = principles.get("external_requires_expected_value") is True

    if task_class in ("trivial", "simple") and self_preferred:
        decision = "SELF"
        rationale = [
            f"{task_class} defaults to SELF",
            "external delegation requires expected value",
            "merely having an executor installed is not a reason to invoke it",
        ]
        if grok_capacity == "exhausted":
            rationale.append("grok exhausted: SELF remains eligible; no discretionary Grok handoffs")
        steps.append({"step": "decide_self_vs_delegate", "decision": decision})
        out.update({
            "result": "selected",
            "decision": decision,
            "rationale": rationale,
            "selection_steps": steps + [{"step": "record_rationale_or_evidence_insufficient"}],
            "independent_verification": class_meta.get("independent_verification", "not_required"),
            "uncertainty": None,
        })
        return _finish_route(out, task_class)

    # Hard constraints / eligibility from registry
    eligible = []
    uncertainty = []
    for ex in registry.get("executors") or []:
        eid = ex.get("id")
        status = ex.get("status")
        bench = ex.get("benchmark_status")
        entry = {"id": eid, "status": status, "benchmark_status": bench}
        if status not in ("available-if-configured", "available"):
            entry["eligible"] = False
            entry["reason"] = f"status={status}"
        elif bench in (
            None,
            "needs-local-eval",
            "unknown",
            "blocked",
            "partially-evaluated",
            "stale",
        ):
            entry["eligible"] = "uncertain"
            entry["reason"] = "evidence-insufficient" if bench != "blocked" else "blocked"
            uncertainty.append(eid)
        elif bench in ("evaluated", "baseline-evaluated"):
            entry["eligible"] = True
            entry["reason"] = "measured evidence present"
        else:
            entry["eligible"] = "uncertain"
            entry["reason"] = f"unrecognized benchmark_status={bench}"
            uncertainty.append(eid)
        eligible.append(entry)
    steps.append({"step": "filter_hard_constraints", "note": "tools/risk/privilege/howlframe/quota applied by operator against task envelope"})
    steps.append({"step": "assess_measured_fit", "profiles": eligible})

    if uncertainty and not any(e.get("eligible") is True for e in eligible):
        decision = "SELF" if task_class in ("trivial", "simple", "bounded") else "evidence-insufficient"
        cold = (selection.get("cold_start") or {})
        rationale = [
            "no fabricated capability scores",
            "registry profiles lack local eval evidence",
            f"cold_start guidance: trivial/simple→SELF; bounded may use Owner-configured path with incomplete evidence marked",
        ]
        if task_class in ("complex", "critical"):
            rationale.append("complex/critical require stronger justification + verification before external pick")
            decision = "evidence-insufficient"
        elif task_class == "bounded":
            decision = "SELF_or_owner_configured_known_capable"
            rationale.append(str(cold.get("bounded")))
        if grok_capacity == "exhausted":
            rationale.append("grok exhausted: prefer SELF or configured external path; mandatory controls unchanged")
        steps.append({"step": "prefer_least_resource_intensive_sufficient", "skipped": True, "reason": "evidence-insufficient"})
        out.update({
            "result": "evidence-insufficient" if decision == "evidence-insufficient" else "selected",
            "decision": decision,
            "rationale": rationale,
            "eligible_profiles": eligible,
            "selection_steps": steps + [
                {"step": "apply_quality_over_cost_when_failure_material"},
                {"step": "require_independent_verification_if_critical",
                 "required": class_meta.get("independent_verification") == "required"},
                {"step": "record_rationale_or_evidence_insufficient"},
            ],
            "independent_verification": class_meta.get("independent_verification", "not_required"),
            "uncertainty": "visible: missing benchmark data; never invent scores",
            "external_requires_expected_value": external_requires_ev,
            "recursive_delegation_default": (selection.get("recursive_delegation") or {}).get("default"),
        })
        return _finish_route(out, task_class)

    # Measured evidence present for at least one profile — still prefer least resource / SELF when sufficient
    if self_preferred and task_class in ("bounded",):
        decision = "SELF_preferred_unless_expected_value"
    else:
        decision = "eligible_profile_by_measured_fit"
    if grok_capacity in ("scarce", "exhausted") and task_class == "bounded":
        decision = "SELF_preferred_unless_expected_value"
    steps.append({"step": "prefer_least_resource_intensive_sufficient", "policy": True})
    steps.append({"step": "apply_quality_over_cost_when_failure_material", "policy": True})
    steps.append({
        "step": "require_independent_verification_if_critical",
        "required": class_meta.get("independent_verification") == "required"
        or (selection.get("verification") or {}).get("critical_requires_independent") is True
        and task_class == "critical",
    })
    rationale = [
        "choose by measured fit not loyalty/rankings",
        "prefer least-resource-intensive sufficient executor",
        "quality over cost when failure material",
    ]
    if grok_capacity == "exhausted":
        rationale.append("grok exhausted: SELF/external executors eligible; discretionary persistent Grok deferred")
    out.update({
        "result": "selected",
        "decision": decision,
        "rationale": rationale,
        "eligible_profiles": eligible,
        "selection_steps": steps + [{"step": "record_rationale_or_evidence_insufficient"}],
        "independent_verification": class_meta.get("independent_verification", "not_required"),
        "uncertainty": None,
        "external_requires_expected_value": external_requires_ev,
    })
    return _finish_route(out, task_class)


def _finish_route(out, task_class):
    """Attach the execution substrate. Provider choice stays inside HowlPlane when delegated."""
    view = execution_substrate_for(task_class, out.get("decision"))
    out["execution_substrate"] = view
    if view.get("path") != "SELF":
        steps = list(out.get("selection_steps") or [])
        dispatch = {
            "step": "dispatch_delegated_work_through_howlplane",
            "substrate": view.get("when_delegated", "HOWLPLANE"),
        }
        if not any(isinstance(s, dict) and s.get("step") == dispatch["step"] for s in steps):
            if steps and isinstance(steps[-1], dict) and steps[-1].get("step") == "record_rationale_or_evidence_insufficient":
                steps.insert(-1, dispatch)
            else:
                steps.append(dispatch)
            out["selection_steps"] = steps
    return out


def validate_participation(errors, routing=None):
    """Demand-driven participation policy invariants."""
    pp_path = ROOT / "routing/participation-policy.yaml"
    if not pp_path.exists():
        errors.append("missing routing/participation-policy.yaml")
        return
    try:
        part = load_yaml(pp_path) or {}
        routing = routing if routing is not None else (load_yaml(ROOT / "routing/routing-policy.yaml") or {})
    except Exception as e:
        errors.append(f"participation load: {e}")
        return

    principles = part.get("principles") or {}
    if principles.get("demand_driven") is not True:
        errors.append("participation: principles.demand_driven must be true")
    if principles.get("full_workflow_mandatory_by_default") is not False:
        errors.append("participation: full_workflow_mandatory_by_default must be false")
    if principles.get("capacity_may_lower_assurance") is not False:
        errors.append("participation: capacity_may_lower_assurance must be false")
    if principles.get("capacity_may_bypass_approvals") is not False:
        errors.append("participation: capacity_may_bypass_approvals must be false")
    if principles.get("capacity_may_downgrade_risk") is not False:
        errors.append("participation: capacity_may_downgrade_risk must be false")
    if principles.get("capacity_may_authorize_unauthorized_executor") is not False:
        errors.append("participation: capacity_may_authorize_unauthorized_executor must be false")
    prec = principles.get("precedence")
    if prec != "mandatory_governance_and_safety_over_capacity_optimization":
        errors.append(
            "participation: precedence must be mandatory_governance_and_safety_over_capacity_optimization"
        )

    gc = part.get("grok_capacity") or {}
    states = gc.get("states") or []
    if set(states) != set(QUOTA_STATES):
        errors.append(f"participation: grok_capacity.states must be exactly {list(QUOTA_STATES)}")
    if gc.get("affects") != "optional_participation_only":
        errors.append("participation: grok_capacity.affects must be optional_participation_only")
    never = set(gc.get("never_overrides") or [])
    for req in (
        "risk_approval",
        "owner_approval",
        "independent_verification",
        "security_review",
        "howlframe_enforcement",
    ):
        if req not in never:
            errors.append(f"participation: grok_capacity.never_overrides missing {req}")

    defaults = part.get("task_defaults") or {}
    for cid in TASK_CLASS_IDS:
        if cid not in defaults:
            errors.append(f"participation: task_defaults missing {cid}")
    crit = defaults.get("critical") or {}
    if crit.get("follow_risk_policy") is not True:
        errors.append("participation: critical.follow_risk_policy must be true")
    if crit.get("capacity_cannot_suppress_mandatory_controls") is not True:
        errors.append("participation: critical.capacity_cannot_suppress_mandatory_controls must be true")

    global_m = part.get("globally_mandatory") or {}
    for role in ("product", "auditor", "rnd", "full_workflow"):
        if global_m.get(role) is not False:
            errors.append(f"participation: globally_mandatory.{role} must be false")

    rr = routing.get("rules") or {}
    if rr.get("demand_driven_persistent_participation") is not True:
        errors.append("routing: demand_driven_persistent_participation must be true")
    if rr.get("full_workflow_mandatory_by_default") is not False:
        errors.append("routing: full_workflow_mandatory_by_default must be false")
    if rr.get("capacity_may_lower_assurance") is not False:
        errors.append("routing: capacity_may_lower_assurance must be false")

    canon = routing.get("canonical") or {}
    if canon.get("participation") != "routing/participation-policy.yaml":
        errors.append("routing: canonical.participation must reference routing/participation-policy.yaml")


def validate():
    errors=[]
    required=[
        "organization.yaml","CHARTER.md","AGENTS.md","ORG.md","bots/manifest.yaml","workforce/roster.yaml",
        "policies/risk-tiers.yaml","policies/approvals.yaml","docs/WORKFORCE_LIFECYCLE.md"
    ]
    for rel in required:
        if not (ROOT/rel).exists(): errors.append(f"missing {rel}")

    # Canonical organization identity.
    try:
        org=organization()
        validate_instance(org,ROOT/"schemas/organization.schema.json","organization.yaml",errors)
        project=__import__("tomllib").loads((ROOT/"pyproject.toml").read_text())["project"]
        if org.get("repository_slug") != project.get("name"):
            errors.append(f"organization repository_slug drift: {org.get('repository_slug')} != {project.get('name')}")
    except Exception as e: errors.append(f"organization: {e}")

    # Durable knowledge / numeric budget policy.
    ka={}
    try:
        mem=load_yaml(ROOT/"policies/memory.yaml") or {}
        if mem.get("rules",{}).get("secrets_in_memory")!="forbidden":
            errors.append("policies/memory.yaml rules.secrets_in_memory must be forbidden")
        bud=load_yaml(ROOT/"policies/budgets.yaml") or {}
        pct=bud.get("defaults",{}).get("context_checkpoint_threshold_percent")
        if not isinstance(pct,int) or not (50<=pct<=90):
            errors.append(f"policies/budgets.yaml defaults.context_checkpoint_threshold_percent must be an integer 50-90, got {pct}")
        ka=bud.get("knowledge_artifacts",{}) or {}
        for key in ("checkpoint_chars","handoff_chars","position_knowledge_file_chars"):
            v=ka.get(key)
            if not isinstance(v,int) or v<=0:
                errors.append(f"policies/budgets.yaml knowledge_artifacts.{key} must be a positive integer")
        if isinstance(ka.get("checkpoint_chars"),int) and isinstance(ka.get("handoff_chars"),int) and ka["checkpoint_chars"]>ka["handoff_chars"]:
            errors.append("policies/budgets.yaml knowledge_artifacts.checkpoint_chars should not exceed handoff_chars")
        if isinstance(ka.get("handoff_chars"),int) and isinstance(ka.get("position_knowledge_file_chars"),int) and ka["handoff_chars"]>ka["position_knowledge_file_chars"]:
            errors.append("policies/budgets.yaml knowledge_artifacts.handoff_chars should not exceed position_knowledge_file_chars")
    except Exception as ex: errors.append(f"memory/budget policy: {ex}")

    # Position/Bot definition validation.
    positions={}
    try:
        m=manifest(); ids=[]
        validate_instance(m,ROOT/"schemas/position-manifest.schema.json","bots/manifest.yaml",errors)
        for bot in m.get("bots",[]):
            bid=bot.get("id"); ids.append(bid); positions[bid]=bot
            if bot.get("risk_ceiling") not in RISKS: errors.append(f"invalid risk ceiling for position {bid}")
            if not isinstance(bot.get("seat_limit",1),int) or bot.get("seat_limit",1)<1: errors.append(f"invalid seat_limit for {bid}")
            if bot.get("staffing_authority") not in {"owner","engineering-manager"}: errors.append(f"invalid staffing_authority for {bid}")
            for rel in [f"bots/{bid}/instructions.md",f"bots/{bid}/context.yaml",f"bots/{bid}/boundaries.yaml"]:
                if not (ROOT/rel).exists(): errors.append(f"missing {rel}")
            kp=ROOT/f"knowledge/positions/{bid}.md"
            pkf_limit=ka.get("position_knowledge_file_chars")
            if kp.exists() and isinstance(pkf_limit,int):
                size=len(kp.read_text())
                if size>pkf_limit:
                    errors.append(f"knowledge/positions/{bid}.md exceeds position_knowledge_file_chars: {size}>{pkf_limit}")
            bp=ROOT/f"bots/{bid}/boundaries.yaml"
            if bp.exists():
                bounds=load_yaml(bp) or {}
                if bounds.get("risk_ceiling")!=bot.get("risk_ceiling"): errors.append(f"risk ceiling drift for {bid}")
                if bounds.get("self_authority_change")!="forbidden": errors.append(f"self authority change must be forbidden for {bid}")
        if len(ids)!=len(set(ids)): errors.append("duplicate position/bot ids")
    except Exception as e: errors.append(f"manifest: {e}")

    # Runtime Context v2: compiled standing contracts and retrieval triggers.
    try:
        validate_runtime_contracts(errors)
    except Exception as e:
        errors.append(f"runtime contract validation: {e}")

    # Workforce current state and durable records.
    emps=[]; eids=[]; profiles={}
    try:
        wf=workforce()
        validate_instance(wf,ROOT/"schemas/workforce-roster.schema.json","workforce/roster.yaml",errors)
        emps=wf.get("employees",[]); eids=[e.get("employee_id") for e in emps]
        if len(eids)!=len(set(eids)): errors.append("duplicate employee ids")
        eidset=set(eids); by_id={e.get("employee_id"):e for e in emps}; occupied={}; generations=set()
        profiles={}
        for e in emps:
            eid=e.get("employee_id"); pos=e.get("position_id"); status=e.get("status")
            if pos not in positions: errors.append(f"{eid} references unknown position {pos}")
            elif e.get("logical_role")!=positions[pos].get("role"):
                errors.append(f"{eid} logical_role drift: {e.get('logical_role')} != {positions[pos].get('role')}")
            if status not in ACTIVE_WORKFORCE|TERMINAL_WORKFORCE: errors.append(f"{eid} invalid workforce status {status}")
            key=(pos,e.get("generation"))
            if key in generations: errors.append(f"duplicate generation for position {pos}: {e.get('generation')}")
            generations.add(key)
            rec=ROOT/e.get("record_path","")
            if not rec.exists(): errors.append(f"{eid} missing record_path {e.get('record_path')}")
            else:
                try:
                    profile=load_yaml(rec) or {}; profiles[eid]=profile
                    validate_instance(profile,ROOT/"schemas/employee-profile.schema.json",e.get('record_path'),errors)
                    if profile.get("employee_id")!=eid: errors.append(f"{eid} profile employee_id mismatch")
                    if profile.get("initial_position_id") not in positions: errors.append(f"{eid} profile references unknown initial position {profile.get('initial_position_id')}")
                    if profile.get("hired_on")!=e.get("hired_on"): errors.append(f"{eid} profile/roster hired_on mismatch")
                    if profile.get("generation")!=e.get("generation"): errors.append(f"{eid} profile/roster generation mismatch")
                    if profile.get("worker_type")!=e.get("worker_type"): errors.append(f"{eid} profile/roster worker_type mismatch")
                    if profile.get("provider_kind")!=e.get("provider_kind"): errors.append(f"{eid} profile/roster provider_kind mismatch")
                except Exception as ex: errors.append(f"{eid} invalid profile: {ex}")
            mgr=e.get("manager_ref")
            if mgr!="owner" and mgr not in eidset: errors.append(f"{eid} unknown manager_ref {mgr}")
            if status in {"hired","active","suspended"}:
                if pos in positions and positions[pos].get("status")!="active": errors.append(f"{eid} occupies non-active position {pos}")
                if mgr!="owner" and by_id.get(mgr,{}).get("status") not in {"hired","active","suspended"}: errors.append(f"{eid} has inactive manager {mgr}")
                occupied[pos]=occupied.get(pos,0)+1
            if status in TERMINAL_WORKFORCE and e.get("deployment_status")=="deployed": errors.append(f"{eid} is departed but deployment_status is deployed")
        for pos,count in occupied.items():
            limit=positions.get(pos,{}).get("seat_limit",1)
            if count>limit: errors.append(f"position {pos} over seat limit: {count}>{limit}")
        # Manager graph for current staff must terminate at owner, never cycle.
        for e in emps:
            if e.get("status") not in {"hired","active","suspended"}: continue
            seen=set(); cur=e
            while cur.get("manager_ref")!="owner":
                mgr=cur.get("manager_ref")
                if mgr in seen or mgr==e.get("employee_id"):
                    errors.append(f"manager cycle detected for {e.get('employee_id')}"); break
                seen.add(mgr); cur=by_id.get(mgr,{})
                if not cur: break
        # Predecessors are immutable historical links within the same position and lower generation.
        for eid,profile in profiles.items():
            pred=profile.get("predecessor_employee_id")
            if not pred: continue
            if pred not in by_id: errors.append(f"{eid} predecessor does not exist: {pred}"); continue
            if by_id[pred].get("position_id")!=by_id[eid].get("position_id"): errors.append(f"{eid} predecessor {pred} held a different position")
            if by_id[pred].get("generation",0)>=by_id[eid].get("generation",0): errors.append(f"{eid} predecessor generation must be lower")
    except Exception as e: errors.append(f"workforce: {e}")

    # Historical workforce/event/context/contribution records.
    event_types_by_employee={}
    for p in (ROOT/"workforce/events").glob("*.yaml"):
        try:
            data=load_yaml(p) or {}
            validate_instance(data,ROOT/"schemas/employment-event.schema.json",str(p.relative_to(ROOT)),errors)
            eid=data.get("employee_id"); event_types_by_employee.setdefault(eid,set()).add(data.get("event_type"))
            if eid not in set(eids): errors.append(f"{p.relative_to(ROOT)} references unknown employee {eid}")
            succ=data.get("successor_employee_id")
            if succ and succ not in set(eids): errors.append(f"{p.relative_to(ROOT)} references unknown successor {succ}")
        except Exception as e: errors.append(f"invalid yaml {p.relative_to(ROOT)}: {e}")
    for e in emps:
        eid=e.get("employee_id"); ev=event_types_by_employee.get(eid,set())
        if not ({"hired","rehired"} & ev): errors.append(f"{eid} has no hire/rehire lifecycle event")
        if e.get("status") in TERMINAL_WORKFORCE and e.get("status") not in ev:
            errors.append(f"{eid} terminal roster status lacks matching lifecycle event {e.get('status')}")
        prof=profiles.get(eid,{})
        if prof.get("initial_position_id") and prof.get("initial_position_id")!=e.get("position_id") and "reassigned" not in ev:
            errors.append(f"{eid} current position differs from initial position without reassigned lifecycle event")
    for p in (ROOT/"workforce/contributions").glob("*.yaml"):
        try:
            data=load_yaml(p) or {}
            validate_instance(data,ROOT/"schemas/contribution.schema.json",str(p.relative_to(ROOT)),errors)
            if data.get("employee_id") not in set(eids): errors.append(f"{p.relative_to(ROOT)} references unknown employee {data.get('employee_id')}")
        except Exception as e: errors.append(f"invalid yaml {p.relative_to(ROOT)}: {e}")
    for p in (ROOT/"workforce/people").glob("*/context/*.yaml"):
        try:
            data=load_yaml(p) or {}
            validate_instance(data,ROOT/"schemas/context-snapshot.schema.json",str(p.relative_to(ROOT)),errors)
            if data.get("employee_id") not in set(eids): errors.append(f"{p.relative_to(ROOT)} references unknown employee {data.get('employee_id')}")
            target=data.get("handoff_to")
            if target and target!="owner" and target not in set(eids): errors.append(f"{p.relative_to(ROOT)} references unknown handoff target {target}")
            limit=ka.get("checkpoint_chars")
            if isinstance(limit,int):
                size=len(p.read_text())
                if size>limit: errors.append(f"{p.relative_to(ROOT)} exceeds checkpoint_chars budget: {size}>{limit}")
        except Exception as e: errors.append(f"invalid yaml {p.relative_to(ROOT)}: {e}")

    for p in (ROOT/"workforce/people").glob("*/handoffs/*"):
        if p.name==".gitkeep" or not p.is_file(): continue
        try:
            size=len(p.read_text())
            limit=ka.get("handoff_chars")
            if isinstance(limit,int) and size>limit:
                errors.append(f"{p.relative_to(ROOT)} exceeds handoff_chars budget: {size}>{limit}")
        except Exception as ex: errors.append(f"invalid handoff {p.relative_to(ROOT)}: {ex}")

    for folder in ["policies","routing"]:
        for p in (ROOT/folder).glob("*.yaml"):
            try: load_yaml(p)
            except Exception as e: errors.append(f"invalid yaml {p.relative_to(ROOT)}: {e}")
    for p in (ROOT/"schemas").glob("*.json"):
        try: load_json(p)
        except Exception as e: errors.append(f"invalid json {p.relative_to(ROOT)}: {e}")

    # All JSON Schema files must have examples and examples must validate.
    for p in (ROOT/"schemas").glob("*.schema.json"):
        stem=p.name.replace('.schema.json','')
        ex=ROOT/"schemas/examples"/f"{stem}.json"
        if not ex.exists(): errors.append(f"missing schema example for {stem}")
        else: validate_instance(load_json(ex),p,f"schema example {stem}",errors)

    # Executor routing policy (HOWL-005).
    try:
        validate_routing(errors)
    except Exception as e:
        errors.append(f"routing validation: {e}")

    if errors:
        print("VALIDATION FAILED")
        for e in errors: print("-",e)
        return 1
    print("VALIDATION PASSED")
    return 0


def list_bots():
    print("POSITION               RISK STATUS     SEATS NAME")
    for b in manifest().get("bots",[]):
        print(f"{b['id']:<22} {b.get('risk_ceiling','?'):<4} {b.get('status','?'):<10} {b.get('seat_limit',1):<5} {b.get('name','')}")


def list_workforce(include_departed=True):
    print("EMPLOYEE ID             STATUS          POSITION               NAME")
    for e in workforce().get("employees",[]):
        if not include_departed and e.get("status") in TERMINAL_WORKFORCE: continue
        print(f"{e['employee_id']:<23} {e.get('status','?'):<15} {e.get('position_id','?'):<22} {e.get('display_name','')}")


# Runtime Context v2 (policies/runtime-contract.yaml, docs/CONTEXT_STRATEGY.md).
# Standing context is a compiled contract; detailed sources are retrieved per trigger.
RUNTIME_POLICY="policies/runtime-contract.yaml"
REQUIRED_RUNTIME_INVARIANTS=(
    "owner_final_authority","no_self_escalation","fail_closed_approvals","exact_approval_binding",
    "untrusted_external_content","independent_verification","evidence_required","no_secrets",
    "memory_non_authoritative","reversible_scoped_actions","refresh_before_consequential","retrieve_on_trigger",
)
# Minimum authoritative sources a trigger must always retrieve (cannot be removed by policy edits).
REQUIRED_TRIGGER_SOURCES={
    "authority_question":("CHARTER.md","policies/approvals.yaml"),
    "risk_classification":("policies/risk-tiers.yaml",),
    "knowledge_checkpoint":("policies/memory.yaml","policies/budgets.yaml"),
    "evidence_verification":("policies/evidence.yaml",),
}
LEGACY_CONTEXT_KEYS=("always_load","load_on_demand","budget_chars")
# Boundary flags already stated by a rendered invariant; still validated structurally.
BOUNDARIES_COVERED_BY_INVARIANTS={
    "self_authority_change":"no_self_escalation",
    "fail_closed_on_missing_required_approval":"fail_closed_approvals",
    "secrets_in_prompt":"no_secrets",
}


def _md_sections(text):
    """Split Markdown into [(h2 heading, body)] preserving order."""
    out=[]; head=None; buf=[]
    for line in text.splitlines():
        if line.startswith("## "):
            if head is not None: out.append((head,"\n".join(buf).strip()))
            head=line[3:].strip(); buf=[]
        elif head is not None:
            buf.append(line)
    if head is not None: out.append((head,"\n".join(buf).strip()))
    return out


def _flag_text(key):
    return key.removeprefix("can_").replace("_"," ")


def compile_runtime_contract(bot, base=None):
    """Pure, deterministic compilation of a position's standing runtime contract.

    Reads position definition + shared runtime policy only. Never reads employee
    continuity material (workforce/people/); that is render-employee's job.
    """
    base=base or ROOT/f"bots/{bot}"
    if not base.exists(): raise SystemExit(f"unknown position {bot}")
    ctx=load_yaml(base/"context.yaml") or {}
    policy=load_yaml(ROOT/RUNTIME_POLICY) or {}
    runtime=(load_yaml(ROOT/"policies/budgets.yaml") or {}).get("agent_runtime") or {}
    org=organization()
    pos=next((b for b in manifest().get("bots",[]) if b.get("id")==bot),{})
    bounds=load_yaml(base/"boundaries.yaml") or {}
    caps=load_yaml(base/"capabilities.yaml") or {}
    ip=base/"instructions.md"
    role_rules=[(h,b) for h,b in _md_sections(ip.read_text() if ip.exists() else "") if h.lower()!="invariants" and b]
    lessons=""
    kp=ROOT/str(ctx.get("position_knowledge",""))
    if ctx.get("position_knowledge") and kp.is_file():
        lessons=next((b for h,b in _md_sections(kp.read_text()) if h.lower()=="durable lessons"),"")
    profile_id=ctx.get("execution_profile")
    ptriggers=policy.get("triggers") or {}
    triggers=[]
    for name,extras in (ctx.get("retrieve_when") or {}).items():
        meta=ptriggers.get(name) or {}
        sources=[]
        for src in list(meta.get("required_sources") or [])+list(extras or []):
            if src not in sources: sources.append(src)
        triggers.append({"name":name,"description":meta.get("description",""),"sources":sources})
    return {
        "organization":{"display_name":org.get("display_name"),"purpose":org.get("purpose"),"provider_neutral":bool(policy.get("provider_neutral"))},
        "position":{"id":bot,"name":pos.get("name",bot),"role":pos.get("role"),"risk_ceiling":bounds.get("risk_ceiling")},
        "execution_profile_id":profile_id,
        "execution_profile":(policy.get("execution_profiles") or {}).get(profile_id) or {},
        "canonical_state":list(policy.get("canonical_state") or []),
        "invariants":list(policy.get("invariants") or []),
        "boundaries":{k:v for k,v in bounds.items() if k not in ("bot_id","risk_ceiling")},
        "capabilities":{k:v for k,v in caps.items() if k!="bot_id"},
        "role_rules":role_rules,
        "runtime_limits":runtime,
        "task_lifecycle":policy.get("task_lifecycle") or {},
        "communication":policy.get("communication") or {},
        "triggers":triggers,
        "position_lessons":lessons,
        "position_knowledge":ctx.get("position_knowledge"),
        "continuity":policy.get("continuity") or {},
        "standing_budget_chars":ctx.get("standing_budget_chars"),
    }


def format_runtime_contract(c):
    """Deterministic Markdown projection of a compiled contract (no timestamps)."""
    p=c["position"]; o=c["organization"]; prof=c["execution_profile"]; rl=c["runtime_limits"]
    L=[f"# {o['display_name']} Runtime Contract: {p['name']}",""]
    role="" if p["role"]==p["id"] else f" (role `{p['role']}`)"
    L.append(f"Position `{p['id']}`{role}. Risk ceiling: {p['risk_ceiling']}. Profile: {c['execution_profile_id']}.")
    L.append("Compiled, provider-neutral; the Git sources below are authoritative.")
    L+=["","## Canonical state"]+[f"- {s}" for s in c["canonical_state"]]
    L+=["","## Invariants"]+[f"- {i['text']}" for i in c["invariants"]]
    b=c["boundaries"]; caps=c["capabilities"]
    L+=["","## Authority"]
    extra={k:v for k,v in b.items() if k not in BOUNDARIES_COVERED_BY_INVARIANTS}
    if extra: L.append("- Boundaries: "+"; ".join(f"{k.replace('_',' ')}={'yes' if v is True else 'no' if v is False else v}" for k,v in extra.items())+".")
    may=[_flag_text(k) for k,v in caps.items() if v is True]
    maynot=[_flag_text(k) for k,v in caps.items() if v is False]
    if may: L.append("- May: "+", ".join(may)+".")
    if maynot: L.append("- May not: "+", ".join(maynot)+".")
    L.append("- Above risk ceiling or approval needed: stop, request approval, fail closed.")
    L+=["","## Role"]
    for h,body in c["role_rules"]:
        L.append(f"- {h}: "+" ".join(body.split()))
    L+=["",f"## Execution ({c['execution_profile_id']})",prof.get("summary","")]
    L+=[f"{n}. {s}" for n,s in enumerate(prof.get("steps") or [],1)]
    if prof.get("direct_work"): L.append(f"Direct work: {prof['direct_work']}")
    dele=rl.get("delegation") or {}
    # The long prefer-list is coordinator standing context only. Implementers retrieve it
    # (budgets.yaml / execution-substrate.yaml) so Dev Lead stays inside the efficiency target.
    if c["execution_profile_id"] == "coordinator" and dele.get("prefer_external_executor_for"):
        L.append(f"Prefer delegation ({dele.get('decide_by','expected_value').replace('_',' ')}) for: "+", ".join(x.replace('_',' ') for x in dele["prefer_external_executor_for"])+".")
    ex=rl.get("exploration") or {}; pl=rl.get("planning") or {}; rt=rl.get("retries") or {}; cb=rl.get("circuit_breaker") or {}
    L.append(
        "Limits (escalate, not hard stops): "
        f"initial reads <= {ex.get('initial_source_reads_max')}; broad repo scan {ex.get('broad_repo_scan_default')}; "
        f"plan passes {pl.get('initial_planning_passes_max')}, replans <= {pl.get('replans_per_work_item_max')}; "
        f"same-failure retries <= {rt.get('same_failure_class_max')}, blind retry {rt.get('blind_retry')}; "
        f"circuit breaker: {cb.get('repeated_same_failure')} repeated failures, {cb.get('no_progress_attempts')} no-progress attempt, or usage spike."
    )
    tl=c["task_lifecycle"]
    L+=["","## Task lifecycle and checkpoint"," -> ".join(tl.get("steps") or [])]
    L.append("Persist only: "+", ".join(x.replace('_',' ') for x in tl.get("persist") or [])+f". Chain-of-thought: {tl.get('store_chain_of_thought')}.")
    cm=c["communication"]; comm=rl.get("communication") or {}
    L+=["","## Communication",f"Progress updates: {cm.get('progress_updates','').replace('_',' ')}. Report when: "+"; ".join(cm.get("report_when") or [])+f". Completion summary <= {comm.get('completion_summary_chars')} chars."]
    L+=["","## Retrieve when"]+[f"- {t['name']} ({t['description']}): "+", ".join(t["sources"]) for t in c["triggers"]]
    if c["position_lessons"]:
        L+=["",f"## Position lessons ({c['position_knowledge']})",c["position_lessons"]]
    cont=c["continuity"]
    L+=["","## Continuity",f"Employee history/handoffs are not standing context; `orgctl {cont.get('employee_continuity_only_via','render-employee')}` only for: "+", ".join(x.replace('_',' ') for x in cont.get("employee_continuity_use") or [])+"."]
    return "\n".join(L)+"\n"


def contract_guarantee_errors(c):
    """Structural checks that a compiled contract carries required guarantees."""
    errs=[]; bid=c["position"]["id"]
    if c["position"].get("risk_ceiling") not in RISKS: errs.append(f"{bid} runtime contract lacks valid risk ceiling")
    if not c["organization"].get("display_name"): errs.append(f"{bid} runtime contract lacks organization identity")
    if not c["organization"].get("provider_neutral"): errs.append(f"{bid} runtime contract must be provider-neutral")
    ids={i.get("id") for i in c["invariants"] if isinstance(i,dict)}
    for req in REQUIRED_RUNTIME_INVARIANTS:
        if req not in ids: errs.append(f"{bid} runtime contract missing invariant {req}")
    if c["boundaries"].get("self_authority_change")!="forbidden": errs.append(f"{bid} runtime contract must forbid self authority change")
    if c["boundaries"].get("fail_closed_on_missing_required_approval") is not True: errs.append(f"{bid} runtime contract must fail closed on missing required approval")
    if c["capabilities"].get("can_self_escalate") is not False: errs.append(f"{bid} runtime contract must set can_self_escalate false")
    if not c["canonical_state"]: errs.append(f"{bid} runtime contract lacks canonical state rules")
    if not c["execution_profile"].get("steps"): errs.append(f"{bid} runtime contract lacks execution profile steps")
    if c["task_lifecycle"].get("store_chain_of_thought")!="forbidden": errs.append(f"{bid} runtime contract must forbid storing chain-of-thought")
    if not c["task_lifecycle"].get("persist"): errs.append(f"{bid} runtime contract lacks checkpoint persistence rules")
    if c["continuity"].get("standing_context_includes_employee_history") is not False: errs.append(f"{bid} runtime contract must exclude employee history")
    names={t["name"]:t for t in c["triggers"]}
    if c["execution_profile_id"] in ("coordinator","implementer"):
        orch=names.get("execution_orchestration")
        if not orch:
            errs.append(f"{bid} runtime contract missing execution_orchestration trigger")
        else:
            for s in ("routing/execution-substrate.yaml","docs/EXECUTOR_ROUTING.md","runbooks/howlplane-recovery.md"):
                if s not in orch["sources"]:
                    errs.append(f"{bid} execution_orchestration missing required source {s}")
    for trig,srcs in REQUIRED_TRIGGER_SOURCES.items():
        if trig not in names: errs.append(f"{bid} runtime contract missing required trigger {trig}")
        else:
            for s in srcs:
                if s not in names[trig]["sources"]: errs.append(f"{bid} trigger {trig} missing required source {s}")
    return errs


def _source_exists(rel):
    if "*" in rel: return any(ROOT.glob(rel.rstrip("/")))
    return (ROOT/rel).exists()


def validate_runtime_contracts(errors):
    """Runtime Context v2 invariants: policy, per-position context, compiled output."""
    pp=ROOT/RUNTIME_POLICY
    if not pp.exists():
        errors.append(f"missing {RUNTIME_POLICY}"); return
    policy=load_yaml(pp) or {}
    budgets=load_yaml(ROOT/"policies/budgets.yaml") or {}
    memory=load_yaml(ROOT/"policies/memory.yaml") or {}
    approvals=load_yaml(ROOT/"policies/approvals.yaml") or {}
    rt=budgets.get("agent_runtime") or {}

    # Shared policy.
    if policy.get("provider_neutral") is not True: errors.append("runtime-contract: provider_neutral must be true")
    inv=policy.get("invariants") or []
    ids=[i.get("id") for i in inv if isinstance(i,dict)]
    if len(ids)!=len(set(ids)): errors.append("runtime-contract: duplicate invariant ids")
    for req in REQUIRED_RUNTIME_INVARIANTS:
        if req not in ids: errors.append(f"runtime-contract: missing required invariant {req}")
    for i in inv:
        if not isinstance(i,dict) or not i.get("text") or not i.get("source"):
            errors.append(f"runtime-contract: invariant needs id/text/source: {i}"); continue
        if not (ROOT/i["source"]).exists(): errors.append(f"runtime-contract: invariant {i.get('id')} source missing {i['source']}")
    if memory.get("rules",{}).get("bot_memory_is_authoritative") is not False:
        errors.append("runtime-contract: policies/memory.yaml bot_memory_is_authoritative must be false")
    if approvals.get("rules",{}).get("fail_closed_if_required_approval_unavailable") is not True:
        errors.append("runtime-contract: approvals fail_closed_if_required_approval_unavailable must be true")
    ptrig=policy.get("triggers") or {}
    for name,meta in ptrig.items():
        for src in (meta or {}).get("required_sources") or []:
            if not _source_exists(src): errors.append(f"runtime-contract: trigger {name} source missing {src}")
    for name,srcs in REQUIRED_TRIGGER_SOURCES.items():
        have=set(((ptrig.get(name) or {}).get("required_sources")) or [])
        for s in srcs:
            if s not in have: errors.append(f"runtime-contract: trigger {name} must require {s}")
    req=policy.get("required_triggers") or {}
    all_req=list(req.get("all_positions") or [])
    for name in REQUIRED_TRIGGER_SOURCES:
        if name not in all_req: errors.append(f"runtime-contract: required_triggers.all_positions missing {name}")
    by_cap=req.get("by_capability") or {}
    for name in all_req+list(by_cap.values()):
        if name not in ptrig: errors.append(f"runtime-contract: required trigger {name} not defined")
    tl=policy.get("task_lifecycle") or {}
    if tl.get("store_chain_of_thought")!="forbidden": errors.append("runtime-contract: task_lifecycle.store_chain_of_thought must be forbidden")
    if tl.get("discard_task_local_history_after_checkpoint") is not True: errors.append("runtime-contract: task_lifecycle.discard_task_local_history_after_checkpoint must be true")
    cont=policy.get("continuity") or {}
    if cont.get("standing_context_includes_employee_history") is not False: errors.append("runtime-contract: continuity.standing_context_includes_employee_history must be false")
    forbidden_prefixes=tuple(cont.get("forbidden_retrieval_prefixes") or ())
    if "workforce/people/" not in forbidden_prefixes: errors.append("runtime-contract: continuity.forbidden_retrieval_prefixes must include workforce/people/")
    profiles=policy.get("execution_profiles") or {}

    # Efficiency policy.
    max_chars=rt.get("standing_context_max_chars")
    if not isinstance(max_chars,int) or max_chars<2000: errors.append("budgets: agent_runtime.standing_context_max_chars must be an integer >= 2000")
    cpt=rt.get("token_estimate_chars_per_token")
    if not isinstance(cpt,int) or cpt<=0: errors.append("budgets: agent_runtime.token_estimate_chars_per_token must be a positive integer")
    retry=(rt.get("retries") or {}).get("same_failure_class_max")
    cap=(budgets.get("defaults") or {}).get("max_retries_per_failure_class")
    if not isinstance(retry,int) or retry<0 or (isinstance(cap,int) and retry>cap):
        errors.append(f"budgets: agent_runtime.retries.same_failure_class_max must be an integer 0..{cap} (defaults.max_retries_per_failure_class)")
    if (rt.get("retries") or {}).get("blind_retry")!="forbidden": errors.append("budgets: agent_runtime.retries.blind_retry must be forbidden")
    if (rt.get("exploration") or {}).get("broad_repo_scan_default")!="forbidden": errors.append("budgets: agent_runtime.exploration.broad_repo_scan_default must be forbidden")
    if rt.get("limits_are_escalation_points_not_hard_stops") is not True: errors.append("budgets: agent_runtime.limits_are_escalation_points_not_hard_stops must be true")
    continuity_budget=organization().get("employee_continuity_budget_chars")

    # Per position.
    for bot in manifest().get("bots",[]):
        bid=bot.get("id"); ctxp=ROOT/f"bots/{bid}/context.yaml"
        if not ctxp.exists(): continue
        ctx=load_yaml(ctxp) or {}
        legacy=[k for k in LEGACY_CONTEXT_KEYS if k in ctx]
        if legacy:
            errors.append(f"{bid} context.yaml uses legacy v1 context schema ({', '.join(legacy)}); migrate to retrieve_when")
            continue
        before=len(errors)
        validate_instance(ctx,ROOT/"schemas/position-context.schema.json",f"bots/{bid}/context.yaml",errors)
        if len(errors)>before: continue
        if ctx["execution_profile"] not in profiles: errors.append(f"{bid} unknown execution_profile {ctx['execution_profile']}")
        if ctx["position_knowledge"]!=f"knowledge/positions/{bid}.md": errors.append(f"{bid} position_knowledge must be knowledge/positions/{bid}.md")
        elif not (ROOT/ctx["position_knowledge"]).is_file(): errors.append(f"{bid} missing {ctx['position_knowledge']}")
        budget=ctx["standing_budget_chars"]
        if isinstance(max_chars,int) and budget>max_chars: errors.append(f"{bid} standing_budget_chars exceeds agent_runtime.standing_context_max_chars: {budget}>{max_chars}")
        if isinstance(continuity_budget,int) and budget>=continuity_budget: errors.append(f"{bid} standing_budget_chars must be below employee_continuity_budget_chars")
        rw=ctx["retrieve_when"]
        for name,srcs in rw.items():
            if name not in ptrig: errors.append(f"{bid} unknown retrieval trigger {name}")
            for src in srcs:
                if src.startswith("/") or ".." in src.split("/"): errors.append(f"{bid} trigger {name} path must be repo-relative: {src}")
                elif forbidden_prefixes and src.startswith(forbidden_prefixes): errors.append(f"{bid} trigger {name} may not retrieve continuity/build material: {src}")
                elif not _source_exists(src): errors.append(f"{bid} trigger {name} source missing {src}")
        for name in all_req:
            if name not in rw: errors.append(f"{bid} retrieve_when missing required trigger {name}")
        caps=load_yaml(ROOT/f"bots/{bid}/capabilities.yaml") or {}
        for flag,name in by_cap.items():
            if caps.get(flag) is True and name not in rw: errors.append(f"{bid} has {flag} but retrieve_when lacks {name}")
        if ctx["execution_profile"] in ("coordinator","implementer") and "execution_orchestration" not in rw:
            errors.append(f"{bid} retrieve_when missing execution_orchestration")
        try:
            contract=compile_runtime_contract(bid)
            errors.extend(contract_guarantee_errors(contract))
            size=len(format_runtime_contract(contract))
            if size>budget: errors.append(f"{bid} runtime contract exceeds standing_budget_chars: {size}>{budget} chars")
        except SystemExit as e: errors.append(str(e))


def context(bot):
    p=ROOT/f"bots/{bot}/context.yaml"
    if not p.exists(): raise SystemExit(f"unknown position {bot}")
    c=compile_runtime_contract(bot)
    print(f"standing_budget_chars: {c['standing_budget_chars']}")
    print(f"standing: build/bots/{bot}.md (compiled by render-bot)")
    print(f"execution_profile: {c['execution_profile_id']}")
    print(f"position_knowledge: {c['position_knowledge']}")
    print("retrieve_when:")
    for t in c["triggers"]:
        print(f"  {t['name']}:")
        for s in t["sources"]: print(f"    - {s}")


def render_bot(bot, proposal=False):
    base=ROOT/(f"bots/proposals/{bot}" if proposal else f"bots/{bot}")
    contract=compile_runtime_contract(bot,base)
    bundle=format_runtime_contract(contract)
    budget=contract["standing_budget_chars"]
    if not isinstance(budget,int):
        raise SystemExit(f"{bot} context.yaml lacks standing_budget_chars (Runtime Context v2)")
    if len(bundle)>budget:
        raise SystemExit(f"rendered context for {bot} exceeds budget: {len(bundle)}>{budget} chars")
    out=ROOT/f"build/bots/{bot}.md"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(bundle)
    digest=hashlib.sha256(out.read_bytes()).hexdigest()
    print(f"{out.relative_to(ROOT)} sha256={digest}")


def context_report(as_json=False):
    cpt=((load_yaml(ROOT/"policies/budgets.yaml") or {}).get("agent_runtime") or {}).get("token_estimate_chars_per_token",4)
    rows=[]
    for b in manifest().get("bots",[]):
        c=compile_runtime_contract(b["id"]); text=format_runtime_contract(c); budget=c["standing_budget_chars"]
        rows.append({
            "position":b["id"],"status":b.get("status"),"chars":len(text),"bytes":len(text.encode()),
            "approx_tokens":-(-len(text)//cpt),"budget_chars":budget,
            "budget_percent":round(100*len(text)/budget,1) if isinstance(budget,int) and budget else None,
            "triggers":len(c["triggers"]),"retrievable_sources":sum(len(t["sources"]) for t in c["triggers"]),
        })
    if as_json:
        print(json.dumps({"token_estimate":f"ceil(chars/{cpt})","positions":rows},indent=2)); return
    print(f"POSITION               CHARS BYTES ~TOKENS BUDGET  USED%  TRIGGERS SOURCES   (tokens ~= chars/{cpt})")
    for r in rows:
        print(f"{r['position']:<22} {r['chars']:<5} {r['bytes']:<5} {r['approx_tokens']:<7} {r['budget_chars']:<7} {r['budget_percent']:<6} {r['triggers']:<8} {r['retrievable_sources']}")


def render_all():
    for b in manifest().get("bots",[]): render_bot(b["id"])


def employee_by_id(eid):
    for e in workforce().get("employees",[]):
        if e.get("employee_id")==eid: return e
    return None


def render_employee(eid):
    e=employee_by_id(eid)
    if not e: raise SystemExit(f"unknown employee {eid}")
    pos=e["position_id"]
    render_bot(pos)
    parts=[f"# Employee Onboarding / Continuity Bundle: {eid}\n\n",f"Current roster record:\n\n```yaml\n{yaml_text(e)}\n```\n"]
    rec=ROOT/e["record_path"]
    base=rec.parent
    for p in [rec,base/"TENURE.md",base/"context/README.md"]:
        if p.exists(): parts.append(f"\n---\n## SOURCE: {p.relative_to(ROOT)}\n\n{p.read_text()}\n")
    profile=load_yaml(rec) or {}
    pred=profile.get("predecessor_employee_id")
    if pred:
        pred_dir=ROOT/"workforce/people"/pred/"handoffs"
        if pred_dir.exists():
            for p in sorted(pred_dir.glob("*.md"))[-2:]: parts.append(f"\n---\n## PREDECESSOR HANDOFF: {p.relative_to(ROOT)}\n\n{p.read_text()}\n")
    for p in sorted((base/"context").glob("*.yaml"))[-3:]:
        parts.append(f"\n---\n## CONTEXT SNAPSHOT: {p.relative_to(ROOT)}\n\n```yaml\n{p.read_text()}\n```\n")
    bot_bundle=ROOT/f"build/bots/{pos}.md"
    parts.append(f"\n---\n## POSITION BUNDLE: {bot_bundle.relative_to(ROOT)}\n\n{bot_bundle.read_text()}\n")
    bundle="".join(parts)
    budget=organization().get("employee_continuity_budget_chars",24000)
    if len(bundle)>budget:
        raise SystemExit(f"employee continuity bundle for {eid} exceeds budget: {len(bundle)}>{budget} chars")
    out=ROOT/f"build/workforce/{eid}.md"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(bundle)
    print(f"{out.relative_to(ROOT)} chars={len(bundle)} budget={budget} sha256={hashlib.sha256(out.read_bytes()).hexdigest()}")


def yaml_text(data):
    import yaml
    return yaml.safe_dump(data,sort_keys=False,allow_unicode=True).rstrip()


def fingerprints():
    for b in manifest().get("bots",[]):
        bid=b["id"]; h=hashlib.sha256()
        for name in ["instructions.md","context.yaml","capabilities.yaml","boundaries.yaml","skills.yaml","routines.yaml"]:
            p=ROOT/f"bots/{bid}/{name}"
            if p.exists(): h.update(name.encode()+b"\0"+p.read_bytes()+b"\0")
        print(f"{bid} {h.hexdigest()}")


def safe_id(s): return bool(re.fullmatch(r"[a-z0-9][a-z0-9-]{1,63}",s))

def manifest_position(position_id):
    for pos in manifest().get("bots",[]):
        if pos.get("id")==position_id: return pos
    raise SystemExit(f"unknown position {position_id}")


def scaffold_bot(args):
    if not safe_id(args.id): raise SystemExit("id must be lowercase kebab-case, 2-64 chars")
    if args.risk not in RISKS: raise SystemExit("risk must be R0-R4")
    if not args.purpose.strip(): raise SystemExit("purpose must be non-empty")
    if not (ROOT/f"roles/{args.role}.md").exists(): raise SystemExit(f"unknown role file roles/{args.role}.md")
    dst=ROOT/f"bots/proposals/{args.id}"
    if dst.exists(): raise SystemExit(f"proposal exists: {dst.relative_to(ROOT)}")
    dst.mkdir(parents=True)
    (dst/"README.md").write_text(f"# {args.name}\n\nCandidate persistent **position** proposal. Not active or staffed until reviewed.\n")
    (dst/"instructions.md").write_text(f"# Operating instructions\n\n## Purpose\n\n{args.purpose.strip()}\n\n## Invariants\n\n- Follow AGENTS.md and policy.\n- Do not self-escalate.\n- Return evidence and handoffs.\n")
    dump_yaml({"schema_version":2,"standing_budget_chars":5000,"execution_profile":"advisor","position_knowledge":f"knowledge/positions/{args.id}.md","retrieve_when":{
        "authority_question":[],"risk_classification":[],"knowledge_checkpoint":["knowledge/company/"],"evidence_verification":[],"external_action":[],
        "incident_response":["runbooks/"],"role_detail":["AGENTS.md","organization.yaml",f"roles/{args.role}.md"]}},dst/"context.yaml")
    dump_yaml({"bot_id":args.id,"can_delegate":False,"can_modify_bot_definitions":False,"can_propose_policy_changes":True,"can_self_escalate":False},dst/"capabilities.yaml")
    dump_yaml({"bot_id":args.id,"risk_ceiling":args.risk,"secrets_in_prompt":"forbidden","self_authority_change":"forbidden","fail_closed_on_missing_required_approval":True},dst/"boundaries.yaml")
    dump_yaml({"bot_id":args.id,"skills":[]},dst/"skills.yaml")
    dump_yaml({"bot_id":args.id,"routines":[]},dst/"routines.yaml")
    proposal=(ROOT/"templates/roster-change.md").read_text().replace("- Candidate ID:",f"- Candidate ID: {args.id}").replace("- Proposed name:",f"- Proposed name: {args.name}").replace("- Logical role:",f"- Logical role: {args.role}").replace("- Proposed risk ceiling:",f"- Proposed risk ceiling: {args.risk}")
    (dst/"ROSTER_CHANGE.md").write_text(proposal)
    print(f"created position proposal {dst.relative_to(ROOT)}")
    print("NOT activated or staffed; review manifest change, then use workforce hire procedure.")


def propose_hire(args):
    if not safe_id(args.employee_id): raise SystemExit("employee id must be lowercase kebab-case")
    positions={b['id'] for b in manifest().get('bots',[])}
    if args.position not in positions: raise SystemExit(f"unknown position {args.position}")
    if employee_by_id(args.employee_id): raise SystemExit(f"employee id already exists: {args.employee_id}")
    current=workforce().get('employees',[])
    if args.manager!='owner':
        mgr=employee_by_id(args.manager)
        if not mgr or mgr.get('status') not in {'hired','active','suspended'}: raise SystemExit(f"manager must be owner or current employee: {args.manager}")
    predecessor=employee_by_id(args.predecessor) if args.predecessor else None
    if args.predecessor and not predecessor: raise SystemExit(f"unknown predecessor {args.predecessor}")
    if predecessor and predecessor.get('position_id')!=args.position: raise SystemExit("predecessor must be from the same position")
    existing_generations=[e.get('generation',0) for e in current if e.get('position_id')==args.position]
    generation=args.generation or (max(existing_generations,default=0)+1)
    if predecessor and generation<=predecessor.get('generation',0): raise SystemExit("generation must be greater than predecessor generation")
    pos=manifest_position(args.position)
    occupied=sum(1 for e in current if e.get('position_id')==args.position and e.get('status') in {'hired','active','suspended'})
    dst=ROOT/f"workforce/proposals/hire-{args.employee_id}"; dst.mkdir(parents=True,exist_ok=False)
    profile={
        'schema_version':1,'employee_id':args.employee_id,'display_name':args.name,'worker_type':'ai_bot',
        'initial_position_id':args.position,'initial_logical_role':pos['role'],
        'hired_on':datetime.now().astimezone().date().isoformat(),'generation':generation,'manager_ref_at_hire':args.manager,
        'provider_kind':args.provider,'predecessor_employee_id':args.predecessor,'notes':'PROPOSAL ONLY; not active until reviewed and applied.'
    }
    dump_yaml(profile,dst/'profile.yaml')
    txt=(ROOT/'templates/hire.md').read_text()
    replacements={
      '- Proposed employee ID:':f'- Proposed employee ID: {args.employee_id}', '- Display name:':f'- Display name: {args.name}',
      '- Position:':f'- Position: {args.position}', '- Manager:':f'- Manager: {args.manager}',
      '- Provider/deployment kind:':f'- Provider/deployment kind: {args.provider}', '- Predecessor:':f'- Predecessor: {args.predecessor or "none"}',
      '- Required review/approval:':f'- Required review/approval: {pos.get("staffing_authority","owner")} staffing authority; any authority/credential expansion follows separate approval policy'
    }
    for a,b in replacements.items(): txt=txt.replace(a,b)
    (dst/'HIRE.md').write_text(txt)
    print(f"created hire proposal {dst.relative_to(ROOT)}")
    if occupied>=pos.get('seat_limit',1): print("NOTICE: position is currently full; activation requires an approved separation/reassignment or seat-limit change.")
    print("NOT added to workforce/roster.yaml or live platform.")


def propose_separation(args):
    e=employee_by_id(args.employee_id)
    if not e: raise SystemExit(f"unknown employee {args.employee_id}")
    if args.type not in SEPARATION_TYPES: raise SystemExit(f"type must be one of {sorted(SEPARATION_TYPES)}")
    stamp=datetime.now().astimezone().strftime('%Y%m%dT%H%M%S')
    dst=ROOT/f"workforce/proposals/separate-{args.employee_id}-{stamp}"; dst.mkdir(parents=True,exist_ok=False)
    txt=(ROOT/'templates/separation.md').read_text()
    for a,b in {
      '- Employee ID:':f'- Employee ID: {args.employee_id}', '- Current position:':f'- Current position: {e["position_id"]}',
      '- Separation type: terminated / retired / laid_off / replaced / provider_retired':f'- Separation type: {args.type}',
      '- Reason code:':f'- Reason code: {args.reason}',
      '- Required approval:':f'- Required approval: {manifest_position(e["position_id"]).get("staffing_authority","owner")} staffing authority'
    }.items(): txt=txt.replace(a,b)
    (dst/'SEPARATION.md').write_text(txt)
    print(f"created separation proposal {dst.relative_to(ROOT)}")
    print("NO workforce status, live Bot, credentials or records changed.")


def record_contribution(args):
    e=employee_by_id(args.employee_id)
    if not e: raise SystemExit(f"unknown employee {args.employee_id}")
    now=datetime.now().astimezone(); cid=args.id or f"contrib-{now.strftime('%Y%m%dt%H%M%S')}-{args.employee_id}"
    if not safe_id(cid): raise SystemExit("contribution id must be lowercase kebab-case")
    p=ROOT/f"workforce/contributions/{cid}.yaml"
    if p.exists(): raise SystemExit(f"contribution exists: {p.relative_to(ROOT)}")
    dump_yaml({
      'schema_version':1,'contribution_id':cid,'employee_id':args.employee_id,'occurred_at':now.isoformat(timespec='seconds'),
      'role_at_time':e['logical_role'],'work_item_id':args.work_item,'summary':args.summary,
      'artifact_refs':args.artifact or [],'evidence_refs':args.evidence or [],'verified_by':args.verified_by
    },p)
    print(p.relative_to(ROOT))


def checkpoint(args):
    e=employee_by_id(args.employee_id)
    if not e: raise SystemExit(f"unknown employee {args.employee_id}")

    schema=load_json(ROOT/"schemas/context-snapshot.schema.json")
    allowed_reasons=set(schema.get("properties",{}).get("reason",{}).get("enum",[]))
    if args.reason not in allowed_reasons:
        raise SystemExit(f"reason must be one of {sorted(allowed_reasons)}")

    if args.handoff_to and args.handoff_to!="owner" and not employee_by_id(args.handoff_to):
        raise SystemExit(f"unknown handoff target {args.handoff_to}; must be 'owner' or an existing employee id")

    now=datetime.now().astimezone()
    snapshot_id=args.id or f"context-{now.strftime('%Y%m%dt%H%M%S')}-{args.employee_id}"
    if not safe_id(snapshot_id): raise SystemExit(f"context snapshot id must be lowercase kebab-case: {snapshot_id}")

    p=ROOT/f"workforce/people/{args.employee_id}/context/{snapshot_id}.yaml"
    if p.exists(): raise SystemExit(f"context snapshot exists: {p.relative_to(ROOT)}")

    data={
        'schema_version':1,
        'snapshot_id':snapshot_id,
        'employee_id':args.employee_id,
        'created_at':now.isoformat(timespec='seconds'),
        'reason':args.reason,
        'stable_knowledge':args.stable,
        'open_work':args.open_work,
        'decisions':args.decision,
        'risks':args.risk,
        'source_refs':args.source_ref,
        'handoff_to':args.handoff_to,
        'contains_raw_chain_of_thought':False,
    }

    errors=[]
    validate_instance(data,ROOT/"schemas/context-snapshot.schema.json",snapshot_id,errors)
    if errors: raise SystemExit("invalid context snapshot: "+"; ".join(errors))

    text=yaml_text(data)
    budgets=load_yaml(ROOT/"policies/budgets.yaml") or {}
    limit=(budgets.get("knowledge_artifacts") or {}).get("checkpoint_chars")
    if isinstance(limit,int) and len(text)>limit:
        raise SystemExit(
            f"checkpoint exceeds checkpoint_chars budget: {len(text)}>{limit} chars; "
            "compact stable_knowledge/open_work/decisions/risks/source_refs before writing"
        )

    dump_yaml(data,p)
    print(f"{p.relative_to(ROOT)} chars={len(text)} limit={limit}")


def org_status():
    org=organization()
    print(f"{org.get('display_name','Organization')} ({org.get('repository_slug','?')})")
    positions=manifest().get("bots",[])
    employees=workforce().get("employees",[])
    current={"hired","active","suspended"}
    print("POSITION               POS STATUS  RISK STAFFING             SEATS FILLED VACANT WORKERS / DEPLOYMENT")
    for pos in positions:
        workers=[e for e in employees if e.get("position_id")==pos["id"] and e.get("status") in current]
        vacant=max(0,pos.get("seat_limit",1)-len(workers))
        names=",".join(f"{e['employee_id']}[{e.get('deployment_status','?')}]" for e in workers) or "-"
        print(f"{pos['id']:<22} {pos.get('status','?'):<10} {pos.get('risk_ceiling','?'):<4} {pos.get('staffing_authority','?'):<20} {pos.get('seat_limit',1):<5} {len(workers):<6} {vacant:<6} {names}")


def employee_history(eid):
    e=employee_by_id(eid)
    if not e: raise SystemExit(f"unknown employee {eid}")
    print("ROSTER")
    print(yaml_text(e))
    print("\nEVENTS")
    found=False
    for p in sorted((ROOT/"workforce/events").glob("*.yaml")):
        d=load_yaml(p) or {}
        if d.get("employee_id")==eid:
            found=True; print(f"- {p.name}: {d.get('event_type')} @ {d.get('occurred_at')} — {d.get('summary')}")
    if not found: print("- none")
    print("\nCONTRIBUTIONS")
    found=False
    for p in sorted((ROOT/"workforce/contributions").glob("*.yaml")):
        d=load_yaml(p) or {}
        if d.get("employee_id")==eid:
            found=True; print(f"- {p.name}: {d.get('summary')}")
    if not found: print("- none recorded")
    base=ROOT/"workforce/people"/eid
    handoffs=sorted((base/"handoffs").glob("*.md")) if (base/"handoffs").exists() else []
    snapshots=sorted((base/"context").glob("*.yaml")) if (base/"context").exists() else []
    print(f"\nHANDOFFS {len(handoffs)} | CONTEXT SNAPSHOTS {len(snapshots)}")


def about():
    print(yaml_text(organization()))

def bootstrap_plan():
    print("1 validate repository and workforce records")
    print("2 render compiled position runtime contracts; render employee continuity bundles only for onboarding/handoff")
    print("3 inventory live Grok roster/configuration and map live IDs to workforce employees")
    print("4 compare desired positions + workforce vs deployed fingerprints")
    print("5 auto-reconcile only within existing authority")
    print("6 propose hires/separations/authority-affecting drift for review")
    print("7 test skills before enabling routines")
    print("8 record reconciliation and workforce events")


def main():
    ap=argparse.ArgumentParser(prog="orgctl"); sub=ap.add_subparsers(dest="cmd",required=True)
    sub.add_parser("validate"); sub.add_parser("about"); sub.add_parser("list-bots"); sub.add_parser("org-status")
    lw=sub.add_parser("list-workforce"); lw.add_argument('--active-only',action='store_true')
    c=sub.add_parser("context"); c.add_argument("bot")
    r=sub.add_parser("render-bot"); r.add_argument("bot")
    re=sub.add_parser("render-employee"); re.add_argument("employee_id")
    sub.add_parser("render-all"); sub.add_parser("fingerprints"); sub.add_parser("bootstrap-plan")
    cr=sub.add_parser("context-report",help="standing runtime-contract size per position"); cr.add_argument("--json",action="store_true")
    s=sub.add_parser("scaffold-bot"); s.add_argument("id"); s.add_argument("--name",required=True); s.add_argument("--role",required=True); s.add_argument("--risk",default="R1"); s.add_argument("--purpose",required=True)
    h=sub.add_parser("propose-hire"); h.add_argument('employee_id'); h.add_argument('--name',required=True); h.add_argument('--position',required=True); h.add_argument('--manager',required=True); h.add_argument('--provider',default='grok-bot'); h.add_argument('--predecessor'); h.add_argument('--generation',type=int)
    sp=sub.add_parser("propose-separation"); sp.add_argument('employee_id'); sp.add_argument('--type',required=True); sp.add_argument('--reason',required=True)
    eh=sub.add_parser("employee-history"); eh.add_argument("employee_id")
    rc=sub.add_parser("record-contribution"); rc.add_argument('employee_id'); rc.add_argument('--summary',required=True); rc.add_argument('--id'); rc.add_argument('--work-item'); rc.add_argument('--artifact',action='append'); rc.add_argument('--evidence',action='append'); rc.add_argument('--verified-by')
    cp=sub.add_parser("checkpoint"); cp.add_argument('employee_id'); cp.add_argument('--reason',required=True); cp.add_argument('--stable',action='append',default=[]); cp.add_argument('--open-work',dest='open_work',action='append',default=[]); cp.add_argument('--decision',action='append',default=[]); cp.add_argument('--risk',action='append',default=[]); cp.add_argument('--source-ref',dest='source_ref',action='append',default=[]); cp.add_argument('--handoff-to',dest='handoff_to',default=None); cp.add_argument('--id')
    rt=sub.add_parser("route",help="deterministic executor routing inspection (no model invoke)")
    rt.add_argument("--task-class",required=True,choices=list(TASK_CLASS_IDS))
    rt.add_argument("--risk",required=True,choices=sorted(RISKS))
    rt.add_argument("--required-tool",action="append",default=[],dest="required_tools")
    rt.add_argument("--objective",default=None)
    rt.add_argument(
        "--grok-capacity",
        default="unknown",
        choices=list(QUOTA_STATES),
        help="operator-declared persistent Grok capacity (never scraped; default unknown)",
    )
    rt.add_argument("--json",action="store_true",help="emit JSON instead of YAML")
    a=ap.parse_args()
    if a.cmd=="validate": raise SystemExit(validate())
    if a.cmd=="about": about()
    if a.cmd=="list-bots": list_bots()
    if a.cmd=="org-status": org_status()
    if a.cmd=="list-workforce": list_workforce(not a.active_only)
    if a.cmd=="context": context(a.bot)
    if a.cmd=="render-bot": render_bot(a.bot)
    if a.cmd=="render-employee": render_employee(a.employee_id)
    if a.cmd=="employee-history": employee_history(a.employee_id)
    if a.cmd=="render-all": render_all()
    if a.cmd=="context-report": context_report(a.json)
    if a.cmd=="fingerprints": fingerprints()
    if a.cmd=="bootstrap-plan": bootstrap_plan()
    if a.cmd=="scaffold-bot": scaffold_bot(a)
    if a.cmd=="propose-hire": propose_hire(a)
    if a.cmd=="propose-separation": propose_separation(a)
    if a.cmd=="record-contribution": record_contribution(a)
    if a.cmd=="checkpoint": checkpoint(a)
    if a.cmd=="route":
        result=route_inspect(
            a.task_class,a.risk,a.required_tools,a.objective,grok_capacity=a.grok_capacity
        )
        if a.json:
            print(json.dumps(result,indent=2,sort_keys=False))
        else:
            print(yaml_text(result))
        raise SystemExit(0 if result.get("result") in {"selected","evidence-insufficient"} else 2)

if __name__=="__main__": main()
