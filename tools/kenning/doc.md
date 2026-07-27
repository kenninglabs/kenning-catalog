# Kenning CLI + MCP

A verified codebase-understanding engine: code graph + search over one or more repos, plus a memory/trace store, exposed both as a CLI and as an MCP server. If you're syncing this catalog at all, you already have kenning running — this doc is about *using* the CLI and *wiring* the MCP server into other AI tools, not a from-scratch install (kenning isn't yet publicly packaged — no Homebrew tap or standalone installer exists at time of writing; it ships as part of the kenning app/daemon).

## CLI overview

```bash
kenning init              # bootstrap the current directory into a hub (.kenning.toml, source/, knowledge/)
kenning repo add <path|url>   # register a repo (clone if it's a URL)
kenning index              # index all registered repos (or one with --repo)
kenning search <query>      # BM25 over symbols + string literals
kenning explore <symbol>    # callers/callees/related edges/blast radius for an exact symbol
kenning recall <query>      # BM25 over docs + memory
kenning ask <query>         # recall + search_code together, two ranked sections in one call
kenning status              # per-repo index freshness/counts
kenning sync                # force an incremental re-index
kenning audit               # doc/hygiene lint over knowledge/ (see this catalog's `cleanup` instruction)
kenning memory-store        # store a typed, tagged memory
kenning trace-submit        # submit a v3 trace: validate -> evidence-audit -> render -> index
kenning wiki                # wiki page bootstrap/get (auto-regenerated, read-only)
kenning up                  # one command: index -> register -> serve
```

`kenning --help` / `kenning <subcommand> --help` for the full flag surface.

## MCP wiring

Two ways to expose kenning's tools (`ask`/`explore`/`search_code`/`recall`/`status`/`sync`/`staleness`/`memory_store`/`trace_submit`/`wiki_get` — see this catalog's `using-kenning` instruction for how to use them) to an MCP-capable AI tool:

- **`kenning mcp`** — serves MCP over stdio for the current hub. Minimal client config:
  ```json
  {
    "mcpServers": {
      "kenning": { "command": "kenning", "args": ["mcp"] }
    }
  }
  ```
- **`kenning serve`** — runs the daemon (file watcher + web UI + MCP over HTTP/SSE) for every hub the daemon has registered, not just the current directory. Use this if you want kenning running continuously in the background rather than spawned per-session.

After adding either to your client's MCP config, restart/reconnect so the client picks up the new server (same "newly-added server needs approval + reconnect" pattern most MCP clients use — see this catalog's `chrome-devtools-mcp` tool for the general shape of that flow).
