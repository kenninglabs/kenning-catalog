#!/bin/sh
if command -v brew >/dev/null 2>&1; then
  brew install git
elif command -v apt >/dev/null 2>&1; then
  sudo apt update && sudo apt install -y git
elif command -v dnf >/dev/null 2>&1; then
  sudo dnf install -y git
else
  echo "no brew/apt/dnf found -- see https://git-scm.com/downloads" >&2
  exit 1
fi
