# Superpowers — Claude Code Skills Plugin

Composable-skills plugin by `obra` that bundles a complete software-development methodology: brainstorming → planning → TDD → debugging → code review → completion, plus support skills (git worktrees, subagent dispatching, parallel agents, skill authoring).

This is the framework behind every `superpowers:*` skill (`superpowers:brainstorming`, `superpowers:test-driven-development`, `superpowers:systematic-debugging`, etc.).

- **Repo:** https://github.com/obra/superpowers
- **Marketplace repo:** https://github.com/obra/superpowers-marketplace
- **Type:** Claude Code plugin (skills bundle) — not an OS CLI, installed via Claude Code's own `/plugin` command, not a shell script.

## Install (two options)

### Option 1 — Anthropic official marketplace (preferred)

```
/plugin install superpowers@claude-plugins-official
```

### Option 2 — author's own marketplace

```
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

Use option 2 if you want the newest skills before they land in the official marketplace, or if option 1 reports the plugin unavailable.

## Verify

```
/plugin list
```

`superpowers` should appear with a version. After install, the `Skill` tool lists `superpowers:*` skills in its available-skills surface.

## What it adds (skill highlights)

- `superpowers:brainstorming` — pre-implementation discovery for creative work.
- `superpowers:writing-plans` — formal plan-doc workflow before code.
- `superpowers:test-driven-development` — strict TDD discipline for features/bugfixes.
- `superpowers:systematic-debugging` — root-cause-first debugging, not shotgun fixes.
- `superpowers:receiving-code-review` / `superpowers:requesting-code-review` — review workflows.
- `superpowers:verification-before-completion` — evidence-before-assertion completion gate.
- `superpowers:using-git-worktrees` / `superpowers:dispatching-parallel-agents` / `superpowers:subagent-driven-development` — concurrency/isolation primitives.
- `superpowers:finishing-a-development-branch` — merge/PR/cleanup decision tree.
- `superpowers:writing-skills` — author your own skills using the framework's conventions.

## Update

```
/plugin update superpowers
```

## Uninstall

```
/plugin uninstall superpowers
```
