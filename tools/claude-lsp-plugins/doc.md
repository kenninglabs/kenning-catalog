# Claude Code LSP Plugins

Anthropic-verified Language Server Protocol plugins. Each wires a real LSP (the same one your IDE uses) into Claude Code for real-time syntax checking, completion, refactor actions, type info, and code navigation in that language.

- **Plugin index:** https://claude.com/plugins (filter for "lsp")
- **Marketplace:** `claude-plugins-official` (all of these are Anthropic-verified)
- **Type:** Claude Code plugins, installed via `claude plugin install` (or the in-session `/plugin install`).

## Install

Running Install requires the `claude` CLI on PATH, then installs all 13 language LSP plugins non-interactively — the value is unlocked when whichever language you happen to edit already has its server attached, so there's little reason to install only some of them. The plugin itself is a thin shim either way; the cost of installing one you don't currently need is negligible.

## Per-language prerequisites

LSP plugins wrap a real language server — the **binary still has to be installed locally** (via `brew`/`apt`/the language's own toolchain). The plugin does not bundle the server.

| Plugin | Language | Required local binary | macOS install |
|---|---|---|---|
| `typescript-lsp` | TypeScript | `typescript-language-server` (npm) | `npm i -g typescript typescript-language-server` |
| `pyright-lsp` | Python | `pyright` (npm) | `npm i -g pyright` |
| `jdtls-lsp` | Java 8-24 | `jdtls` + JDK 17+ | `brew install jdtls openjdk@17` |
| `gopls-lsp` | Go | `gopls` | `brew install gopls` |
| `rust-analyzer-lsp` | Rust | `rust-analyzer` | `brew install rust-analyzer` (or via `rustup`) |
| `csharp-lsp` | C# | OmniSharp/Roslyn LSP | `brew install omnisharp` |
| `php-lsp` | PHP | Intelephense/phpactor | `npm i -g intelephense` |
| `clangd-lsp` | C/C++ | `clangd` | `brew install llvm` (provides clangd) |
| `swift-lsp` | Swift | `sourcekit-lsp` (ships with Xcode) | `xcode-select --install` |
| `kotlin-lsp` | Kotlin | `kotlin-language-server` | `brew install kotlin-language-server` |
| `lua-lsp` | Lua | `lua-language-server` | `brew install lua-language-server` |
| `ruby-lsp` | Ruby | `ruby-lsp` gem | `gem install ruby-lsp` |
| `elixir-ls-lsp` | Elixir | `elixir-ls` | `brew install elixir-ls` |

If a plugin installs successfully but the LSP isn't picking up, the local binary is the most likely missing piece — install it per the table above, then restart Claude Code.

## Verify

```
/plugin list
```

Each installed LSP appears with version + status. The `LSP` tool becomes more capable as more LSPs are attached.

## Update / uninstall

```
claude plugin update <plugin-slug>
claude plugin uninstall <plugin-slug>
```
