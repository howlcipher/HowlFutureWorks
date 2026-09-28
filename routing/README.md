# Executor Routing

Three decisions: which roles participate, SELF or delegated implementation, then which executor HowlPlane selects. Self for small bounded work; delegated implementation through HowlPlane when expected value justifies it. Measured fit — not loyalty or rankings.
See `task-classes.yaml`, `selection-policy.yaml`, `execution-substrate.yaml`, `capability-registry.yaml`, `routing-policy.yaml`, `fallback-policy.yaml`, `participation-policy.yaml`, `docs/EXECUTOR_ROUTING.md`.
`python tools/orgctl.py route --help`.

Status (compact): Claude / Codex / AGY — installed, authenticated, baseline-evaluated. Astra — alias of Codex. AVAILABLE ≠ preferred. Details on demand: `capability-registry.yaml`.
