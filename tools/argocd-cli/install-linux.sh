#!/bin/sh
if command -v brew >/dev/null 2>&1; then
  brew install argocd
  exit 0
fi
arch=$(uname -m)
case "$arch" in
  x86_64) target=amd64 ;;
  aarch64|arm64) target=arm64 ;;
  *) echo "unsupported architecture: $arch" >&2; exit 1 ;;
esac
curl -sSL -o "argocd-linux-$target" "https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-$target"
sudo install -m 555 "argocd-linux-$target" /usr/local/bin/argocd
rm "argocd-linux-$target"
