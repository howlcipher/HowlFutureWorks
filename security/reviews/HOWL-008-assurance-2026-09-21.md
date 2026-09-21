# HOWL-008 — Assurance security review

**Date:** 2026-09-21 13:23:45 EDT  
**Product tip:** `41a91af6a6432e0df4eeec03f0a93acdb09e3794`  
**PR:** https://github.com/howlcipher/howlboard/pull/8  
**Verdict (dual QA+Security):** PASS  
**Owner-complete:** NOT declared

## Scope

Independent security verification of HOWL-008 navigable informational mission `depends_on` on howlboard tip above. Did not trust implementer evidence alone. Did not merge. Did not start HOWL-009. Did not print secrets. Did not re-pick executor.

## Results

| Control | Result | Evidence |
|---|---|---|
| Untrusted dependency ID → `data-mission-id` via `esc` | **Pass** | `(call esc dep)` in `mission_view.howl`; XSS harness asserts `&lt;script&gt;` in attribute |
| Constant handler; no ID→JS source interpolation | **Pass** | Constant `window.open_mission(this.dataset.missionId)`; render + source guards |
| Hostile / quote-bearing IDs | **Pass** | Quote/`O'Brien` breakout cases in `TestDependsOnRender` |
| App get body structured encode | **Pass** | `encode_json (dict ("id" id))`; `TestOpenMissionUsesEncodeJSON` |
| Honest missing-target failure | **Pass** | App + demo not-found paths; tests PASS |
| Demo read-only / shared renderer | **Pass** | docs tests: shared renderer; no mutating actions |
| HOWL-007 contracts preserved | **Pass** | create/round-trip/empty/DEMO still PASS; server.howl unchanged |
| Secrets in changed files | **Pass** | Independent scan 0 hits (`assurance-secret-scan.txt`) |
| CI green on tip | **Pass** | PR #8 check SUCCESS; headOid matches tip |

## Findings (security-relevant)

None blocking.

## Residual risk

Dependency IDs remain free-form informational strings. Navigation opens whatever ID is stored; missing IDs fail honestly. Operators must not interpret navigable controls as ordering, blocking, authority, or scheduling (copy + docs mitigate). Residual XSS surface is the same esc/data-attribute pattern as mission rows.

## Non-actions

No merge; no HOWL-009; no Owner-complete; no secrets printed; no executor re-pick.
