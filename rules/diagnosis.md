# Harness Diagnosis — where this setup wastes tokens, loses focus, and breaks

> 中文摘要：這份是 2026-07-05 由 Fable 5 對本機 Claude Code 環境做的體檢報告。
> 三大類問題（漏 token／失焦／出錯）各列前三名，附具體修法。
> 其他規則檔（dispatch.md、judgment.md 等）都引用這份的結論。

Written 2026-07-05 by a Fable 5 session, based on direct inspection of this
machine's config (`~/.claude/settings.json`, plugins, skills, project folders).
Facts below were verified at write time; re-verify before acting if this file
is more than a few months old.

## 1. Token leaks (biggest first)

### 1.1 The main conversation does its own bulk reading
**Symptom:** the driving model Reads whole files, greps the repo, and fetches
web pages in the main conversation. Raw dumps fill the context window; when the
context is later compacted, the *instructions* get summarized away along with
the dumps, and quality drops for the rest of the session.
**Fix:** follow `~/.claude/rules/dispatch.md`. Rule of thumb: if you cannot
name the exact file(s) you need, or you expect to touch more than ~3 files /
~400 lines just to *find* something, delegate to an `Explore` subagent and let
only the conclusion enter the main conversation.

### 1.2 Fixed session-start overhead from plugins
**Symptom:** every session, regardless of task, loads: the full
`superpowers:using-superpowers` skill text, the ARS plugin's SessionStart
summary (13 slash commands + agent list), and descriptions for ~50 skills.
That is several thousand tokens before the user types a word. For a 5-minute
task in a non-academic folder, most of it is dead weight.
**Fix (allowed without asking):** nothing — a session cannot remove plugin
injections about itself.
**Fix (user decision, see maintenance.md):** disable plugins for periods when
they are unused via `enabledPlugins` in `~/.claude/settings.json` (e.g. turn
off `academic-research-skills` outside paper-writing weeks). Suggest this to
the user when the overhead is clearly wasted; do not edit settings.json
yourself.

### 1.3 Re-deriving the environment every session
**Symptom:** before 2026-07-05 there was NO global CLAUDE.md and no saved
memory. Every session re-discovered the same facts by trial and error: that
PowerShell 5.1 rejects `&&`, that paths contain Chinese characters, that a
local Ollama harness (`lmh`) exists, which cloud models are available. Each
re-discovery costs a failed tool call or an exploratory detour.
**Fix:** per-machine facts now live in the untracked `~/.claude/machine.md`
(imported by CLAUDE.md at session start; created from
`templates/machine.md.template`). Update machine.md directly when a fact
changes — no backup/commit needed (maintenance.md §2). Portable lessons still
go through the lessons loop (maintenance.md §4) — a mistake made twice and
written down once is a leak plugged; unwritten, it recurs.

## 2. Focus-loss risks

### 2.1 Skill over-triggering
**Symptom:** the superpowers preamble demands invoking a skill before ANY
response ("even a 1% chance"). A weaker model obeys literally and runs
`brainstorming` for a one-line fix or `test-driven-development` for a doc
edit, spending the first 2k tokens of the task on process instead of the task.
**Fix:** the superpowers skill itself states that CLAUDE.md instructions take
precedence over skills. `~/.claude/CLAUDE.md` therefore scopes skill use:
process skills (brainstorming, TDD, writing-plans) only for tasks that will
create or modify code across multiple files or where the user asked for design
help. For single-file edits, questions, and lookups: just do the task.

### 2.2 Blind retry loops on Windows/PowerShell errors
**Symptom:** PS 5.1 syntax errors (`&&`, ternary), UTF-16 default encoding,
OneDrive file locks, and Chinese path segments produce failures that *look*
transient. Weaker models retry the same command verbatim 3–5 times, each retry
adding a full error dump to context.
**Fix:** hard cap in CLAUDE.md Hard rule 2 (details in dispatch.md §5): same
command may be retried at most once unchanged. Second failure means the
command is wrong — consult machine.md (imported via CLAUDE.md
§ Environment facts), change the command, or change approach.

### 2.3 Heavyweight pipelines when a light mode suffices
**Symptom:** the ARS `/ars-full` pipeline costs ≈$4–6 and produces a very
long transcript. Invoking it (or multi-agent review flows) when the user
wanted one section revised burns budget and buries the user's actual request.
**Fix:** match mode to request size first: single-section or single-question
work uses the light ARS modes (`/ars-revision`, `/ars-abstract`, …) or no
skill at all; full pipelines only when the user asks for end-to-end output.
When unsure which the user wants, ask — that one question is cheaper than the
wrong pipeline.

## 3. Error sources

### 3.1 PowerShell 5.1 + encoding
Top recurring failures: `&&` / `||` (parser error), `Out-File` writing UTF-16
that later tools misread, `2>&1` on native exes poisoning `$?`. The
known-good patterns are pinned in this machine's `~/.claude/machine.md`.
Prefer the Bash tool for anything POSIX-shaped.

### 3.2 Trusting local-model (lmh) output
`lmh` routes to 4B–8B Ollama models. They are drafting tools: useful for
first-pass translation, summarization, boilerplate. Their factual claims and
code DO NOT count as verified. Anything from lmh that will be shown to the
user or written to a file must be checked by the cloud model first (run the
code, spot-check the facts). This rule already exists in the lmh skill; it is
repeated here because violating it produces confident wrong output, the worst
failure mode.

### 3.3 Self-verification
**Symptom:** the model that wrote a change declares it works. In a long
session the writer's context is contaminated by its own intentions — it sees
what it meant to write. This produced (industry-wide, and observably with
smaller models) false "done" reports.
**Fix:** the verification contract in `~/.claude/rules/dispatch.md` § 6:
files get read back, code gets run, and acceptance checks go to a
fresh-context subagent (`verifier`) that receives only the acceptance
criteria, not the implementation story.

### 3.4 (bonus) Stale environment beliefs
Example found during this diagnosis: `c:\Users\ak990\OneDrive\桌面\DCIM` has
an empty `.git` directory — the harness banner claims "is a git repository:
true" but every git command fails. Lesson generalized: harness banners and
memory notes are *hints*, not facts. If a git/file operation contradicts the
banner, trust the command output and verify with `ls`/`git status` before
building plans on top.
