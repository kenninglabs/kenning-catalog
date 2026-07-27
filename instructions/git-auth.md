# Git / GitHub Auth — Credential Helper Hygiene

**Triggers:** a browser keeps opening a `http://127.0.0.1:<port>/?code=…&state=…` page for GitHub; git clone/fetch/push against `github.com` re-prompts for credentials repeatedly; a Git Credential Manager (GCM) OAuth popup appears on every git operation.

## Symptom
Every git operation against `github.com` launches an interactive Git Credential Manager (GCM) browser OAuth flow — the loopback callback is `http://127.0.0.1:<port>/?code=…&state=…`. It never persists, so it re-prompts on every op (clone, fetch, push, submodule update).

## Root cause
Global `~/.gitconfig` points the credential helper at GCM:
```
credential.helper = /usr/local/share/gcm-core/git-credential-manager
```
GCM has no `credential.credentialStore` configured and no cached `github.com` entry, so it does a fresh, non-persisting OAuth dance each time — even when a valid token is already available via `gh` (or `GITHUB_TOKEN` in the environment).

## Fix — route github.com through `gh` (scoped, reversible)
```sh
gh auth setup-git
```
This appends a `github.com`-only override to global `~/.gitconfig` (GCM stays in place for every other host):
```
credential.https://github.com.helper =
credential.https://github.com.helper = !/opt/homebrew/bin/gh auth git-credential
```
`github.com` auth now resolves through the existing `gh` token — no browser.

**Prereq:** `gh auth status` shows a logged-in account with the needed scopes (`repo`, `workflow`, and `read:packages` if you pull from GitHub Packages). The token may come from `GITHUB_TOKEN` env or `gh`'s own store; either works for `gh auth git-credential`.

## Verify (no prompt, no browser)
```sh
printf 'protocol=https\nhost=github.com\n\n' | git credential fill   # → username=x-access-token, password=<token>
GIT_TERMINAL_PROMPT=0 git ls-remote https://github.com/<any-org>/<any-repo>.git HEAD
```

## Notes
- Reversible: `git config --global --unset-all credential.https://github.com.helper`.
- If the token later expires, run `gh auth refresh` (or re-set `GITHUB_TOKEN`) — not the browser flow.
- `gh`'s path may differ per machine (`/opt/homebrew/bin/gh` on Apple Silicon, `/usr/local/bin/gh` on Intel); `gh auth setup-git` writes the correct absolute path automatically.
