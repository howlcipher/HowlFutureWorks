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

Missing durable remote publish of redacted `factory status --json` (and a documented admit path verified end-to-end from Grok). See `reports/work-items/HOWL-011.json`.

## Related open host work — do not duplicate

- `howlcipher/howlplane` PR #122 — ecosystem multi-repository Factory execution (Owner).
