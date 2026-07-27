# Consolidating Scattered Docs Into a Standard Taxonomy

**Triggers:** "migrate this project's docs", "convert existing notes to the standard layout", "set up context docs for this project", "clean up all these loose markdown files" — a project has AI/context docs scattered across loose root `.md` files, ad-hoc `notes/`/`docs/` folders, or tool-specific config (`.cursor/rules/`, `.github/copilot-instructions.md`), and needs them consolidated into the taxonomy `file-layout` describes, for the first time.

This is a one-time consolidation, not ongoing maintenance — see `cleanup` for pruning an *already*-organized tree.

## Pre-flight — inventory before touching anything

1. **Find what exists:**
   - Loose root `.md` (`CONTEXT.md`, `NOTES.md`, `AI_INSTRUCTIONS.md`, `ARCHITECTURE.md`, …)
   - Tool-specific AI config (`.cursor/rules/`, `.github/copilot-instructions.md`, `.windsurf/`)
   - Existing `context/`/`docs/`/`notes/` folders, any index file
2. **Classify each doc's actual content**, not its filename:
   - Rules/methodology the assistant should follow → instructions
   - Findings/notes about how the code behaves, integration quirks, incident write-ups → context
   - Requirement digests, gap analyses (reasoned *from*, not handed off) → analysis
   - Design docs / plans written before implementation → plans/specs
   - Reports, exports, diagrams (handed *off*, not reasoned from) → generated artifacts
   - A file that mixes rules and findings → split it; default the ambiguous remainder to context.
3. **Report a plan before executing** — what moves where, what gets left alone. Wait for confirmation. Migration is disruptive if wrong; don't guess silently on ambiguous files, ask.

## Migration plan (target shape — see `file-layout`)

```
Loose root .md, rules-like content        → your project's own AI-instructions file
                                              (CLAUDE.md/AGENTS.md/etc., wherever one exists)
Loose root .md, findings/notes-like        → knowledge/<repo>/context/CXT_<TOPIC>.md
Existing context/ or notes/ folders        → knowledge/<repo>/context/ (rename to CXT_<TOPIC>.md)
Requirement analysis docs                  → knowledge/<repo>/analysis/
Design docs / plans                        → knowledge/<repo>/superpowers/{plans,specs}/YYYY-MM-DD-*.md
Reports, exports, diagrams                 → assets/<responsibility>/
Tool-specific AI config (.cursor/rules/…)  → leave the original in place (the tool auto-loads it);
                                              copy just the RULE content into your instructions file
                                              too, so the guidance is consistent across tools
```

## Execution

1. Preserve git history — `git mv` when the source is already tracked, not delete-and-recreate.
2. Split mixed files: the rules portion goes to instructions, the descriptive portion to context. If splitting is genuinely hard, default to context and note that a rule might be buried in it.
3. Never lose a unique fact in the move — same discipline as `cleanup`'s iron rules (verify every fact from the source is present in the destination before treating the source as migrated).
4. Fix any cross-references / index files pointing at the old locations.
5. **Never auto-delete the originals.** Leave them in place until the user explicitly confirms the new locations are good and asks for cleanup.

## What NOT to migrate

Source code, build/config files (`pom.xml`, `package.json`, `Cargo.toml`, …), `.git*`, user-facing docs (`README`/`LICENSE`/`CHANGELOG`/`CONTRIBUTING`), compiled/vendor folders, and any AI tool's own global memory directory outside the project (that lives with the tool, not the repo).

## Final report

Summarize what moved where (counts, not a blow-by-blow), what was left alone and why, and end with an explicit pending question: delete the originals now, or leave them until you're sure? Don't decide that for the user.
