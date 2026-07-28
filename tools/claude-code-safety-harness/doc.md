# claude-code-safety-harness

Installs a **safety-only** `.claude/settings.json` baseline for Claude Code: a curated
allowlist of read-only Bash prefixes (so routine safe commands — `git status`, `ls`, `grep`,
`cat`, …  — don't need a permission prompt every time) plus a `git push` PreToolUse hook
that hard-blocks any real `git push` invocation regardless of the allowlist, forcing a human
to push manually.

## Why two pieces, not one

- **Allowlist** narrows what auto-runs to genuinely non-destructive, read-only commands — no
  write/delete/network-install/push entries anywhere in it. Everything else still prompts.
- **`git push` block** is a categorical deny, not a prompt. Pushing is the one write operation
  explicit enough to warrant blocking outright rather than relying on the allowlist's absence
  alone — an agent with broad write access elsewhere could still reach for `git push` unless
  it's denied at the hook level. Subcommand-aware and quote-aware (tokenizes the actual shell
  command via `shlex` rather than a naive substring match, so it doesn't false-positive on the
  phrase "git push" appearing inside a comment/echo/heredoc), falls back to a deny-safe check
  only when the input is genuinely unparseable.

## Install

Running Install runs `apply_harness_config.py` **directly from wherever it lives** (typically
the synced catalog cache, `~/.kenning/catalog/tools/claude-code-safety-harness/`) against the
current directory — **nothing gets copied into your repo**. It writes `.claude/settings.json`
with a `PreToolUse` hook whose command points back at this tool's own `hooks/block-git-push.py`
in that same location, so a future catalog update to the hook is picked up automatically on
your next `kenning init`/sync — no reinstall step required.

```bash
python3 ~/.kenning/catalog/tools/claude-code-safety-harness/apply_harness_config.py          # writes .claude/settings.json
python3 ~/.kenning/catalog/tools/claude-code-safety-harness/apply_harness_config.py --check  # report drift only, writes nothing
```

Run it from the hub root you want to configure — `_REPO` is your current directory, not this
script's own location. Idempotent — safe to re-run. Unions the allowlist (never removes an
existing entry, yours or a teammate's) and only adds the hook if no `PreToolUse` hook already
references it.

## Self-test

```bash
python3 ~/.kenning/catalog/tools/claude-code-safety-harness/hooks/block-git-push.py --selftest
```

## Portability

The `.claude/settings.json` this produces is safety-only and meant to be **committed** across
your team — the allowlist has no absolute paths, and the hook command is the fixed string
`$HOME/.kenning/catalog/tools/claude-code-safety-harness/hooks/block-git-push.py`, which Claude
Code expands per-user, so it works identically for every teammate regardless of their own home
directory. Personal allows belong in the gitignored `.claude/settings.local.json`, which Claude
Code deep-merges over this baseline.

If you commit this settings.json, run `kenning init` (which syncs the catalog into
`~/.kenning/catalog`) at least once before opening Claude Code in a fresh clone — otherwise the
hook path won't resolve yet and the first Bash call will fail closed.

## Uninstall

Remove the `PreToolUse` hook entry (sentinel `block-git-push`) and any `allow` entries you
don't want from `.claude/settings.json`. There's nothing installed locally to delete.
