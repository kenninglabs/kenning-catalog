#!/bin/sh
if ! command -v claude >/dev/null 2>&1; then
  echo "claude CLI not found on PATH -- nothing to uninstall it from" >&2
  exit 1
fi
for plugin in typescript-lsp pyright-lsp jdtls-lsp gopls-lsp rust-analyzer-lsp csharp-lsp php-lsp clangd-lsp swift-lsp kotlin-lsp lua-lsp ruby-lsp elixir-ls-lsp; do
  claude plugin uninstall "${plugin}" || echo "warning: ${plugin} uninstall failed" >&2
done
