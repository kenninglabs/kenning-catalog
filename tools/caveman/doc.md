# Caveman — Token-Compression Skill

Skill (Claude Code / Codex / Gemini / Cursor) that compresses agent output by ~65-75% via terse, fragment-based responses. Useful when you want concise, high-density replies without sacrificing technical accuracy.

- **Repo:** https://github.com/JuliusBrussee/caveman
- **Type:** skill, not an OS CLI.
- **Activation:** in-session `/caveman` slash command after install.

## Verify

Requires Node >= 18. The install is idempotent — safe to re-run.

## Activate / use

```
/caveman           # default compression
/caveman lite       # lightest compression
/caveman full       # full caveman mode
/caveman ultra      # maximum compression
/caveman wenyan     # classical-Chinese-style compression
```

Stop with:

```
normal mode
```

## Companion commands

```
/caveman-stats              # token savings tracker
/caveman-compress <file>    # compress a memory or notes file in place
```

Also affects commit-message and PR-review output when invoked from those flows.

## When to suggest this

- The user has said the assistant is too verbose.
- A long-running task is burning context and denser updates would help.
- Memory/notes files are bloated and need recompression.

Don't auto-activate it — it changes voice/formatting noticeably; let the user opt in.

## Uninstall

Re-run the install script with the uninstall flag (see the repo README), or remove the skill directory under `~/.claude/skills/caveman`.
