"""HOWL-005: deterministic executor routing policy and tooling."""
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


def test_routing_files_exist():
    for rel in [
        "routing/task-classes.yaml",
        "routing/selection-policy.yaml",
        "routing/capability-registry.yaml",
        "routing/routing-policy.yaml",
        "routing/fallback-policy.yaml",
        "routing/README.md",
        "routing/decision-records/README.md",
        "routing/decision-records/TEMPLATE.md",
        "docs/EXECUTOR_ROUTING.md",
        "EVALS.md",
        "reports/work-items/HOWL-005.json",
        "reports/work-items/HOWL-005/product-definition.md",
        "reports/work-items/HOWL-005/em-acceptance.md",
        "reports/work-items/HOWL-005/security-review.md",
    ]:
        assert (ROOT / rel).exists(), rel


def test_registry_membership_includes_astra_and_prior_executors():
    ids = [e["id"] for e in y("routing/capability-registry.yaml")["executors"]]
    assert ids == ["claude", "codex", "agy", "astra"] or set(ids) >= {
        "claude",
        "codex",
        "agy",
        "astra",
    }
    assert len(ids) == len(set(ids))
    for ex in y("routing/capability-registry.yaml")["executors"]:
        assert ex["status"] in {"available-if-configured", "available", "unavailable"}
        assert ex["benchmark_status"] in {
            "needs-local-eval",
            "evaluated",
            "baseline-evaluated",
            "partially-evaluated",
            "blocked",
            "unknown",
            "stale",
        }
        # Honesty: no fabricated numeric scores in registry entries
        for k, v in ex.items():
            if isinstance(v, (int, float)) and k not in {"version"}:
                pytest.fail(f"unexpected numeric capability field {k}={v}")


def test_trivial_and_simple_default_to_self():
    classes = y("routing/task-classes.yaml")["classes"]
    assert classes["trivial"]["default_executor"] == "SELF"
    assert classes["simple"]["default_executor"] == "SELF"
    for cid in ("trivial", "simple", "bounded", "complex", "critical"):
        assert cid in classes


def test_complexity_does_not_override_risk():
    rules = y("routing/task-classes.yaml")["rules"]
    assert rules["complexity_does_not_override_risk"] is True
    assert (ROOT / rules["risk_policy_source"]).exists()
    assert y("routing/routing-policy.yaml")["rules"]["complexity_does_not_override_risk"] is True


def test_selection_neutrality_forbids_loyalty_and_rankings():
    p = y("routing/selection-policy.yaml")["principles"]
    assert p["provider_loyalty"] == "forbidden"
    assert p["permanent_ranking"] == "forbidden"
    assert p["self_preferred_when_sufficient"] is True
    assert p["external_requires_expected_value"] is True
    assert p["least_resource_intensive_sufficient"] is True
    assert p["quality_over_cost_when_failure_material"] is True
    assert p["invent_capability_scores"] == "forbidden"
    rr = y("routing/routing-policy.yaml")["rules"]
    assert rr["provider_loyalty"] == "forbidden"
    assert rr["permanent_ranking"] == "forbidden"


def test_quota_states_and_exclusions():
    sel = y("routing/selection-policy.yaml")
    assert set(sel["quota_states"]) == {
        "healthy",
        "constrained",
        "scarce",
        "exhausted",
        "unknown",
    }
    assert sel["principles"]["multi_model_fan_out"] == "not_normalized"
    fb = y("routing/fallback-policy.yaml")["fallback_behavior"]
    assert fb["blind_retry"] == "forbidden"
    assert fb["multi_model_fan_out"] == "not_normalized"
    assert fb["max_retries_per_failure_class"] == 2
    assert fb["preserve_assurance_and_approvals"] is True


def test_uncertainty_honesty_no_invented_scores():
    sel = y("routing/selection-policy.yaml")
    assert sel["principles"]["invent_capability_scores"] == "forbidden"
    assert sel["cold_start"]["never_auto_pick_most_expensive_when_evidence_missing"] is True
    r = run_orgctl("route", "--task-class", "critical", "--risk", "R4", "--json")
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["model_invoke"] is False
    # After HOWL-006 baseline-evaluated evidence, critical may select measured-fit
    # without inventing scores/rankings. Cold-start "evidence-insufficient" remains
    # when no measured evidence exists (see test_cold_start_without_baseline).
    assert data["result"] in {"evidence-insufficient", "selected"}
    joined = " ".join(data.get("rationale") or []).lower()
    if data["result"] == "evidence-insufficient":
        assert "invent" in joined or data.get("uncertainty")
    else:
        assert data["decision"] == "eligible_profile_by_measured_fit"
        assert "loyalty" in joined or "ranking" in joined or "measured" in joined
        # Honesty: no numeric scores invented in route payload
        blob = json.dumps(data)
        assert "score" not in blob.lower() or "invent" in joined


def test_cold_start_without_baseline(repo_copy):
    """With benchmarks blocked/needs-local-eval, critical stays evidence-insufficient."""
    import yaml
    reg_path = repo_copy / "routing" / "capability-registry.yaml"
    reg = yaml.safe_load(reg_path.read_text())
    for ex in reg["executors"]:
        ex["benchmark_status"] = "needs-local-eval"
    reg_path.write_text(yaml.safe_dump(reg, sort_keys=False))
    r = run_orgctl("route", "--task-class", "critical", "--risk", "R4", "--json", cwd=repo_copy)
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["model_invoke"] is False
    assert data["result"] == "evidence-insufficient"
    assert "invent" in " ".join(data["rationale"]).lower() or data.get("uncertainty")


def test_privilege_howlframe_recursive_defaults():
    sec = y("routing/selection-policy.yaml")["security"]
    assert sec["howlframe_bypass"] == "forbidden"
    assert sec["child_privilege_may_exceed_parent"] is False
    assert sec["secrets_in_routing_config"] == "forbidden"
    assert sec["fallback_may_lower_assurance"] is False
    assert y("routing/selection-policy.yaml")["recursive_delegation"]["default"] == "off"
    ta = y("policies/tool-access.yaml")["rules"]
    assert ta["direct_executor_cli_bypass_of_howlframe"] == "forbidden"
    assert ta["child_worker_may_exceed_parent_scope"] is False
    ver = y("routing/selection-policy.yaml")["verification"]
    assert ver["critical_requires_independent"] is True
    assert ver["builder_not_sole_verifier"] is True
    assert y("routing/task-classes.yaml")["classes"]["critical"]["independent_verification"] == "required"


def test_agents_md_has_routing_invariant():
    text = (ROOT / "AGENTS.md").read_text()
    assert "## Executor routing" in text
    assert "loyalty" in text.lower() or "rankings" in text.lower()
    assert "ordinary work" in text.lower() or "Persistent members" in text


def test_route_trivial_selects_self():
    r = run_orgctl("route", "--task-class", "trivial", "--risk", "R1", "--json")
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["decision"] == "SELF"
    assert data["result"] == "selected"
    assert data["deterministic"] is True


def test_route_simple_selects_self():
    r = run_orgctl("route", "--task-class", "simple", "--risk", "R2")
    assert r.returncode == 0, r.stderr
    assert "decision: SELF" in r.stdout


def test_validate_detects_missing_astra(repo_copy):
    reg_path = repo_copy / "routing" / "capability-registry.yaml"
    reg = yaml.safe_load(reg_path.read_text())
    reg["executors"] = [e for e in reg["executors"] if e["id"] != "astra"]
    reg_path.write_text(yaml.safe_dump(reg, sort_keys=False))
    r = run_orgctl("validate", cwd=repo_copy)
    assert r.returncode != 0
    assert "astra" in r.stdout.lower()


def test_validate_detects_loyalty_enabled(repo_copy):
    sel_path = repo_copy / "routing" / "selection-policy.yaml"
    sel = yaml.safe_load(sel_path.read_text())
    sel["principles"]["provider_loyalty"] = True
    sel_path.write_text(yaml.safe_dump(sel, sort_keys=False))
    r = run_orgctl("validate", cwd=repo_copy)
    assert r.returncode != 0
    assert "provider_loyalty" in r.stdout


def test_validate_detects_recursive_default_on(repo_copy):
    sel_path = repo_copy / "routing" / "selection-policy.yaml"
    sel = yaml.safe_load(sel_path.read_text())
    sel["recursive_delegation"]["default"] = "on"
    sel_path.write_text(yaml.safe_dump(sel, sort_keys=False))
    r = run_orgctl("validate", cwd=repo_copy)
    assert r.returncode != 0
    assert "recursive_delegation" in r.stdout


def test_validate_detects_duplicate_executor_ids(repo_copy):
    reg_path = repo_copy / "routing" / "capability-registry.yaml"
    reg = yaml.safe_load(reg_path.read_text())
    reg["executors"].append(dict(reg["executors"][0]))
    reg_path.write_text(yaml.safe_dump(reg, sort_keys=False))
    r = run_orgctl("validate", cwd=repo_copy)
    assert r.returncode != 0
    assert "duplicate" in r.stdout.lower()


def test_validate_detects_howlframe_bypass_weakened(repo_copy):
    ta_path = repo_copy / "policies" / "tool-access.yaml"
    ta = yaml.safe_load(ta_path.read_text())
    ta["rules"]["direct_executor_cli_bypass_of_howlframe"] = "allowed"
    ta_path.write_text(yaml.safe_dump(ta, sort_keys=False))
    r = run_orgctl("validate", cwd=repo_copy)
    assert r.returncode != 0
    assert "HowlFrame" in r.stdout or "howlframe" in r.stdout.lower()


def test_fields_to_maintain_present_for_future_profiles():
    fields = y("routing/capability-registry.yaml")["fields_to_maintain"]
    for f in (
        "reliability",
        "latency",
        "cost_or_usage",
        "quota_state",
        "context_capacity",
        "known_failure_modes",
        "allowed_risk_classes",
        "last_evaluated_at",
    ):
        assert f in fields


def test_evals_doc_points_at_registry_population():
    text = (ROOT / "EVALS.md").read_text()
    assert "capability-registry" in text
    assert "needs-local-eval" in text or "fields_to_maintain" in text
    assert "HOWL-005" in text or "fabricate" in text.lower()


def test_executor_routing_doc_covers_required_topics():
    text = (ROOT / "docs/EXECUTOR_ROUTING.md").read_text().lower()
    for topic in [
        "persistent",
        "ephemeral",
        "self",
        "delegate",
        "task class",
        "risk",
        "registry",
        "selection",
        "quota",
        "fallback",
        "recursive",
        "independent verification",
        "cold-start",
        "cold start",
        "evaluation",
        "credential",
    ]:
        # cold-start may be hyphenated
        if topic in ("cold start",):
            continue
        assert topic in text or topic.replace("-", " ") in text, topic


def test_security_review_covers_owner_challenges():
    text = (ROOT / "reports/work-items/HOWL-005/security-review.md").read_text().lower()
    for needle in [
        "prompt injection",
        "privilege",
        "risk downgrade",
        "recursive",
        "secret",
        "quota",
        "self-verify",
        "untrusted",
        "fan-out",
    ]:
        assert needle in text, needle
