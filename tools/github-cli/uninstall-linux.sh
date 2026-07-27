#!/bin/sh
if command -v brew >/dev/null 2>&1 && brew list gh >/dev/null 2>&1; then
  brew uninstall gh
elif command -v apt >/dev/null 2>&1; then
  sudo apt remove -y gh
elif command -v dnf >/dev/null 2>&1; then
  sudo dnf remove -y gh
else
  echo "no brew/apt/dnf found -- can't tell how gh was installed, nothing to uninstall" >&2
  exit 1
fi
