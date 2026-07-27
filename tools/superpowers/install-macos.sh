#!/bin/sh
if ! command -v claude >/dev/null 2>&1; then
  echo "claude CLI not found on PATH -- install Claude Code first: https://claude.com/claude-code" >&2
  exit 1
fi
if claude plugin install superpowers@claude-plugins-official; then
  exit 0
fi
echo "official marketplace install failed -- falling back to the author's marketplace" >&2
claude plugin marketplace add obra/superpowers-marketplace
claude plugin install superpowers@superpowers-marketplace
