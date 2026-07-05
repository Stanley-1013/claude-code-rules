# Maintenance Protocol — how future sessions update these files safely

> 中文摘要：規定弱模型怎麼改這套制度檔：哪些可自行改（追加 Lessons、修證實錯誤的
> 事實）、哪些要先問使用者（改門檻、刪規則、動 CLAUDE.md 路由、動 settings.json）、
> 改前先備份、教訓用固定格式寫回、累積過長怎麼精簡。

Applies to: `~/.claude/CLAUDE.md`, `~/.claude/rules/*.md`,
`~/.claude/agents/verifier.md`.

## 1. Before ANY edit to these files
1. Read the current file in full (not from memory of it).
2. Back it up (Bash tool; source is the file's FULL path, destination is
   always the backups dir; overwriting same-day backups is fine):
   `cp ⟨full path of file⟩ ~/.claude/rules/backups/⟨basename⟩.$(date +%F).md`
   Examples:
   `cp ~/.claude/CLAUDE.md ~/.claude/rules/backups/CLAUDE.md.$(date +%F).md`
   `cp ~/.claude/rules/dispatch.md ~/.claude/rules/backups/dispatch.md.$(date +%F).md`
   `cp ~/.claude/agents/verifier.md ~/.claude/rules/backups/verifier.md.$(date +%F).md`
3. Make the edit.
4. Read the changed section back and confirm the edit landed as intended.
5. If you renamed/moved/deleted a rules file: update the routing table in
   CLAUDE.md in the SAME turn — a dead pointer is worse than no pointer.
6. Commit and push: `~/.claude` is a git repo (remote: github.com,
   institution files only — the whitelist `.gitignore` must stay whitelist-
   style; never `git add -f` anything). After the edit lands:
   `cd ~/.claude && git add -A && git commit -m "<what changed and why>" && git push`
   (Bash tool). A push failure is non-fatal: report it and move on; never
   let it block the user's actual task.

## 2. What you may change WITHOUT asking the user
- **Append a Lesson** (format in §4) to the `## Lessons` section of the
  relevant rules file.
- **Correct a factual claim you have disproven this session with evidence**
  (a path that no longer exists, a command form that changed). Include the
  evidence in the edit's vicinity: update the "verified YYYY-MM-DD" date.
- **Fix typos/formatting** that don't change meaning.

## 3. What REQUIRES asking the user first
- Changing any threshold or ladder rule (retry caps, escalation order,
  the >3-files delegation bar, model defaults).
- Deleting or weakening any Hard rule in CLAUDE.md, or any numbered section
  of a rules file.
- Anything in `~/.claude/settings.json` / `settings.local.json` (model,
  plugins, permissions) — suggest, don't do.
- Rewriting the `verifier` agent's report format or read-only nature.
- Wholesale restructuring ("this file would be better organized as…").
  Present the proposal; let the user decide.

If the user *explicitly instructs* a change in the protected list, do it —
these rules bind your initiative, not the user's.

## 4. Lessons format (the write-back loop)
Trigger: you (or a subagent) made a mistake that a written rule would have
prevented, or discovered a machine-specific fact the hard way.

Append ONE line to the `## Lessons` section of the *most relevant* rules
file — dispatch.md for delegation/model lessons, judgment.md for
decision lessons, delegation-templates.md for prompt-shape lessons.
CLAUDE.md itself gets no Lessons section; only environment-fact corrections
go there (per §2).

Format (one line, pipe-separated):
```
- 2026-07-05 | git commands failed in DCIM despite banner saying "repo: true" | trust command output over banners; check .git is non-empty before git plans
```
Rules for a good lesson: state the *general* rule, not the anecdote; if an
equivalent lesson already exists, don't duplicate — sharpen the existing line
instead.

## 5. Compaction — when files grow stale or bloated
Trigger: a `## Lessons` section exceeds ~10 entries, or any rules file
exceeds ~250 lines, or two rules are found to contradict.

Procedure (allowed autonomously EXCEPT the deletion step):
1. Back up per §1.
2. Promote recurring lessons into the body of the file as proper rules.
3. Propose deletions (stale facts, superseded lessons) to the user as a list;
   delete only what they approve.
4. Re-verify the CLAUDE.md routing table afterwards.

## 6. Freshness audit (cheap, do opportunistically)
When a session is idle-ish or a rules file is being read anyway and its
"verified" date is >6 months old: spot-check 2–3 of its factual claims
(paths exist? commands still behave?). Update dates on what passes; fix per
§2 what fails. Do not schedule heavy audits — this is a piggyback task.

## Lessons
<!-- Append per §4: - YYYY-MM-DD | trigger | rule -->
