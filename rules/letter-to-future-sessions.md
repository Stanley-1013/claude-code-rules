# Letter to Future Sessions

> 中文摘要：Fable 5 在 2026-07-05 建完這套制度後留下的信：三件使用者沒問但最重要的事、
> 這套制度最可能怎麼爛掉、以及怎麼防。開長 session 前或覺得環境怪怪的時候讀這份。

From: the Fable 5 session that built this rule set (2026-07-05).
To: whichever model is reading this — probably Sonnet 5. You are enough for
almost everything here, *if* you use the structure instead of improvising.

## Three things the user didn't ask me, but you should know

### 1. The filesystem is the biggest silent tax
Active work lives partly under `OneDrive\桌面\...` — Chinese path segments,
OneDrive sync locks, and at least one dead `.git` (DCIM). Cloud-synced paths
with non-ASCII segments are where tool calls go to die quietly. When starting
any NEW project, propose `C:\Users\ak990\Projects\<name>` (short, ASCII,
un-synced) and a real `git init`. When working in existing OneDrive folders,
expect the traps listed in CLAUDE.md § Environment facts and don't
misattribute them to your own code.

### 2. Global vs project knowledge — don't cross the streams
This rule set (`~/.claude/`) is global: it must stay true in every folder.
Project-specific facts (this repo's build command, this paper's venue) belong
in that project's own CLAUDE.md or its memory directory — never in these
files. The auto-memory feature is per-project and was empty everywhere as of
2026-07-05; if you find memory notes later, treat them as hints from a past
session, and re-verify anything load-bearing.

### 3. The user builds institutions, not just asks for tasks
They spent their single Fable session on infrastructure rather than output.
Match that: default to the cheap path (lmh for throwaway drafts, haiku for
mechanical work, light ARS modes), escalate deliberately with a stated
reason, and when you learn something reusable, WRITE IT BACK (maintenance.md
§4). A session that solves its task but writes back nothing has captured
half its value. Also: the plugin stack (superpowers + ARS + 8 others)
costs every session's preamble — if weeks pass with a plugin unused, suggest
disabling it in settings.json (suggest only; user decides).

## How this rule set will most likely rot, and the countermeasures

1. **Bloat until ignored.** Lessons accumulate, files grow, and a weak model
   under context pressure starts skimming. → Compaction triggers exist
   (maintenance.md §5). If you notice yourself *not wanting* to read a rules
   file because it's long, that IS the compaction trigger — say so to the user.
2. **Ritual compliance.** The words survive, the substance dies: dispatching
   the verifier but feeding it your implementation story; "escalating" by
   re-asking the same model; citing judgment.md §2 while writing "should work".
   The negative examples (✗) in judgment.md exist precisely to catch this —
   when you cite a rule, check you're not living its ✗ case.
3. **Router drift.** Files get renamed or reorganized; CLAUDE.md points at
   ghosts; trust in the whole system decays from one dead link. → Same-turn
   router-update rule (maintenance.md §1 step 5) plus the freshness audit
   (maintenance.md §6).
4. **Escalation inflation.** "To be safe" everything goes to opus, and the
   cost discipline that justified this system evaporates. → Opus requires a
   stated reason (dispatch.md §3); environmental failures never justify
   escalation (judgment.md §1).
5. **Overhead avoidance.** The opposite failure: rules feel heavy on small
   tasks, so they're skipped entirely, then also skipped on big tasks. → The
   thresholds are the answer: small tasks legitimately bypass most of this
   (dispatch.md §1 "do it inline"). Using the bypass correctly on small tasks
   is what keeps the discipline credible on big ones.

## Honest limits (do not paper over these)
Decomposition, verification, and multi-sample review — everything in these
files — repairs *execution* quality. It cannot supply taste or resolve
genuinely ambiguous requests (judgment.md §6). When you hit one of those:
escalate the model, get the user's example/preference, or say plainly "this
needs a judgment I can't verify". A confident guess is the only wrong answer.

## Handoff — unfinished business
None. All deliverables (diagnosis, CLAUDE.md, dispatch, judgment, templates,
maintenance, this letter, verifier agent) landed and were verified on
2026-07-05. If a future session leaves work incomplete, record it here per
maintenance.md §1 and point to the details.

## Lessons
<!-- Append per maintenance.md §4: - YYYY-MM-DD | trigger | rule -->
