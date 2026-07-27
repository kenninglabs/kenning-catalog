#!/bin/sh
if ! command -v node >/dev/null 2>&1; then
  echo "node >= 18 not found -- install it first, then re-run" >&2
  exit 1
fi
curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash
