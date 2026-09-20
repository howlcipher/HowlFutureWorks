from pathlib import Path
import json
import tomllib
import yaml
import jsonschema

ROOT=Path(__file__).resolve().parents[1]
_PROJECT_VERSION=tomllib.loads((ROOT/"pyproject.toml").read_text())["project"]["version"]
RISKS={"R0","R1","R2","R3","R4"}
TERMINAL={"terminated","retired","laid_off","replaced","provider_retired"}


def y(rel): return yaml.safe_load((ROOT/rel).read_text())


def test_core_files_exist():
    for p in [
        "organization.yaml","CHARTER.md","AGENTS.md","ORG.md","bots/manifest.yaml","workforce/roster.yaml",
        "policies/risk-tiers.yaml","policies/approvals.yaml","docs/BOOTSTRAP_LIVE_ORG.md",
        "docs/WORKFORCE_LIFECYCLE.md","adr/0002-roles-outlive-workers.md"
    ]:
        assert (ROOT/p).exists(), p


def test_policy_yaml_parses():
    for folder in ["policies","routing"]:
        for p in (ROOT/folder).glob("*.yaml"):
            assert yaml.safe_load(p.read_text()) is not None, p


def test_position_definitions_are_complete_and_consistent():
    m=y("bots/manifest.yaml")
    assert m["version"] >= 2
    assert m["semantics"]["entries_are"] == "persistent_positions_not_employee_history"
    ids=set()
    for bot in m["bots"]:
        bid=bot["id"]
        assert bid not in ids
        ids.add(bid)
        assert bot["risk_ceiling"] in RISKS
        assert bot["seat_limit"] >= 1
        assert bot["staffing_authority"] in {"owner","engineering-manager"}
        base=ROOT/"bots"/bid
        for name in ["README.md","instructions.md","context.yaml","capabilities.yaml","boundaries.yaml","skills.yaml","routines.yaml"]:
            assert (base/name).exists(), f"{bid}: {name}"
        boundary=y(f"bots/{bid}/boundaries.yaml")
        assert boundary["risk_ceiling"] == bot["risk_ceiling"]
        assert boundary["self_authority_change"] == "forbidden"
        caps=y(f"bots/{bid}/capabilities.yaml")
        assert caps["can_self_escalate"] is False


def test_workforce_is_separate_from_positions_and_records_survive():
    positions={b["id"]:b for b in y("bots/manifest.yaml")["bots"]}
    wf=y("workforce/roster.yaml")
    ids=set(); active_counts={}
    assert wf["model"] == "positions_outlive_workers"
    for e in wf["employees"]:
        eid=e["employee_id"]
        assert eid not in ids; ids.add(eid)
        assert e["position_id"] in positions
        rec=ROOT/e["record_path"]
        assert rec.exists(), rec
        assert y(e["record_path"])["employee_id"] == eid
        if e["status"] not in TERMINAL:
            active_counts[e["position_id"]]=active_counts.get(e["position_id"],0)+1
    for pos,count in active_counts.items():
        assert count <= positions[pos]["seat_limit"]


def test_founders_have_hire_events_and_durable_context_dirs():
    wf=y("workforce/roster.yaml")
    events=list((ROOT/"workforce/events").glob("*.yaml"))
    event_employees={y(p)["employee_id"] for p in events if y(p).get("event_type")=="hired"}
    for e in wf["employees"]:
        assert e["employee_id"] in event_employees
        base=ROOT/"workforce/people"/e["employee_id"]
        assert (base/"TENURE.md").exists()
        assert (base/"context/README.md").exists()
        assert (base/"handoffs").exists()
        assert (base/"reviews").exists()


def test_context_always_load_paths_exist():
    for bot in y("bots/manifest.yaml")["bots"]:
        bid=bot["id"]
        ctx=y(f"bots/{bid}/context.yaml")
        for rel in ctx.get("always_load",[]):
            assert "*" not in rel, f"always_load cannot be a wildcard: {bid} {rel}"
            assert (ROOT/rel).exists(), f"{bid} context points to missing {rel}"


def test_organizer_is_not_self_escalating():
    caps=y("bots/engineering-manager/capabilities.yaml")
    bounds=y("bots/engineering-manager/boundaries.yaml")
    assert caps["can_modify_bot_definitions"] is True
    assert caps["can_self_escalate"] is False
    assert bounds["self_authority_change"] == "forbidden"


def test_json_schemas_parse_and_examples_validate():
    for p in (ROOT/"schemas").glob("*.schema.json"):
        schema=json.loads(p.read_text())
        jsonschema.Draft202012Validator.check_schema(schema)
        stem=p.name.replace('.schema.json','')
        ex=ROOT/"schemas/examples"/f"{stem}.json"
        assert ex.exists(), f"missing example for {stem}"
        jsonschema.validate(json.loads(ex.read_text()), schema)


def test_workforce_events_validate():
    schema=json.loads((ROOT/"schemas/employment-event.schema.json").read_text())
    for p in (ROOT/"workforce/events").glob("*.yaml"):
        jsonschema.validate(yaml.safe_load(p.read_text()),schema)


def test_contribution_and_context_directories_are_structured():
    assert (ROOT/"workforce/contributions/README.md").exists()
    assert (ROOT/"templates/context-snapshot.md").exists()
    assert (ROOT/"templates/tenure-summary.md").exists()
    assert (ROOT/"templates/performance-review.md").exists()
    assert (ROOT/"runbooks/fire-worker.md").exists()
    assert (ROOT/"runbooks/suspend-worker.md").exists()
    assert (ROOT/"runbooks/succession.md").exists()


def test_no_obvious_secret_files_or_secret_literals():
    banned_names={".env","id_rsa","id_ed25519","credentials.json","secrets.json"}
    for p in ROOT.rglob("*"):
        if ".git" in p.parts or "build" in p.parts or "dist" in p.parts:
            continue
        if p.is_file():
            assert p.name not in banned_names, p
            if p.suffix.lower() in {".md",".yaml",".yml",".json",".toml",".py"}:
                text=p.read_text(errors="ignore")
                assert ("BEGIN " + "PRIVATE KEY") not in text, p


def test_approval_policy_forbids_self_authority_expansion():
    a=y("policies/approvals.yaml")
    assert a["rules"]["self_approval_for_authority_expansion"] is False
    assert a["rules"]["fail_closed_if_required_approval_unavailable"] is True


def test_charter_markdown_export_artifacts_were_cleaned():
    text=(ROOT/"CHARTER.md").read_text()
    assert "**1\\." not in text
    assert "&nbsp;" not in text
    assert "# 1. Purpose" in text
    assert "# 31. North Star" in text


def test_distribution_tool_exists_and_ci_is_read_only():
    assert (ROOT/"tools/package_release.py").exists()
    workflow=(ROOT/".github/workflows/validate.yml").read_text()
    assert "contents: read" in workflow
    assert "persist-credentials: false" in workflow


def test_protected_positions_require_owner_staffing_authority():
    positions={b["id"]:b for b in y("bots/manifest.yaml")["bots"]}
    assert positions["engineering-manager"]["staffing_authority"] == "owner"
    assert positions["auditor"]["staffing_authority"] == "owner"
    policy=y("policies/workforce.yaml")
    protected=set(policy["staffing"]["protected_positions_requiring_owner_for_permanent_staffing_change"])
    assert {"engineering-manager","auditor"} <= protected


def test_position_knowledge_exists_and_is_in_context():
    manifest=y("bots/manifest.yaml")
    for bot in manifest["bots"]:
        bid=bot["id"]
        kp=ROOT/f"knowledge/positions/{bid}.md"
        assert kp.exists(), kp
        ctx=y(f"bots/{bid}/context.yaml")
        assert str(kp.relative_to(ROOT)) in ctx["always_load"]
        assert isinstance(ctx.get("budget_chars"),int) and ctx["budget_chars"] >= 2000


def test_rendered_contexts_fit_declared_budgets():
    for bot in y("bots/manifest.yaml")["bots"]:
        bid=bot["id"]; ctx=y(f"bots/{bid}/context.yaml")
        total=0
        for rel in ctx["always_load"]:
            total += len((ROOT/rel).read_text())
        for name in ["instructions.md","capabilities.yaml","boundaries.yaml"]:
            total += len((ROOT/f"bots/{bid}/{name}").read_text())
        assert total <= ctx["budget_chars"], (bid,total,ctx["budget_chars"])


def test_employee_profiles_and_position_manifest_have_schemas():
    assert (ROOT/"schemas/employee-profile.schema.json").exists()
    assert (ROOT/"schemas/position-manifest.schema.json").exists()
    profile_schema=json.loads((ROOT/"schemas/employee-profile.schema.json").read_text())
    manifest_schema=json.loads((ROOT/"schemas/position-manifest.schema.json").read_text())
    jsonschema.Draft202012Validator.check_schema(profile_schema)
    jsonschema.Draft202012Validator.check_schema(manifest_schema)
    jsonschema.validate(y("bots/manifest.yaml"),manifest_schema)
    for e in y("workforce/roster.yaml")["employees"]:
        jsonschema.validate(y(e["record_path"]),profile_schema)


def test_performance_policy_is_evidence_based():
    policy=y("policies/performance.yaml")
    assert policy["principles"]["evidence_based"] is True
    assert policy["principles"]["personality_judgments_prohibited"] is True
    assert policy["requirements"]["evidence_refs_required_for_adverse_action"] is True
    assert (ROOT/"runbooks/performance-review.md").exists()


def test_scaffold_source_has_no_todo_placeholder():
    text=(ROOT/"tools/orgctl.py").read_text()
    assert "TODO: define durable ownership" not in text
    assert "--purpose" in text


def test_complete_workforce_lifecycle_runbooks_exist():
    for rel in [
        "runbooks/hire-worker.md","runbooks/fire-worker.md","runbooks/suspend-worker.md",
        "runbooks/reassign-worker.md","runbooks/rehire-worker.md","runbooks/succession.md",
        "runbooks/retire-position.md","runbooks/performance-review.md"
    ]:
        assert (ROOT/rel).exists(), rel


def test_workforce_roster_has_reconciliation_fields():
    schema=json.loads((ROOT/"schemas/workforce-roster.schema.json").read_text())
    props=schema["properties"]["employees"]["items"]["properties"]
    assert "deployment_ref" in props
    assert "deployed_fingerprint" in props
    for e in y("workforce/roster.yaml")["employees"]:
        assert "deployment_ref" in e
        assert "deployed_fingerprint" in e


def test_howlfutureworks_identity_is_canonical():
    org=y("organization.yaml")
    assert org["display_name"] == "HowlFutureWorks"
    assert org["repository_slug"] == "howl-future-works"
    assert org["provider_neutral_design"] is True
    schema=json.loads((ROOT/"schemas/organization.schema.json").read_text())
    jsonschema.validate(org,schema)
    pyproject=(ROOT/"pyproject.toml").read_text()
    assert 'name = "howl-future-works"' in pyproject
    assert 'version = "0.4.1"' in pyproject


def test_all_position_contexts_include_organization_identity():
    for bot in y("bots/manifest.yaml")["bots"]:
        ctx=y(f"bots/{bot['id']}/context.yaml")
        assert "organization.yaml" in ctx["always_load"]


def test_platform_offboarding_safeguards_are_explicit():
    policy=y("policies/workforce.yaml")["platform_offboarding"]
    assert policy["hiding_counts_as_routine_suspension"] is False
    assert policy["archive_required_routine_configuration_before_live_bot_delete"] is True
    assert policy["live_bot_delete_counts_as_access_revocation"] is False
    fire=(ROOT/"runbooks/fire-worker.md").read_text()
    suspend=(ROOT/"runbooks/suspend-worker.md").read_text()
    assert "Hiding the live Grok Bot is not sufficient" in fire
    assert "hiding does not pause routines" in suspend


def test_ci_actions_are_immutable_pins_and_dependabot_exists():
    workflow=(ROOT/".github/workflows/validate.yml").read_text()
    assert "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" in workflow
    assert "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97" in workflow
    assert (ROOT/".github/dependabot.yml").exists()


def test_current_docs_use_howlfutureworks_identity():
    assert "# HowlFutureWorks" in (ROOT/"README.md").read_text()
    assert "# HowlFutureWorks" in (ROOT/"CHARTER.md").read_text()
    assert "howl-future-works" in (ROOT/"docs/PUBLISH_GITHUB.md").read_text()


def test_publish_guide_handles_bundle_origin():
    guide=(ROOT/"docs/PUBLISH_GITHUB.md").read_text()
    assert "git remote remove origin" in guide
    assert "git push origin --tags" in guide
    assert f"howl-future-works-v{_PROJECT_VERSION}.bundle" in guide


def test_dev_dependencies_are_exactly_pinned():
    lines=[x.strip() for x in (ROOT/"requirements-dev.txt").read_text().splitlines() if x.strip()]
    assert lines == ["PyYAML==6.0.3", "jsonschema==4.26.0", "pytest==9.1.1"]


def test_ci_covers_minimum_and_current_python_and_distribution():
    workflow=(ROOT/".github/workflows/validate.yml").read_text()
    assert "'3.11'" in workflow and "'3.13'" in workflow
    assert "make dist" in workflow and "make verify-dist" in workflow
    assert "python -m pip check" in workflow


def test_reconciliation_fields_are_schema_required():
    schema=json.loads((ROOT/"schemas/workforce-roster.schema.json").read_text())
    required=set(schema["properties"]["employees"]["items"]["required"])
    assert {"deployment_ref","deployed_fingerprint"} <= required


def test_employee_continuity_has_explicit_budget():
    org=y("organization.yaml")
    assert 12000 <= org["employee_continuity_budget_chars"] <= 50000
    schema=json.loads((ROOT/"schemas/organization.schema.json").read_text())
    assert "employee_continuity_budget_chars" in schema["required"]


def test_org_status_exposes_staffing_authority_source():
    text=(ROOT/"tools/orgctl.py").read_text()
    assert "STAFFING" in text
    assert "staffing_authority" in text


def test_local_markdown_links_resolve():
    import re
    pattern=re.compile(r'\[[^\]]*\]\(([^)]+)\)')
    broken=[]
    for p in ROOT.rglob('*.md'):
        if any(part in {'.git','build','dist'} for part in p.parts):
            continue
        for match in pattern.finditer(p.read_text(errors='ignore')):
            href=match.group(1).strip().split()[0].strip('<>')
            if href.startswith(('http://','https://','mailto:','#')):
                continue
            href=href.split('#',1)[0]
            if not href:
                continue
            target=(p.parent/href).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                continue
            if not target.exists():
                broken.append((str(p.relative_to(ROOT)),href))
    assert not broken, broken


def test_legacy_repo_slug_only_appears_in_history_or_migration_docs():
    allowed={
        'docs/AUDIT_2026-09-19.md',
        'docs/AUDIT_FINAL_2026-09-19.md',
        'docs/MIGRATION_0.4.0.md',
        'adr/0003-howlfutureworks-identity.md',
    }
    offenders=[]
    for p in ROOT.rglob('*'):
        if not p.is_file() or any(part in {'.git','build','dist','__pycache__','.pytest_cache'} for part in p.parts):
            continue
        rel=str(p.relative_to(ROOT))
        if rel in allowed:
            continue
        if p.suffix.lower() in {'.md','.yaml','.yml','.json','.toml','.py','.txt'} and ('howl' + '-org') in p.read_text(errors='ignore'):
            offenders.append(rel)
    assert not offenders, offenders


def test_charter_describes_repository_as_current_policy_source():
    charter=(ROOT/'CHARTER.md').read_text()
    assert '# 23. Repository Form' in charter
    assert '# 23. Future Repository Form' not in charter
    assert '`howl-future-works` policy repository' in charter


def test_charter_repository_map_matches_implemented_structure():
    charter=(ROOT/'CHARTER.md').read_text()
    for stale in ['PRODUCT_DISCOVERY.md','RND.md','DELIVERY.md','POLICIES/','ROUTING/','SCHEMAS/','RUNBOOKS/']:
        assert stale not in charter
    for current in ['`workforce/`','`knowledge/`','`product/`','`rnd/`','`policies/`','`runbooks/`','`tools/` and `tests/`']:
        assert current in charter
