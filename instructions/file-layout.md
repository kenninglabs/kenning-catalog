# File & Folder Conventions

**Triggers:** about to save/create a context doc, memory note, plan, spec, or generated artifact; user asks "where should this go".

kenning scaffolds a standard doc taxonomy for every repo it indexes (`kenning init` / the daemon's auto-bootstrap create these automatically — you don't need to `mkdir` them yourself):

```
source/<repo>/     the indexed codebase itself (cloned/copied in) — read from,
                   never written to; this is not your notebook
knowledge/<repo>/
  context/       runtime / integration / code-behavior / incident findings
  memory/        decisions, preferences, references, bug-fix root causes
  analysis/      requirement digests, gap analyses
  superpowers/
    plans/       implementation plans (written before code)
    specs/       design specs (written before code)
  scripts/       reusable helper scripts/utilities FOR this repo (one-off
                 data-fix scripts, local dev setup, repo-specific tooling)
assets/          generated deliverables shared across all repos (reports, data
                 dumps, diagrams, exports — anything you *hand off*, not
                 anything you *reason from*)
```

## Rules

1. **Source code** → `source/<repo>/`. Read-only from an assistant's perspective — it's the thing being indexed, not a place to save findings, notes, or generated docs.
2. **Context docs** → `knowledge/<repo>/context/CXT_<TOPIC>.md` (uppercase-snake topic, `CXT_` prefix). One topic per file; consolidate rather than duplicate on overlap.
3. **Memory notes** → `knowledge/<repo>/memory/`. One file per note, or a single self-indexing file with `## <slug>` sections — pick one convention per hub and stay consistent.
4. **Plans/specs** → `knowledge/<repo>/superpowers/{plans,specs}/YYYY-MM-DD-description.md`. ISO date prefix sorts chronologically.
5. **Reusable scripts/utilities** → `knowledge/<repo>/scripts/`. Anything you write to automate a repeated task against this specific repo (a data-fix script, a local setup helper, a repo-specific lint/codegen wrapper) lives here — not loose in the repo root, not duplicated per-task under `assets/`.
6. **Generated artifacts** (reports, exports, diagrams, data dumps) → `assets/`, grouped by responsibility (e.g. `assets/reports/`, `assets/diagrams/`) rather than by feature. Pick a small, stable set of responsibility folders for your project and reuse them — don't spin up a new top-level folder per artifact. If something is analysis you'll load back into context to reason from, it belongs in `knowledge/<repo>/analysis/`, not `assets/` — the distinction is *produced/handed-off* vs. *consumed/reasoned-from*.
7. **Non-repo areas are exempt from the per-repo taxonomy.** Two common ones:
   - `knowledge/infra/` — project-wide operational docs that aren't about any one repo: environment/cluster guides, service maps, domain glossaries, deploy topology. Filenames: `UPPERCASE_SNAKE_CASE.md`, no `CXT_`/`INSTRUCT_` prefix (these are references, not context findings or instructions).
   - `knowledge/incidents/` — dated incident write-ups (production outages, regressions, anomalies worth a permanent record). Filename `YYYY-MM-DD-<slug>.md` (ISO date sorts chronologically), one incident per file, an index file (`knowledge/incidents/README.md` or `MEMORY.md`) with one row per file. A useful skeleton per incident: header (date/env/service/severity/status), TL;DR, timeline, root cause, evidence, fix options + recommendation, open items, cross-refs to the relevant `knowledge/<repo>/context/`. Mask any secrets/PII/card data before saving — see `secrets-and-pci`.
   Don't force either of these into the `context/memory/analysis/superpowers/scripts` per-repo shape — they're a different genre (operational reference / dated record, not per-repo findings), and forcing the fit just makes them harder to find.

## When a repo's name isn't obvious

Two situations where `knowledge/<repo>/` alone doesn't make the mapping self-evident — write it down explicitly the first time you hit it, rather than making every future session re-derive it:

- **Source name ≠ deployed/runtime name.** If a repo is checked out as `source/foo/` but runs in production (or ships) under a different name (e.g. a service named `foo-worker` in its deploy config), note that mapping in `knowledge/foo/context/` or `knowledge/foo/memory/` the first time it comes up. Don't rely on remembering it later.
- **Several repos got consolidated into one monorepo.** When standalone repos merge into `source/<monorepo>/<subrepo>/`, add one short pointer doc noting the old repo names and where they now live, and route new work to the monorepo, not the deprecated standalones. Anyone still looking under the old repo's `knowledge/<old-repo>/` should find that pointer, not silence.

For a hub tracking many repos where these mismatches pile up, a single top-level index (one table: repo name → its `knowledge/<repo>/` path, with a note per row for anything non-obvious) is worth maintaining — but only add it once the mismatches are real; don't pre-build an index for a hub that doesn't need one yet.

## Why a fixed taxonomy

Consistent locations mean an AI assistant (or teammate) starting a fresh session can find "what do we already know about this repo" without asking, and a `knowledge/<repo>/` tree that grows in a fixed shape stays skimmable instead of turning into a pile of ad hoc `notes.md` files scattered by whoever wrote them last.
