# ai-velocity-forensics

Git-history forensic script that judges whether commits were likely AI-assisted, from implementation velocity across all branches. Companion to this catalog's `ai-velocity-forensics` instruction (read it for the evidence ranking + hard limits before trusting the output).

## What it computes (per author, deduped across all branches)

- `logic`/`gen`/`test` LOC split — judge AI usage on **logic** only (`gen` = xml/json/yaml/properties/lock/gradle/md/dto/mapper/changelog/sql; `test` = `*Test.java`-style test files).
- `actDay` active days, `msgLen` avg subject length, `terse%` (subject &lt;25 chars — a mild human tell).
- `peakLPH` — peak sustained logic-LOC/hour over any ≥15-minute multi-commit session.
- `CoPilot` = `Nm`/`Na` — N Copilot-mentioning commit messages / N Copilot-Autofix co-authored commits.
- **VELOCITY FLAGS** — any commit with ≥250 logic LOC landing ≤30 minutes after the author's prior commit.
- **BRANCH LIFESPAN** — per branch, first→last unique-vs-base-branch commit span, days, LOC added.

## Install

Running Install writes `ai_velocity_forensics.py` into the current directory (it's a plain script, not an OS package — there's nothing to actually "install," just a file to place where you can run it).

## Run

```bash
git -C <repo> fetch --all --prune
python3 ai_velocity_forensics.py <repo_path> <since=YYYY-MM-DD> [label] [base_branch]
```

`base_branch` defaults to `main` — pass `master` (or whatever your default branch is) if that's what the target repo uses; branch-lifespan numbers are measured against it.

## Tunables (top of the script)

`BURST_GAP_MIN=45`, `BIG_LOGIC=250`, `FAST_BIG=30`, `HIGH_LPH=400`, plus the `GEN_PAT`/`TEST_PAT` regexes classifying generated/test files — adjust these to your stack's own file conventions if the defaults misclassify.

## Interpreting — never overclaim

Hard proof of AI is trailers/messages only, and even that usually means a bot reviewer, not an author. Velocity is circumstantial. IDE inline autocomplete leaves no git trace and cannot be ruled out by this script.
