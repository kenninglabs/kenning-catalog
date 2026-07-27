# Ponytail — Lazy-Senior-Developer Persona Skill

Claude Code skill that biases toward minimal, efficient implementations: stdlib/native-platform/existing-dependency solutions before writing new code, no unrequested abstractions, deletion over addition, and a "ladder" of preference (does this need to exist at all → already in the codebase → stdlib → native platform feature → existing dependency → one line → only then custom code).

- **Repo:** https://github.com/DietrichGebert/ponytail
- **Type:** Claude Code plugin (skill), installed via a marketplace add + plugin install (its own repo doubles as its marketplace).

## Install

Adds the plugin's own repo as a marketplace, then installs it — non-interactive.

## Activate / use

Active by default at `full` intensity once installed. Switch level or turn off:

```
/ponytail lite      # names the lazier alternative, lets you choose
/ponytail full      # the ladder enforced (default) -- stdlib/native first, shortest diff
/ponytail ultra     # YAGNI-extremist -- deletion before addition, challenges scope aggressively
stop ponytail       # revert to normal mode
normal mode         # same as above
```

## When to suggest this

- The user wants less over-engineering, fewer premature abstractions, or smaller diffs by default.
- A codebase has accumulated speculative complexity (unused config knobs, one-off interfaces) and the user wants a bias toward trimming it.

Not a fit when the task explicitly calls for the fuller version of something (input validation at trust boundaries, security measures, accessibility, anything the user asked for in full) — the skill itself carves these out as exceptions, not places to apply "lazy."

## Uninstall

```
claude plugin uninstall ponytail
```
