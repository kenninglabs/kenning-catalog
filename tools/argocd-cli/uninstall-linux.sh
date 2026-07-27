#!/bin/sh
if command -v brew >/dev/null 2>&1 && brew list argocd >/dev/null 2>&1; then
  brew uninstall argocd
elif [ -f /usr/local/bin/argocd ]; then
  sudo rm -f /usr/local/bin/argocd
else
  echo "argocd not found via brew or /usr/local/bin -- nothing to uninstall" >&2
  exit 1
fi
