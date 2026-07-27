# Detecting AI Usage From Git History

**Triggers:** "did &lt;team/person&gt; use AI", "validate AI usage", "was this AI-generated", or judging implementation velocity/efficiency from commit cadence across branches.

Companion to `ai-productivity-methodology`: that one is for *time-saved* math on **known-AI** work; this one is for *deciding whether AI was used at all*. Companion tool: `ai-velocity-forensics` (this catalog's `tools/`) — the script that computes the numbers below.

## Order of evidence (strongest → weakest)

1. **Hard trailers/messages (proof).** `Co-authored-by: Copilot/Claude/Cursor/aider`, "🤖 Generated with", "Apply suggestion from @Copilot". These *prove* a tool touched the commit/PR — but often mean **Copilot-as-PR-reviewer/Autofix bot**, not AI authoring. Always say which.
2. **Velocity anomalies (circumstantial).** Large *logic* LOC landing minutes after the author's prior commit; sustained kept-logic LOC/hour far above human norm.
3. **Commit-message style (weak).** AI-authored commits skew long/structured/conventional. Terse messages ("fix bug", "ABC-1234") are a mild human tell.
4. **Branch lifespan/cadence (context).** First→last commit span, active days, LOC/day.

## The hard limits — state these every time

- **IDE inline autocomplete (Copilot/Cursor tab-completion) leaves ZERO git trace.** Velocity forensics **cannot** rule it out. Absence of bursts ≠ "no AI."
- **Drip-committing** AI output across many small commits defeats velocity detection.
- **Generated/boilerplate inflates velocity** (XML config, DTOs, mappers, JSON, lockfiles). Separate `logic` vs `gen` vs `test` LOC and judge on **logic** only.
- **Refactors look fast.** Extract/rename/move operations produce high kept-LOC/hour by a human. A single elevated session during a known refactor is not, by itself, an AI signal.
- State the conclusion **evidence-bracketed**: "confirmed AI footprint = X; no evidence of bulk generation; cannot rule out invisible IDE autocomplete."

## How to run

```bash
git -C <repo> fetch --all --prune
python3 ai_velocity_forensics.py <repo_path> <since=YYYY-MM-DD> [label]
```

Scans all branches, dedups commits by hash. Save the output somewhere durable (e.g. `knowledge/<repo>/context/` for the write-up, `assets/` for the raw report — see `file-layout`).

## Reading the output

| Column | AI-leaning | Human-leaning |
|---|---|---|
| `terse%` (subject &lt;25 chars) | low (verbose) | high |
| `peakLPH` (logic LOC/hr, ≥15min session) | &gt;400 sustained on greenfield | 0, or only during a refactor |
| VELOCITY FLAGS (big logic commit &lt;30min after prior) | present | none |
| `CoPilot` (Nm msgs / Na autofix) | proves bot reviewer/autofix only, not authoring | 0/0 |

## Interpreting — never overclaim

Hard proof of AI authorship is trailers/messages only, and even that usually means a bot reviewer, not an author. Velocity is circumstantial — a green flag warrants a closer look (read the actual diffs), not a conclusion by itself. Write your conclusion as a bracket of confidence, not a verdict: what's confirmed, what's suggestive, and what genuinely can't be ruled out (IDE autocomplete, chief among them).
