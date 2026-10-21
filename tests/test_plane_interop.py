"""The HowlPlane commands HowlFutureWorks lists must exist in HowlPlane.

`orgctl check-plane` judges routing/execution-substrate.yaml against HowlPlane's
howl.interop/v1 descriptor (`howlplane interop --json`), so a listed command or
flag HowlPlane does not offer is caught instead of failing when first used.
"""
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


def interfaces():
    return yaml.safe_load((ROOT / "routing/execution-substrate.yaml").read_text())["verified_interfaces"]


def descriptor_offering(listed):
    """A synthetic HowlPlane descriptor that offers exactly the given command strings."""
    commands = {}
    for item in listed:
        words = item.split()[1:]
        path = tuple(w for w in words if not w.startswith("-"))
        commands.setdefault(path, set()).update(w for w in words if w.startswith("-"))
    return {"schema": "howl.interop/v1", "component": "howlplane", "version": "0.1.0",
            "commands": [{"path": list(p), "flags": sorted(f), "json": False} for p, f in commands.items()],
            "exit_codes": {"0": "ok"}}


def test_every_listed_command_is_checked():
    listed = orgctl.plane_command_strings(interfaces())
    assert "howlplane factory queue --retry" in listed
    assert all(item.startswith("howlplane ") for item in listed)
    assert orgctl.check_plane_commands(interfaces(), descriptor_offering(listed)) == []


def test_a_command_howlplane_does_not_offer_is_reported():
    listed = orgctl.plane_command_strings(interfaces())
    plane = descriptor_offering([c for c in listed if c != "howlplane factory queue --retry"] + ["howlplane factory queue"])
    stale = dict(interfaces(), commands=list(interfaces()["commands"]) + ["howlplane factory retry"])
    problems = orgctl.check_plane_commands(stale, plane)
    assert any("no command `factory retry`" in p for p in problems)
    assert any("does not accept --retry" in p for p in problems)


def test_a_non_howlplane_descriptor_is_rejected():
    assert orgctl.check_plane_commands(interfaces(), {"schema": "howl.interop/v1", "component": "howlwriter"})


def test_cli_exit_codes(tmp_path):
    good = tmp_path / "plane.json"
    good.write_text(json.dumps(descriptor_offering(orgctl.plane_command_strings(interfaces()))))
    run = lambda *a: subprocess.run([sys.executable, str(ROOT / "tools/orgctl.py"), "check-plane", *a],
                                    capture_output=True, text=True, cwd=ROOT)
    ok = run("--descriptor", str(good), "--json")
    assert ok.returncode == 0 and json.loads(ok.stdout)["ok"] is True
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(descriptor_offering(["howlplane work"])))
    assert run("--descriptor", str(bad)).returncode == 1
    assert run("--descriptor", str(tmp_path / "missing.json")).returncode == 2


@pytest.mark.skipif(not shutil.which("howlplane"), reason="no howlplane on PATH")
def test_against_the_installed_howlplane_when_it_has_a_descriptor():
    done = subprocess.run(["howlplane", "interop", "--json"], capture_output=True, text=True, check=False)
    if done.returncode != 0:
        pytest.skip("installed howlplane predates `interop --json`")
    assert orgctl.check_plane_commands(interfaces(), json.loads(done.stdout)) == []
