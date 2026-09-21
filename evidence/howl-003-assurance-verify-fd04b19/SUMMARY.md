# HOWL-003 Assurance Verification SUMMARY (AUTHORITATIVE)

- **Date:** 2026-09-20 (America/Detroit, EDT)
- **PR:** https://github.com/howlcipher/HowlFutureWorks/pull/2
- **Branch:** fix/howl-003-dist-pr-checkout
- **Tip SHA:** `fd04b190ffd5c44af5401e3a945cbfff837d2d6e`
- **Base:** `main` @ `3b9c3bc64d4e0bbef3a34637c0b2dd60faf43121`
- **Worktree:** `/workspace/HowlFutureWorks-howl003` (detached at tip)
- **Venv:** `/workspace/.venv-hfw`
- **Product code:** not modified; no push/commit
- **Overall:** **PASS** (checks 1–8)

## Checks

| # | Check | Result |
|---|--------|--------|
| 1 | Reproduce original failure / tip prevents it | **PASS** |
| 2 | Normal local main: dist + verify-dist | **PASS** |
| 3 | PR-like (detached, no local main): dist + verify-dist; main absent after | **PASS** |
| 4 | Bundle advertises refs/heads/main + HEAD; clone -b main matches packaged HEAD | **PASS** |
| 5 | Archive vs bundle tree identity (verify path) | **PASS** |
| 6 | Full pytest + orgctl validate; test_package_release.py | **PASS** |
| 7 | Distribution CI gate not weakened | **PASS** |
| 8 | Scope packaging-only; no HOWL-002/orgctl.py; secret scan clean | **PASS** |

## Check details

### 1 — Original failure + tip fix
- Bare `git bundle create … HEAD main` on detached/no-main fixture: **exit 128**, `fatal: ambiguous argument 'main'`.
- Tip `tools/package_release.py build` on detached/no-main tip-tree fixture: **exit 0**; artifacts written; main not left behind.
- Evidence: `dist-check1-reproduce.log`, `packaging_main_ref-excerpt.txt`.

### 2 — Normal local main
- `make` not installed; ran Makefile recipes manually.
- `python tools/package_release.py build` → exit 0; `verify` → exit 0.
- Evidence: `dist-normal.log`.

### 3 — PR-like checkout
- Detached HEAD at tip; deleted local `main`; build+verify exit 0.
- After packaging: `refs/heads/main` still **ABSENT**.
- Evidence: `dist-pr-like.log`.

### 4 — Bundle refs + clone
- `git bundle list-heads`: HEAD and `refs/heads/main` both at `fd04b19…`.
- `git clone -b main` of bundle → HEAD `fd04b190ffd5c44af5401e3a945cbfff837d2d6e` (matches packaged).
- Evidence: `bundle-heads.txt`, `clone-main-sha.txt`.

### 5 — Archive vs bundle identity
- Covered by `package_release.py verify`: ZIP vs bundle tracked tree byte-for-byte; message `distribution verification passed; ZIP and bundle trees are identical` (both normal and PR-like runs).

### 6 — Tests / validate
- `tests/test_package_release.py`: **3 passed** (incl. `test_package_release_restores_divergent_main`).
- Full pytest: **74 passed**.
- `python tools/orgctl.py validate`: **VALIDATION PASSED**.
- Evidence: `pytest-package-release.txt`, `pytest-full.txt`, `orgctl-validate.txt`.

### 7 — Distribution CI gate
- `.github/workflows/validate.yml` **unchanged** vs `origin/main` in this PR.
- Still has `distribution` job with `make dist` and `make verify-dist`.
- Parent reported GHA `distribution=success` on PR #2; local `gh` not authenticated — could not re-query check_runs.
- Evidence: `workflow-dist-gate.txt`.

### 8 — Scope / secrets
```
A	reports/work-items/HOWL-003.json
A	reports/work-items/HOWL-003/product-definition.md
A	tests/test_package_release.py
M	tools/package_release.py
```
- No `tools/orgctl.py` changes; no HOWL-002 paths.
- Secret pattern scan on new/changed files: **CLEAN**.
- Evidence: `files-changed-vs-main.txt`, `secret-scan.txt`.

## packaging_main_ref / restore behavior
- Context manager temporarily points `refs/heads/main` at packaged HEAD for `git bundle create`, then deletes the ref if it did not exist, or restores previous SHA if it did (covers divergent main).
- Pytest `test_package_release_restores_divergent_main` **PASSED**.

## Recommendation
Assurance verification **PASS**. Safe to proceed with merge review / owner decision. **Owner-complete NOT declared** by this verification.

## Blockers
None for checks 1–8. Informational: `make` missing on verifier (recipes run manually); `gh` unauthenticated (workflow file verified locally; GHA success per parent).
