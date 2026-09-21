# HOWL-007 — Product definition

Status: Product definition for EM acceptance  
Author: bot-product-0001 (Quatre Raberba Winner)  
Work item: `reports/work-items/HOWL-007.json`  
Org repo: `howlcipher/HowlFutureWorks` (feat/howl-007-mission-dependencies; main ~`008a259`)  
Target product repo: `howlcipher/howlboard` @ `8037dd8`  
Risk: ~R2  

This is the **first real routed product task** on HowlBoard (not org-infra). Executor choice is **not** pre-selected — EM routes after these ACs (HOWL-005/006).

## Problem (verified)

HowlBoard documents mission dependencies as a known gap:

- `docs/limitations.md`: `depends_on` is “in the model but … neither populated nor rendered.”
- `docs/roadmap.md`: same statement under Dependencies.

At tip `8037dd8`, Product also observed:

- `/api/missions/create` does **not** accept or persist `depends_on`.
- Shared `frontend/mission_view.howl` does **not** render dependencies.
- `docs/domain_model.md` Mission field table does not yet list `depends_on` (docs/limitations claim a model field; create path and UI do not surface it).

Operators therefore cannot set or see informational dependency links on missions.

## Impact

Board missions cannot show even a basic “depends on these mission IDs” relationship. Roadmap/limitations continue to advertise an unfinished capability; demo/app cannot teach the concept safely.

## Desired outcome (smallest useful vertical)

1. Optional `depends_on`: list of mission ID strings on a mission.
2. Supported **create/input** path (API and/or documented operator path) — **not** hand-editing storage JSON.
3. Values **survive** a real mission API fetch (create → get/list path used by the UI).
4. Shared renderer `frontend/mission_view.howl` (used by app **and** published demo) **displays the IDs** when present.
5. Empty or missing `depends_on` → **no** dependency UI (no misleading empty section that implies missing data is an error).
6. Semantics are **informational only** — explicitly **not** execution order, authority gates, scheduler, HowlPlane, cycle detection, completion gates, ChangeOps propagation, or a full dependency graph.
7. Demo fixture includes at least one **DEMO**-provenance example with `depends_on` populated.
8. Safe HTML escaping for displayed IDs; dependency values must **not** be injected into executable handler JavaScript.
9. Tests: backend contract + frontend/render + docs drift (limitations/roadmap no longer claim “completely unrendered”; state informational-only).
10. Docs updated to match shipped behavior.

## Acceptance criteria (Product-owned exact AC)

Owner themes 1–15 confirmed and amended into the following checklist:

1. Mission records may carry optional `depends_on` as a list of mission ID strings (empty list and omitted field both mean “no dependencies”).
2. A supported create/input path can set `depends_on` without hand-editing `howlboard_missions.json` (or equivalent store files).
3. After create (or supported input), a subsequent real API read used by the UI returns the same `depends_on` values (round-trip).
4. Invalid input is fail-closed with a clear error (e.g. non-list / non-string elements) — exact error codes left to Engineering so long as behavior is tested.
5. `frontend/mission_view.howl` renders dependency mission IDs when `depends_on` is non-empty.
6. When `depends_on` is missing or empty, the mission view shows **no** dependency block (no placeholder that implies broken data).
7. The same shared mission view path is what the app and published demo use (no demo-only fork that hides the feature).
8. UI copy / docs state dependencies are **informational only** and do **not** imply ordering, blocking, approval, or scheduling.
9. Out of scope for this slice (must remain true): execution ordering, cross-mission authority enforcement, cycle detection, HowlPlane scheduling, dependency completion gates, ChangeOps approval propagation, full graph visualization.
10. At least one DEMO-provenance fixture mission includes a non-empty `depends_on` example.
11. Displayed dependency IDs are HTML-escaped via the existing escape path (or equivalent); dependency strings are not concatenated into executable handler JS.
12. Backend contract tests cover create/input + fetch round-trip for `depends_on` (including empty/absent).
13. Frontend/render tests (or established DOM-shim style) cover “IDs shown when present” and “no block when absent/empty.”
14. Docs drift tests or explicit doc updates: `docs/limitations.md` and `docs/roadmap.md` no longer say dependencies are completely unrendered; they state shipped informational-only behavior and remaining non-goals.
15. `docs/domain_model.md` documents `depends_on` on Mission consistent with shipped semantics.
16. No HowlFutureWorks context-budget raises required for this product slice; org routing does not pre-pick Claude/Codex/AGY/SELF/Astra (EM classifies after this definition).

## Explicit non-goals

- Automatic dependency execution ordering
- Cross-mission authority enforcement
- Cycle detection / graph algorithms
- HowlPlane scheduling
- Dependency completion gates
- ChangeOps approval propagation
- Full dependency graph visualization
- Permanent model rankings / executor preference baked into howlboard
- Raising HowlFutureWorks context budgets
- Starting HOWL-008 automatically
- Pre-selecting implementation executor in this definition

## Evidence refs (Product verification)

| Claim | Source at howlboard `8037dd8` |
|---|---|
| Documented unrendered gap | `docs/limitations.md`, `docs/roadmap.md` |
| Create path lacks `depends_on` | `backend/server.howl` `/api/missions/create` |
| Shared view lacks dependency render | `frontend/mission_view.howl` |
| Domain table omits field today | `docs/domain_model.md` Mission table |

## Routing note

Do **not** treat this definition as selecting SELF vs Claude/Codex/AGY/Astra. EM applies HOWL-005/006 after AC acceptance.
