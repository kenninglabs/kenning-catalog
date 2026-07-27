# Debugging Playbook — Generic Template

**Triggers:** writing a debugging playbook for a recurring failure scenario; you just root-caused an incident that took >30 minutes, or an oncall thread re-asks the same diagnostic questions twice.

> **Project-independent.** How to write a high-signal debugging playbook for a known failure scenario. Distilled from working playbooks across distributed systems.

## Why playbooks matter

Most production incidents follow patterns. The first time you debug a class of failure, you discover a sequence of checks that narrows the cause. A playbook captures that sequence so the next person (or you, six months later) doesn't re-derive it.

A good playbook is:
- **Triggered by a symptom** (what the user/oncall reports), not a root cause
- **Sequenced** (numbered steps that progressively narrow the cause)
- **Cite-able** (each step says where to look — service, log pattern, DB query)
- **Closes with resolution** (what to do when each step's check fails)

## Mandatory structure

Every playbook follows this skeleton:

```markdown
## Playbook N: <Symptom Description>

**Symptom:** <one-line description of what the user/oncall sees, in plain language>

```
Step 1: <First check — usually the upstream-most service or external dependency>
  → <Where to look — log pattern, file, dashboard, DB query>
  → <What to verify — specific field, value, count, status code>
  → Common error: <if this check fails, this is the most likely cause>

Step 2: <Next check — usually the next service in the call chain>
  → <Where to look>
  → <What to verify>
  → Common error: <root cause if this fails>

[... continue until the failure is localized ...]

Step N: <Resolution>
  → <What to do once the cause is identified>
```

Known issue: <if the playbook is for a recurring problem with a workaround, document it here>
Workaround: <step-by-step recovery>
```

## Rules

### 1. Symptom-first naming

The playbook title and symptom line must describe **what an oncall person sees**, not what's wrong internally. Bad: *"Playbook 3: Kafka consumer rebalance during bulk processing"*. Good: *"Playbook 3: Bulk Pipeline Stall"* with symptom *"Items stuck in PENDING/IN_PROGRESS after upload"*.

The reader is searching by their symptom, not your diagnosis.

### 2. One playbook per failure class, not per root cause

If three different root causes produce the same symptom, they belong in ONE playbook with steps that distinguish them. Don't fragment.

### 3. Steps go from cheap to expensive

- Step 1 = cheapest check (read a log line you already have)
- Last step = most expensive check (DB query, restart, escalate)

This way the most common root cause is found in the fewest minutes.

### 4. Each step has a "Common error" callout

After describing the check, name the specific failure that justifies investigating this step. Without this, the step is just busy-work; with it, the playbook is also a teaching artifact.

### 5. Reference paths, not narratives

Bad: "First, you should look at the gateway logs to see if there's a problem with the request..."

Good: "Search `<service>` logs for `<exact log pattern>` → verify `<field>=<expected value>`."

The reader doesn't need persuasion that this step matters — they need the command/path.

### 6. Quick-reference table at the bottom

End the file with an error-pattern table that maps log lines / status codes to which playbook covers them:

```markdown
## Quick Reference: Error Patterns

| Log Pattern | Service | Meaning |
|-------------|---------|---------|
| `<distinctive log line>` | `<service>` | `<which playbook> / <one-line meaning>` |
| `<error status code or message>` | `<service>` | `<which playbook>` |
```

This lets oncall paste a log line into the file and find the matching playbook.

## When to write a new playbook

Trigger | Action
---|---
You just debugged a failure that took >30 minutes to root-cause | Write a playbook before the steps fade from memory
You see an oncall thread asking the same diagnostic questions twice | Capture the sequence as a playbook
A class of failure has a workaround that's not obvious from logs alone | Document the workaround at the bottom of the playbook

## What's NOT a playbook

- **Root-cause analysis docs** — those go in incident postmortems, not in playbooks
- **Architecture descriptions** — those go in service maps and dataflow docs
- **Deployment runbooks** — those are for releasing, not debugging
- **Code fix descriptions** — those go in commit messages and PRs

A playbook is a **diagnostic flowchart**, not a narrative. Treat it as a tree of `if-this-then-look-there` branches.

## Project-specific playbook collections

Specific playbooks for actual failure scenarios in your project belong in your own project's docs, not here. This file is the template/methodology; your project-specific file has the real playbooks indexed by symptom.
