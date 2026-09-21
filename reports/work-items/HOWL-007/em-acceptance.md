# HOWL-007 — EM acceptance + routing decision

Status: **ACCEPTED**  
Author: bot-engmgr-0001 (Rintaro Okabe)  
Product definition: `reports/work-items/HOWL-007/product-definition.md` — accepted (16 ACs)  
Target: `howlcipher/howlboard` @ `8037dd8`  
Org branch: `feat/howl-007-mission-dependencies`  
Implementation owner: bot-devlead-0001 (Motoko Kusanagi)  
Risk: R2

## Product AC

Accepted as written. Informational `depends_on` visibility slice only; non-goals unchanged.

## Classification (HOWL-005/006)

| Field | Value |
|---|---|
| Task class | **bounded** — scoped vertical slice (create path + persistence + shared renderer + fixtures + tests + docs) |
| Risk | **R2** — development; HTML escaping required but existing `esc` conventions apply; not authority/lifecycle change |
| Target | howlboard (HowlFrame `.howl`, Go contract tests, fixtures) |
| Tools | coding, git, howlframe build/test |
| Security | untrusted dependency ID strings → HTML text only; no handler-JS interpolation |

## orgctl route probe

```
python tools/orgctl.py route --task-class bounded --risk R2 --required-tool coding
→ decision: SELF_preferred_unless_expected_value
→ eligible (if delegated): claude, codex, agy, astra(=codex) — baseline-evaluated
```

## SELF sufficient?

**Yes.** Persistent Dev Lead can implement this slice:

- Bounded cross-cut inside one product repo with clear AC
- Create path, shared `mission_view.howl`, fixtures, contract/render/docs tests are ordinary engineering
- Escape helpers already exist; HOWL-007 extends them rather than inventing a security model
- Assurance provides independent verification (builder not sole verifier)

## External expected value?

**Not established for this task.** HOWL-006 baselines show Claude/Codex/AGY can do small coding fixtures, but that is low-sample general evidence — not a measured HowlBoard/HowlFrame advantage over SELF for this specific slice. Policy: external requires expected value; installed ≠ invoke; no loyalty/rankings.

Quota state: **unknown** → treat conservatively (constrained). Avoid external spend without expected value.

## Selection

| Option | Role |
|---|---|
| **SELF** (Dev Lead + org workflow) | **SELECTED** |
| Claude | Eligible if expected value later proven — not selected |
| Codex / Astra (alias) | Eligible — not selected; Astra is not a fourth runtime |
| AGY | Eligible — not selected |
| evidence-insufficient forcing largest model | Forbidden |

**Rationale:** bounded + R2 + SELF sufficient + no task-specific expected-value case for specialist + conservative quota → SELF.

## Verification

- Assurance independent of implementer
- Deterministic howlboard tests first
- Auditor reconstructs Product → routing → implementation → Assurance

## Envelope for Dev Lead (SELF)

Implement on howlboard branch e.g. `feat/howl-007-mission-dependencies` (repo conventions OK):

1. Optional `depends_on: list[string]` on mission
2. Extend `/api/missions/create` (narrowest path) with validation; fail-closed on bad types
3. Round-trip via get/list used by UI
4. Render in `frontend/mission_view.howl` (app+demo shared); empty/missing → no block
5. DEMO fixture with non-empty `depends_on` + DEMO provenance
6. Escape via existing `esc`; never into handler JS
7. Contract + frontend/render + docs drift tests
8. Update domain_model / limitations / roadmap — informational only

Do **not**: ordering, authority, cycles, HowlPlane, completion gates, ChangeOps, graph UI, recursive external delegation, budget raises, HOWL-008.

Publish: native git/gh on howlboard. Reference SHAs/PR from HowlFutureWorks evidence — do not copy full product diff into org repo.

When PR ready + local tests green, hand Assurance.
