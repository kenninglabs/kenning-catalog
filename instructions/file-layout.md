# File & Folder Conventions

**Triggers:** about to save/create a context doc, memory note, plan, spec, or generated artifact; user asks "where should this go".

kenning scaffolds a standard doc taxonomy for every repo it indexes (`kenning init` / the daemon's auto-bootstrap create these automatically — you don't need to `mkdir` them yourself):

```
knowledge/<repo>/
  context/       runtime / integration / code-behavior / incident findings
  memory/        decisions, preferences, references, bug-fix root causes
  analysis/      requirement digests, gap analyses
  superpowers/
    plans/       implementation plans (written before code)
    specs/       design specs (written before code)
  scripts/       reusable helper scripts for this repo
assets/          generated deliverables shared across all repos (reports, data
                 dumps, diagrams, exports — anything you *hand off*, not
                 anything you *reason from*)
```

## Rules

1. **Context docs** → `knowledge/<repo>/context/CXT_<TOPIC>.md` (uppercase-snake topic, `CXT_` prefix). One topic per file; consolidate rather than duplicate on overlap.
2. **Memory notes** → `knowledge/<repo>/memory/`. One file per note, or a single self-indexing file with `## <slug>` sections — pick one convention per hub and stay consistent.
3. **Plans/specs** → `knowledge/<repo>/superpowers/{plans,specs}/YYYY-MM-DD-description.md`. ISO date prefix sorts chronologically.
4. **Generated artifacts** (reports, exports, diagrams, data dumps) → `assets/`, grouped by responsibility (e.g. `assets/reports/`, `assets/diagrams/`) rather than by feature. Pick a small, stable set of responsibility folders for your project and reuse them — don't spin up a new top-level folder per artifact. If something is analysis you'll load back into context to reason from, it belongs in `knowledge/<repo>/analysis/`, not `assets/` — the distinction is *produced/handed-off* vs. *consumed/reasoned-from*.
5. **Source code stays untouched.** Never write findings, notes, or generated docs into `source/<repo>/` — that's the indexed codebase, not your notebook.

## Why a fixed taxonomy

Consistent locations mean an AI assistant (or teammate) starting a fresh session can find "what do we already know about this repo" without asking, and a `knowledge/<repo>/` tree that grows in a fixed shape stays skimmable instead of turning into a pile of ad hoc `notes.md` files scattered by whoever wrote them last.
