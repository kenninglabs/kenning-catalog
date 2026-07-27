# Versioning Convention — Shared/Common Libraries

**Triggers:** about to bump a shared-library version (`build.gradle`/`pom.xml`/`package.json`/`Cargo.toml`); user mentions "release the shared lib", "bump the common module", "pre-release / dev-iteration version".

The generic, portable principle for versioning a library that other services/packages depend on. Fill in your own concrete artifact names, chosen pre-release tag, and worked examples in your own project notes — the principle below is what stays constant across projects.

## Separate stable releases from dev iterations

```
Base release version: X.Y.Z                                ← stable, promoted
Dev iterations:        X.Y.Z-<pre>.1, X.Y.Z-<pre>.2, ...    ← in-development, pre-release
Next base release:     X.Y.(Z+1)                            ← when the work stabilizes and is promoted
```

- Use a pre-release suffix (`-<pre>.N`, where `<pre>` is your project's chosen tag, e.g. `dev`/`rc`/`beta`) for every dev-iteration bump — bug fix, field addition, schema tweak made during active work. Increment the `.N` counter; do **not** bump the base version.
- Bump the base version (`X.Y.Z` → `X.Y.(Z+1)`) only when leaving the dev cycle — typically on merge to a release/stable branch.
- Downstream pins follow the same suffix: consumers pin to the exact pre-release (`X.Y.Z-<pre>.N`, not the base) while integrating in-development iterations, then move to the base version once it's promoted.
- Each pre-release bump needs a meaningful commit message — treat it as a release note, since downstream consumers will pull it.

## Why

- Preserves a predictable sort order in the package registry (Maven/npm/crates.io/etc.).
- Avoids version collisions between parallel feature branches.
- Makes pre-release / in-development status obvious from the version string alone.
