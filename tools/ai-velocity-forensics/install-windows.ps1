$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item "$scriptDir\ai_velocity_forensics.py" -Destination ".\ai_velocity_forensics.py"
Write-Host "wrote .\ai_velocity_forensics.py -- run: python ai_velocity_forensics.py <repo_path> <since=YYYY-MM-DD> [label] [base_branch]"
