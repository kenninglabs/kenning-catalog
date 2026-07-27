#!/bin/sh
if command -v brew >/dev/null 2>&1; then
  brew install uv
else
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
