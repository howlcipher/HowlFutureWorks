import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import jsonschema
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]

SAFE_ID = re.compile(r"[a-z0-9][a-z0-9-]{1,63}")
EMPLOYEE = "bot-devlead-0001"


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


def contribution_schema(repo):
    return json.loads((repo / "schemas" / "contribution.schema.json").read_text())


def load_contribution(path):
    return yaml.safe_load(path.read_text())


def test_record_contribution_auto_id_writes_schema_valid_file(repo_copy):
    r = run_orgctl(
        repo_copy,
        "record-contribution",
        EMPLOYEE,
        "--summary",
        "HOWL-002 regression auto-id",
    )
    assert r.returncode == 0, r.stderr
    rel = r.stdout.strip()
    path = repo_copy / rel
    assert path.exists()
    doc = load_contribution(path)
    jsonschema.validate(doc, contribution_schema(repo_copy))
    cid = doc["contribution_id"]
    assert SAFE_ID.fullmatch(cid)
    assert cid.startswith("contrib-")
    assert cid.endswith(f"-{EMPLOYEE}")
    # stamp segment must use lowercase t (safe_id compliant), not uppercase T
    stamp = cid.removeprefix("contrib-").removesuffix(f"-{EMPLOYEE}")
    assert "T" not in stamp
    assert "t" in stamp
    assert doc["employee_id"] == EMPLOYEE
    assert doc["summary"] == "HOWL-002 regression auto-id"


def test_record_contribution_explicit_valid_id_works(repo_copy):
    cid = "contrib-howl002-explicit-valid"
    r = run_orgctl(
        repo_copy,
        "record-contribution",
        EMPLOYEE,
        "--summary",
        "explicit valid",
        "--id",
        cid,
    )
    assert r.returncode == 0, r.stderr
    path = repo_copy / "workforce" / "contributions" / f"{cid}.yaml"
    assert path.exists()
    doc = load_contribution(path)
    jsonschema.validate(doc, contribution_schema(repo_copy))
    assert doc["contribution_id"] == cid


def test_record_contribution_explicit_invalid_id_rejected(repo_copy):
    r = run_orgctl(
        repo_copy,
        "record-contribution",
        EMPLOYEE,
        "--summary",
        "explicit invalid",
        "--id",
        "Contrib-Bad",
    )
    assert r.returncode != 0
    assert "lowercase kebab-case" in (r.stderr + r.stdout)
    assert not (repo_copy / "workforce" / "contributions" / "Contrib-Bad.yaml").exists()


def test_existing_contribution_records_remain_loadable(repo_copy):
    """Pre-existing contribution docs (if any) still parse and schema-validate."""
    schema = contribution_schema(repo_copy)
    contrib_dir = repo_copy / "workforce" / "contributions"
    yaml_files = sorted(contrib_dir.glob("*.yaml"))
    # README-only is fine; if fixtures exist, they must stay compatible
    for path in yaml_files:
        doc = load_contribution(path)
        jsonschema.validate(doc, schema)
        assert SAFE_ID.fullmatch(doc["contribution_id"])
