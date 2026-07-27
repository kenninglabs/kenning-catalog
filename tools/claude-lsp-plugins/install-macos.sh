#!/bin/sh
if ! command -v claude >/dev/null 2>&1; then
  echo "claude CLI not found on PATH -- install Claude Code first: https://claude.com/claude-code" >&2
  exit 1
fi
for plugin in typescript-lsp pyright-lsp jdtls-lsp gopls-lsp rust-analyzer-lsp csharp-lsp php-lsp clangd-lsp swift-lsp kotlin-lsp lua-lsp ruby-lsp elixir-ls-lsp; do
  claude plugin install "${plugin}@claude-plugins-official" || echo "warning: ${plugin} install failed" >&2
done
