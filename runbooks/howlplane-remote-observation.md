# HowlPlane remote observation (Grok / non-colocated roles)

Companion to `runbooks/howlplane-recovery.md` and `routing/execution-substrate.yaml`.

## Where the active Factory runs

The live continuous-improvement campaign is defined in `howlcipher/howlplane`:

| Artifact | Location |
|---|---|
| Campaign id | `2026-09-27-continuous-improvement` |
| Contract | `factory/CONTINUOUS_IMPROVEMENT.md` |
| Workspace | `factory/howl-workspace.yaml` |
| Host checkouts (absolute) | `/run/media/system/tallgeese/dev/{howl,howlplane,howlframe,grocery-optimizer}` |
| Product repo | `howlcipher/grocery-optimizer` |

Supervisor state is **host-local** (XDG state home / explicit `--state-dir`) with **one lock per state directory**. A second Factory process against the same campaign is rejected. Do **not** install or start HowlPlane Factory inside the Grok Bot cloud.

Registered Grok desktop `epyon` may be the same operator machine family; connectivity is not guaranteed. Prefer durable artifacts over assuming a live desktop session.

## How EM observes today (interim)

Until HOWL-011 lands a published status snapshot, observe **without** starting Plane:

1. **Campaign contract + workspace** — read `factory/CONTINUOUS_IMPROVEMENT.md` and `factory/howl-workspace.yaml` on `howlcipher/howlplane` main (or the campaign branch).
2. **Mission state** — e.g. `grocery-optimizer` `.product/mission_state.json`, `howlplane` `.dogfood/mission_state.json` (campaign_id, status, next_mission).
3. **Open PRs / recent commits** on the four portfolio repos — proxy for in-flight Factory or Owner work. Do not duplicate those branches.
4. **HowlBoard** — authoritative **work** state when a Board instance is running; LEDGER provenance means projected Plane evidence, not live supervisor status. Board does **not** dispatch.
5. **Local `howlplane factory status`** — only on the Factory host (or after Owner publishes its `--json` output). Not available on the default Grok PATH.

If status is unknown, record `Unknown` and avoid starting competing implementation.

## How EM dispatches work (interim)

Prefer surfaces the **existing** host Factory already understands:

| Mechanism | Use when |
|---|---|
| Git work item / mission / ranked backlog `Pending` row in the target repo | Factory discovery / backlog admission |
| Explicit `howlplane factory queue QUEUE.json` on the Factory host | Owner or host-side operator runs finite queue |
| Owner direction into Factory inbox / `owner_direction` origin | Trusted Owner-authored direction |
| HowlFutureWorks `reports/work-items/HOWL-*.json` | Org desired state + evidence; not a live Plane queue by itself |

Do **not**: start `howlplane factory start` from Grok, spawn a second campaign, or fall back to raw Codex/Claude/AGY as a Plane substitute.

## How results return

| Channel | Role |
|---|---|
| GitHub PRs / commits on the target repo | Primary ship evidence |
| HowlPlane evidence ledger on the Factory host | Authoritative execution evidence |
| HowlBoard `make import LEDGER=...` | Offline projection of ledger → missions (`provenance: LEDGER`) |
| HowlFutureWorks work-item / audit reports | Org checkpoint |

## Gap tracked as HOWL-011

Missing durable remote publish of redacted `factory status --json` (and a documented admit path verified end-to-end from Grok). See `reports/work-items/HOWL-011.json`. Phase is `implementation`: Owner prioritized the publish + admit path on 2026-09-29, and howlplane PR #123 is merged. The gap stays open until the host publish below has actually landed.

## HOWL-011 Plane PR #123 is merged

Plane implementation cloud agent: https://cursor.com/agents/bc-1dfb7d89-05ef-58f1-bfa1-cbdfd7e0c2e2 (`howlcipher/howlplane`). Plane PR https://github.com/howlcipher/howlplane/pull/123 (#123) is squash-merged to howlplane main (`c2abe920aa4ef1ee52f8f28a375df8041bac59d4`). Host publish on tallgeese is the remaining gate. Do not duplicate that branch, and do not compete with PR #122.

Publish from the **Factory host** (tallgeese), not from Grok:

1. Publish the redacted status snapshot with `howlplane factory status --publish`.
2. Durable artifact: `factory/status/remote-snapshot.json` in the howlplane checkout. It carries campaign identity, state, current dispatch or idle, and blockers. Read it from Git after the host commits it.
3. Admit path: an exact `Pending` row in `issues.md`, `bugs.md`, or `improvements.md`. Still do not start a second Factory from Grok.
4. PR URL, publish command, artifact path, and admit path are recorded on HOWL-011 (`reports/work-items/HOWL-011.json`). After the host publish, add evidence that `factory/status/remote-snapshot.json` was read remotely and that no second campaign started.

## Related host work — do not duplicate

- `howlcipher/howlplane` PR #122 — ecosystem multi-repository Factory execution (Owner).
- `howlcipher/howlplane` PR #123 — HOWL-011 remote status publish and Pending admit (https://github.com/howlcipher/howlplane/pull/123). Squash-merged to main at `c2abe920aa4ef1ee52f8f28a375df8041bac59d4`. Remaining gate is host `howlplane factory status --publish`. Distinct from PR #122.
