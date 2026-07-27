#!/bin/sh
if command -v apt >/dev/null 2>&1; then
  sudo apt update && sudo apt install -y gh
elif command -v dnf >/dev/null 2>&1; then
  sudo dnf install -y gh
else
  echo "no supported package manager found (expected apt or dnf) -- see https://github.com/cli/cli#installation" >&2
  exit 1
fi
