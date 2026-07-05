"""PreToolUse guard: block Windows PowerShell 5.1 parser traps before they run.

Scope & safety across machines/OSes (this file travels with the git repo):
- Non-Windows (macOS/Linux): the script exits 0 immediately (platform guard),
  and the `matcher: "PowerShell"` in settings means it is normally never even
  invoked there. Double-safe: enabling it on any OS cannot block anything
  that isn't Windows PowerShell.
- Windows with PowerShell 7+ as the harness shell: `&&`/`||` are VALID there.
  Claude Code's PowerShell tool uses Windows PowerShell 5.1 today; if a
  future machine's tool reports PS 7+ (`$PSVersionTable.PSVersion`), remove
  this hook entry from settings.json — the block message says so too.
- Fail-open by design: any malfunction of this script (bad JSON, missing
  python) exits non-2, which Claude Code treats as non-blocking. The guard
  can only ever block the two known-bad patterns, never break other tools.
- Stdlib only (json/re/sys/platform); works on Python 3.6+, `python` or
  `python3`, no pip dependencies.

Enable by adding to the machine's settings.json ("hooks" key, merge if one
exists — multiple PreToolUse entries coexist; all run, any exit-2 blocks):

  Windows:   "command": "python %USERPROFILE%/.claude/hooks/ps51_guard.py"
  mac/Linux: "command": "python3 ~/.claude/hooks/ps51_guard.py"
             (harmless there; only add it if you want symmetry)

  "hooks": {
    "PreToolUse": [
      { "matcher": "PowerShell",
        "hooks": [ { "type": "command", "command": "<see above>" } ] }
    ]
  }

Hook config is read at session start — changes take effect next session.
"""
import json
import platform
import re
import sys


def check(tool_name: str, command: str, system: str) -> "tuple[int, str]":
    """Return (exit_code, message). Pure function so it can be tested."""
    if system != "Windows":
        return 0, ""
    if tool_name != "PowerShell":
        return 0, ""

    # Strip single-quoted here-strings and strings; && inside a literal is
    # legal text, not an operator. Double-quoted strings are kept: && there
    # is almost always a real mistake.
    stripped = re.sub(r"@'.*?'@", "", command, flags=re.S)
    stripped = re.sub(r"'[^']*'", "", stripped)

    if re.search(r"&&|\|\|", stripped):
        return 2, (
            "Blocked: this machine's PowerShell tool is Windows PowerShell "
            "5.1 - '&&' and '||' are parser errors. Use ';' to chain, "
            "'if ($?) { B }' for conditional, or the Bash tool. "
            "(If this machine actually runs PS 7+, ask the user to remove "
            "the ps51_guard hook from settings.json.)"
        )
    if "2>&1" in stripped:
        return 2, (
            "Blocked: '2>&1' on native exes in PS 5.1 wraps stderr lines in "
            "ErrorRecords and poisons $?. stderr is captured for you - drop "
            "the redirection, or use the Bash tool."
        )
    return 0, ""


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # fail open: never block on our own malfunction
    code, message = check(
        payload.get("tool_name", ""),
        payload.get("tool_input", {}).get("command", ""),
        platform.system(),
    )
    if message:
        sys.stderr.write(message)
    return code


if __name__ == "__main__":
    sys.exit(main())
