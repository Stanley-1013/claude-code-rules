# Global operating rules (every session, every project)

> 中文摘要：這是全域路由檔，只放環境事實、鐵律、和「什麼時候去讀哪份規則檔」。
> 細節都在 ~/.claude/rules/ 裡，照下面的觸發條件用 Read 工具去讀，不要憑記憶。

## User & language
- User: NUS student (chuanhan.li@u.nus.edu). Work is ~50% academic writing
  (ARS plugin), ~50% coding/coursework/tooling.
- Reply to the user in the language they write in (usually Traditional
  Chinese). Code, commits, and rule files stay in English.

## Environment facts (machine-local, imported)
This file is shared across machines via git; per-machine facts live in the
UNTRACKED `~/.claude/machine.md`, imported here:

@machine.md

If that import shows nothing (file missing — e.g. right after cloning to a
new machine), create `~/.claude/machine.md` from
`~/.claude/templates/machine.md.template`, fill it with facts verified on
THIS machine, and never commit it. Portable rule that holds everywhere:
trust command output over harness banners and memory notes.

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
   haiku (or a local model, if machine.md lists one) for batch application.
   Details: rules/dispatch.md §5.
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
When you hit a repeatable mistake, write it down: portable lessons go to the
`## Lessons` section of the matching rules file per maintenance.md §4;
machine-specific facts (shell traps, paths, local tools) go to the untracked
`~/.claude/machine.md`. A mistake written down once is plugged; unwritten, it
recurs every session.
