# HOWL-002 Dev Lead implementation package

Status: implemented; handed to Assurance (not declared fully complete)
Implementer: bot-devlead-0001 (Motoko Kusanagi)
Date: 2026-09-20 (America/Detroit)

## Work item
- Id: HOWL-002
- Title: Fix auto-generated contribution ID failing safe_id validation
- Product definition: reports/work-items/HOWL-002/product-definition.md
- Work item JSON: reports/work-items/HOWL-002.json

## Independent reproduction (before change)
- Repo: /workspace/HowlFutureWorks @ origin/main `3b9c3bc`
- Command: `.venv/bin/python tools/orgctl.py record-contribution bot-devlead-0001 --summary "HOWL-002 independent repro (auto-id)"`
- Observed: exit 1 — `contribution id must be lowercase kebab-case`
- Expected: write schema-valid contribution under workforce/contributions/
- Control valid `--id contrib-howl002-repro-valid`: exit 0 (file removed after repro)
- Control invalid `--id Contrib-Bad`: exit 1, same message

## Root cause
`record_contribution` auto-id used `strftime('%Y%m%dT%H%M%S')` (uppercase `T`). `safe_id()` requires `[a-z0-9][a-z0-9-]{1,63}`, so the default path always failed. Checkpoint already used lowercase `t`; no shared helper required.

## Fix
Contribution-only one-line change in `tools/orgctl.py`: uppercase `T` → lowercase `t` in auto-generated contribution ids. No checkpoint / separation stamp changes.

## Files changed
- `tools/orgctl.py` (auto-id stamp)
- `tests/test_record_contribution.py` (new regression coverage)
- `evidence/work-items/HOWL-002/dev-lead-implementation.md` (this package)

## Tests
Commands:
```
.venv/bin/pytest -q tests/test_record_contribution.py
.venv/bin/pytest -q
```
Results: `tests/test_record_contribution.py` — 4 passed; full suite — see CI/local run output at handoff time.

Coverage maps to AC:
1. Auto path creates schema-valid contribution
2. Auto ID satisfies safe_id
3. Explicit valid `--id` works
4. Explicit invalid `--id` rejected
5. Existing contribution YAMLs (if present) still load/validate
6. Unrelated identifier formats unchanged (separation stamp still uppercase T by design for this change)
7. Regression tests prevent recurrence

## Post-fix smoke
`.venv/bin/python tools/orgctl.py record-contribution bot-devlead-0001 --summary "HOWL-002 post-fix auto-id verify"`
→ wrote `workforce/contributions/contrib-20260920t214533-bot-devlead-0001.yaml`, schema-valid, safe_id True; file removed after smoke (not committed).

## Limitations
- Does not change historical docs that mention uppercase-T examples except via code/tests.
- Separation proposal directory stamps still use uppercase `T` (out of scope; not contribution ids).
- Not declared fully complete pending Assurance review.

## Evidence refs
- reports/work-items/HOWL-002.json
- reports/work-items/HOWL-002/product-definition.md
- evidence/work-items/HOWL-002/dev-lead-implementation.md
