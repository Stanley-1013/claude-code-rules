# claude-code-rules — a governance layer for weaker-model sessions

> 中文摘要：這是 `~/.claude/` 的制度層版本控制。由一次性的 Fable 5 session
> 於 2026-07-05 建立，目的是讓之後由 Sonnet/Haiku 執行的每個 session 都照同一套
> 調度、驗收、升降級規則運作。**安裝方式：把這個 repo 的網址貼給任何新的
> Claude Code session，它照下面的 Agent Bootstrap 一節執行即可。**

Built in a single Claude Fable 5 session (2026-07-05) whose only task was to
convert one strong model's judgment into rules that smaller models (Sonnet 5
as the daily driver) can execute. Everything here is written FOR a
Sonnet-level reader: concrete thresholds, checkable criteria, positive and
negative examples.

## Agent Bootstrap — READ THIS FIRST if a user pasted this repo's URL at you

You are a Claude Code session being asked to install (or update) this
governance layer on the current machine. Do not reconstruct files from the
web view — install via git. Follow the steps exactly; where a step says
verify, actually run the command. Report per §B4 when done.

### B0. Which case am I in? (decide, don't guess)

Run: `git -C ~/.claude remote get-url origin`
- Prints this repo's URL → **already installed.** Run
  `git -C ~/.claude pull --ff-only`, then go to §B3 (verify).
- Prints a DIFFERENT URL → stop and ask the user which repo should win.
- Errors (not a repo) → **fresh install.** Continue with §B1.

### B1. Fresh install (Bash tool; identical in Git Bash on Windows and POSIX)

`~/.claude` already exists on any machine that has run Claude Code — you are
installing INTO it, never deleting it. Any pre-existing institution files are
preserved, not overwritten silently:

```bash
cd ~/.claude
BK="backups/pre-bootstrap-$(date +%F)"; mkdir -p "$BK"
for f in CLAUDE.md README.md rules agents hooks .gitignore; do
  [ -e "$f" ] && mv "$f" "$BK/"
done
git init -b main
git remote add origin https://github.com/Stanley-1013/claude-code-rules.git
git fetch origin
git reset --hard origin/main
git branch --set-upstream-to=origin/main main
[ -e machine.md ] || cp templates/machine.md.template machine.md
```

Notes:
- The repo's `.gitignore` is whitelist-style: `git reset --hard` only ever
  touches the institution files. Sessions, caches, and `settings.json` are
  untracked and untouched.
- If anything was moved into `$BK`, tell the user: those were this machine's
  previous versions; they can diff and merge or delete.
- If a command fails, fix the cause and retry ONCE (CLAUDE.md Hard rule 2
  binds you from this point on). Two failures → report the blocker.

### B2. Wire the PowerShell 5.1 guard hook (Windows machines only)

Skip entirely on macOS/Linux (the guard is a no-op there by design).
On Windows: open `~/.claude/settings.json` (Read tool; if the `hooks` key
already exists, MERGE — append to its `PreToolUse` array instead of
replacing it; never remove existing entries) and add:

```json
"hooks": {
  "PreToolUse": [
    {
      "matcher": "PowerShell",
      "hooks": [
        { "type": "command",
          "command": "python C:/Users/<USERNAME>/.claude/hooks/ps51_guard.py" }
      ]
    }
  ]
}
```

Replace `<USERNAME>` with the real Windows username (forward slashes, full
path — do not leave `~` in the command). Then confirm the whole file still
parses: `python -c "import json;json.load(open('<path>'))"`.
Do NOT commit settings.json — it is untracked by design; never `git add -f`.

### B3. Verify (run each; PASS/FAIL, no assuming)

1. `ls ~/.claude/rules` → the 6 rules files + `backups/` are present.
2. Read `~/.claude/CLAUDE.md` → every path in its routing table resolves
   (check with `ls`).
3. Hook self-test:
   `echo '{"tool_name":"PowerShell","tool_input":{"command":"a && b"}}' | python ~/.claude/hooks/ps51_guard.py; echo "exit=$?"`
   → Windows: prints a "Blocked:" message and `exit=2`.
   → macOS/Linux: prints nothing and `exit=0`. (Use `python3` if `python` is
   absent.)
4. `git -C ~/.claude status --short` → clean, or only expected local changes.

### B4. Report to the user, then stop

Tell them: (a) installed or updated, with the commit hash
(`git -C ~/.claude log -1 --oneline`); (b) the B3 checklist results;
(c) the path of any pre-bootstrap backup from B1; and (d) this exact
sentence: **"Restart the Claude Code session — CLAUDE.md, the `verifier`
agent, and the guard hook all load at session start, so they take effect in
the next session, not this one."**

### B5. Machine-specific facts (first session after install)

Machine facts live in `~/.claude/machine.md` — UNTRACKED, one per machine,
imported by CLAUDE.md at session start. B1 created it from
`templates/machine.md.template`; in the first working session, fill its
⟨blanks⟩ with facts you verify on THIS machine (shell type and traps, path
quirks, local models, enabled hooks). Never commit machine.md, never copy
another machine's version, and never write per-machine facts into the
tracked CLAUDE.md — two machines sharing this repo would fight over them
(this happened once; see rules/maintenance.md § Lessons).

## Layout

| Path | Role |
|---|---|
| `CLAUDE.md` | Auto-loaded every session. Environment facts, 5 hard rules, routing table to the files below. Kept ≤80 lines on purpose. |
| `rules/diagnosis.md` | Why these rules exist: top token leaks / focus risks / error sources of this machine, with fixes. |
| `rules/dispatch.md` | Delegation & model-selection protocol: when the main conversation must not do its own bulk work, escalation/downgrade ladder, verification contract. |
| `rules/judgment.md` | Externalized judgment: when to escalate, when work is DONE, when to ask the user, wrong-direction signals, quality floor. Each with ✓/✗ examples. |
| `rules/delegation-templates.md` | Five fill-in-the-blank dispatch prompts (search / implement / refactor / research / review). |
| `rules/maintenance.md` | How future sessions may edit these files: backup-first, lessons format, compaction triggers, what requires user approval. |
| `rules/letter-to-future-sessions.md` | Handoff letter: unasked-but-important facts, predicted failure modes of this rule set, countermeasures. |
| `rules/backups/` | Dated copies made before edits (maintenance.md §1). Local-only, untracked — shared backups from two machines would collide. |
| `templates/machine.md.template` | Skeleton for the untracked per-machine `~/.claude/machine.md` (created by B1, filled per B5). |
| `agents/verifier.md` | Read-only fresh-context acceptance agent (PASS/FAIL/CANNOT-VERIFY per criterion). |
| `hooks/ps51_guard.py` | PreToolUse hook: blocks PowerShell 5.1 parser traps (`&&`, `\|\|`, `2>&1`) before execution. Cross-OS safe: platform guard exits 0 on non-Windows, fail-open on malfunction, stdlib-only Python. Enablement is per-machine (§B2) — cloning never auto-enables it. |

## Design notes

- **MD is advisory, hooks are enforcement.** The rules files steer the model;
  the hook physically blocks a known-bad call. Only failure modes that are
  mechanical and high-frequency deserve a hook — everything else stays in MD
  where it costs zero when unused.
- **Token budget:** `CLAUDE.md` is the only always-loaded file (~67 lines).
  The `rules/*.md` files load on demand via the routing table. The hook costs
  tokens only when it fires — and firing *saves* tokens vs. a failed call.
- **Version control is part of the maintenance loop:** after any rule edit
  (see `rules/maintenance.md`), commit and push so the institution survives
  machine loss and stays diffable.

## Not included, deliberately

`settings.json`, `settings.local.json`, `machine.md`, `rules/backups/`,
session history, caches, plugin state, credentials — anything that is
machine state rather than institution. The whitelist `.gitignore` enforces
this; keep it whitelist-style.
