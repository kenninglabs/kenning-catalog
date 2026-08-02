# Catalog authoring conventions

## Rule vs. rationale split

In `instructions/*.md`, a trailing `## Why` (or `## Why <topic>`) heading marks pure rationale — content that explains *why* a rule exists, not the rule itself. Everything else in the file is the actionable rule.

This split exists so a future kenning feature can splice only the actionable content into a token-constrained system prompt (e.g. when an output-compression skill like caveman/ponytail is active) while keeping the full doc, rationale included, as what a human reads when reviewing the catalog. No new markup was needed for this — several instructions already ended in a natural `## Why ...` section; the convention is just to keep doing that consistently rather than weaving justification into rule prose.

**Not every instruction has one.** Force-splitting a doc where the "why" is fused into the rule itself (e.g. a classification rule whose bias — "toward preservation" — is part of correctly applying it, not decoration on top of it) produces a worse doc, not a better one. Add a `## Why` section only when there's a genuinely separable chunk of justification; leave rule-dense docs without one alone.

## `[limits]` — tier limits published to clients

`catalog.toml` may carry an optional `[limits.<tier>]` block that raises a tier's compiled-in
limits, so a number can change without cutting a kenning release:

```toml
[limits.free]
repos_per_hub = 30
hubs = 1
agents = 1
```

Tier keys are lowercase (`free`, `team`, `enterprise`). Every key is optional — a missing key
means "no override", and the client keeps its built-in value.

Three properties to know before publishing one:

- **A published value can only ever RAISE a limit, never lower it.** The client takes
  `max(built-in, published)`. This is deliberate: the worst a typo or a compromised push can do
  is be over-generous, rather than remotely locking every user out of their own hubs. Lowering a
  limit requires a kenning release.
- **There is no way to publish "unlimited".** Publish a large number instead. A sentinel value
  would be one more thing to get wrong for a case that rarely comes up.
- **Limits are version-scoped for free.** Clients resolve the catalog to the highest tag at or
  below their own version, so an older kenning can't pick up limits meant for a newer one — tag
  the catalog when publishing a change that should only reach newer clients.

A malformed or absent block is ignored and the client falls back to its built-in defaults; a
limits lookup is never allowed to fail an operation.

## Everything else

See `instructions/file-layout.md` for the doc-location/naming conventions this catalog's own content follows, and `instructions/migrate-docs.md`/`cleanup.md` for how existing content gets folded in or pruned over time.
