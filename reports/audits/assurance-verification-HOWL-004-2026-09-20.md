# Assurance Verification — HOWL-004 (2026-09-20)

**Role:** Independent Assurance (QA + Security dual sections)  
**Subject:** PR #3 `ops/howl-004-github-publishing` @ `4d24315c50600d67272fc8d99575a7505cd38520`  
**Base:** `main` @ `efab575f29c64c1b48c64b95f7e5fcf6cd2df32e`  
**Evidence dir:** `evidence/howl-004-assurance-verify-4d24315/`  
**Authoritative summary:** `evidence/howl-004-assurance-verify-4d24315/SUMMARY.md`  
**Owner-complete:** **NOT declared**

## Overall: PASS

All six delegated checks passed. Verifier wrote Assurance evidence only under `/workspace/HowlFutureWorks`; did not modify product/runbook content beyond evidence artifacts; did not push.

---

## QA

### Intent
HOWL-004 establishes governed bot-native GitHub publishing from the shared Grok Bot computer: ordinary approved feature-branch push + PR via native `git`/`gh`, with CloudAgent retained as fallback only, documenting shared-computer credential boundary and auth≠authorization.

### Verification performed
1. **Publication / tip:** `origin/ops/howl-004-github-publishing` at expected tip; PR #3 open to `main` from that branch; authorship howlcipher; no Cursor Agent co-author trailer; PR/commit claim native publish without CloudAgent (git alone cannot absolute-negative-proof transport tooling).
2. **Delta cleanliness:** three documentation/work-item adds; secret-pattern scan CLEAN.
3. **Runbook concepts:** shared-computer + auth≠authorization accurately stated (quoted in SUMMARY / runbook-excerpts).
4. **Workflow:** ops/ branch → PR → main; runbook forbids convenience push to main; pre-existing `docs/PUBLISH_GITHUB.md` bootstrap `push … main` noted as informational only.
5. **Governance:** CloudAgent fallback retained with evidence requirements; approval/Assurance/merge-per-policy flow intact; non-goals forbid weakening merge/HowlFrame.
6. **Deterministic:** pytest 78 passed; orgctl validate PASSED; `--stat` / name-status recorded.

### QA verdict: PASS

---

## Security

### Threat considerations
- Shared-computer credential state: runbook correctly states shared GitHub auth across Bots and that credential presence ≠ org authorization — reduces confusion that could lead to unauthorized pushes.
- Secret hygiene: PR delta contains no live tokens/keys/cookies; runbook forbids token-display commands and secret placement in chat/Git/evidence.
- Direct-main bypass: runbook and acceptance criteria prohibit convenience pushes to main; ordinary path is feature branch + PR + policy merge.
- CloudAgent: remains authorized fallback only (not removed); weakens neither native path governance nor fallback accountability (must record native attempt + error class).
- Residual: pre-existing initial-publish doc still shows `git push -u origin main` for bootstrap — outside HOWL-004 delta; not a new convenience path for bot-native ops.

### Secret / credential handling in this verification
- No `gh auth token` / `--show-token`; no hosts.yml contents echoed.
- Secret scan reports CLEAN without printing candidate values.

### Security verdict: PASS

---

## Gaps / notes
- Absolute proof that CloudAgent was unused for the git transport is limited to authorship trailers, account identity, PR body claims, and tip/PR presence on origin.
- Host lacked `make`; orgctl invoked as `python tools/orgctl.py validate` (Makefile equivalent).
- Evidence written on main clone path; worktree at tip used for inspection only.

## Recommendation
PASS — proceed to Owner merge decision. Do not declare owner-complete from this report alone. Parent publishes evidence artifacts.
