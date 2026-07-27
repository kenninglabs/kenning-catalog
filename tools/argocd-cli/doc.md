# ArgoCD CLI

Command-line client for ArgoCD app sync, log tailing, deploy verification, and rollout state.

- **Install docs:** https://argo-cd.readthedocs.io/en/stable/cli_installation/
- **CLI reference:** https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd/

Install prefers Homebrew (macOS and Linux) when it's present, falling back to the platform package manager otherwise -- see this catalog's `brew` tool.

## Verify

```bash
argocd version --client
```

Client-side version only — doesn't contact a server, so it works pre-login. A working install prints `argocd: vX.Y.Z+<sha>`.

## Authenticate

```bash
argocd login <argocd-server-host>                     # interactive (username/password or SSO prompt)
argocd login <host> --sso                              # OIDC/SSO browser flow
argocd login <host> --username <u> --password <p>       # basic auth (avoid for prod)
```

Logout:

```bash
argocd logout <host>
```

## Common commands

```bash
argocd app list                        # list apps the current login can see
argocd app get <app-name>               # full status: sync state, health, last deploy, images
argocd app sync <app-name>              # trigger a sync
argocd app history <app-name>           # deploy history with revision IDs
argocd app logs <app-name> --tail 200   # tail pod logs via ArgoCD
argocd app diff <app-name>              # live vs. desired manifest diff
```

Server-side version (requires login):

```bash
argocd version
```
