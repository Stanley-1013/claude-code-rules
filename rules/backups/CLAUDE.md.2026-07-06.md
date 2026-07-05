# Global operating rules (every session, every project)

> 中文摘要：這是全域路由檔，只放環境事實、鐵律、和「什麼時候去讀哪份規則檔」。
> 細節都在 ~/.claude/rules/ 裡，照下面的觸發條件用 Read 工具去讀，不要憑記憶。

## User & language
- User: NUS student (chuanhan.li@u.nus.edu). Work is ~50% academic writing
  (ARS plugin), ~50% coding/coursework/tooling.
- Reply to the user in the language they write in (usually Traditional
  Chinese). Code, commits, and rule files stay in English.

## Environment facts (Windows 11, verified 2026-07-05)
- Shell traps — PowerShell here is 5.1: no `&&`/`||` (use `;` or
  `if ($?) {}`), `Out-File`/`Set-Content` default to UTF-16 (always pass
  `-Encoding utf8`), don't append `2>&1` to native exes. Prefer the Bash tool
  for POSIX-shaped work.
- Paths contain Chinese segments (e.g. `OneDrive\桌面\...`) — always quote;
  OneDrive can hold file locks; a failed write may be sync interference, retry
  once then suspect the path.
- Trust command output over harness banners: at least one folder here
  (`OneDrive\桌面\DCIM`) has a dead `.git` that the banner reports as a repo.
- Local free models exist: the `lmh` CLI (documented by the `lmh` user
  skill) runs 4B–8B Ollama models for zero-stakes drafting. Their output is
  never verified — check before use.

## Hard rules (non-negotiable)
1. **Never self-verify.** Files: read back. Code: run tests or the real flow.
   Delegated/multi-step work: dispatch the `verifier` agent with only the
   acceptance criteria. Details: rules/dispatch.md §6.
2. **Retry cap (canonical).** An identical command: max 1 unchanged retry
   (2 attempts total). The same approach with variations: max 2 rounds. Then
   change approach, escalate the model, or report the blocker.
3. **Evidence before claims.** "Done/fixed/passing" requires the command
   output or read-back that proves it, in the same turn.
4. **Escalation ladder.** haiku fails once → sonnet. sonnet fails same subtask
   twice → opus WITH the full failure trail. Solved pattern → downgrade to
   haiku/lmh for batch application. Details: rules/dispatch.md §5.
5. **Don't burn the main context.** Can't name the exact file, or >3 files /
   >400 lines to read? Delegate to Explore/subagent; only conclusions come
   back. Details: rules/dispatch.md §1.

## Skill scoping (this section takes precedence over skill preambles)
Process skills (brainstorming, TDD, writing-plans, etc.) are for work that
creates or changes code/designs across multiple files, or when the user asks
for design help. For questions, lookups, single-file edits, and mechanical
tasks: skip process skills and do the task. Explicit user `/command` requests
always win. ARS: match mode to request size — light modes for single
sections/questions; `/ars-full` (≈$4–6) only when the user asks for
end-to-end output.

## Routing — Read these files when the trigger fires (they are NOT auto-loaded)
| When you are about to… | Read |
|---|---|
| Delegate anything, pick a model, or verify finished work | `~/.claude/rules/dispatch.md` |
| Write a dispatch prompt (search/implement/refactor/research/review) | `~/.claude/rules/delegation-templates.md` |
| Decide: escalate? done? ask user? change approach? | `~/.claude/rules/judgment.md` |
| Edit any file under `~/.claude/` (incl. this one) | `~/.claude/rules/maintenance.md` |
| Start a long/ambitious session, or something feels off about the setup | `~/.claude/rules/letter-to-future-sessions.md`, `~/.claude/rules/diagnosis.md` |

If a referenced file is missing, say so to the user and continue with this
file's hard rules — do not invent the missing content.

## Lessons loop
When you hit a repeatable mistake (wrong command form, wrong assumption about
this machine), append it to the `## Lessons` section of the matching rules
file per maintenance.md. A mistake written down once is plugged; unwritten, it
recurs every session.
