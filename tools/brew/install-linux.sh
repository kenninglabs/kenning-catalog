#!/bin/sh
NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo "installed -- add to PATH in a new shell: eval \"\$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)\"" >&2
