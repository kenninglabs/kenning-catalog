#!/bin/sh
if command -v brew >/dev/null 2>&1 && brew list terraform >/dev/null 2>&1; then
  brew uninstall terraform
elif command -v apt >/dev/null 2>&1; then
  sudo apt remove -y terraform
elif command -v dnf >/dev/null 2>&1; then
  sudo dnf remove -y terraform
else
  echo "no brew/apt/dnf found -- can't tell how terraform was installed, nothing to uninstall" >&2
  exit 1
fi
