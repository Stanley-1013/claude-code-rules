# claude-code-rules — a governance layer for weaker-model sessions

> 中文摘要：這是 `~/.claude/` 的制度層版本控制。由一次性的 Fable 5 session
> 於 2026-07-05 建立，目的是讓之後由 Sonnet/Haiku 執行的每個 session 都照同一套
> 調度、驗收、升降級規則運作。只納入制度檔；session 紀錄、快取、settings 一律不進版控。

Built in a single Claude Fable 5 session (2026-07-05) whose only task was to
convert one strong model's judgment into rules that smaller models (Sonnet 5
as the daily driver) can execute. Everything here is written FOR a
Sonnet-level reader: concrete thresholds, checkable criteria, positive and
negative examples.

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
| `rules/backups/` | Dated copies made before edits (maintenance.md §1). |
| `agents/verifier.md` | Read-only fresh-context acceptance agent (PASS/FAIL/CANNOT-VERIFY per criterion). |
| `hooks/ps51_guard.py` | Optional PreToolUse hook: blocks PowerShell 5.1 parser traps (`&&`, `\|\|`, `2>&1`) before execution. Enablement snippet in the file's docstring. Not active unless wired into `settings.json`. |

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

`settings.json`, `settings.local.json`, session history, caches, plugin
state, credentials — anything that is machine state rather than institution.
The whitelist `.gitignore` enforces this; keep it whitelist-style.
