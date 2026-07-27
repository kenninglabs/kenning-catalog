# Postman CLI

Command-line client for running Postman collections, workspaces, flows, and API/spec linting — from CI or an agent session.

- **Install docs:** https://learning.postman.com/docs/postman-cli/postman-cli-installation/
- **Auth docs:** https://learning.postman.com/docs/postman-cli/postman-cli-auth/
- **Options reference:** https://learning.postman.com/docs/postman-cli/postman-cli-options/

This is the official `postman` binary (Postman CLI), **not** `newman`. Newman is the older Node-based collection runner; `postman` is the modern first-party CLI that authenticates against a Postman account and integrates with Postman API governance (lint/publish). Prefer it for new work.

## Verify

```bash
postman --version
```

A successful install prints a semver like `1.x.x` (works pre-login — no server contact). If `command -v postman` returns nothing right after install, restart the shell so PATH refreshes.

## Authenticate

Generate an API key: Postman web → **Account Settings → API keys → Generate API Key** (https://go.postman.co/settings/me/api-keys).

```bash
postman login --with-api-key <POSTMAN_API_KEY>
postman login --with-api-key <POSTMAN_API_KEY> --region eu   # EU region
```

Interactive (opens browser) / logout:

```bash
postman login
postman logout
```

Store the key in `.env` or a secret manager — never commit it. Login is only needed for workspace-linked runs (cloud collections, API/spec lint/publish, flows); a local collection JSON can be run without login.

## Common commands

```bash
# Run a collection (local file or Postman cloud UID), with an environment
postman collection run <collection>.postman_collection.json -e <env>.postman_environment.json
postman collection run <collection-uid> -e <environment-uid>   # cloud-linked

# Pass variables / iteration data
postman collection run <collection> --env-var "baseUrl=https://<host>" -d <data>.csv

# Workspace snapshot / push (requires login)
postman workspace prepare
postman workspace push

# API governance (requires login)
postman api lint <api-uid>
postman spec lint <spec-uid>
postman flows trigger <flow-id>
```

Exit code is non-zero if any request/assertion fails — usable as a CI gate.
