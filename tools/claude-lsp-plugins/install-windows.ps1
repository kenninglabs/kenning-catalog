if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
  Write-Error "claude CLI not found on PATH -- install Claude Code first: https://claude.com/claude-code"
  exit 1
}
$plugins = "typescript-lsp","pyright-lsp","jdtls-lsp","gopls-lsp","rust-analyzer-lsp","csharp-lsp","php-lsp","clangd-lsp","swift-lsp","kotlin-lsp","lua-lsp","ruby-lsp","elixir-ls-lsp"
foreach ($plugin in $plugins) {
  claude plugin install "$plugin@claude-plugins-official"
  if ($LASTEXITCODE -ne 0) { Write-Warning "$plugin install failed" }
}
