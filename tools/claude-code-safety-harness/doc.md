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

Running Install copies `apply_harness_config.py` + `hooks/block-git-push.py` +
`harness/allowlist.common.json` into `tools/` in the current repo (creating the subfolders).
Nothing is applied yet — that's a deliberate separate step:

```bash
python3 tools/apply_harness_config.py          # writes .claude/settings.json
python3 tools/apply_harness_config.py --check  # report drift only, writes nothing
```

Idempotent — safe to re-run. Unions the allowlist (never removes an existing entry, yours or
a teammate's) and only adds the hook if no `PreToolUse` hook already references it.

## Self-test

```bash
python3 tools/hooks/block-git-push.py --selftest
```

## Portability

The `.claude/settings.json` this produces is safety-only and meant to be **committed** — no
absolute paths (the hook command uses `${CLAUDE_PROJECT_DIR}`), no personal/machine config.
Personal allows belong in the gitignored `.claude/settings.local.json`, which Claude Code
deep-merges over this baseline.

## Uninstall

Remove the `PreToolUse` hook entry (sentinel `block-git-push`) and any `allow` entries you
don't want from `.claude/settings.json`, or delete `tools/apply_harness_config.py` /
`tools/hooks/block-git-push.py` / `tools/harness/allowlist.common.json` and stop re-running it.
