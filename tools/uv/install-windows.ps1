if (Get-Command scoop -ErrorAction SilentlyContinue) {
  scoop install uv
} else {
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
}
