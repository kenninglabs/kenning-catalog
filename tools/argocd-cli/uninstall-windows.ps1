if (-not (Get-Command scoop -ErrorAction SilentlyContinue)) {
  Write-Error "scoop not found -- argocd was installed via scoop, nothing to uninstall without it"
  exit 1
}
scoop uninstall argocd
