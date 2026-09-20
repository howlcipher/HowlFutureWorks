# Changelog

## 0.4.0 - 2026-09-19

- Pin current audit dependencies (`PyYAML 6.0.3`, `jsonschema 4.26.0`, `pytest 9.1.1`) and verify dependency health in CI.
- Test both the declared minimum Python 3.11 and Python 3.13; clean-room verify distributions in CI.
- Require deployment reconciliation fields at the workforce-schema level and enforce a 24,000-character employee continuity ceiling.
- Populate staffing approval authority automatically in hire/separation proposals.
- Update Charter Section 23 from a future proposed layout to the repository's actual current structure.
- Adopt **HowlFutureWorks** as the organization identity and `howl-future-works` as the canonical repository/package slug.
- Add machine-readable `organization.yaml`, JSON Schema validation, identity documentation and ADR 0003.
- Harden Grok Bot separation/suspension for current platform behavior: hiding does not stop routines, deleting removes routines, and shared-computer files/sign-ins can remain.
- Classify external/public Bot-template sharing as an approval-gated external action.
- Pin GitHub Actions dependencies to verified immutable commit SHAs and add Dependabot update configuration.
- Make release packaging derive artifact names/prefixes from the project slug instead of hard-coding the former repo name.
- Extend tests/validation for organization identity, platform-offboarding safeguards, and pinned CI actions.
- Replace the stale generated repository map with a semantic map and add v0.4.0 migration/final-audit documentation.
- Produce versioned release artifact names (`howl-future-works-v0.4.0.*`).
- Include a matching `v<version>` tag in the Git bundle when that tag points at the release commit.
- Fix bundle-clone publication instructions so the temporary bundle `origin` cannot collide with the GitHub remote.

## 0.3.0 — 2026-09-19
- Added compact position/company institutional-memory layer for succession without transcript replay.
- Added per-position context character budgets and budget validation.
- Added schemas and validation for employee profiles and the persistent-position manifest.
- Hardened workforce referential integrity: managers, generations, predecessors, events, position state and terminal deployment state.
- Added evidence-based performance policy and performance-review runbook.
- Added `org-status` and employee-history CLI views for staffing operations.
- Removed the last generated Bot-position TODO by requiring an explicit scaffold purpose.
- Added non-secret deployed-worker identity/fingerprint reconciliation fields.
- Added rehire and persistent-position retirement runbooks to complete the lifecycle.
- Expanded clean-room distribution manifest/checksum verification, including byte-for-byte ZIP vs bundle tree comparison.
- Added provider-neutral GitHub publication guidance and private-first release commands.


## 0.2.0 — 2026-09-19
- Added workforce lifecycle with immutable employee IDs and preserved institutional memory.
- Added hire/fire/suspend/reassign/succession runbooks and skills.
- Added workforce/event/contribution/context schemas and validation.
- Distinguished positions/Bot definitions from employee instances.
- Expanded operational runbooks.
- Normalized CHARTER.md Markdown formatting.
- Added reproducible distribution verification.
- Hardened CI defaults.

## 0.1.0 — 2026-09-19
- Initial autonomous organization infrastructure bootstrap.
