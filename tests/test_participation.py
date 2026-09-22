"""Demand-driven persistent-role participation and Grok capacity awareness."""
from pathlib import Path
import json
import shutil
import subprocess
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


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
        ignore=shutil.ignore_patterns(
            ".git", "build", "dist", "__pycache__", ".pytest_cache", ".venv"
        ),
    )
    return dst


def test_participation_policy_file_exists_and_invariants():
    part = y("routing/participation-policy.yaml")
    p = part["principles"]
    assert p["demand_driven"] is True
    assert p["full_workflow_mandatory_by_default"] is False
    assert p["capacity_may_lower_assurance"] is False
    assert p["capacity_may_bypass_approvals"] is False
    assert p["capacity_may_downgrade_risk"] is False
    assert p["precedence"] == "mandatory_governance_and_safety_over_capacity_optimization"
    assert set(part["grok_capacity"]["states"]) == {
        "healthy",
        "constrained",
        "scarce",
        "exhausted",
        "unknown",
    }
    assert part["grok_capacity"]["affects"] == "optional_participation_only"
    assert part["globally_mandatory"]["product"] is False
    assert part["globally_mandatory"]["auditor"] is False
    assert part["globally_mandatory"]["rnd"] is False
    assert part["globally_mandatory"]["full_workflow"] is False
    assert part["task_defaults"]["critical"]["follow_risk_policy"] is True
    assert part["task_defaults"]["critical"]["capacity_cannot_suppress_mandatory_controls"] is True
    rr = y("routing/routing-policy.yaml")
    assert rr["canonical"]["participation"] == "routing/participation-policy.yaml"
    assert rr["rules"]["demand_driven_persistent_participation"] is True
    assert rr["rules"]["full_workflow_mandatory_by_default"] is False
    assert rr["rules"]["capacity_may_lower_assurance"] is False


def test_trivial_r0_responsible_only():
    r = run_orgctl(
        "route", "--task-class", "trivial", "--risk", "R0",
        "--grok-capacity", "healthy", "--json",
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    roles = data["persistent_participation"]
    assert roles["responsible"] == "required"
    assert roles["product"] == "not_required"
    assert roles["auditor"] == "not_required"
    assert roles["rnd"] == "not_required"
    assert roles["engineering_manager"] == "not_required"
    assert data["capacity_overrode_safety"] is False
    assert data["decision"] == "SELF"


def test_simple_r1_minimal_participation():
    r = run_orgctl(
        "route", "--task-class", "simple", "--risk", "R1",
        "--grok-capacity", "healthy", "--json",
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    roles = data["persistent_participation"]
    assert roles["responsible"] == "required"
    assert roles["product"] == "not_required"
    assert roles["auditor"] == "not_required"
    assert roles["rnd"] == "not_required"
    assert roles["assurance"] in {"conditional", "not_required", "optional"}


def test_bounded_r2_implementer_assurance_conditional():
    r = run_orgctl(
        "route", "--task-class", "bounded", "--risk", "R2",
        "--grok-capacity", "healthy", "--json",
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    roles = data["persistent_participation"]
    assert roles["implementer"] == "required"
    assert roles["assurance"] == "conditional"
    assert roles["product"] == "conditional"
    assert roles["auditor"] == "not_required"
    assert roles["rnd"] == "not_required"


def test_complex_allows_additional_participation():
    r = run_orgctl(
        "route", "--task-class", "complex", "--risk", "R2",
        "--grok-capacity", "healthy", "--json",
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    roles = data["persistent_participation"]
    assert roles["implementer"] == "required"
    assert roles["engineering_manager"] == "likely"
    assert roles["assurance"] == "likely"
    assert roles["product"] == "conditional"


def test_critical_r4_mandatory_controls_under_all_capacity():
    for cap in ("healthy", "constrained", "scarce", "exhausted", "unknown"):
        r = run_orgctl(
            "route", "--task-class", "critical", "--risk", "R4",
            "--grok-capacity", cap, "--json",
        )
        assert r.returncode == 0, (cap, r.stderr)
        data = json.loads(r.stdout)
        assert data["capacity_overrode_safety"] is False
        assert data["persistent_participation"]["assurance"] == "required"
        assert data["independent_verification"] == "required"
        # Auditor may be conditional but never silently dropped to not_required under R4
        assert data["persistent_participation"]["auditor"] in {
            "conditional",
            "required",
            "deferred_optional",
        }
        if cap == "exhausted":
            # Auditor stays conditional for R4 (not deferred past governance need)
            assert data["persistent_participation"]["auditor"] == "conditional"


def test_scarce_reduces_optional_preserves_mandatory():
    r = run_orgctl(
        "route", "--task-class", "bounded", "--risk", "R2",
        "--grok-capacity", "scarce", "--json",
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    roles = data["persistent_participation"]
    assert roles["implementer"] == "required"
    assert roles["assurance"] == "conditional"
    assert roles["product"] == "deferred_optional"
    assert data["capacity_overrode_safety"] is False


def test_exhausted_defers_discretionary_keeps_execution_path():
    r = run_orgctl(
        "route", "--task-class", "bounded", "--risk", "R2",
        "--grok-capacity", "exhausted", "--json",
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["capacity_overrode_safety"] is False
    assert data["persistent_participation"]["implementer"] == "required"
    assert data["persistent_participation"]["product"] == "deferred_optional"
    assert data["decision"] in {
        "SELF",
        "SELF_preferred_unless_expected_value",
        "SELF_or_owner_configured_known_capable",
        "eligible_profile_by_measured_fit",
    }
    assert data.get("execution_capacity_note") or any(
        "exhausted" in x.lower() for x in (data.get("rationale") or [])
    )


def test_agents_md_has_participation_invariant():
    text = (ROOT / "AGENTS.md").read_text()
    assert "demand-driven" in text.lower()
    assert "never weaken mandatory" in text.lower() or "mandatory governance" in text.lower()


def test_executor_routing_doc_covers_participation():
    text = (ROOT / "docs/EXECUTOR_ROUTING.md").read_text().lower()
    for topic in (
        "demand-driven",
        "participation",
        "ceremony",
        "capacity",
        "precedence",
    ):
        assert topic in text, topic


def test_validate_detects_demand_driven_disabled(repo_copy):
    pp = repo_copy / "routing" / "participation-policy.yaml"
    data = yaml.safe_load(pp.read_text())
    data["principles"]["demand_driven"] = False
    pp.write_text(yaml.safe_dump(data, sort_keys=False))
    r = run_orgctl("validate", cwd=repo_copy)
    assert r.returncode != 0
    assert "demand_driven" in r.stdout


def test_validate_detects_capacity_may_lower_assurance(repo_copy):
    pp = repo_copy / "routing" / "participation-policy.yaml"
    data = yaml.safe_load(pp.read_text())
    data["principles"]["capacity_may_lower_assurance"] = True
    pp.write_text(yaml.safe_dump(data, sort_keys=False))
    r = run_orgctl("validate", cwd=repo_copy)
    assert r.returncode != 0
    assert "capacity_may_lower_assurance" in r.stdout


def test_validate_detects_missing_participation_file(repo_copy):
    (repo_copy / "routing" / "participation-policy.yaml").unlink()
    r = run_orgctl("validate", cwd=repo_copy)
    assert r.returncode != 0
    assert "participation-policy" in r.stdout


def test_default_grok_capacity_is_unknown():
    r = run_orgctl("route", "--task-class", "trivial", "--risk", "R0", "--json")
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["grok_capacity"] == "unknown"
    assert data["capacity_overrode_safety"] is False
