# Using Kenning's Retrieval + Memory Tools

**Triggers:** any codebase/docs/memory question ("where/how/what calls/what depends on/how does X relate to Y"); before answering from grep alone; before claiming something doesn't exist in the codebase.

Kenning is a codebase-understanding engine with its own MCP tools. Default to them over raw file reading/grepping for anything beyond an exact literal lookup — they're built for exactly this and stay fresh as the code changes.

## The core decision: which tool

- **`ask`** — default to this first for almost everything. One call, free-text query, returns two independently-ranked sections: `docs_and_memory` (docs + stored memory) and `code` (symbols + string literals). Don't compare `score` *across* the two sections — they're on different scales — only compare `rank` within one section. `ask` does not call `explore`; it can't guess an exact symbol name from free text reliably.
- **`explore`** — reach for this only once you already have an *exact* symbol name and need its definition sites, callers, callees, or blast radius. It's syntactic, not semantic — verify a hop by actually reading the `file:line` it points to before asserting a call relationship as fact.
- **`search_code`** / **`recall`** individually — the two halves `ask` fuses together. Call one directly only when you specifically want just code-symbol hits or just docs/memory hits and want to skip the other half's noise.
- **`status`** — per-repo index freshness (node/edge/literal counts, stale counts). Check this if results feel thin or wrong before assuming the codebase itself lacks what you're looking for.
- **`sync`** — force an incremental re-index (one repo or all) if `status` shows the index is behind.
- **`staleness`** — re-audits stored trace/wiki evidence against the current files and flags what's gone stale. Different from `kenning audit` (see `cleanup`) — this checks whether *recorded evidence about the code* is still true, not documentation folder-structure hygiene.

## Saving what you learn

- **`memory_store`** — save a typed, tagged memory (`reference`/`feedback`/`project`/`user`/`decision`/`bug`). Upserts by `(scope, slug)`, so re-saving the same slug updates in place rather than duplicating. Writes to a single `memory.md` mirror per scope (`knowledge/<scope>/memory/memory.md`, or the shared scope's file for cross-cutting notes) — the file is the portable source of truth, this tool is just a convenient write path into it plus a semantic index on top.
- **`trace_submit`** — the rigorous path: submit a structured trace, which gets evidence-audited (grep-verified) before being rendered into a context doc and indexed. Hard-fails on fabricated evidence — nothing gets saved if the claims don't check out against the actual files. Prefer this over a plain memory note when you want the evidence chain preserved, not just the conclusion.
- **`wiki_get`** — read-only. Fetches a wiki page for a repo, auto-regenerated from the code graph on index change. There's no propose/review step — you can't edit it directly, only read the current generated state (including stale-section markers if the underlying code moved on without a regen yet).

## When to fall back to grep instead

An empty or thin result from `ask`/`recall` means the index doesn't have it *yet* — not that it doesn't exist. Check `status` for staleness before concluding something is genuinely absent from the codebase. If the daemon/tools aren't reachable at all, or a repo hasn't been indexed by kenning yet, grep is the correct fallback, not a failure — it has perfect recall on literal matches that a semantic index can miss, at the cost of not understanding structure the way `explore` does.
