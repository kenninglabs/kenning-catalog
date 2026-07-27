if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
  Write-Error "claude CLI not found on PATH -- install Claude Code first: https://claude.com/claude-code"
  exit 1
}
claude plugin marketplace add DietrichGebert/ponytail
claude plugin install ponytail@ponytail
