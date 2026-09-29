# HOWL-011 — Product definition

**Status:** Implementation in flight (2026-09-29). Owner prioritized remote status publish + admit path. Factory is running on local host tallgeese. Plane PR https://github.com/howlcipher/howlplane/pull/123 is squash-merged to howlplane main (`c2abe920aa4ef1ee52f8f28a375df8041bac59d4`). Host publish on tallgeese is the remaining gate.  
**Owner:** bot-engmgr-0001  
**Risk:** R2  
**Predecessor:** HOWL-010

## Plane PR merged; host publish remains

- howlplane PR #123 is squash-merged to main: https://github.com/howlcipher/howlplane/pull/123 (`c2abe920aa4ef1ee52f8f28a375df8041bac59d4`; cloud agent https://cursor.com/agents/bc-1dfb7d89-05ef-58f1-bfa1-cbdfd7e0c2e2).
- Remaining gate: the first status publish on the Factory host (tallgeese): `howlplane factory status --publish` writes `factory/status/remote-snapshot.json`. See `runbooks/howlplane-remote-observation.md`.
- Admit path: an exact `Pending` row in `issues.md`, `bugs.md`, or `improvements.md`.
- This repository does not install HowlPlane in Grok and does not compete with howlplane PR #122.

## Problem

Persistent Grok roles do not share a shell with the live HowlPlane Factory. The continuous-improvement campaign workspace (`howlcipher/howlplane` `factory/howl-workspace.yaml`) binds repositories to absolute paths on the Owner host (`/run/media/system/tallgeese/dev/...`). Factory status is a local CLI (`howlplane factory status [--json]`) over XDG/state-dir supervisor state with one lock per campaign. HowlBoard projects evidence ledgers offline (`make import`) and explicitly does not dispatch work to HowlPlane. Installing HowlPlane inside the Grok cloud would create a competing Factory and is out of scope.

## Desired outcome

1. Discover active campaign identity, status, and blockers from durable remote state (Git and/or HowlBoard) without Factory-host shell access.
2. Submit bounded implementation work into the **existing** Factory admission surfaces.
3. Receive results as Git PRs/commits and/or HowlBoard LEDGER-projected missions.
4. Document an interim EM protocol usable before the publish bridge lands.

## Acceptance criteria

1. HFW runbook names Factory host/workspace evidence and forbids a second Grok-local Factory.
2. A redacted durable status artifact at howlplane `factory/status/remote-snapshot.json` (written by `howlplane factory status --publish` on the Factory host) is readable from Git and includes at least: campaign_id, state, current_dispatch (or idle), blockers/`OWNER_REQUIRED`, last tick / last error.
3. Submit path is an exact `Pending` row in `issues.md`, `bugs.md`, or `improvements.md` that the host Factory will pick up.
4. Evidence return path documents Git + HowlBoard LEDGER import.
5. Verification shows remote read of the status artifact and that no second campaign was started from Grok.
6. HowlPlane code changes (if any) are implemented on the Factory host through a governed Plane entrypoint — not a Grok install.
7. Standing context budgets unchanged; `orgctl validate` passes.

## Non-goals

- Grok-cloud HowlPlane/Factory install
- Steady-state SSH/desktop takeover as the observability design
- Competing with howlplane PR #122 or campaign `2026-09-27-continuous-improvement`
- Authority expansion / HowlFrame bypass / multi-tenant Plane SaaS

## Roles

| Role | Needed? |
|---|---|
| EM | Yes — coordination, WI, interim protocol |
| Product | Only if AC wording needs product judgment beyond this draft |
| Dev Lead / HowlPlane implementer | Yes for Plane publish/admit wiring on Factory host |
| Assurance | When security of status snapshot redaction warrants it |
| Auditor | Not default for bounded R2 |

## Routing note

HFW documentation + work-item publish: **SELF**.  
HowlPlane implementation: **HOWLPLANE** on the existing Factory host (`--target self` or ecosystem campaign), after expected value is established. Do not treat missing Grok `howlplane` PATH as permission to install a second Plane.
