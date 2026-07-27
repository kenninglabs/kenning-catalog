#!/bin/sh
if ! command -v npx >/dev/null 2>&1; then
  echo "npx not found -- install Node.js first: https://nodejs.org/" >&2
  exit 1
fi
npx -y chrome-devtools-mcp@latest --version
