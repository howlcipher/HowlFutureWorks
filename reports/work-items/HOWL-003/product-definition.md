# HOWL-003 Product work definition

Status: accepted by Engineering Manager for implementation
Author: bot-product-0001 (Quatre Raberba Winner)
Accepted: 2026-09-21

## Problem
`tools/package_release.py` builds a Git bundle with `git bundle create … HEAD main` so clones can use `git clone -b main`. GitHub Actions `pull_request` checkouts are detached and usually have no local `main` branch. Bundle create then fails (`fatal: ambiguous argument 'main'`), so the distribution CI job is red on every PR even when validate and pytest pass.

## Impact
PRs cannot go green through the existing dist gate. Release-bundle verification is untested on the workflow that actually runs for proposed changes. Push-to-`main` still succeeds, hiding the break until a pull request is opened.

## Reproduction
- Code: `tools/package_release.py` `build()` refs `HEAD` + `main`
- GHA `actions/checkout` on `pull_request` with `fetch-depth: 0`: detached HEAD, no `refs/heads/main`
- `make dist` → `git bundle create dist/howl-future-works-v<version>.bundle HEAD main` exit 128
- Contrast: push to `main` has a local `main` and the same command succeeds

## Expected
Temporarily point `refs/heads/main` at the packaged HEAD during bundle create so the bundle advertises `refs/heads/main` and `git clone -b main` works. Restore the previous `main` SHA afterward, or delete the packaging ref if `main` did not exist. Do not change `tools/orgctl.py`, HOWL-002 files, or the dist CI gate.

## Acceptance criteria
1. Bundle create succeeds on detached checkout with no local `main`
2. Bundle advertises HEAD and `refs/heads/main` at packaged HEAD
3. `git clone -b main` of the bundle checks out packaged HEAD
4. Pre-existing (including divergent) local `main` is restored after packaging
5. Absent local `main` stays absent after packaging
6. On-main packaging path still works
7. Dist CI gate kept
8. Regression tests cover local main, detached/no-main, and divergent main restore

## Non-goals
`orgctl.py` changes; HOWL-002 / PR #1; removing dist CI; version bump; ZIP/checksum format changes.
