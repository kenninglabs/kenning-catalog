if (-not (Get-Command npx -ErrorAction SilentlyContinue)) {
  Write-Error "npx not found -- install Node.js first: https://nodejs.org/"
  exit 1
}
npx -y chrome-devtools-mcp@latest --version
