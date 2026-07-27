# Session Start — Sync Before You Trust Local State

**Triggers:** the start of a new session, before addressing the user's first message.

The job: make sure your view of instructions and context matches the latest state on disk (and in any shared remote), not a stale cached view from a previous session. Other sessions, other machines, or other collaborators can push updates to shared instructions/context between when you last read them and now — skipping the refresh means silently operating on stale rules and out-of-date indexes.

## Sequence

1. **Sync first, before reading anything.** If you're working in a git repo with a remote others might push shared instructions/context/docs to, bring it up to date before trusting local state: pull if you're on the default branch, or fetch the default branch's ref (without merging into your own working branch) otherwise. Run this quietly — only surface output if it fails (conflict, dirty tree, network error), and report that in one line rather than blocking. Never force, rebase, stash, or auto-resolve to make a sync succeed — leave conflicts for the user.
2. **Note what changed**, if anything — a before/after ref diff over the instruction/context paths that matter, so you know what to flag in steps 4-5.
3. **Read your instructions fresh from disk every session start**, even if they "look familiar" from a prior session. Disk is current truth; your memory of last session is not.
4. **If the sync brought in changed instructions, say so before applying them.** One line — what changed, roughly where. The user needs to know the rules shifted under them; don't start silently following different guidance.
5. **If it brought in changed context/memory indexes, re-read just the indexes** (stay lazy on the bodies) so "what do we already know about X" stays accurate without a full reload.
6. **Check whether the project's own standard structure is current** (see `file-layout`) — a fast existence/shape check, not a rebuild. If something's missing or looks behind, list it and ask before running any fix (`migrate-docs`, or whatever setup step applies) — these can be slow, so keep them opt-in per session rather than auto-running.
7. **Probe required CLIs once, don't assume.** If the session will plausibly need a tool (this catalog's `tools/`, or anything else the task implies), check once whether it's on PATH. For each missing one, surface exactly one line pointing at how to install it, and wait for acknowledgement before actually running an install — these often touch `sudo`/package managers/shell config, which is out of scope for standing authorization. If everything needed is already present, stay silent about it.

## Why this order

Sync-then-read matters specifically in that order: reading stale instructions and *then* syncing means you've already started reasoning from rules that might be about to change under you. Doing the sync first, before you've read or acted on anything, avoids that whole class of "I was following the old rule" mistake.
