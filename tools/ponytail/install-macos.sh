#!/bin/sh
if ! command -v claude >/dev/null 2>&1; then
  echo "claude CLI not found on PATH -- install Claude Code first: https://claude.com/claude-code" >&2
  exit 1
fi
claude plugin marketplace add DietrichGebert/ponytail
claude plugin install ponytail@ponytail
