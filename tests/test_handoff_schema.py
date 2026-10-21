"""The organizational handoff carries a versioned schema id (docs/INTEROP.md in howl)."""
import json
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/handoff.schema.json").read_text())
EXAMPLE = json.loads((ROOT / "schemas/examples/handoff.json").read_text())


def test_schema_is_identified_and_example_declares_it():
    assert SCHEMA["$id"] == "howlfutureworks.handoff/v1"
    assert EXAMPLE["schema_version"] == "howlfutureworks.handoff/v1"
    jsonschema.validate(EXAMPLE, SCHEMA)


def test_unversioned_handoffs_still_validate_but_a_wrong_version_does_not():
    legacy = {k: v for k, v in EXAMPLE.items() if k != "schema_version"}
    jsonschema.validate(legacy, SCHEMA)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate({**EXAMPLE, "schema_version": "ai.handoff/v1"}, SCHEMA)
