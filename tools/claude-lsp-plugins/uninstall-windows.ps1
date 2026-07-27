if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
  Write-Error "claude CLI not found on PATH -- nothing to uninstall it from"
  exit 1
}
$plugins = "typescript-lsp","pyright-lsp","jdtls-lsp","gopls-lsp","rust-analyzer-lsp","csharp-lsp","php-lsp","clangd-lsp","swift-lsp","kotlin-lsp","lua-lsp","ruby-lsp","elixir-ls-lsp"
foreach ($plugin in $plugins) {
  claude plugin uninstall "$plugin"
  if ($LASTEXITCODE -ne 0) { Write-Warning "$plugin uninstall failed" }
}
