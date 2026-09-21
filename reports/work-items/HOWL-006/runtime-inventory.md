# HOWL-006 — Runtime inventory (non-secret)

**Captured:** 2026-09-21 11:22 EDT  
**Branch:** `feat/howl-006-executor-baseline`  
**Probe rule:** record only `authenticated` | `not_authenticated` | `blocked` | `unknown`. No secrets/tokens/cookies/OTP.

## Install / auth / tool inventory

| Executor | Installed | Version | Auth status | Binary | Tool surface (non-secret) | Notes |
|---|---|---|---|---|---|---|
| SELF | n/a (persistent member path) | orgctl present | n/a | `python tools/orgctl.py` | `validate`, `route`, `render-*`, workforce ops | Deterministic; `model_invoke: false` on `route` |
| Claude | yes | 2.1.278 (Claude Code) | **authenticated** (`loggedIn: true`, `authMethod: claude.ai`) | `/home/box/.local/bin/claude` | CLI `-p` print, MCP, allowed/disallowed tools, agents | Owner-controlled auth on this box |
| Codex | yes | 0.155.1 (codex-cli) | **authenticated** (ChatGPT login) | `/home/box/.local/bin/codex` | `exec`, `review`, `login`, `mcp`, `sandbox`, `doctor` | `codex login status` → Logged in using ChatGPT |
| AGY | yes | 1.2.7 | **authenticated** (`agy models` lists models) | `/home/box/.local/bin/agy` | print mode, models, mcp, plugins, agents, sandbox | Models enumerable without sign-in prompt |
| Astra | yes (via Codex) | 0.155.1 (Codex CLI) | **authenticated** (follows Codex) | same as Codex (`/home/box/.local/bin/codex`) | same as Codex | **Owner clarification:** Astra **is** Codex — not a separate CLI/binary. `runtime_alias_of: codex`. Do not install a distinct Astra package. |

## Astra mapping (Owner/EM clarification 2026-09-21)

- Astra is **not** a missing/blocked binary.
- Astra maps to the **Codex** runtime (same install, auth, CLI version, tool surface).
- Baseline EVAL evidence for Astra **shares** Codex EVAL-A..E results; explicit alias note in registry + results.
- No separate Astra install was (or will be) pursued under this clarification.

## Unknowns (honest gaps)

- Long-horizon reliability, quota_state trends, cost curves beyond this low-sample baseline.
- Full per-executor MCP plugin catalogs beyond default CLI surfaces (not exhaustively enumerated).
- Model-routing choices inside each CLI across future versions (versions recorded at capture time only).

## Auth probe summary (safe statuses only)

| Executor | Status |
|---|---|
| claude | authenticated |
| codex | authenticated |
| agy | authenticated |
| astra | authenticated (alias of Codex; same auth) |

## Baseline eval note

Minimal EVAL-A..E: **one combined isolated run per authenticated runtime** (Claude, Codex, AGY). Astra does not get a separate API burn — shares Codex outcomes. Labels: **INITIAL BASELINE / LOW SAMPLE / NOT PERMANENT RANKING**. No silent cross-executor fallback. No invented rankings.
