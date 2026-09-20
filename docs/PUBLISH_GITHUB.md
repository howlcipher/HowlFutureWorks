# Publish to GitHub

Canonical repository name: **`howl-future-works`**. The display name is **HowlFutureWorks**. The name is provider-neutral while preserving the Howl identity and the organization's future-facing R&D/build mission.

## Recommended first publication

Start **private** while the live organization is being reconciled and reports/workforce records are still evolving. Review operational data before changing visibility.

From the release Git bundle:

```bash
git clone -b main howl-future-works-v0.4.1.bundle howl-future-works
cd howl-future-works
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
make validate
make test

git tag --list v0.4.1
# The final release bundle should already contain v0.4.1.

# A bundle clone creates an origin that points back to the bundle file.
git remote -v
git remote remove origin

gh auth status
gh repo create howlcipher/howl-future-works \
  --private \
  --description "HowlFutureWorks: version-controlled operating system for the Howl autonomous software organization" \
  --source=. \
  --remote=origin \
  --push

git push origin --tags
```

If the GitHub repository already exists after cloning the bundle:

```bash
git remote set-url origin git@github.com:howlcipher/howl-future-works.git
# If you already removed origin, use: git remote add origin git@github.com:howlcipher/howl-future-works.git
git push -u origin main
git push origin --tags
```

## Before making public

- review `reports/`, `workforce/`, reconciliation metadata and future incident records for sensitive operational information;
- choose an explicit repository license;
- confirm no provider IDs or evidence pointers reveal private infrastructure;
- run `make validate test dist verify-dist`;
- review the latest audit report.

Do not make visibility changes merely because the rest of the Howl ecosystem is public; this repository can contain organizational and operational metadata that product repositories do not.
