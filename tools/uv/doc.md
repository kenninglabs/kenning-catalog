# uv

Fast Python package/project manager and installer, from Astral. Brings its own isolated Python, so it can install Python-packaged CLI tools without touching (or needing) the system Python.

- **Install docs:** https://docs.astral.sh/uv/getting-started/installation/
- **Docs:** https://docs.astral.sh/uv/

## Verify

```bash
uv --version
```

## Common commands

```bash
uv tool install <package>     # install a Python-packaged CLI in its own isolated env (like pipx)
uv tool update-shell           # make sure ~/.local/bin is on PATH after a tool install
uv venv                        # create a project virtualenv
uv pip install <package>       # pip-compatible install into the active venv
```

Prefer `uv tool install` over a bare `pip install --user` for any Python-packaged CLI in this catalog — it isolates each tool's dependencies instead of polluting one global environment.
