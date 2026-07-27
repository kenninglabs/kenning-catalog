#!/bin/sh
if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew not found -- install it first (this catalog's 'brew' tool), or see https://github.com/cli/cli#installation" >&2
  exit 1
fi
brew install gh
