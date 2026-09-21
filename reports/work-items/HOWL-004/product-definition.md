# HOWL-004 — Product / ops definition (lightweight)

## Problem
Authorized HowlFutureWorks Bots cannot publish approved feature branches and PRs from the shared Grok Bot computer using native `git`/`gh`. HOWL-002/003 required CloudAgent for publication.

## Impact
Ordinary governed publish is slow and CloudAgent-dependent. Technical inability is confused with policy authority.

## Expected outcome
After Owner-authorized human authentication on the shared computer, an appropriately authorized member (typically Dev Lead under EM task envelope) can: create feature branch → commit → push → open/update PR **without CloudAgent**, while merge/main protection and HowlFrame remain unchanged. CloudAgent stays fallback only.

## Acceptance criteria
1–17 as listed in Owner HOWL-004 brief (auth, git publish, governance, recovery runbook).

## Non-goals
Executor auth (Claude/Codex/AGY/Astra), HowlBoard, CI redesign, production deploy, weakening approvals, inventing per-Bot secret isolation on a shared computer.
