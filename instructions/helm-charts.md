# Helm / Deployment Config Repos — Environment-Tiered Push Discipline

**Triggers:** user mentions Helm, `image.tag` bump, an application-config repo, ArgoCD sync, "deploy to &lt;env&gt;", "merge to deployment branch".

For Helm/Kubernetes/ArgoCD config repositories that drive deploys, apply an **environment-tiered** push policy.

## Lower environments (dev / uat / staging / nonprod) — standing authorization

Once the user has asked to bump/deploy a tag to a lower environment, you may directly:
1. Edit the values file.
2. Commit and push to the config repo's default branch.
3. Trigger the ArgoCD sync (`argocd app sync <app>`).
4. Report sync + health status.

No per-step acknowledgement is needed once the user has said "deploy to uat" / "bump to &lt;env&gt;" — that one instruction covers the full commit→push→sync chain for the named lower environment. If a permission hook denies the push, surface the hook's message and wait — don't try to work around it.

## Production — diff first, push only after explicit acknowledgement

For production config repos/branches (path contains `prod`, branch is a prod release line, or the user explicitly names a prod target), the contract is stricter:

1. Make the edit locally (commit locally is fine).
2. **Show the user the diff** before pushing — the values change, plus one line on blast radius (which env, which service, which image tag is moving from → to).
3. **Wait for explicit acknowledgement** in the next user turn ("push it" / "go" / "approved" all count; silence or a hedged reply does not).
4. Only after acknowledgement: push + ArgoCD sync.

A prior "deploy to uat" acknowledgement does **not** carry forward to a production push, even in the same session. Each production push gets its own diff+acknowledge cycle.

## Why the asymmetry

Lower environments are recoverable — a bad tag bump rolls forward with the next push. Production tag bumps are observable to real users within seconds, and the rollback path (revert + re-sync) is slower than the forward path. That asymmetry justifies the different acknowledgement contracts.
