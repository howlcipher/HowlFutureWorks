# Assurance Verification — HOWL-003 (2026-09-20)

**Role:** Independent Assurance (QA + Security dual sections)  
**Subject:** PR #2 `fix/howl-003-dist-pr-checkout` @ `fd04b190ffd5c44af5401e3a945cbfff837d2d6e`  
**Base:** `main` @ `3b9c3bc`  
**Evidence dir:** `evidence/howl-003-assurance-verify-fd04b19/`  
**Owner-complete:** **NOT declared**

## Overall: PASS

All eight delegated checks passed. Product code under test was not modified; no push/commit performed. Evidence written under the main clone paths only.

---

## QA

### Intent
HOWL-003 fixes release packaging when GitHub Actions (or any) checkouts are detached and lack a local `main`, so `git bundle create … HEAD main` no longer fails with ambiguous/missing `main`. Temporary `packaging_main_ref` advertises HEAD as `refs/heads/main` for the bundle, then restores or deletes the ref.

### Verification performed
1. **Failure reproduction:** bare `git bundle create HEAD main` on detached/no-main → exit 128 (`ambiguous argument 'main'`). Tip `package_release.py build` on equivalent tip-code fixture → exit 0.
2. **Normal main:** build + verify recipes succeed with local `main` at tip.
3. **PR-like:** detach, delete `main`, build + verify succeed; `main` remains absent afterward.
4. **Bundle contract:** list-heads shows HEAD + `refs/heads/main`; `git clone -b main` matches packaged tip SHA.
5. **Tree identity:** verify path asserts ZIP ↔ bundle tracked content identity (passed in both dist modes).
6. **Regression:** `tests/test_package_release.py` 3/3 (including divergent-main restore); full suite 74 passed; `orgctl validate` passed.
7. **CI gate:** `validate.yml` distribution job still runs `make dist` / `make verify-dist`; file not weakened by this PR.
8. **Scope:** packaging + work-item docs/tests only.

### QA verdict: PASS

---

## Security

### Threat considerations
- Temporary mutation of `refs/heads/main` during packaging could leave the working repo rewritten if restore failed → covered by finally-block restore/delete and pytest (absent main stays absent; divergent main restored).
- Bundle advertising `main` at packaged HEAD is intentional for consumer `git clone -b main`; does not elevate privileges.
- No credential or network changes in packaging path beyond local git/subprocess.
- Secret pattern scan on PR delta: clean. No orgctl or workforce logic changes.

### Distribution gate integrity
Workflow distribution job unchanged vs main; still requires successful dist+verify. Parent-reported GHA distribution success on PR #2; this verifier could not re-query `gh` (unauthenticated) but confirmed YAML gate presence.

### Security verdict: PASS

---

## Gaps / notes
- Verifier host lacked `make`; recipes invoked directly (equivalent to Makefile targets).
- `gh` auth unavailable for live check_runs reconfirm.
- Shared worktree briefly created/deleted local `main` for checks; restored to `origin/main` after Check 3.

## Recommendation
Merge-ready from Assurance perspective pending Owner. Do not declare owner-complete from this report alone.
