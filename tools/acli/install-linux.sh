#!/bin/sh
if command -v brew >/dev/null 2>&1; then
  brew tap atlassian/homebrew-acli
  brew install acli
  exit 0
fi
arch=$(uname -m)
case "$arch" in
  x86_64) target=amd64 ;;
  aarch64|arm64) target=arm64 ;;
  *) echo "unsupported architecture: $arch" >&2; exit 1 ;;
esac
curl -LO "https://acli.atlassian.com/linux/latest/acli_linux_${target}/acli"
chmod +x ./acli
sudo install -o root -g root -m 0755 acli /usr/local/bin/acli
rm -f ./acli
