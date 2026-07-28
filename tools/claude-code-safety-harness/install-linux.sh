#!/bin/sh
script_dir=$(cd "$(dirname "$0")" && pwd)
python3 "$script_dir/apply_harness_config.py"
