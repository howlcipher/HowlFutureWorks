# Skill: Propose a Persistent Bot

## Use when
A logical role has recurring work and may deserve durable Bot ownership.

## Inputs
- durable ownership problem
- role definition
- expected tools/sources
- recurring routines
- required approval boundary
- proposed risk ceiling

## Steps
1. Prove that an invoked specialist is insufficient.
2. Run `python tools/orgctl.py scaffold-bot <id> --name "..." --role <role> --risk <R0-R4> --purpose "durable ownership statement"`.
3. Complete the generated roster-change proposal.
4. Define minimal always-load context; keep larger context on demand.
5. Define capabilities and hard boundaries.
6. Validate the repo and render the candidate bundle manually if needed.
7. Obtain review required by current policy.
8. Only after approval, activate it in `bots/manifest.yaml` and reconcile live Grok state.

## Must stop for approval
Any requested authority increase, new R3/R4 capability, credential expansion, or weaker approval requirement.
