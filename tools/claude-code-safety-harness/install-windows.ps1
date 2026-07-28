$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
New-Item -ItemType Directory -Force -Path .\tools\hooks, .\tools\harness | Out-Null
Copy-Item "$scriptDir\apply_harness_config.py" .\tools\apply_harness_config.py -Force
Copy-Item "$scriptDir\hooks\block-git-push.py" .\tools\hooks\block-git-push.py -Force
Copy-Item "$scriptDir\harness\allowlist.common.json" .\tools\harness\allowlist.common.json -Force
Write-Host "wrote tools/apply_harness_config.py + tools/hooks/block-git-push.py + tools/harness/allowlist.common.json -- run: python3 tools/apply_harness_config.py"
