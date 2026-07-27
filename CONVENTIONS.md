# Catalog authoring conventions

## Rule vs. rationale split

In `instructions/*.md`, a trailing `## Why` (or `## Why <topic>`) heading marks pure rationale — content that explains *why* a rule exists, not the rule itself. Everything else in the file is the actionable rule.

This split exists so a future kenning feature can splice only the actionable content into a token-constrained system prompt (e.g. when an output-compression skill like caveman/ponytail is active) while keeping the full doc, rationale included, as what a human reads when reviewing the catalog. No new markup was needed for this — several instructions already ended in a natural `## Why ...` section; the convention is just to keep doing that consistently rather than weaving justification into rule prose.

**Not every instruction has one.** Force-splitting a doc where the "why" is fused into the rule itself (e.g. a classification rule whose bias — "toward preservation" — is part of correctly applying it, not decoration on top of it) produces a worse doc, not a better one. Add a `## Why` section only when there's a genuinely separable chunk of justification; leave rule-dense docs without one alone.

## Everything else

See `instructions/file-layout.md` for the doc-location/naming conventions this catalog's own content follows, and `instructions/migrate-docs.md`/`cleanup.md` for how existing content gets folded in or pruned over time.
