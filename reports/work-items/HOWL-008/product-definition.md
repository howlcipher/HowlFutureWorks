# HOWL-008 — Product definition

Status: Product definition for EM acceptance  
Author: bot-product-0001 (Quatre Raberba Winner)  
Work item: `reports/work-items/HOWL-008.json`  
Org repo: `howlcipher/HowlFutureWorks` @ `27b8528` (branch `feat/howl-008-dependency-navigation`)  
Target product repo: `howlcipher/howlboard` @ `cab020c` (HOWL-007 merged)  
Predecessor: HOWL-007  
Risk: ~R2  

Executor choice is **not** pre-selected — EM routes after these ACs (HOWL-005/006). HOWL-007 SELF success is evidence, not a rule.

## Problem (verified)

HOWL-007 shipped informational `depends_on` and renders IDs in shared `frontend/mission_view.howl` as inert escaped `<code>` text:

```text
<li><code>…esc(dep)…</code></li>
```

Operators can see A→B IDs but cannot follow them. Meanwhile:

- Mission list rows already use `data-mission-id` + constant `onclick="window.open_mission(this.dataset.missionId)"`.
- `frontend/app.howl` and `docs/demo.howl` both expose `open_mission(id)`.
- App `open_mission` currently builds the `/api/missions/get` body via **string concatenation** of JSON (`"{\"id\":\"" id "\"}"`), which is the hardening target for the lookup path.

## Impact

Informational dependencies are visible but not operable. Operators must copy IDs and hunt manually; the Board cannot demonstrate safe navigation of dependency references.

## Desired outcome

Dependency IDs become **navigable controls** in shared `frontend/mission_view.howl` (app + published demo):

- Activate via existing `open_mission` (same pattern as mission rows).
- Missing / unknown targets **fail honestly** (visible error or clear empty-detail state — not silent no-op).
- Semantics remain **informational only** (HOWL-007 non-goals preserved).
- Security: ID in `data-*` via `esc`; handler source remains a **constant** string; `open_mission` request body for the lookup path uses `encode_json` (not string-concat JSON); hostile IDs cannot inject script/HTML/handler source.

## Acceptance criteria (Product-owned exact AC)

Owner themes 1–16 confirmed and amended:

1. Non-empty `depends_on` IDs render as **activatable controls** (button/link-styled control), not inert `<code>`-only text.
2. Controls live in shared `frontend/mission_view.howl` used by **both** app and published demo (no demo-only fork).
3. Activation calls existing `window.open_mission` / `open_mission` with the dependency mission ID (same entry point as mission rows).
4. Mission ID is placed in a `data-mission-id` (or equivalent data-attribute) value produced via **`esc`**.
5. The `onclick` (or equivalent) handler source is a **constant** string (e.g. `window.open_mission(this.dataset.missionId)`), not built by concatenating the mission ID into JavaScript source.
6. App `open_mission` lookup request body for `/api/missions/get` is built with **`encode_json`** (or equivalent structured JSON encode) — **not** string-concatenated JSON — unless Engineering proposes a tiny adjacent shared helper that EM/Product explicitly accept; default scope is harden `open_mission` only.
7. Hostile / quote-bearing / HTML-bearing IDs cannot break out of the data-attribute or inject into handler source or HTML structure (covered by tests).
8. Opening a dependency that exists loads that mission detail (app API path and demo fixture path each work in their environment).
9. Opening a dependency that is **missing** fails honestly: user-visible error or explicit “not found” detail state — **not** a silent no-op.
10. Empty or missing `depends_on` still shows **no** dependency block (HOWL-007 behavior preserved).
11. UI/docs continue to state dependencies are **informational only** — no implication of ordering, blocking, satisfaction, approval, or scheduling.
12. Non-goals remain true: no execution ordering, blocking/satisfaction, cycle detection, authority/ChangeOps propagation, HowlPlane scheduling, automatic dispatch, or full graph visualization.
13. Backend contract for `depends_on` storage/API from HOWL-007 remains compatible (this slice is primarily navigation/UX + secure open path).
14. Tests cover: navigable control present when deps exist; absent when empty; activation invokes open path; missing target honest failure; escape/data-attribute safety; `encode_json` (or accepted helper) used for app get-body; docs drift if limitations/roadmap need wording for “navigable informational deps.”
15. No HowlFutureWorks context-budget raises; no broad API request serialization refactor beyond the open_mission lookup harden (unless tiny adjacent abstraction explicitly accepted).
16. Product definition published to org Git early on the HOWL-008 branch (this file); implementer does not wait for chat-only AC.
17. Do **not** pre-pick SELF / Claude / Codex / AGY / Astra in this definition — EM routes after acceptance.

## Explicit non-goals

- Execution ordering
- Blocking / satisfaction semantics
- Cycle detection
- Authority / ChangeOps propagation
- HowlPlane scheduling
- Automatic dispatch
- Graph visualization
- Broad API request serialization refactor
- Context budget increases
- HOWL-009 auto-start
- Executor pre-selection

## Evidence refs (Product verification @ howlboard `cab020c`)

| Claim | Source |
|---|---|
| Inert `<code>` dependency IDs | `frontend/mission_view.howl` depends block |
| Row navigation pattern | `frontend/mission_view.howl` list buttons: `data-mission-id` + constant `onclick` |
| App open_mission + concat JSON body | `frontend/app.howl` `open_mission` |
| Demo open_mission | `docs/demo.howl` |

## Routing note

EM classifies after Product AC using live HOWL-005/006 policy. Astra = Codex alias per org routing note.
