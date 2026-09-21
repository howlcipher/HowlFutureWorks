# Governed GitHub publishing (bot-native)

## Purpose

Authorized HowlFutureWorks members on the shared Grok Bot computer may publish **approved** work to feature branches and pull requests using native `git` / `gh`, without requiring CloudAgent for ordinary publication.

## Security boundary

- All Bots on this Owner account **share one computer** and therefore share GitHub authentication state.
- Technical ability to push is **not** organizational authorization.
- Authorization comes from: HowlFutureWorks role + task envelope + risk/approval policy (+ Owner when required).
- Do **not** push to `main` merely because credentials work. Use feature branches and PRs.
- Do **not** put tokens, passwords, OTPs, cookies, or private keys in chat, Git, evidence, Bot memory, or logs.
- Never run token-display commands (for example `gh auth token` or `gh auth status --show-token`) for evidence.

## Normal flow

```
approved work item
      ↓
feature branch
      ↓
commit (repo conventions)
      ↓
validation (orgctl / make validate / tests as applicable)
      ↓
git push -u origin <branch>
      ↓
gh pr create / gh pr edit
      ↓
Assurance
      ↓
Auditor / approvals as required
      ↓
merge according to policy (not convenience push to main)
```

## Safe status checks (non-secret)

```bash
gh --version
gh auth status          # do not use --show-token
gh api user --jq .login
gh repo view howlcipher/HowlFutureWorks
git ls-remote origin HEAD
git config --get credential.helper
```

Expected healthy state: logged into github.com; git credential helper uses `gh auth git-credential`; remote is HTTPS to `howlcipher/HowlFutureWorks`.

## Authentication recovery

If `gh auth status` shows not logged in:

1. Stop. Request Owner **desktop takeover** (do not ask for a pasted token in chat).
2. Owner runs interactive login, e.g. `gh auth login --hostname github.com --git-protocol https --web` (device/browser flow).
3. Do **not** use `--insecure-storage` as a shortcut.
4. After login: `gh auth setup-git`
5. Re-run safe status checks above.
6. If the environment can only store credentials in knowingly unprotected plaintext beyond GitHub CLI’s normal owner-restricted host config, **stop** and report `SECURE_CREDENTIAL_STORAGE_BLOCKED` to the Owner rather than weakening storage.

## Fallback

CloudAgent remains an authorized **publication fallback** when native GitHub access is unavailable (auth loss, credential helper broken, network/ACL issues).

When fallback is used, record in the work item / evidence:

- that native publish was attempted;
- the non-secret error class;
- that CloudAgent was used as fallback only.

## Related

- Initial repo publication from release bundles: `docs/PUBLISH_GITHUB.md`
- Shared-computer notes: `docs/GROK_PLATFORM_NOTES.md`
