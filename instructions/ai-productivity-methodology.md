# AI Productivity Reporting — Mandatory Format

**Triggers:** "how much time did this save", "time taken for X", "productivity gain", "what's the multiplier", "how long would this have taken without AI" — any direct question about hours, engineering days, or relative pace with vs. without AI, on work you can point to (commits, docs, deployments).

When asked this kind of question, answer in the structured format below, not a single headline number.

**This format stays mandatory even under an active output-compression skill (caveman, ponytail, or similar).** Compress the surrounding prose and caveats, not the numeric structure — the per-work-type rows, the ranges, and the Total row are the actual content being asked for; a compression skill should shrink the words around them, not collapse them into a single unqualified number.

## The format

### Section 1 — Scope-level aggregate (only when comparing 2+ tasks/scopes)

If the question spans multiple tasks/scopes/windows ("Task A vs Task B", "this quarter vs last"), open with a side-by-side table:

```
| Metric                                       | Scope A         | Scope B         | ... |
|-----------------------------------------------|-----------------|-----------------|-----|
| Without AI (normal solo pace)                | X–Y hrs         | X–Y hrs         | ... |
| With AI, task duration                       | ~X hrs          | ~X hrs          | ... |
| With AI, your active hours                    | ~X–Y hrs        | ~X–Y hrs        | ... |
| Multiplier (without-AI ÷ with-AI-active-hrs) | ~X–Yx           | ~X–Yx           | ... |
```

Skip this section for a single-task question.

### Section 2 — Per work-type breakdown (mandatory, per scope)

For each scope, render a 5-column table — work type, without-AI estimate, with-AI task duration, your active hours, and the resulting multiplier. Typical work-type rows: investigation/debugging, spec/design/doc writing, implementation, integration/wiring/config (only if the task has real architecture decisions in it), tests/ops/deployment/judgment. Always include a bold **Total** row.

Rules:
- Always use **ranges** (`44–68 hrs`), never single points.
- Always show **both** task duration AND your active hours as separate columns — task duration (wall clock while AI worked) and your active engagement time are different numbers and conflating them overstates the multiplier.
- Anchor every row to something checkable when possible — a commit range, a file path, a doc name — in the row label or a footnote.

### Section 3 — Reconciliation flag (when scopes don't add up cleanly)

If per-work-type numbers across scopes don't reconcile (e.g. a 2-task subset's implementation estimate roughly equals a much-larger full-window estimate), say so explicitly. Show what the discrepancy is, which estimate you trust more and why (bottom-up task-level detail usually beats a top-down guess), and how much it shifts the aggregate.

### Section 4 — Headline observations

Close with a few bullets: consistency of the multiplier across scopes, which work types show the highest/lowest multipliers and why, and anything about domain familiarity affecting the comparison (an engineer who already knows the codebase has a smaller "without AI" gap than a newcomer would).

### Section 5 — Compounding notes (only when relevant)

Worth mentioning when they apply:
- Running multiple agents in parallel adds further speedup on investigation/research phases — additive, not multiplicative, with the base multiplier.
- Fixed costs don't compress: standups, deployment windows, review wait times stay constant regardless of how fast the work itself goes.
- Quality cost: bugs introduced by moving faster have their own cost, typically eating back a small fraction of the hours saved.
- Hours saved are only valuable if engineering capacity was actually the bottleneck for the thing being measured.

## Calculating the numbers

For any task:

1. **Task duration with AI** (`T_ai`) — clock time from artifacts (commit timestamps, session logs, your own recollection).
2. **Estimate the without-AI baseline** (`T_baseline`) — what the same task would take without AI assistance, for whoever you're comparing against (yourself solo, a mid-level engineer unfamiliar with the codebase, etc. — state which). Use your own calibrated per-work-type multiplier ranges here; don't reuse someone else's numbers as if they were universal — they aren't, they're calibrated to a specific person's pace and a specific kind of work.
3. **Estimate your active hours** (`T_active`) via an engagement ratio per work type — investigation/docs work tends to need much less active engagement than implementation, which needs more, which needs more still for tests/ops/judgment-heavy work. Calibrate this from your own experience rather than assuming a fixed ratio.
4. **Multiplier** = `T_baseline ÷ T_active`, per row, then aggregated.
5. **Bracket everything** (low–high), never a single point.

## Surface premise conflicts before applying them

If the user's framing of the question contradicts what the underlying data actually shows (e.g. they ask you to exclude a period assuming no work happened then, but the commit history shows real delivery in that window), stop and show the data before producing the report — don't silently apply a premise you can already see is wrong. A real recurring failure mode: several people assumed to have stopped contributing by a given month turned out to have substantial later delivery once the actual dates were checked. Verify against live data, not against what anyone (including the person asking) remembers.

## Caveats — state these when they apply

- "Without AI" baselines are estimated, not measured — reasonable brackets, not precision numbers.
- The multiplier compresses a lot for a solo comparison (you vs. yourself without AI) versus a comparison against someone unfamiliar with the codebase, since a newcomer's baseline includes ramp-up time you already skip.
- Don't double-count parallel-agent speedup and the active-hours multiplier on the same phase.
- Don't extrapolate a single task's multiplier to whole-team productivity.
- Anchor every claim to an artifact — a commit, a doc, a deployment — never an abstract assertion.

## Why this format

A bare "3x faster" claim without a breakdown, ranges, or artifacts to anchor it is easy to produce and hard to trust — that's the whole reason this format exists. Anything less — a single unqualified number, no ranges, no work-type breakdown — is non-conformant for this kind of question, not just a lighter-weight answer.
