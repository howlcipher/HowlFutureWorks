# Contributing

Organizational configuration is production-like infrastructure.

## Rules

- Keep constitutional changes separate from routine docs changes.
- Machine-readable policy changes require validation.
- Authority-expanding changes require explicit review according to `policies/approvals.yaml`.
- Never commit credentials or sensitive tokens.
- Update examples/tests with schema changes.
- Add an ADR when a change alters architecture, authority model, source-of-truth contracts, or Bot topology.

## Validation

```bash
python -m pip install -r requirements-dev.txt
python tools/orgctl.py validate
python -m pytest -q
```
