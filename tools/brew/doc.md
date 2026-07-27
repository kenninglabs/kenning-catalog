# Homebrew

Package manager for macOS (and Linux — "Linuxbrew"). Most of this catalog's other tools prefer installing through `brew` when it's present, since it's the one package manager that works the same way on both platforms.

- **Install docs:** https://brew.sh
- **Formulae search:** https://formulae.brew.sh

## Verify

```bash
brew --version
```

## Common commands

```bash
brew install <formula>     # install a package
brew upgrade <formula>     # upgrade one (or all, with no argument)
brew list                  # what's installed
brew tap <org>/<repo>      # add a third-party formula repository (e.g. hashicorp/tap)
```
