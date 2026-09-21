# HOWL-006 — Runtime inventory (non-secret)

**Captured:** 2026-09-21 00:01 EDT  
**Branch:** `feat/howl-006-executor-baseline`  
**Probe rule:** record only `authenticated` | `not_authenticated` | `blocked` | `unknown`. No secrets/tokens/cookies/OTP.

## Install / auth / tool inventory

| Executor | Installed | Version | Auth status | Binary | Tool surface (non-secret) | Notes |
|---|---|---|---|---|---|---|
| SELF | n/a (persistent member path) | orgctl present | n/a | `python tools/orgctl.py` | `validate`, `route`, `render-*`, workforce ops | Deterministic; `model_invoke: false` on `route` |
| Claude | yes | 2.1.278 (Claude Code) | **not_authenticated** (`loggedIn: false`) | `/home/box/.local/bin/claude` | CLI session, `-p` print, MCP config, allowed/disallowed tools (Bash/Edit/…), agents | `claude auth status` → loggedIn false |
| Codex | yes | 0.155.1 (codex-cli) | **not_authenticated** | `/home/box/.local/bin/codex` | `exec`, `review`, `login`, `mcp`, `sandbox`, `doctor`, session mgmt | `codex login status` → Not logged in; doctor: no credentials |
| AGY | yes | 1.2.7 | **not_authenticated** | `/home/box/.local/bin/agy` | print mode, models, mcp, plugins, agents, sandbox | `agy models` → sign-in required |
| Astra | **no** | — | **n/a** | not on PATH | — | `installation_status: blocked` (see below) |

## Astra official install attempt

Attempted to establish the **official** install path for the Howl executor profile named `astra`.

**Result:** `installation_status: blocked`

**Reason:** The repository registers `astra` as an ephemeral coding executor alongside Claude/Codex/AGY, but does not name a vendor package. Public “Astra CLI” hits are ambiguous:

1. DataStax **Astra CLI** (`docs.datastax.com/en/astra-cli`, `curl … ibm.biz/astra-cli`) — database/streaming ops, not an AI coding executor.
2. **Open Astra** (`openastra.net`, `npm i -g @open-astra/astra`) — agent runtime; not confirmed as the Owner-intended Howl profile.

Per HOWL-006: do **not** improvise mirrors or guess. Owner must designate the official binary/docs before install. No install was performed.

## Unknowns (honest gaps)

- Which product is Howl `astra` (Owner confirmation required).
- Full per-executor tool catalogs / MCP sets after authentication (cannot enumerate authenticated tools without login).
- Latency, quota_state, reliability, task success — **unknown** until authenticated EVAL runs.
- Model versions behind each CLI after login — **unknown**.
- Whether Owner desktop login will land on this shared box path vs a different machine.

## Auth probe summary (safe statuses only)

| Executor | Status |
|---|---|
| claude | not_authenticated |
| codex | not_authenticated |
| agy | not_authenticated |
| astra | blocked (not installed; official path unclear) |

No eval scores invented. No silent cross-executor fallback.
