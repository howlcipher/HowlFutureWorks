# HOWL-002 Product work definition

Status: accepted by Engineering Manager for implementation
Author: bot-product-0001 (Quatre Raberba Winner)
Accepted: 2026-09-20

## Problem
`orgctl record-contribution` without `--id` auto-generates `contrib-{YYYYMMDDTHHMMSS}-{employee_id}` using uppercase `T`. `safe_id()` requires lowercase kebab-case, so the default path always fails before writing.

## Impact
Contribution recording (durable org control) cannot use the intended default path; only callers who supply a valid `--id` succeed.

## Reproduction
- Code: `tools/orgctl.py` record_contribution + safe_id
- Contrast: checkpoint already uses lowercase `t`
- Auto without `--id`: exit 1, safe_id message
- Explicit valid `--id`: success
- Explicit invalid `--id`: rejected

## Expected
Auto path creates schema-valid contribution with safe_id-compliant id; explicit valid/invalid behavior unchanged; existing records compatible; unrelated ID formats unchanged unless shared helper demonstrably required.

## Acceptance criteria
1. Auto path creates schema-valid contribution
2. Auto ID satisfies safe_id
3. Explicit valid `--id` works
4. Explicit invalid `--id` rejected
5. Existing contributions compatible
6. No unrelated identifier format changes (prefer contribution-only fix)
7. Regression coverage prevents recurrence

## Non-goals
General orgctl refactor; unnecessary checkpoint changes; drive-by cleanup; release solely for this; open discovery/Board; prescribing a specific patch.
