if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
  Write-Error "claude CLI not found on PATH -- nothing to uninstall it from"
  exit 1
}
claude plugin uninstall superpowers
