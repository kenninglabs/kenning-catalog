#!/bin/sh
if command -v brew >/dev/null 2>&1 && brew list acli >/dev/null 2>&1; then
  brew uninstall acli
elif [ -f /usr/local/bin/acli ]; then
  sudo rm -f /usr/local/bin/acli
else
  echo "acli not found via brew or /usr/local/bin -- nothing to uninstall" >&2
  exit 1
fi
