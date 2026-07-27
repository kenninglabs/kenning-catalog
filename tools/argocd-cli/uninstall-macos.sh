#!/bin/sh
if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew not found -- argocd was installed via brew, nothing to uninstall without it" >&2
  exit 1
fi
brew uninstall argocd
