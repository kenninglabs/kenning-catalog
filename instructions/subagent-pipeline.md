# Multi-Agent Development Orchestration

**Triggers:** orchestrating multiple subagents to build/refactor/review a feature; parallelizing development across a codebase; coordinating with a peer agent sharing your branch/working tree.

## The pipeline

1. **Spec/plan before implementation.** Save specs/plans under `knowledge/<repo>/superpowers/{plans,specs}/` before writing code. If you have the Superpowers skill (`superpowers:brainstorming` → `writing-plans` → `subagent-driven-development`), use its fresh-implementer-per-task + per-task review workflow. If not, the same shape works plain: one subagent per task, a review pass (by you or a second subagent) before merging its work, and a final whole-diff review at the end.
2. **Decompose the plan into tasks tagged by the file(s) each touches** — this is what makes parallelism safe.
3. **Execute**, fanning out where files are disjoint, serializing where they aren't.
4. **Per-task review** → fix issues → re-review.
5. **Final whole-diff review** over the cumulative change → fix → ship.

## The parallelism rule that actually matters

**Parallel subagents ONLY across disjoint file sets.** One file cannot have two concurrent editors — simultaneous edits clobber each other or produce merge conflicts.

- Group tasks by file. Tasks on disjoint files → dispatch concurrently.
- Tasks that share a file (especially one large shared file) are serial — no number of agents speeds them up.
- **Serial-tail bundling**: when the remaining tasks all funnel through one big file, hand the whole serial chain to ONE subagent (with a commit + test per unit) instead of round-tripping through the orchestrator repeatedly.
- If pushed for "more agents, faster," the honest answer is often "the rest is one file, so it's serial" — say so.

## Shared-branch / peer-agent coordination

When another agent works the same branch/working tree concurrently:
- **Keep file sets disjoint.** Commits from different agents interleave on the branch without conflict as long as they touch different files. Map who-owns-what up front; if one file is genuinely shared, name it and hand it to one owner rather than both editing it.
- **One working tree has one branch/HEAD.** You cannot be on a different branch than a peer in the same tree — either both commit to the shared branch (disjoint files) or use a dedicated worktree.
- **Transient build/test races are expected** when a peer is mid-edit — retry before escalating. A peer's persistently-broken shared file blocks your build; surface it, don't work around it by stashing their in-progress work.
- **Namespace your own tracking artifacts.** If you keep a task ledger or status file for the work, don't share one generic file across every peer — give each feature/task its own (a `progress-<feature>.md` rather than one shared `progress.md`), and put reports/briefs a subagent produces under a namespaced directory for that feature rather than a generic `task-N` name any peer could collide with. Implementers should write directly into their own namespaced path, never copy a generic file over a peer's.
- **Order ledger entries newest-first, not chronological append-only.** A ledger's whole point is fast resume after a pause — a fresh session's first read should land on the current state, not scroll past months of history to reach it. Prepend each new entry above the previous one (the current/active state stays pinned at the top). Once an entry's narrative has been fully absorbed into a proper doc elsewhere, collapse it to a one-line pointer rather than letting the ledger re-accumulate the full text — the ledger indexes state, the doc holds the story.

## Review scoping under interleaved commits

If a peer's commits land between your task's commits, a full-branch diff review will sweep in their changes too. Scope the review to your specific commits or path-filter to your files before dispatching a reviewer.

## Deploy discipline

- **Build must succeed before deploy** — watch for a pipe masking the exit code (e.g. `build | tail -1` returns `tail`'s exit code, not the build's, so a naive build-then-deploy can ship a stale binary on a broken build). Check the build result explicitly.
- **Verify the deployed artifact is actually current** before trusting an "it's still broken" report — confirm the binary you're testing came from a build that includes the change.

## Model selection

Cheap/fast model for mechanical, code-complete implementation tasks (the plan already specifies the code — it's transcription+test); a stronger model for tasks needing judgment; the strongest available model for the final whole-diff review. Set the model explicitly per subagent rather than letting it default to whatever the orchestrator itself is running.

## File handoffs

Pass briefs, reports, and diffs as file paths, not pasted directly into prompts — anything pasted stays resident in the orchestrator's own context for the rest of the session. Give each subagent its task brief + report path; give a reviewer the brief + report + diff paths.
