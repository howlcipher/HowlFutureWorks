"""Runtime Context v2: compiled standing contracts, retrieval triggers, and budgets."""
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

TARGETS = {
    "engineering-manager": 6000,
    "product": 5000,
    "rnd": 5000,
    "dev-lead": 5000,
    "assurance": 5500,
    "auditor": 5500,
}


def y(rel):
    return yaml.safe_load((ROOT / rel).read_text())


def active_positions():
    return [b["id"] for b in y("bots/manifest.yaml")["bots"] if b.get("status") == "active" and b.get("persistent")]


@pytest.fixture
def repo_copy(tmp_path):
    dst = tmp_path / "repo"
    shutil.copytree(
        ROOT,
        dst,
        ignore=shutil.ignore_patterns(".git", "build", "dist", "__pycache__", ".pytest_cache", ".venv"),
    )
    return dst


def run_orgctl(repo, *args):
    return subprocess.run(
        [sys.executable, str(repo / "tools" / "orgctl.py"), *args],
        cwd=repo,
        capture_output=True,
        text=True,
    )


def edit_yaml(path, fn):
    data = yaml.safe_load(path.read_text())
    fn(data)
    path.write_text(yaml.safe_dump(data, sort_keys=False))


def render(bid):
    return orgctl.format_runtime_contract(orgctl.compile_runtime_contract(bid))


# --- generation, coverage, determinism, size -------------------------------------------------


def test_every_active_persistent_position_has_a_runtime_contract():
    ids = active_positions()
    assert set(ids) == set(TARGETS), "update TARGETS when positions change"
    for bid in ids:
        c = orgctl.compile_runtime_contract(bid)
        assert c["position"]["id"] == bid
        assert orgctl.contract_guarantee_errors(c) == []


@pytest.mark.parametrize("bid,target", sorted(TARGETS.items()))
def test_runtime_contract_meets_size_target(bid, target):
    size = len(render(bid))
    assert size <= target, (bid, size, target)
    assert size <= y(f"bots/{bid}/context.yaml")["standing_budget_chars"]


def test_rendering_is_deterministic():
    for bid in active_positions():
        assert render(bid) == render(bid)


def test_render_bot_output_is_byte_identical_across_runs(repo_copy):
    r1 = run_orgctl(repo_copy, "render-bot", "engineering-manager")
    first = (repo_copy / "build/bots/engineering-manager.md").read_bytes()
    r2 = run_orgctl(repo_copy, "render-bot", "engineering-manager")
    assert r1.returncode == 0 and r2.returncode == 0, r1.stderr + r2.stderr
    assert r1.stdout == r2.stdout
    assert (repo_copy / "build/bots/engineering-manager.md").read_bytes() == first


def test_runtime_contract_is_not_a_concatenation_of_sources():
    text = render("engineering-manager")
    assert "## SOURCE:" not in text
    for rel in ("AGENTS.md", "ORG.md", "policies/workforce.yaml", "policies/memory.yaml"):
        body = (ROOT / rel).read_text()
        assert body not in text, rel
        assert rel in text, f"{rel} must remain referenced for retrieval"


# --- required governance fields -------------------------------------------------------------


def test_contract_carries_required_governance_structurally():
    for bid in active_positions():
        c = orgctl.compile_runtime_contract(bid)
        ids = {i["id"] for i in c["invariants"]}
        assert set(orgctl.REQUIRED_RUNTIME_INVARIANTS) <= ids
        assert c["position"]["risk_ceiling"] == next(
            b["risk_ceiling"] for b in y("bots/manifest.yaml")["bots"] if b["id"] == bid
        )
        assert c["boundaries"]["self_authority_change"] == "forbidden"
        assert c["boundaries"]["fail_closed_on_missing_required_approval"] is True
        assert c["capabilities"]["can_self_escalate"] is False
        assert c["task_lifecycle"]["store_chain_of_thought"] == "forbidden"
        assert c["continuity"]["standing_context_includes_employee_history"] is False
        names = {t["name"]: t["sources"] for t in c["triggers"]}
        for trig, srcs in orgctl.REQUIRED_TRIGGER_SOURCES.items():
            assert set(srcs) <= set(names[trig]), (bid, trig)


def test_rendered_contract_states_risk_ceiling_and_every_invariant():
    policy = y("policies/runtime-contract.yaml")
    for bid in active_positions():
        text = render(bid)
        c = orgctl.compile_runtime_contract(bid)
        assert f"Risk ceiling: {c['position']['risk_ceiling']}" in text
        for inv in policy["invariants"]:
            assert inv["text"] in text, (bid, inv["id"])


def test_engineering_manager_is_a_delegating_coordinator():
    ctx = y("bots/engineering-manager/context.yaml")
    assert ctx["execution_profile"] == "coordinator"
    text = render("engineering-manager")
    assert "Delegate to Dev Lead" in text
    assert "implementation heavy work" in text


def test_guarantee_check_detects_missing_invariant_and_weakened_boundary():
    c = orgctl.compile_runtime_contract("dev-lead")
    c["invariants"] = [i for i in c["invariants"] if i["id"] != "no_self_escalation"]
    c["boundaries"]["fail_closed_on_missing_required_approval"] = False
    errs = orgctl.contract_guarantee_errors(c)
    assert any("no_self_escalation" in e for e in errs)
    assert any("fail closed" in e for e in errs)


# --- validate: failure modes ----------------------------------------------------------------


def test_repository_validates():
    r = subprocess.run([sys.executable, str(ROOT / "tools/orgctl.py"), "validate"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout


def test_validate_fails_when_required_invariant_removed(repo_copy):
    edit_yaml(
        repo_copy / "policies/runtime-contract.yaml",
        lambda d: d.__setitem__("invariants", [i for i in d["invariants"] if i["id"] != "fail_closed_approvals"]),
    )
    r = run_orgctl(repo_copy, "validate")
    assert r.returncode != 0
    assert "fail_closed_approvals" in r.stdout


def test_validate_fails_when_required_policy_reference_missing(repo_copy):
    def drop(d):
        t = d["triggers"]["authority_question"]
        t["required_sources"] = [s for s in t["required_sources"] if s != "policies/approvals.yaml"]

    edit_yaml(repo_copy / "policies/runtime-contract.yaml", drop)
    r = run_orgctl(repo_copy, "validate")
    assert r.returncode != 0
    assert "authority_question" in r.stdout and "policies/approvals.yaml" in r.stdout


def test_validate_fails_when_referenced_policy_file_deleted(repo_copy):
    (repo_copy / "policies/evidence.yaml").unlink()
    r = run_orgctl(repo_copy, "validate")
    assert r.returncode != 0
    assert "policies/evidence.yaml" in r.stdout


def test_validate_fails_on_unknown_trigger(repo_copy):
    edit_yaml(repo_copy / "bots/product/context.yaml", lambda d: d["retrieve_when"].__setitem__("whenever_bored", ["README.md"]))
    r = run_orgctl(repo_copy, "validate")
    assert r.returncode != 0
    assert "unknown retrieval trigger whenever_bored" in r.stdout


def test_validate_fails_on_missing_trigger_path(repo_copy):
    edit_yaml(repo_copy / "bots/product/context.yaml", lambda d: d["retrieve_when"]["domain_reference"].append("product/nope.md"))
    r = run_orgctl(repo_copy, "validate")
    assert r.returncode != 0
    assert "product/nope.md" in r.stdout


def test_validate_fails_when_required_trigger_absent(repo_copy):
    edit_yaml(repo_copy / "bots/auditor/context.yaml", lambda d: d["retrieve_when"].pop("authority_question"))
    r = run_orgctl(repo_copy, "validate")
    assert r.returncode != 0
    assert "auditor retrieve_when missing required trigger authority_question" in r.stdout


def test_validate_requires_capability_coupled_triggers(repo_copy):
    edit_yaml(repo_copy / "bots/engineering-manager/context.yaml", lambda d: d["retrieve_when"].pop("staffing_change"))
    r = run_orgctl(repo_copy, "validate")
    assert r.returncode != 0
    assert "can_manage_workforce_records" in r.stdout and "staffing_change" in r.stdout


def test_validate_rejects_legacy_v1_context_keys(repo_copy):
    edit_yaml(repo_copy / "bots/rnd/context.yaml", lambda d: d.__setitem__("always_load", ["AGENTS.md"]))
    r = run_orgctl(repo_copy, "validate")
    assert r.returncode != 0
    assert "legacy v1 context schema" in r.stdout


@pytest.mark.parametrize(
    "mutate",
    [
        lambda d: d.__setitem__("standing_budget_chars", "lots"),
        lambda d: d.__setitem__("execution_profile", "freelancer"),
        lambda d: d.__setitem__("retrieve_when", ["CHARTER.md"]),
        lambda d: d.pop("position_knowledge"),
        lambda d: d.__setitem__("schema_version", 3),
    ],
)
def test_validate_rejects_malformed_context(repo_copy, mutate):
    edit_yaml(repo_copy / "bots/rnd/context.yaml", mutate)
    r = run_orgctl(repo_copy, "validate")
    assert r.returncode != 0
    assert "bots/rnd/context.yaml" in r.stdout


def test_oversized_runtime_is_detected_by_validate_and_render(repo_copy):
    kp = repo_copy / "knowledge/positions/product.md"
    text = kp.read_text().replace("## Durable lessons\n", "## Durable lessons\n\n- " + "x" * 1500 + "\n", 1)
    kp.write_text(text)
    r = run_orgctl(repo_copy, "validate")
    assert r.returncode != 0
    assert "product runtime contract exceeds standing_budget_chars" in r.stdout
    r = run_orgctl(repo_copy, "render-bot", "product")
    assert r.returncode != 0
    assert "exceeds budget" in r.stderr


def test_standing_budget_cannot_exceed_global_ceiling(repo_copy):
    edit_yaml(repo_copy / "bots/product/context.yaml", lambda d: d.__setitem__("standing_budget_chars", 9000))
    r = run_orgctl(repo_copy, "validate")
    assert r.returncode != 0
    assert "standing_context_max_chars" in r.stdout


def test_runtime_retry_cap_cannot_exceed_global_retry_cap(repo_copy):
    edit_yaml(repo_copy / "policies/budgets.yaml", lambda d: d["agent_runtime"]["retries"].__setitem__("same_failure_class_max", 5))
    r = run_orgctl(repo_copy, "validate")
    assert r.returncode != 0
    assert "same_failure_class_max" in r.stdout


def test_chain_of_thought_storage_must_stay_forbidden(repo_copy):
    edit_yaml(repo_copy / "policies/runtime-contract.yaml", lambda d: d["task_lifecycle"].__setitem__("store_chain_of_thought", "allowed"))
    r = run_orgctl(repo_copy, "validate")
    assert r.returncode != 0
    assert "store_chain_of_thought" in r.stdout


# --- employee continuity stays out of routine context ---------------------------------------


def test_employee_continuity_is_not_in_normal_runtime(repo_copy):
    before = run_orgctl(repo_copy, "render-bot", "engineering-manager")
    before_text = (repo_copy / "build/bots/engineering-manager.md").read_text()
    marker = "PREDECESSOR-ONLY-HANDOFF-MARKER"
    person = repo_copy / "workforce/people/bot-engmgr-0001"
    (person / "handoffs/2026-09-28-handoff.md").write_text(f"# Handoff\n\n{marker}\n")
    (person / "TENURE.md").write_text((person / "TENURE.md").read_text() + f"\n{marker}\n")
    after = run_orgctl(repo_copy, "render-bot", "engineering-manager")
    assert before.returncode == 0 and after.returncode == 0
    assert before.stdout == after.stdout
    assert (repo_copy / "build/bots/engineering-manager.md").read_text() == before_text
    assert marker not in before_text
    emp = run_orgctl(repo_copy, "render-employee", "bot-engmgr-0001")
    assert emp.returncode == 0, emp.stderr
    assert marker in (repo_copy / "build/workforce/bot-engmgr-0001.md").read_text()


def test_retrieval_triggers_may_not_point_at_employee_continuity(repo_copy):
    edit_yaml(
        repo_copy / "bots/engineering-manager/context.yaml",
        lambda d: d["retrieve_when"]["staffing_change"].append("workforce/people/bot-engmgr-0001/TENURE.md"),
    )
    r = run_orgctl(repo_copy, "validate")
    assert r.returncode != 0
    assert "continuity/build material" in r.stdout


# --- measurement ----------------------------------------------------------------------------


def test_context_report_covers_every_position_with_budget_math():
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools/orgctl.py"), "context-report", "--json"], cwd=ROOT, capture_output=True, text=True
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    rows = {row["position"]: row for row in data["positions"]}
    assert set(rows) == {b["id"] for b in y("bots/manifest.yaml")["bots"]}
    cpt = y("policies/budgets.yaml")["agent_runtime"]["token_estimate_chars_per_token"]
    for bid, row in rows.items():
        assert row["chars"] == len(render(bid))
        assert row["approx_tokens"] == -(-row["chars"] // cpt)
        assert row["budget_percent"] <= 100
