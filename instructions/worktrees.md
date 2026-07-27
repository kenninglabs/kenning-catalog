# Git Worktrees — Clean Up When Work Is Done

**Triggers:** user mentions `git worktree`, "create a worktree", isolated build, parallel-branch work; or you're about to run `git worktree add`/`remove`/`prune`.

`git worktree add` isolates per-branch forward-port/cherry-pick/parallel-build work without disturbing the main checkout. Treat it as **temporary scaffolding, not a long-term workspace** — lingering worktrees accumulate dangling branches, stale build state, and block a plain `git checkout` of the branch elsewhere.

**Default rule:** work committed + pushed → remove the worktree.

## When to remove (do it without asking)

All of these true:
- Working tree clean (nothing to commit).
- Branch tip is on the remote.
- The worktree was created for a finite task that's now done (forward-port landed, cherry-pick pushed, build verified).

```bash
# from the main repo root, NOT inside the worktree
git worktree remove /path/to/worktree
```

## When NOT to remove (pause and ask)

- Working tree has staged/unstaged changes.
- Branch isn't on the remote yet (local-only or ahead) — removing would risk losing work.
- The worktree is on a long-lived branch the user actively switches between.

Surface the situation, list what would be lost, and ask before a force-removal.

## Orphan local branches

After removing a worktree, its local branch ref usually remains. For a one-off branch (no remote, fully superseded) `git branch -D <branch>` only after confirming with the user — `-D` skips the merged-check and is destructive if the ref held unique commits. Default: leave the ref and mention it; let the user opt in to deleting it.

## Why this matters

Lingering worktrees block `git checkout <branch>` elsewhere ("branch is already used by worktree"), silently retain old build state that can mask real conflicts, and — the opposite failure — deleting one too eagerly loses track of in-progress work the user wanted to resume. Treat a worktree like a feature branch: create it for the task, remove it when done.
