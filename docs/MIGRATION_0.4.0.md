# Migration to HowlFutureWorks / v0.4.0

The descriptive working name `howl-org` was replaced by the canonical organization identity **HowlFutureWorks** and repository slug **`howl-future-works`**.

## If the old repository was never published

Use the v0.4.0 bundle and create `howlcipher/howl-future-works`. No migration is required.

## If an old `howl-org` remote already exists

Prefer renaming the GitHub repository to `howl-future-works` so issue/PR history and redirects are preserved, then update the local remote:

```bash
git remote set-url origin git@github.com:howlcipher/howl-future-works.git
```

Do not rewrite historical commits or audit documents merely to erase the former working name. Provenance should remain intact.
