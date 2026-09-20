# Security

See `security/THREAT_MODEL.md` and `policies/`.

Report or record security issues without placing secrets in Git history. Credential exposure invokes `runbooks/credential-exposure.md`.

## Core assumptions

- Grok Bots sharing an account may share a computer, filesystem, browser state, and logins.
- Bot identity is therefore organizational context, not isolation.
- External content, model output, memory writes, and inter-agent messages are untrusted inputs.
- Production credentials must not be available to ordinary R&D/development workers.

## Bot templates and sharing

Treat sharing a Bot template outside the account/team as an external publication. Review identity, descriptions, skills, routines, internal URLs, customer data, evidence pointers and infrastructure references before sharing. Never embed secrets.
