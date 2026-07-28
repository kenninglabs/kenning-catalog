#!/usr/bin/env python3
"""PreToolUse deny hook — block a *real* `git push` statement.

Reads the Claude Code PreToolUse JSON on stdin, inspects `tool_input.command`,
and emits a deny decision only when the command actually invokes `git push` as a
subcommand — not when the phrase merely appears inside an echo/grep/comment or a
quoted argument. This fixes the substring false-positive of the older
`grep -qE '\\bgit push\\b'` hook (which blocked commands that only mentioned the
phrase). Deny-safe: on a parse failure where both `git` and `push` appear, it blocks.

Contract: print the deny JSON to stdout and exit 0 to block; print nothing and
exit 0 to let the normal permission flow proceed.
"""
import json
import re
import shlex
import sys

# A heredoc body is data, never shell syntax — scanning its literal text for
# "git"/"push" (e.g. prose that happens to mention both, far apart) is exactly
# the substring false-positive this hook exists to avoid. `<<-?'DELIM'` /
# `<<-?DELIM` introduces one; `(?!<)` excludes `<<<` (herestring, no body).
_HEREDOC_RE = re.compile(r"<<-?(?!<)\s*(['\"]?)(\w+)\1")

DENY = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": (
            "`git push` is blocked by the hub's PreToolUse safety hook "
            "(tools/hooks/block-git-push.py). Ask the user to push manually."
        ),
    }
}

# git global options that consume the FOLLOWING token as their value; a bare
# `push` appearing as such a value is not the subcommand.
_OPTS_WITH_VALUE = {
    "-C", "-c", "--git-dir", "--work-tree", "--namespace",
    "--exec-path", "--super-prefix", "--config-env",
}
_ENV_ASSIGN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
_CONTROL_OPS = {"&&", "||", ";", "|", "&", "|&", ";;", "(", ")", "{", "}"}


def _normalize_newlines(cmd):
    """Turn top-level (unquoted, unescaped) newlines into `;` so statements split.

    Quote- and escape-aware so a newline inside a quoted string is left intact.
    """
    out, single, double, esc = [], False, False, False
    for ch in cmd:
        if esc:
            out.append(ch)
            esc = False
            continue
        if ch == "\\" and not single:
            out.append(ch)
            esc = True
            continue
        if ch == "'" and not double:
            single = not single
            out.append(ch)
            continue
        if ch == '"' and not single:
            double = not double
            out.append(ch)
            continue
        if ch in "\n\r" and not single and not double:
            out.append(";")
            continue
        out.append(ch)
    return "".join(out)


def _strip_heredocs(command):
    """Remove heredoc bodies so `shlex` only ever sees real shell syntax — a
    heredoc's introducer line (`cmd << 'EOF'`) is normal syntax and parses fine;
    it's the body between it and the closing delimiter line that breaks `shlex`
    (unbalanced quotes/backticks in arbitrary text) and would otherwise fall
    through to the word-anywhere deny-safe check below."""
    lines = command.split("\n")
    out = []
    i = 0
    while i < len(lines):
        out.append(lines[i])
        m = _HEREDOC_RE.search(lines[i])
        if m:
            delim = m.group(2)
            i += 1
            while i < len(lines) and lines[i].strip() != delim:
                i += 1
            i += 1  # consume the delimiter line itself too
            continue
        i += 1
    return "\n".join(out)


def _statements(tokens):
    """Split a token stream into statements on shell control operators."""
    current, statements = [], []
    for tok in tokens:
        if tok in _CONTROL_OPS:
            if current:
                statements.append(current)
                current = []
        else:
            current.append(tok)
    if current:
        statements.append(current)
    return statements


def _is_git(token):
    # `git` or `/usr/bin/git`, but not `github`, `gitk`, `git-foo`.
    return token.rsplit("/", 1)[-1] == "git"


def _git_subcommand(statement):
    """Return the git subcommand of a git statement, else None."""
    i = 0
    while i < len(statement) and _ENV_ASSIGN.match(statement[i]):  # skip FOO=bar
        i += 1
    if i >= len(statement) or not _is_git(statement[i]):
        return None
    i += 1
    while i < len(statement):
        tok = statement[i]
        if tok.startswith("-"):
            if "=" not in tok and tok in _OPTS_WITH_VALUE:
                i += 2  # option + its value
            else:
                i += 1
            continue
        return tok  # first non-option token = subcommand
    return None


def _invokes_git_push(command):
    normalized = _normalize_newlines(_strip_heredocs(command))
    try:
        lexer = shlex.shlex(normalized, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        # Still unparseable after stripping heredoc bodies (genuinely unbalanced
        # quotes) → deny-safe, but require "git push" adjacent (only whitespace
        # between), not just both words present anywhere — matches what the
        # pre-this-hook naive `grep -qE '\bgit push\b'` caught, no broader.
        return bool(re.search(r"\bgit\s+push\b", command))
    return any(_git_subcommand(stmt) == "push" for stmt in _statements(tokens))


def main():
    try:
        data = json.loads(sys.stdin.read())
        command = (data.get("tool_input") or {}).get("command") or ""
    except (ValueError, AttributeError):
        return  # can't read the hook envelope → defer to normal flow
    if command and _invokes_git_push(command):
        sys.stdout.write(json.dumps(DENY))


def _selftest():
    cases = [
        ("git push", True),
        ("git push origin main", True),
        ("git -C /repo push --force", True),
        ("cd /repo && git push", True),
        ("git add -A && git commit -m 'x' && git push", True),
        ("echo 'run git push manually'", False),
        ("grep -n 'git push' README.md", False),
        ("git status", False),
        ("gh pr create --title push", False),
        (
            "cat >> memory.md << 'EOF'\n"
            "cross-referenced git diff mtimes; iced's Column::push drops void children\n"
            "EOF",
            False,
        ),
    ]
    failed = [cmd for cmd, want in cases if _invokes_git_push(cmd) != want]
    if failed:
        for cmd in failed:
            print(f"FAIL: {cmd!r} -> {_invokes_git_push(cmd)}", file=sys.stderr)
        sys.exit(1)
    print(f"ok: {len(cases)} cases")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
    else:
        main()
