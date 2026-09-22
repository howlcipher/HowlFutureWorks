# HOWL-008 — EM acceptance + routing decision

Status: **ACCEPTED**  
Author: bot-engmgr-0001 (Rintaro Okabe)  
Product: `reports/work-items/HOWL-008/product-definition.md` — accepted (17 ACs) @ `af14374`  
Target: `howlcipher/howlboard` @ `cab020c`  
Org branch: `feat/howl-008-dependency-navigation` (publish early — HOWL-007 lesson)  
Implementation: bot-devlead-0001 (Motoko Kusanagi)  
Risk: R2

## Product AC

Accepted. Navigable informational `depends_on` via shared `mission_view.howl`; `data-mission-id` + constant handler; `open_mission` lookup body via `encode_json`; honest missing-target failure; HOWL-007 non-goals preserved.

## Classification (live HOWL-005/006)

| Field | Value |
|---|---|
| Task class | **bounded** — UI navigation + narrow open_mission JSON harden + tests/docs |
| Risk | **R2** — untrusted ID in HTML attribute + request body; existing row pattern applies |
| Tools | HowlFrame, frontend render, contract/render/docs tests, Git |
| Security | esc into data-attribute; constant onclick; encode_json body; no ID→JS source |

## orgctl probe

```
orgctl route --task-class bounded --risk R2 --required-tool coding \
  --objective "navigable depends_on; encode_json open_mission; informational only"
→ decision: SELF_preferred_unless_expected_value
→ eligible if delegated: claude, codex, agy (astra = codex alias)
```

## SELF sufficiency (re-evaluated; not automatic)

**Yes, with fresh rationale:**

- Pattern already in-repo: mission rows use `data-mission-id` + constant `open_mission` onclick in the same shared view.
- Scope is a vertical extension of HOWL-007 surfaces, not new architecture.
- HOWL-007 is **sufficiency evidence** that SELF can ship HowlBoard HowlFrame shared-view + contract/docs slices — **not** a standing “prefer SELF forever” rule.
- Independent Assurance remains the verification gate for injection/escaping claims.

## External expected value?

**Not established for this slice.** HOWL-006 baselines remain low-sample general coding evidence; they do not show a measured HowlBoard-navigation/XSS advantage over copying the local row pattern and adding regression tests. Policy: external requires expected value; installed ≠ invoke; least-resource sufficient preferred. Quota **unknown** → treat constrained.

## Selection

| Path | Role |
|---|---|
| **SELF** (Dev Lead) | **SELECTED** |
| Claude / Codex / AGY | Eligible — not selected |
| Astra | Codex alias — not a fourth runtime |

**Rationale:** bounded + R2 + SELF sufficient on demonstrated HowlBoard pattern + no task-specific specialist EV + conservative quota → SELF.

## Envelope (SELF)

On howlboard branch e.g. `feat/howl-008-dependency-navigation`:

1. In `frontend/mission_view.howl`, render non-empty `depends_on` as button/control with `data-mission-id="(esc id)"` and constant `onclick="window.open_mission(this.dataset.missionId)"` (match row pattern).
2. Empty/missing deps → no block (HOWL-007).
3. Harden app `open_mission` get-body with `encode_json` (not string concat). Demo stays read-only fixture lookup; no mutating actions.
4. Missing target → honest failure (existing cannot-load / not-found).
5. Tests: control present/absent; navigation; missing target; hostile IDs; no handler interpolation; encode_json body; HOWL-007 contracts preserved; demo shared renderer.
6. Docs: navigable informational deps; non-goals unchanged.

**Do not:** ordering, blocking, satisfaction, cycles, authority/ChangeOps, HowlPlane, dispatch, graph, broad request-serialization refactor, budget raises, HOWL-009, recursive external delegation.

Publish howlboard PR natively. Push org evidence (this file + routing record + work-item updates) to **this same org branch** before Assurance — do not leave AC/routing only local.
