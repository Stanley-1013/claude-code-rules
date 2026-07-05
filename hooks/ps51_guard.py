"""PreToolUse guard: block PowerShell 5.1 parser errors before they run.

Not enabled by default. To enable, add to ~/.claude/settings.json:

  "hooks": {
    "PreToolUse": [
      {
        "matcher": "PowerShell",
        "hooks": [
          {
            "type": "command",
            "command": "python C:/Users/ak990/.claude/hooks/ps51_guard.py"
          }
        ]
      }
    ]
  }

Exit 2 blocks the tool call and feeds stderr back to the model, replacing a
failed execution + long parser-error dump with a one-line correction. Exit 0
lets the call through. Token cost when not triggered: zero.
"""
import json
import re
import sys


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0  # never block on our own malfunction

    if payload.get("tool_name") != "PowerShell":
        return 0
    command = payload.get("tool_input", {}).get("command", "")

    # Strip single-quoted strings and here-strings; && inside a literal
    # string is legal. Double-quoted strings still interpolate, but && there
    # is almost always a mistake too, so we keep them.
    stripped = re.sub(r"@'.*?'@", "", command, flags=re.S)
    stripped = re.sub(r"'[^']*'", "", stripped)

    if re.search(r"&&|\|\|", stripped):
        sys.stderr.write(
            "Blocked: this machine runs Windows PowerShell 5.1 - '&&' and "
            "'||' are parser errors. Use ';' to chain, 'if ($?) { B }' for "
            "conditional, or the Bash tool. (CLAUDE.md - Environment facts)"
        )
        return 2

    if re.search(r"2>&1", stripped):
        sys.stderr.write(
            "Blocked: '2>&1' on native exes in PS 5.1 wraps stderr lines in "
            "ErrorRecords and poisons $?. stderr is captured for you - drop "
            "the redirection, or use the Bash tool."
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
