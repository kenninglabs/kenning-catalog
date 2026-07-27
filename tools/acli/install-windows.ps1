$arch = if ([System.Environment]::Is64BitOperatingSystem -and ($env:PROCESSOR_ARCHITECTURE -eq "ARM64")) { "arm64" } else { "amd64" }
Invoke-WebRequest -Uri "https://acli.atlassian.com/windows/latest/acli_windows_$arch/acli.exe" -OutFile "$env:LOCALAPPDATA\Microsoft\WindowsApps\acli.exe"
