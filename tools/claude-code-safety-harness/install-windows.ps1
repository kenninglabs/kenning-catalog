$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
python3 "$scriptDir\apply_harness_config.py"
