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
            ctxp=ROOT/f"bots/{bid}/context.yaml"
            if ctxp.exists():
                ctx=load_yaml(ctxp) or {}
                always=ctx.get("always_load",[])
                for req_policy in ("policies/memory.yaml","policies/budgets.yaml"):
                    if req_policy not in always:
                        errors.append(f"{bid} context.yaml always_load missing {req_policy}")
                kp=ROOT/f"knowledge/positions/{bid}.md"
                pkf_limit=ka.get("position_knowledge_file_chars")
                if kp.exists() and isinstance(pkf_limit,int):
                    size=len(kp.read_text())
                    if size>pkf_limit:
                        errors.append(f"knowledge/positions/{bid}.md exceeds position_knowledge_file_chars: {size}>{pkf_limit}")
                budget=ctx.get("budget_chars")
                if not isinstance(budget,int) or budget<2000:
                    errors.append(f"{bid} context budget_chars must be an integer >= 2000")
                estimated=0
                for rel in ctx.get("always_load",[]):
                    if "*" in rel: errors.append(f"{bid} always_load cannot contain wildcard: {rel}")
                    elif not (ROOT/rel).exists(): errors.append(f"{bid} context missing {rel}")
                    elif (ROOT/rel).is_file(): estimated += len((ROOT/rel).read_text())
                for name in ["instructions.md","capabilities.yaml","boundaries.yaml"]:
                    q=ROOT/f"bots/{bid}/{name}"
                    if q.exists(): estimated += len(q.read_text())
                if isinstance(budget,int) and estimated>budget:
                    errors.append(f"{bid} always-load context exceeds budget: {estimated}>{budget} chars")
            bp=ROOT/f"bots/{bid}/boundaries.yaml"
            if bp.exists():
                bounds=load_yaml(bp) or {}
                if bounds.get("risk_ceiling")!=bot.get("risk_ceiling"): errors.append(f"risk ceiling drift for {bid}")
                if bounds.get("self_authority_change")!="forbidden": errors.append(f"self authority change must be forbidden for {bid}")
        if len(ids)!=len(set(ids)): errors.append("duplicate position/bot ids")
    except Exception as e: errors.append(f"manifest: {e}")

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


def context(bot):
    p=ROOT/f"bots/{bot}/context.yaml"
    if not p.exists(): raise SystemExit(f"unknown position {bot}")
    data=load_yaml(p) or {}
    print(f"budget_chars: {data.get('budget_chars','unset')}")
    for k in ("always_load","load_on_demand"):
        print(f"{k}:")
        for x in data.get(k,[]): print(f"  - {x}")


def render_bot(bot, proposal=False):
    base=ROOT/(f"bots/proposals/{bot}" if proposal else f"bots/{bot}")
    if not base.exists(): raise SystemExit(f"unknown position {bot}")
    ctx=load_yaml(base/"context.yaml") or {}
    parts=[f"# Rendered Position Bundle: {bot}\n"]
    for rel in ctx.get("always_load",[]):
        p=ROOT/rel
        if p.is_file(): parts.append(f"\n---\n## SOURCE: {rel}\n\n{p.read_text()}\n")
    for name in ["instructions.md","capabilities.yaml","boundaries.yaml"]:
        p=base/name
        if p.exists(): parts.append(f"\n---\n## SOURCE: {p.relative_to(ROOT)}\n\n{p.read_text()}\n")
    bundle="".join(parts)
    budget=ctx.get("budget_chars")
    if isinstance(budget,int) and len(bundle)>budget:
        raise SystemExit(f"rendered context for {bot} exceeds budget: {len(bundle)}>{budget} chars")
    out=ROOT/f"build/bots/{bot}.md"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(bundle)
    digest=hashlib.sha256(out.read_bytes()).hexdigest()
    print(f"{out.relative_to(ROOT)} sha256={digest}")


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
    dump_yaml({"budget_chars":12000,"always_load":["AGENTS.md","organization.yaml",f"roles/{args.role}.md","policies/risk-tiers.yaml"],"load_on_demand":["CHARTER.md","knowledge/company/","runbooks/","workforce/"]},dst/"context.yaml")
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
    now=datetime.now().astimezone(); cid=args.id or f"contrib-{now.strftime('%Y%m%dT%H%M%S')}-{args.employee_id}"
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
    print("2 render active position bundles and current employee continuity bundles")
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
    s=sub.add_parser("scaffold-bot"); s.add_argument("id"); s.add_argument("--name",required=True); s.add_argument("--role",required=True); s.add_argument("--risk",default="R1"); s.add_argument("--purpose",required=True)
    h=sub.add_parser("propose-hire"); h.add_argument('employee_id'); h.add_argument('--name',required=True); h.add_argument('--position',required=True); h.add_argument('--manager',required=True); h.add_argument('--provider',default='grok-bot'); h.add_argument('--predecessor'); h.add_argument('--generation',type=int)
    sp=sub.add_parser("propose-separation"); sp.add_argument('employee_id'); sp.add_argument('--type',required=True); sp.add_argument('--reason',required=True)
    eh=sub.add_parser("employee-history"); eh.add_argument("employee_id")
    rc=sub.add_parser("record-contribution"); rc.add_argument('employee_id'); rc.add_argument('--summary',required=True); rc.add_argument('--id'); rc.add_argument('--work-item'); rc.add_argument('--artifact',action='append'); rc.add_argument('--evidence',action='append'); rc.add_argument('--verified-by')
    cp=sub.add_parser("checkpoint"); cp.add_argument('employee_id'); cp.add_argument('--reason',required=True); cp.add_argument('--stable',action='append',default=[]); cp.add_argument('--open-work',dest='open_work',action='append',default=[]); cp.add_argument('--decision',action='append',default=[]); cp.add_argument('--risk',action='append',default=[]); cp.add_argument('--source-ref',dest='source_ref',action='append',default=[]); cp.add_argument('--handoff-to',dest='handoff_to',default=None); cp.add_argument('--id')
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
    if a.cmd=="fingerprints": fingerprints()
    if a.cmd=="bootstrap-plan": bootstrap_plan()
    if a.cmd=="scaffold-bot": scaffold_bot(a)
    if a.cmd=="propose-hire": propose_hire(a)
    if a.cmd=="propose-separation": propose_separation(a)
    if a.cmd=="record-contribution": record_contribution(a)
    if a.cmd=="checkpoint": checkpoint(a)

if __name__=="__main__": main()
