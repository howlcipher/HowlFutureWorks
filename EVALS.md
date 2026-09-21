# Executor Evaluation

Routing is evidence-driven, not provider folklore.

## Purpose

Representative local evals populate `routing/capability-registry.yaml` fields listed
under `fields_to_maintain` (success rate, reliability, latency, cost/usage, tools,
failure modes, allowed risk, last evaluated). Until evals exist, profiles remain
`benchmark_status: needs-local-eval` and the router must report **evidence-insufficient**
rather than invent scores.

## Suite layout

| Path | Role |
|------|------|
| `evals/benchmark-suite/` | Representative cases (fixes, cross-repo, debug, security, UI, orchestration) |
| `evals/results/` | Timestamped measured results (cite these from registry updates) |
| `evals/routing-recommendations/` | Recommendations that **cite** eval evidence |

## What to record

Quality, reviewer acceptance, reliability, latency, cost/usage, tool fit, policy
behavior, and known failure modes. Prefer schema `schemas/evaluation-result.schema.json`.

## Rules

- Do not fabricate capability scores or large synthetic benchmarks to satisfy routing.
- Update the registry after representative evals; rankings are never permanent.
- Auth to Claude/Codex/AGY/Astra and large benchmark campaigns are out of HOWL-005 scope.

See also `docs/EXECUTOR_ROUTING.md`.
