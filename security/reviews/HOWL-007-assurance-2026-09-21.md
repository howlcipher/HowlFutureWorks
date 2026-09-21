# HOWL-007 — Assurance security review

**Date:** 2026-09-21 12:47:43 EDT  
**Product tip:** `eb86e95f40e7e794f338f33100814cb52967fe5c`  
**PR:** https://github.com/howlcipher/howlboard/pull/7  
**Verdict (dual QA+Security):** PASS  
**Owner-complete:** NOT declared

## Scope

Independent security verification of HOWL-007 informational mission `depends_on` on howlboard tip above. Did not trust implementer evidence alone. Did not merge. Did not start HOWL-008. Did not print secrets.

## Results

| Control | Result | Evidence |
|---|---|---|
| Untrusted dependency ID → HTML text only | **Pass** | `(call esc dep)` in `mission_view.howl`; XSS harness asserts `&lt;script&gt;` |
| No handler-JS injection of dependency values | **Pass** | `TestDependsOnNeverInHandlerJS`; render harness onclick guard |
| Fail-closed typed validation | **Pass** | `INVALID_DEPENDS_ON` for non-list / non-string elements |
| Authority / lifecycle unchanged | **Pass** | Create still seeds REQUIRE_APPROVAL + empty gates; verification list empty; no can_transition semantic edit |
| Informational-only (no gate/order enforcement) | **Pass** | Code comments + UI copy + docs non-goals; no completion/authority cross-mission logic added |
| Secrets in changed files | **Pass** | Independent scan 0 hits (`assurance-secret-scan.txt`) |
| CI green on tip | **Pass** | PR #7 check SUCCESS; headOid matches tip |

## Findings (security-relevant)

None blocking.

## Residual risk

Dependency IDs are free-form strings (informational). No existence check against other missions — by design for this slice. Operators must not interpret the UI as an authority or ordering control (copy and docs mitigate).

## Non-actions

No merge; no HOWL-008; no Owner-complete; no secrets printed; no executor re-pick.
