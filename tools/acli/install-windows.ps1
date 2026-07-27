$arch = if ($env:PROCESSOR_ARCHITECTURE -eq "ARM64") { "arm64" } else { "amd64" }
Invoke-WebRequest -Uri "https://acli.atlassian.com/windows/latest/acli_windows_$arch/acli.exe" -OutFile ".\acli.exe"
Write-Host "wrote .\acli.exe -- run .\acli.exe --version to verify, then move it onto PATH yourself"
