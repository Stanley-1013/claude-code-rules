# Delegation Prompt Templates — copy, fill the ⟨blanks⟩, dispatch

> 中文摘要：五種常見派工（搜尋／實作／重構／研究／審查）的現成 prompt 模板。
> 每份都內建三件套（目標動機／驗收條件／回報格式）。照抄再填空，不要即興發揮。

Rules that apply to every template:
- Fill EVERY ⟨blank⟩. A blank you can't fill means the task isn't ready to
  delegate — sharpen it first (dispatch.md §2).
- Default agent/model is listed per template; escalate/downgrade per
  dispatch.md §5.
- Long outputs go to a file; the report carries the path (dispatch.md §4).
- After the agent reports: verify per dispatch.md §6 before using the result.

---

## T1 — Search / locate  (agent: `Explore`, model: sonnet; haiku if the target is precisely described)

```
Find: ⟨what — symbol, behavior, config, text⟩
Why: ⟨what I'll do with it, so you can judge relevance⟩
Search in: ⟨repo/dir/paths; say "medium" or "very thorough" breadth⟩
It probably looks like: ⟨naming guesses, file types, frameworks — or "unknown"⟩

Acceptance: every match listed as path:line with a ≤2-line role description;
say explicitly if you searched X and found nothing (absence is a finding).
Report: ≤15 lines. Locations + one-line conclusion. No file contents.
```

## T2 — Implementation  (agent: `general-purpose`, model: sonnet)

```
Implement: ⟨the change, concretely⟩
Why: ⟨user goal this serves⟩
Where: ⟨files/modules if known; otherwise the entry point to start from⟩
Constraints: ⟨style to match, APIs to use/avoid, what NOT to touch⟩

Acceptance:
1. ⟨observable behavior, testable: "running X prints/returns Y"⟩
2. ⟨tests: "existing tests pass" / "new test covering Z exists and passes"⟩
3. No changes outside ⟨scope⟩.
Report: files changed as path:line ranges; test/command output proving
acceptance 1–2 (paste ONLY the relevant lines); anything unverified, flagged.
Do not paste full diffs.
```

## T3 — Refactor / batch pattern application  (model: haiku WITH a worked example; sonnet without one)

```
Apply this proven pattern: ⟨before → after, abstractly⟩
Worked example (already completed and verified):
⟨paste ONE real before/after from this codebase⟩
Apply to: ⟨explicit file list — enumerate, don't say "everywhere"⟩
Do NOT: change behavior, reformat untouched lines, edit files outside the list.

Acceptance: every listed file transformed; ⟨verification command, e.g. build/
test/grep for the old pattern returning 0 hits⟩ passes.
Report: per file, one line: path — done/skipped(reason). Then the
verification command's output. Nothing else.
```

## T4 — Research (web or docs)  (agent: `general-purpose`, model: sonnet; opus only for contested/high-stakes questions)

```
Question: ⟨the precise question — one question per dispatch⟩
Decision it feeds: ⟨what will be chosen based on the answer⟩
Sources to prefer: ⟨official docs / repo / paper — or "any, but rank them"⟩
As of: today's date matters? ⟨yes/no — if yes, prioritize recency⟩

Acceptance: answer states its confidence; every load-bearing claim has a
source URL or file path; contradictions between sources reported, not
resolved silently; "not findable" is an acceptable answer.
Report: ≤20 lines: answer → evidence list → what remains uncertain. Long
notes go to a scratchpad file; give the path.
```

## T5 — Review / acceptance check  (agent: `verifier` for acceptance; `feature-dev:code-reviewer` or /code-review for code quality)

```
[for the verifier agent — send ONLY this, no implementation story:]
Artifacts: ⟨paths / diff / test command⟩
Acceptance criteria:
1. ⟨checkable criterion⟩
2. ⟨checkable criterion⟩
Context the checks may need: ⟨how to run things, where fixtures live⟩
```
The verifier's report format is fixed in its agent definition
(PASS/FAIL/CANNOT-VERIFY per criterion + final VERDICT). If `verifier` is not
in the available agent list, use the fallback in dispatch.md §6
(general-purpose + the verifier.md body as prompt preamble). If it REJECTs, fix
and re-dispatch; never argue it into an ACCEPT. Two REJECT cycles on the same
criterion = escalate per dispatch.md §5.

---

## Anti-patterns (all real failure modes)
- Delegating with "look into X and improve it" — no acceptance criteria, the
  agent returns an essay. Sharpen or don't delegate.
- Pasting half the conversation as context — if it needs that much context,
  do it inline (dispatch.md §1).
- One mega-dispatch with 4 unrelated asks — one task shape per dispatch;
  parallel dispatches are fine.
- Accepting a report that answers a *different* question than asked — re-read
  your own acceptance line before accepting theirs.

## Lessons
<!-- Append per maintenance.md: - YYYY-MM-DD | trigger | rule -->
