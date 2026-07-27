#!/bin/sh
if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew not found -- install it first (this catalog's 'brew' tool), or see https://developer.atlassian.com/cloud/acli/guides/install-macos/" >&2
  exit 1
fi
brew tap atlassian/homebrew-acli
brew install acli
