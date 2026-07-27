# GitHub CLI (`gh`)

Official GitHub command-line client. Needed for any PR/issue/check/release operation an agent runs on your behalf.

- **Install docs:** https://github.com/cli/cli#installation
- **Manual:** https://cli.github.com/manual/

Install prefers Homebrew (macOS and Linux) when it's present, falling back to the platform package manager otherwise -- see this catalog's `brew` tool.

## Verify

```bash
gh --version
```

A working install prints `gh version X.Y.Z (YYYY-MM-DD)` plus the release URL.

## Authenticate

```bash
gh auth login
```

Interactive prompt: pick **GitHub.com** (or **GitHub Enterprise Server** for self-hosted), choose **HTTPS** for the git protocol, authenticate via **web browser** (opens a device-code flow) — paste the one-time code, approve in browser, done.

Non-interactive (CI / scripted, token via stdin):

```bash
gh auth login --with-token < ~/.config/gh-token
```

Status / logout:

```bash
gh auth status
gh auth logout
```

## Common commands

```bash
gh pr create --title "..." --body "..."       # open a PR
gh pr view <num>                                # PR metadata + comments
gh pr checks <num>                              # CI check status
gh pr diff <num>                                # diff
gh pr merge <num>                               # merge (only on explicit user ack)
gh issue view <num>                             # issue body + comments
gh api repos/<org>/<repo>/pulls/<n>/comments    # inline review comments
gh run list                                     # workflow runs
gh run view <run-id> --log                      # workflow log
```
