#!/bin/sh
script_dir=$(cd "$(dirname "$0")" && pwd)
mkdir -p ./tools/hooks ./tools/harness
cp "$script_dir/apply_harness_config.py" ./tools/apply_harness_config.py
cp "$script_dir/hooks/block-git-push.py" ./tools/hooks/block-git-push.py
cp "$script_dir/harness/allowlist.common.json" ./tools/harness/allowlist.common.json
chmod +x ./tools/apply_harness_config.py ./tools/hooks/block-git-push.py
echo "wrote tools/apply_harness_config.py + tools/hooks/block-git-push.py + tools/harness/allowlist.common.json -- run: python3 tools/apply_harness_config.py"
