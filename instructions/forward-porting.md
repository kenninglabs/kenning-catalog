# Forward-Porting / Patch Application — Preserve Every Source Change

**Triggers:** cherry-pick / rebase / forward-port / back-port / "port X from branch Y" / "apply patch" / "bring commit X to branch Y".

When applying a commit, merge, branch, or patch from one branch to another (cherry-pick, rebase, manual port, conflict resolution), **the contract is: every change in the source must end up in the target — semantically equivalent, not literally identical**. Nothing is allowed to silently disappear.

## Do NOT apply patches directly across diverged branches

**Default to manual, file-by-file re-application** — not `git cherry-pick`, not `git apply`, not `git merge` — when source and target have diverged (different upstream evolution, different refactors, different prerequisites). Automatic merge tools can produce conflicts that mask intent and silently drop logic. Manual application forces you to actually understand each change.

**Workflow:**
1. List the source commits in chronological order (`git log --reverse <range>`).
2. For each commit, read its diff with full context (`git show <commit> -- <file>`). Understand what it changes and why (commit message + any linked spec).
3. Open the corresponding file on the target branch and apply the change by editing it directly — adapting to the target's surrounding code (different field names, different method shapes, upstream renames, etc.).
4. Stage and commit each logical change separately on the target, referencing the source commit for traceability.
5. After each commit, run the target's build + full test suite for the touched area.

**Acceptable shortcuts** (only when source and target are nearly identical for that file): a pure-add file with no pre-existing target version can be created directly from the source and committed (still review before committing); a trivial one-line change with no surrounding divergence can be edited directly without ceremony.

**Never use** `git cherry-pick`/`git rebase`/`git apply`/`git merge --strategy=ours|theirs` across diverged branches. If you find yourself reaching for one of these, stop and re-read this section.

## Method/function-signature audit is mandatory

For every file touched by the port, diff the source and target's exposed signatures (functions/methods/exports). Any symbol present in the source but missing from the target after the port must be classified:
- **Intentional** — replaced by a refactored variant, or a spec-mandated removal. Note the reason in the commit message.
- **Accidental** — a regression, silently dropped during conflict resolution. Restore it.

Do not classify something as "intentional" just because it would simplify your conflict resolution — the bias must be toward preservation.

## Resolving conflicts — analyze, don't shortcut

When a conflict appears:
1. Read both sides fully — the source-branch hunk and the target-branch hunk. Don't accept either side blindly.
2. Understand the intent of each: what was the source commit trying to add/change? What was the target's pre-existing logic doing?
3. Synthesize so both intents survive. If the source adds a field and the target renamed an adjacent field, the resolution must include both the new field AND the rename, not pick one.
4. If you can't reconcile the two, stop and ask — don't drop one side just to make the build pass.

Recurring patterns to watch for: a conditional branch or switch case added on the source but missing on the target; a setter/builder call added on the source but missing on the target; a narrowed query/projection on the target that silently breaks a caller the source relied on.

## Verification gates

Before claiming the port is done: the target's build is clean, its full test suite passes, and the signature audit shows zero unintended removals on every in-scope file. If the source was already verified end-to-end somewhere (staging/production), call out that the target needs the same verification.

## Documentation

Every non-trivial forward-port gets a short note (branch correspondences, scope leaks found and reverted, symbol removals classified as intentional vs. accidental, any cross-repo coordination needed) — this is how the next person understands what was done and why, not optional bookkeeping.
