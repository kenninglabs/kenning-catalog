#!/bin/sh
if ! command -v claude >/dev/null 2>&1; then
  echo "claude CLI not found on PATH -- nothing to uninstall it from" >&2
  exit 1
fi
claude plugin uninstall ponytail
