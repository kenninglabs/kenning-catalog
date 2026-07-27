#!/bin/sh
if command -v brew >/dev/null 2>&1; then
  brew install git
else
  echo "Homebrew not found -- run 'xcode-select --install' for Apple's Command Line Tools (includes git), or install Homebrew first (this catalog's 'brew' tool)" >&2
  exit 1
fi
