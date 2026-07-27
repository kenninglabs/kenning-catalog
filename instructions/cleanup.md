# Context/Memory Reduction — Reduce Doc Debt Without Losing Information

**Triggers:** user asks to "clean up" / "reduce" / "prune" / "what can be reduced" for context, memory, plans, specs, or analysis docs under `knowledge/<repo>/` (or `knowledge/infra/`, `knowledge/incidents/`), or for your own user-authored instructions.

## Scope

- Per repo: `knowledge/<repo>/{context,memory,analysis,superpowers,scripts}/` — the usual case, see the workflow below.
- Non-repo areas (`knowledge/infra/`, `knowledge/incidents/` — see `file-layout`): same iron rules apply, but skip the folder-structure/naming checks that only make sense for the per-repo shape (they're a different genre by design, not a drift to fix).
- **User-authored instructions**: the same doc-debt problem applies to instructions you've accumulated over time — one that's now fully covered by a public catalog instruction is a DUPLICATE (merge any unique bits, then delete); one nobody's triggered in months might be STALE or dead. Apply the same classify-then-act workflow to these as to any other doc, just scoped to instruction content instead of context/memory.

## Iron rules (non-negotiable)

1. **Never lose a unique fact.** Error codes, commit hashes, PR numbers, `file:line`, config values, deploy tags — each must survive into a kept doc before its source is deleted.
2. **Merge before delete.** For any consolidation: list the source's unique facts → fold into the keeper → verify each is present → only then delete.
3. **Keep in-progress work.** Delete only docs for work that is shipped/merged/deployed, or a finished one-off analysis. Anything still being implemented (open/unmerged PR, branch not shipped, "WIP" markers) → keep. Unsure → keep, mark uncertain.
4. **Stale ≠ deletable — update it instead.** If a doc's topic is still relevant but its facts are out of date, update the doc to current truth. Deletion is only for work that's genuinely done/superseded/duplicated; staleness is a refresh, not a removal.
5. **Verify completion with evidence, not assumption** — a PR number, deploy tag, "DONE/SHIPPED" marker, or another doc confirming delivery. No evidence → keep.
6. **Commit only when the user asks.** Show the deletion list before committing.

## Fast path — run the audit first

`kenning audit` (built into kenning itself — no separate install) checks the folder-structure compliance this instruction cares about: standard subfolder names, `CXT_`/`memory_`-prefix naming, dangling doc→doc links, un-indexed docs, staleness (docs with no verified-date, or older than ~120 days). Run it before doing anything by hand — `kenning audit --strict` exits non-zero on any hit, `kenning audit` alone reports errors only (warnings are the backlog, not blockers). Fix every ERROR it reports; work down WARNs over time.

## Workflow

### 1. Inventory
List tracked docs under `knowledge/<repo>/{context,memory,analysis,superpowers}/` with sizes; note the largest files.

### 2. Classify
Each doc → one of:
- **KEEP** — load-bearing current doc.
- **UNDER-DEV** — work still being implemented → keep, never delete.
- **STALE** — topic relevant, facts out of date → update, don't delete.
- **COMPLETED** — shipped/merged/deployed → delete candidate (verify evidence first).
- **SUPERSEDED** — fully covered by a newer doc → delete after confirming coverage.
- **DUPLICATE** — same facts in 2+ files → merge into one.
- **BLOAT** — file far larger than its actual information content → trim in place.

Default to KEEP/UNDER-DEV when completion is unproven; default to STALE→update (not delete) when a doc is merely out of date.

### 3. Execute
- **Merge**: fold unique facts into the keeper, verify, then delete the source.
- **Trim**: cut prose/duplication/settled design churn; keep every surviving fact.
- **Delete**: only verified-COMPLETED / confirmed-SUPERSEDED docs.
- **Refresh**: update STALE docs' facts to current truth.

### 4. Fix dangling links
Sweep for references to anything deleted or renamed (`grep` the old filename/stem across `*.md`); repoint dead links to the surviving doc, or annotate that the source was removed post-delivery and the current doc is now the record.

### 5. Record + commit
Save a short audit note (what was deleted/merged/trimmed/kept, and what was deliberately deferred). Commit with a clear message listing the changes, only when the user asks.

## Deferral discipline

Surface — don't silently skip — what you didn't delete: PR-pending one-offs, conditional archives, anything uncertain. List them for the user to decide.

## Out of scope

Source code, deploy config, the content of presentation/report assets, and any uncommitted user work in the tree. This is doc/index reduction only.
