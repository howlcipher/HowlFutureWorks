"""HOWL-010: HowlPlane-first execution, governed recovery, bounded repair."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import orgctl  # noqa: E402


def y(rel):
    return yaml.safe_load((ROOT / rel).read_text())


def run_orgctl(*args, cwd=None):
    return subprocess.run(
        [sys.executable, str((cwd or ROOT) / "tools" / "orgctl.py"), *args],
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
    )


@pytest.fixture
def repo_copy(tmp_path):
    dst = tmp_path / "repo"
    shutil.copytree(
        ROOT,
        dst,
        ignore=shutil.ignore_patterns(".git", "build", "dist", "__pycache__", ".pytest_cache", ".venv"),
    )
    return dst


def substrate():
    return y("routing/execution-substrate.yaml")


def test_three_decisions_stay_separate():
    assert substrate()["decisions"] == list(orgctl.REQUIRED_EXECUTION_DECISIONS)
    assert y("routing/participation-policy.yaml")["principles"]["demand_driven"] is True
    assert y("routing/selection-policy.yaml")["principles"]["self_preferred_when_sufficient"] is True
    assert y("routing/selection-policy.yaml")["principles"]["delegated_substrate"] == "howlplane"
    delegation = y("policies/budgets.yaml")["agent_runtime"]["delegation"]
    assert delegation["delegated_substrate"] == "howlplane"
    assert delegation["raw_executor_cli"] == "not_normalized"
    enum = y("schemas/result-envelope.schema.json")["properties"]["efficiency"]["properties"]["execution_substrate"]["enum"]
    assert enum == ["SELF", "HOWLPLANE", "governed_recovery"]


def test_trivial_and_simple_route_stays_self():
    for task_class in ("trivial", "simple"):
        data = json.loads(run_orgctl("route", "--task-class", task_class, "--risk", "R1", "--json").stdout)
        assert data["decision"] == "SELF"
        assert data["execution_substrate"]["path"] == "SELF"
        assert data["execution_substrate"]["orchestration"] == "none"
        assert data["execution_substrate"]["raw_executor_cli"] == "not_normalized"


def test_delegated_implementation_prefers_howlplane():
    data = json.loads(run_orgctl("route", "--task-class", "complex", "--risk", "R2", "--json").stdout)
    assert data["decision"] == "eligible_profile_by_measured_fit"
    sub = data["execution_substrate"]
    assert sub["path"] == "HOWLPLANE"
    assert sub["executor_selection"] == "howlplane"
    assert sub["raw_executor_cli"] == "not_normalized"
    steps = [s["step"] for s in data["selection_steps"]]
    assert "dispatch_delegated_work_through_howlplane" in steps
    assert "raw_provider_cli" not in json.dumps(data["execution_substrate"])


def test_bounded_work_stays_self_until_delegation_is_justified():
    data = json.loads(run_orgctl("route", "--task-class", "bounded", "--risk", "R2", "--json").stdout)
    assert data["decision"] == "SELF_preferred_unless_expected_value"
    sub = data["execution_substrate"]
    assert sub["path"] == "SELF_unless_delegated"
    assert sub["when_delegated"] == "HOWLPLANE"


def test_plane_failure_does_not_remove_policy_controls():
    recovery = substrate()["recovery"]
    assert recovery["applies_to"] == "orchestration_layer_only"
    assert set(recovery["must_preserve"]) == set(orgctl.REQUIRED_RECOVERY_PRESERVE)
    assert recovery["howlplane_failure_is_governance_bypass"] is False
    assert recovery["raw_executor_cli"] == "forbidden"
    assert recovery["when_no_governed_entrypoint_works"] == "checkpoint_stop_escalate"
    assert y("routing/fallback-policy.yaml")["orchestration_failure"]["howlplane_failure_is_governance_bypass"] is False
    assert y("policies/tool-access.yaml")["rules"]["direct_executor_cli_bypass_of_howlframe"] == "forbidden"


def test_recovery_conditions_are_orchestration_only():
    assert set(substrate()["recovery"]["conditions"]) == set(orgctl.REQUIRED_RECOVERY_CONDITIONS)


def test_howlplane_is_a_tracked_repair_target_and_recursion_is_bounded():
    repair = substrate()["repair"]
    assert "howlplane" in repair["eligible_targets"]
    assert repair["mechanism"] == "one_tracked_work_item"
    assert repair["plane_self_target"] == "self"
    assert "self" in substrate()["verified_interfaces"]["factory_target_values"]
    rec = repair["recursion"]
    assert rec["max_repair_objectives_per_failure"] == 1
    assert rec["unbounded_recursive_repair"] == "forbidden"
    assert rec["if_governed_repair_path_fails"] == "checkpoint_stop_escalate"
    assert substrate()["executor_failure_is_plane_defect"] is False
    assert set(substrate()["failure_classes"]) == set(orgctl.REQUIRED_FAILURE_CLASSES)


def test_improvement_requires_evidence_and_cannot_expand_authority():
    improvement = substrate()["improvement"]
    assert improvement["requires_evidence"] is True
    assert improvement["unsupported_model_opinion"] == "insufficient"
    assert improvement["follows_normal_prioritization"] is True
    assert {"observation", "evidence", "tracked_work_item", "verification", "measure"} <= set(improvement["loop"])
    assert "howlplane" in improvement["eligible_targets"]
    assert set(substrate()["self_improvement"]["may_not"]) == set(orgctl.REQUIRED_SELF_IMPROVEMENT_DENIALS)
    assert substrate()["self_improvement"]["within_existing_authority"] is True


def test_durable_work_state_is_outside_the_conversation():
    work = substrate()["work_state"]
    assert work["git"] == "desired_organizational_and_product_state"
    assert work["howlboard"] == "authoritative_work_state"
    assert work["howlplane"] == "authoritative_execution_state"
    assert work["grok_conversation"] == "disposable_working_context"
    assert "execution_failures" in work["durable_outside_conversation"]
    assert "repair_work" in work["durable_outside_conversation"]


def test_verified_interfaces_are_howlplane_entrypoints():
    interfaces = substrate()["verified_interfaces"]
    commands = set(interfaces["commands"])
    assert set(orgctl.REQUIRED_PLANE_COMMANDS) <= commands
    assert all(cmd.startswith("howlplane ") for cmd in commands)
    assert interfaces["not_a_default_path"] == "raw_provider_cli"
    assert all(cmd.startswith("howlplane ") for cmd in interfaces["default_delegated_commands"])


def test_orchestration_trigger_is_structural_and_budgets_hold():
    policy = y("policies/runtime-contract.yaml")["triggers"]["execution_orchestration"]
    required = {"routing/execution-substrate.yaml", "docs/EXECUTOR_ROUTING.md", "runbooks/howlplane-recovery.md"}
    assert required <= set(policy["required_sources"])
    for bid, profile in (("engineering-manager", "coordinator"), ("dev-lead", "implementer")):
        contract = orgctl.compile_runtime_contract(bid)
        assert contract["execution_profile_id"] == profile
        sources = {t["name"]: t["sources"] for t in contract["triggers"]}
        assert required <= set(sources["execution_orchestration"])
        text = orgctl.format_runtime_contract(contract)
        budget = y(f"bots/{bid}/context.yaml")["standing_budget_chars"]
        assert len(text) <= budget
    # Other positions do not pay for Plane documentation in standing context.
    for bid in ("product", "rnd", "assurance", "auditor"):
        names = [t["name"] for t in orgctl.compile_runtime_contract(bid)["triggers"]]
        assert "execution_orchestration" not in names


def test_validate_rejects_governance_bypass(repo_copy):
    path = repo_copy / "routing" / "execution-substrate.yaml"
    data = yaml.safe_load(path.read_text())
    data["recovery"]["howlplane_failure_is_governance_bypass"] = True
    path.write_text(yaml.safe_dump(data, sort_keys=False))
    result = run_orgctl("validate", cwd=repo_copy)
    assert result.returncode != 0
    assert "governance bypass" in result.stdout


def test_validate_rejects_unbounded_repair(repo_copy):
    path = repo_copy / "routing" / "execution-substrate.yaml"
    data = yaml.safe_load(path.read_text())
    data["repair"]["recursion"]["max_repair_objectives_per_failure"] = 9
    data["repair"]["recursion"]["unbounded_recursive_repair"] = "allowed"
    path.write_text(yaml.safe_dump(data, sort_keys=False))
    result = run_orgctl("validate", cwd=repo_copy)
    assert result.returncode != 0
    assert "repair recursion" in result.stdout or "unbounded_recursive_repair" in result.stdout


def test_validate_rejects_opinion_as_improvement_evidence(repo_copy):
    path = repo_copy / "routing" / "execution-substrate.yaml"
    data = yaml.safe_load(path.read_text())
    data["improvement"]["requires_evidence"] = False
    data["improvement"]["unsupported_model_opinion"] = "sufficient"
    path.write_text(yaml.safe_dump(data, sort_keys=False))
    result = run_orgctl("validate", cwd=repo_copy)
    assert result.returncode != 0
    assert "requires_evidence" in result.stdout


def test_validate_rejects_authority_expansion(repo_copy):
    path = repo_copy / "routing" / "execution-substrate.yaml"
    data = yaml.safe_load(path.read_text())
    data["self_improvement"]["may_not"] = [x for x in data["self_improvement"]["may_not"] if x != "increase_authority"]
    path.write_text(yaml.safe_dump(data, sort_keys=False))
    result = run_orgctl("validate", cwd=repo_copy)
    assert result.returncode != 0
    assert "self_improvement.may_not" in result.stdout


def test_validate_rejects_raw_cli_as_default(repo_copy):
    path = repo_copy / "routing" / "selection-policy.yaml"
    data = yaml.safe_load(path.read_text())
    data["principles"]["raw_executor_cli"] = "normalized"
    path.write_text(yaml.safe_dump(data, sort_keys=False))
    result = run_orgctl("validate", cwd=repo_copy)
    assert result.returncode != 0
    assert "raw_executor_cli" in result.stdout


def test_participation_defaults_still_do_not_summon_the_full_workflow():
    part = y("routing/participation-policy.yaml")
    assert part["principles"]["full_workflow_mandatory_by_default"] is False
    assert part["task_defaults"]["trivial"]["auditor"] == "not_required"
    data = json.loads(run_orgctl("route", "--task-class", "simple", "--risk", "R1", "--grok-capacity", "healthy", "--json").stdout)
    roles = data["persistent_participation"]
    assert roles.get("auditor") in (None, "not_required")
    assert data["capacity_overrode_safety"] is False
