import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


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


def run_orgctl(repo, *args):
    return subprocess.run(
        [sys.executable, str(repo / "tools" / "orgctl.py"), *args],
        cwd=repo,
        capture_output=True,
        text=True,
    )


def context_dir(repo, employee_id):
    return repo / "workforce" / "people" / employee_id / "context"


def snapshot_files(repo, employee_id):
    return sorted(p for p in context_dir(repo, employee_id).glob("*.yaml"))


def schema_reasons(repo):
    import json

    schema = json.loads(
        (repo / "schemas" / "context-snapshot.schema.json").read_text()
    )
    return schema["properties"]["reason"]["enum"]


EMPLOYEE = "bot-devlead-0001"
OTHER_EMPLOYEE = "bot-product-0001"


def test_checkpoint_writes_schema_valid_snapshot(repo_copy):
    r = run_orgctl(
        repo_copy,
        "checkpoint",
        EMPLOYEE,
        "--reason",
        "manual",
        "--stable",
        "lesson one",
        "--id",
        "snap-happy-path",
    )
    assert r.returncode == 0, r.stderr
    files = snapshot_files(repo_copy, EMPLOYEE)
    assert len(files) == 1
    data = yaml.safe_load(files[0].read_text())
    assert data["schema_version"] == 1
    assert data["snapshot_id"] == "snap-happy-path"
    assert data["employee_id"] == EMPLOYEE
    assert data["reason"] == "manual"
    assert data["stable_knowledge"] == ["lesson one"]
    assert data["contains_raw_chain_of_thought"] is False


def test_checkpoint_rejects_unknown_employee(repo_copy):
    r = run_orgctl(repo_copy, "checkpoint", "bot-nope-9999", "--reason", "manual")
    assert r.returncode != 0
    assert "unknown employee" in r.stderr


def test_checkpoint_rejects_unknown_reason(repo_copy):
    r = run_orgctl(repo_copy, "checkpoint", EMPLOYEE, "--reason", "bogus-reason")
    assert r.returncode != 0
    assert "reason must be one of" in r.stderr


@pytest.mark.parametrize("reason_index", range(12))
def test_checkpoint_accepts_all_schema_reasons(repo_copy, reason_index):
    reasons = schema_reasons(repo_copy)
    reason = reasons[reason_index]
    r = run_orgctl(
        repo_copy,
        "checkpoint",
        EMPLOYEE,
        "--reason",
        reason,
        "--id",
        f"snap-reason-{reason_index}",
    )
    assert r.returncode == 0, r.stderr
    data = yaml.safe_load(
        (context_dir(repo_copy, EMPLOYEE) / f"snap-reason-{reason_index}.yaml").read_text()
    )
    assert data["reason"] == reason


def test_checkpoint_accepts_owner_as_handoff_target(repo_copy):
    r = run_orgctl(
        repo_copy,
        "checkpoint",
        EMPLOYEE,
        "--reason",
        "handoff",
        "--handoff-to",
        "owner",
        "--id",
        "snap-owner",
    )
    assert r.returncode == 0, r.stderr
    data = yaml.safe_load((context_dir(repo_copy, EMPLOYEE) / "snap-owner.yaml").read_text())
    assert data["handoff_to"] == "owner"


def test_checkpoint_accepts_existing_employee_as_handoff_target(repo_copy):
    r = run_orgctl(
        repo_copy,
        "checkpoint",
        EMPLOYEE,
        "--reason",
        "handoff",
        "--handoff-to",
        OTHER_EMPLOYEE,
        "--id",
        "snap-handoff-real",
    )
    assert r.returncode == 0, r.stderr
    data = yaml.safe_load(
        (context_dir(repo_copy, EMPLOYEE) / "snap-handoff-real.yaml").read_text()
    )
    assert data["handoff_to"] == OTHER_EMPLOYEE


def test_checkpoint_rejects_unknown_handoff_target(repo_copy):
    r = run_orgctl(
        repo_copy,
        "checkpoint",
        EMPLOYEE,
        "--reason",
        "handoff",
        "--handoff-to",
        "bot-nope-9999",
        "--id",
        "snap-bad-handoff",
    )
    assert r.returncode != 0
    assert not snapshot_files(repo_copy, EMPLOYEE)


def test_checkpoint_refuses_to_overwrite_existing_snapshot(repo_copy):
    r1 = run_orgctl(
        repo_copy, "checkpoint", EMPLOYEE, "--reason", "manual", "--id", "snap-dupe"
    )
    assert r1.returncode == 0, r1.stderr
    p = context_dir(repo_copy, EMPLOYEE) / "snap-dupe.yaml"
    before = p.read_text()
    r2 = run_orgctl(
        repo_copy,
        "checkpoint",
        EMPLOYEE,
        "--reason",
        "manual",
        "--id",
        "snap-dupe",
        "--stable",
        "different content",
    )
    assert r2.returncode != 0
    assert "exists" in r2.stderr
    assert p.read_text() == before


def test_checkpoint_rejects_output_exceeding_checkpoint_chars_budget(repo_copy):
    big = "x" * 500
    args = ["checkpoint", EMPLOYEE, "--reason", "manual", "--id", "snap-too-big"]
    for _ in range(20):
        args += ["--stable", big]
    r = run_orgctl(repo_copy, *args)
    assert r.returncode != 0
    assert "checkpoint_chars" in r.stderr
    assert not snapshot_files(repo_copy, EMPLOYEE)


@pytest.mark.parametrize(
    "args",
    [
        ["checkpoint", "bot-nope-9999", "--reason", "manual"],
        ["checkpoint", EMPLOYEE, "--reason", "bogus-reason"],
        [
            "checkpoint",
            EMPLOYEE,
            "--reason",
            "manual",
            "--handoff-to",
            "bot-nope-9999",
        ],
    ],
)
def test_checkpoint_never_writes_file_on_any_validation_failure(repo_copy, args):
    before = snapshot_files(repo_copy, EMPLOYEE)
    r = run_orgctl(repo_copy, *args)
    assert r.returncode != 0
    assert snapshot_files(repo_copy, EMPLOYEE) == before


def test_checkpoint_snapshot_id_is_lowercase_kebab_case(repo_copy):
    r = run_orgctl(repo_copy, "checkpoint", EMPLOYEE, "--reason", "manual")
    assert r.returncode == 0, r.stderr
    files = snapshot_files(repo_copy, EMPLOYEE)
    assert len(files) == 1
    snapshot_id = files[0].stem
    import re

    assert re.fullmatch(r"[a-z0-9][a-z0-9-]{1,63}", snapshot_id)


def test_checkpoint_respects_explicit_id_override(repo_copy):
    r = run_orgctl(
        repo_copy, "checkpoint", EMPLOYEE, "--reason", "manual", "--id", "my-custom-id"
    )
    assert r.returncode == 0, r.stderr
    p = context_dir(repo_copy, EMPLOYEE) / "my-custom-id.yaml"
    assert p.exists()
    data = yaml.safe_load(p.read_text())
    assert data["snapshot_id"] == "my-custom-id"


def test_checkpoint_explicit_id_must_be_kebab_case(repo_copy):
    r = run_orgctl(
        repo_copy, "checkpoint", EMPLOYEE, "--reason", "manual", "--id", "Bad_ID"
    )
    assert r.returncode != 0
    assert not snapshot_files(repo_copy, EMPLOYEE)


def test_checkpoint_does_not_mutate_real_repository():
    real_context_files = [
        p
        for p in (ROOT / "workforce" / "people").glob("*/context/*.yaml")
    ]
    assert real_context_files == []


def test_checkpoint_round_trips_repeated_list_arguments(repo_copy):
    r = run_orgctl(
        repo_copy,
        "checkpoint",
        EMPLOYEE,
        "--reason",
        "manual",
        "--id",
        "snap-lists",
        "--stable",
        "one",
        "--stable",
        "two",
        "--open-work",
        "HOWL-1",
        "--open-work",
        "HOWL-2",
        "--decision",
        "dec-a",
        "--decision",
        "dec-b",
        "--risk",
        "risk-a",
        "--source-ref",
        "ref-a",
        "--source-ref",
        "ref-b",
    )
    assert r.returncode == 0, r.stderr
    data = yaml.safe_load(
        (context_dir(repo_copy, EMPLOYEE) / "snap-lists.yaml").read_text()
    )
    assert data["stable_knowledge"] == ["one", "two"]
    assert data["open_work"] == ["HOWL-1", "HOWL-2"]
    assert data["decisions"] == ["dec-a", "dec-b"]
    assert data["risks"] == ["risk-a"]
    assert data["source_refs"] == ["ref-a", "ref-b"]


def test_checkpoint_created_at_is_timezone_aware_iso(repo_copy):
    from datetime import datetime

    r = run_orgctl(repo_copy, "checkpoint", EMPLOYEE, "--reason", "manual", "--id", "snap-tz")
    assert r.returncode == 0, r.stderr
    data = yaml.safe_load((context_dir(repo_copy, EMPLOYEE) / "snap-tz.yaml").read_text())
    parsed = datetime.fromisoformat(data["created_at"])
    assert parsed.tzinfo is not None


def test_checkpoint_prints_path_chars_and_limit_on_success(repo_copy):
    budgets = yaml.safe_load((repo_copy / "policies" / "budgets.yaml").read_text())
    limit = budgets["knowledge_artifacts"]["checkpoint_chars"]
    r = run_orgctl(
        repo_copy, "checkpoint", EMPLOYEE, "--reason", "manual", "--id", "snap-print"
    )
    assert r.returncode == 0, r.stderr
    assert "workforce/people" in r.stdout
    assert "chars=" in r.stdout
    assert f"limit={limit}" in r.stdout


def test_validate_fails_when_bot_always_load_missing_memory_or_budgets_policy(repo_copy):
    ctxp = repo_copy / "bots" / "dev-lead" / "context.yaml"
    ctx = yaml.safe_load(ctxp.read_text())
    ctx["always_load"] = [x for x in ctx["always_load"] if x != "policies/memory.yaml"]
    ctxp.write_text(yaml.safe_dump(ctx, sort_keys=False))
    r = run_orgctl(repo_copy, "validate")
    assert r.returncode != 0
    assert "dev-lead" in r.stdout
    assert "policies/memory.yaml" in r.stdout


def test_validate_fails_when_context_checkpoint_threshold_percent_out_of_range(repo_copy):
    bp = repo_copy / "policies" / "budgets.yaml"
    bud = yaml.safe_load(bp.read_text())
    bud["defaults"]["context_checkpoint_threshold_percent"] = 10
    bp.write_text(yaml.safe_dump(bud, sort_keys=False))
    r = run_orgctl(repo_copy, "validate")
    assert r.returncode != 0
    assert "context_checkpoint_threshold_percent" in r.stdout


def test_validate_fails_when_position_knowledge_file_exceeds_budget(repo_copy):
    kp = repo_copy / "knowledge" / "positions" / "dev-lead.md"
    kp.write_text("x" * 9000)
    r = run_orgctl(repo_copy, "validate")
    assert r.returncode != 0
    assert "position_knowledge_file_chars" in r.stdout


def test_validate_fails_when_handoff_file_exceeds_handoff_chars_budget(repo_copy):
    hp = repo_copy / "workforce" / "people" / EMPLOYEE / "handoffs" / "oversized.md"
    hp.write_text("x" * 7000)
    r = run_orgctl(repo_copy, "validate")
    assert r.returncode != 0
    assert "handoff_chars" in r.stdout
