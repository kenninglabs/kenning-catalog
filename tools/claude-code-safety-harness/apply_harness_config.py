#!/usr/bin/env python3
"""Idempotently merge the hub's harness safety baseline into .claude/settings.json.

- Unions the curated non-destructive allowlist (tools/harness/allowlist.common.json)
  into `permissions.allow` — dedupes, preserves existing entries and their order.
- Installs the git-push PreToolUse deny hook (tools/hooks/block-git-push.py) if no
  PreToolUse hook already references it.
- Preserves every other key in the file. Safe to re-run (no-op once applied).

The committed .claude/settings.json is a SAFETY-ONLY baseline (M1) that carries no absolute
paths (M2, hook uses ${CLAUDE_PROJECT_DIR}); personal/machine-specific config stays in the
gitignored .claude/settings.local.json (M3), which Claude Code deep-merges over this file.

Usage: python3 tools/apply_harness_config.py [--check]
  --check : report drift and exit 1 if changes are needed; write nothing (for audits).
"""
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))               # tools/
_REPO = os.path.abspath(os.path.join(_HERE, ".."))               # hub root
_ALLOWLIST = os.path.join(_HERE, "harness", "allowlist.common.json")
_SETTINGS = os.path.join(_REPO, ".claude", "settings.json")
_SCHEMA = "https://json.schemastore.org/claude-code-settings.json"
_HOOK_SENTINEL = "block-git-push"
_HOOK_CMD = 'python3 "${CLAUDE_PROJECT_DIR:-.}/tools/hooks/block-git-push.py"'


def _load(path, default):
    if not os.path.exists(path):
        return default
    with open(path) as fh:
        return json.load(fh)


def _hook_present(pre_tool_use):
    return any(
        _HOOK_SENTINEL in hook.get("command", "")
        for group in pre_tool_use
        for hook in group.get("hooks", [])
    )


def main(argv):
    check_only = "--check" in argv[1:]

    baseline = _load(_ALLOWLIST, {})
    want_allow = baseline.get("permissions", {}).get("allow", [])

    settings = _load(_SETTINGS, {})
    if not isinstance(settings, dict):
        print("refusing: existing .claude/settings.json is not a JSON object", file=sys.stderr)
        return 2

    settings.setdefault("$schema", _SCHEMA)

    perms = settings.setdefault("permissions", {})
    allow = perms.setdefault("allow", [])
    have = set(allow)
    missing = [entry for entry in want_allow if entry not in have]
    for entry in missing:
        allow.append(entry)

    hooks = settings.setdefault("hooks", {})
    pre = hooks.setdefault("PreToolUse", [])
    hook_present = _hook_present(pre)
    if not hook_present:
        pre.append({
            "matcher": "Bash",
            "hooks": [{"type": "command", "command": _HOOK_CMD, "timeout": 5}],
        })

    changed = bool(missing) or not hook_present

    if check_only:
        if changed:
            gaps = []
            if missing:
                gaps.append(f"{len(missing)} allow entr{'y' if len(missing) == 1 else 'ies'} missing")
            if not hook_present:
                gaps.append("git-push hook missing")
            print("harness config: DRIFT — " + "; ".join(gaps))
            return 1
        print(f"harness config: OK ({len(allow)} allow entries, git-push hook present)")
        return 0

    if not changed:
        print(f"harness config: already applied ({len(allow)} allow entries, git-push hook present) — no change")
        return 0

    os.makedirs(os.path.dirname(_SETTINGS), exist_ok=True)
    with open(_SETTINGS, "w") as fh:
        json.dump(settings, fh, indent=2)
        fh.write("\n")
    print(
        f"harness config: wrote {os.path.relpath(_SETTINGS, _REPO)} "
        f"(+{len(missing)} allow entries, git-push hook {'added' if not hook_present else 'present'})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
