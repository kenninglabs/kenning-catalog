# ArgoCD REST API Access — Generic Patterns

**Triggers:** `argocd` CLI fails with SSO/gRPC-web errors (`cluster.SettingsService/Get 404`, transport `EOF`) against a non-prod ArgoCD; need to fetch pod logs or trigger a sync when the CLI path is blocked.

> **Project-independent.** How to read logs and trigger syncs through ArgoCD when the CLI is blocked or grpc-web is required. Distilled from the a large fintech deployment setup but applicable to any team running ArgoCD with SSO + Dex.

## Two access modes

ArgoCD typically has two flavors deployed per environment, and they behave differently for CLI-vs-REST access:

| Environment shape | CLI behavior | REST behavior | When |
|---|---|---|---|
| **Production-style** — direct gRPC ingress | `argocd app logs ... --grpc-web` works | Same REST endpoints exist | Often the case for prod-tier ArgoCD instances |
| **Non-prod / multi-tenant** — fronted by HTTP/L7 ingress that exposes REST + UI but NOT gRPC-Web | `argocd login --sso` fails (`cluster.SettingsService/Get 404`); CLI is effectively blocked | REST API works with a session token | Often the case for shared dev/uat ArgoCD instances behind enterprise SSO |

The CLI's gRPC-Web requirement collides with HTTP-only ingress, so non-prod usage typically falls back to REST.

## Production CLI usage

When CLI works:
- Always pass `--grpc-web` — many enterprise ingresses require HTTP/1.1 + gRPC-Web framing.
- Plain gRPC over the public ingress will fail with `EOF` or transport errors.
- Pin `--tail` to a deliberate value (`50000` or `100000`) — defaults are too low to find recent traces.
- Use `--kind Deployment --name <service>` to scope multi-pod log fetches; without scoping, you'll hit "max pods to view logs" or `stream read failed`.

```bash
argocd app logs argocd/<app-name> \
  --grpc-web --tail 50000 --follow=false \
  --kind Deployment --name <service>
```

## Non-prod REST workaround

When CLI is blocked:

### Step 1 — Get a token from a browser session

1. Sign in to the ArgoCD UI in your browser.
2. DevTools → Application → Cookies → ArgoCD origin → copy the value of `argocd.token`.
3. The token is a Dex `id_token`, valid ~24h, no refresh-token exposed.

### Step 2 — (Optional) store the token for the CLI

The CLI may still fail account/cluster lookups, but REST calls work with the same token:

```bash
# ~/.config/argocd/config — under users[name=<argocd-host>]:
auth-token: <paste-here>
```

### Step 3 — Use the REST endpoints directly

All paths relative to `https://<argocd-host>/<base-path>/api/v1` (base-path is often `/cd` for non-prod).

| Endpoint | Purpose |
|---|---|
| `GET /applications/{app}` | Status (sync.status, health.status, operationState.phase) |
| `POST /applications/{app}/sync` | Trigger sync. Body: `{"prune":false,"dryRun":false,"strategy":{"hook":{}},"syncOptions":{"items":["ApplyOutOfSyncOnly=true"]}}` |
| `GET /applications/{app}/resource-tree` | Pod-level details, including running image tags |
| `GET /applications/{app}/pods/{pod}/logs?container={c}&tailLines={n}&namespace={ns}` | Log stream from a specific pod |
| `GET /account` | List local accounts and capabilities |

Header on every request: `Authorization: Bearer <token>`. No cookies needed.

```bash
TOKEN="<paste-token>"
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://<argocd-host>/<base>/api/v1/applications/<app>/pods/<pod>/logs?container=<c>&tailLines=2000&namespace=<ns>"
```

The log endpoint returns NDJSON (one JSON object per line) — pipe through a parser:

```bash
curl ... | python3 -c "
import json, sys
for line in sys.stdin:
    line = line.strip()
    if not line: continue
    try:
        d = json.loads(line)
        c = d.get('result', {}).get('content', '')
        if c: print(c)
    except: pass
"
```

## Account-token limitation under SSO

If your ArgoCD uses Dex/SAML SSO and you try `POST /account/<self>/token` to mint a long-lived API key, expect a 403:

> SSO users are projected via SAML groups — they are NOT local accounts and have no `apiKey` capability.

Workarounds:
- Re-grab the browser token every ~24h (manual but audit-clean).
- Use the local `common` account if your ArgoCD has one with `apiKey` capability — but this breaks audit trail and is generally discouraged.
- **Long-term fix:** ask your infra team to enable `apiKey` capability on the SSO-group RBAC binding. That's the cleanest path.

## Log-access policy

When ArgoCD is in front, route ALL log access through it (CLI for prod, REST for non-prod) — do not bypass to `kubectl` against the cluster. Reasons:
- ArgoCD enforces RBAC and audit logging.
- `kubectl` access typically requires elevated privileges and bypasses the audit trail.
- Consistency: same access model in dev/uat/prod.

## Project-specific instances

Project-specific ArgoCD app names, environment matrix entries, and per-app log-fetch commands belong in your own project's docs, not here. This file documents the generic access pattern; your project-specific equivalent lists the actual app names and URLs.
