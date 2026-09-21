> **SUPERSEDED for current-head disposition.**  
> Authoritative pack is now `evidence/howl-002-assurance-verify-a4c9d09/`  
> Authoritative report: `reports/audits/assurance-verification-HOWL-002-current-head-2026-09-20.md`  
> Tip covered by successor: `a4c9d09b8d770540c7090b109c1eb7eb88fb7239`  
> This file is retained for history (prior tip b7e55fc). Do not treat as AUTHORITATIVE NOW.

---

# HOWL-002 Assurance Verification Evidence Pack

- **Date:** 2026-09-20 (America/Detroit, EDT / UTC-4)
- **PR:** https://github.com/howlcipher/HowlFutureWorks/pull/1
- **Branch:** fix/howl-002-contribution-auto-id
- **Expected tip:** `b7e55fc`
- **Verified tip SHA:** `b7e55fc6c6d1ef751b825c3e26a57c344149e833` (MATCH)
- **Verification checkout:** `/workspace/HowlFutureWorks-howl002` (detached worktree of `origin/pr-1`)
- **Main clone preserved:** `/workspace/HowlFutureWorks` left on local branch tip `a890886` with untracked assurance/roster files untouched
- **Venv:** `/workspace/.venv-hfw` (PyYAML, jsonschema, pytest)
- **Product code:** not modified during verification

## Tip / history

```
b7e55fc fix(HOWL-002): contribution auto-id safe_id compliance
3b9c3bc docs: add HowlFutureWorks Pages site
a154e84 Add durable knowledge and checkpoint policy
3d0e1d8 Publish HowlFutureWorks v0.4.0
```

`git show --stat` at tip: 3 files, +179/-1 — `tools/orgctl.py` (1-line), `tests/test_record_contribution.py` (new), `evidence/work-items/HOWL-002/dev-lead-implementation.md` (new).

## Auto-id code path

- **File:** `tools/orgctl.py`
- **Function:** `record_contribution` (+ `safe_id`)
- **Fix proof:** `strftime('%Y%m%dt%H%M%S')` uses lowercase `t` (was `%Y%m%dT%H%M%S`)
- Excerpt in `excerpts/auto-id-code.txt`

## Checklist (1–8)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `record-contribution` WITHOUT `--id` succeeds and creates auto id | **PASS** | exit 0 → `workforce/contributions/contrib-20260920t220851-bot-devlead-0001.yaml` |
| 2 | Auto id satisfies `safe_id` (lowercase kebab; no uppercase `T`) | **PASS** | cid=`contrib-20260920t220851-bot-devlead-0001`; `safe_id` True; stamp=`20260920t220851`; no `T` |
| 3 | Explicit valid `--id` still works | **PASS** | `--id contrib-howl002-assurance-valid` exit 0 |
| 4 | Explicit invalid `--id` still fails | **PASS** | `--id Contrib-Bad` exit 1; stderr `contribution id must be lowercase kebab-case`; no file written |
| 5 | Schema validation succeeds for written contribution | **PASS** | jsonschema validate vs `schemas/contribution.schema.json` for both samples |
| 6 | Existing tests / validate / audit | **PASS*** | see notes |
| 7 | Diff scope contribution-scoped | **PASS** | only 3 files vs `origin/main`; no unrelated churn |
| 8 | Checkpoint behavior unchanged | **PASS** | orgctl diff is 1-line in `record_contribution` only; `tests/test_checkpoint.py` 34 passed; checkpoint smoke with `--reason periodic` exit 0 |

### Check 6 detail
- `pytest tests/test_record_contribution.py`: **4 passed** (exit 0)
- `orgctl validate`: **VALIDATION PASSED** (exit 0)
- `python -m pytest -q` (full): **75 passed** (exit 0)
- `make audit`: **make binary missing** (exit 127) — Makefile `audit` recipe run manually: validate + pytest + compileall + `git diff --check` all exit 0 → **PASS (manual recipe)**

### Check 7 files vs origin/main
```
A	evidence/work-items/HOWL-002/dev-lead-implementation.md
A	tests/test_record_contribution.py
M	tools/orgctl.py
```
Flag: none — change stayed contribution-scoped (plus Dev Lead evidence + regression tests).

### Check 8 checkpoint
- Diff of `tools/orgctl.py` vs main is solely the contribution auto-id `T`→`t` change.
- `tests/test_checkpoint.py` unchanged vs main; 34 passed.
- Smoke: `orgctl checkpoint bot-devlead-0001 --reason periodic --stable smoke --id howl002-cp-periodic` → exit 0 (throwaway copy; cleaned up).

## Samples (no secrets)

- `samples/contrib-20260920t220851-bot-devlead-0001.yaml`
- `samples/contrib-howl002-assurance-valid.yaml`

CLI mutation tests used throwaway path `/workspace/hfw-howl002-cli-throwaway` (removed after collection). Verification worktree left clean of disposable contributions.

## Dev Lead handoff (not treated as proof)

- Committed on tip: `evidence/work-items/HOWL-002/dev-lead-implementation.md`
- Summary: reports independent repro of uppercase-`T` auto-id failure on main; one-line fix to lowercase `t`; new regression tests; states checkpoint/separation stamps intentionally out of scope; status “handed to Assurance (not declared fully complete)”.
- `workforce/people/*/handoffs/` empty (`.gitkeep` only) on tip.
- Untracked on main clone (not in verification worktree): `reports/work-items/HOWL-002*` etc. — not used as proof.

## Blockers

- None for functional verification.
- Minor env note: `make` not installed on the box; audit recipe executed manually with equivalent success.

## Recommendation (for parent)

**Assurance PASS** — all 8 checks passed on tip `b7e55fc`; original uppercase-`T` auto-id failure is fixed; explicit valid/invalid paths preserved; schema-valid artifacts; tests green; scope contribution-only; checkpoint unchanged.
