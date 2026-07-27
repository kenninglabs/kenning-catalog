#!/bin/sh
script_dir=$(cd "$(dirname "$0")" && pwd)
cp "$script_dir/ai_velocity_forensics.py" ./ai_velocity_forensics.py
chmod +x ./ai_velocity_forensics.py
echo "wrote ./ai_velocity_forensics.py -- run: python3 ai_velocity_forensics.py <repo_path> <since=YYYY-MM-DD> [label] [base_branch]"
