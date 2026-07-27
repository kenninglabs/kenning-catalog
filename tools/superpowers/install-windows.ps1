if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
  Write-Error "claude CLI not found on PATH -- install Claude Code first: https://claude.com/claude-code"
  exit 1
}
claude plugin install superpowers@claude-plugins-official
if ($LASTEXITCODE -ne 0) {
  Write-Warning "official marketplace install failed -- falling back to the author's marketplace"
  claude plugin marketplace add obra/superpowers-marketplace
  claude plugin install superpowers@superpowers-marketplace
}
