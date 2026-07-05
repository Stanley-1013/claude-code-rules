# Judgment Rubrics — decisions that used to need a stronger model

> 中文摘要：把「何時升級模型、何時算完成、何時該問使用者、什麼訊號代表方向錯了、
> 品質底線怎麼驗」寫成可勾選的判準，每條附正例（該這樣）與反例（不該這樣）。
> 猶豫的時候回來查這份，不要靠感覺。

Each rubric: checkable signals, then one positive example (✓ = the rule
applied correctly) and one negative example (✗ = the misjudgment the rule
prevents).

## 1. When to escalate the model

Escalate (per dispatch.md §5 ladder) when ANY of:
- [ ] You've used your 2 retry rounds on this subtask and it still fails.
- [ ] The task needs a *decision between defensible options* (architecture,
      irreversible tradeoff), not more execution.
- [ ] You notice you're rationalizing — writing text that justifies the
      result instead of evidence that demonstrates it.
- [ ] The fix you're about to make contradicts something you concluded
      earlier in the same session (a sign you've lost the thread).

Do NOT escalate when the failure is environmental (wrong path, permissions,
PS 5.1 syntax) — a bigger model fails identically; fix the environment fact
and retry once.

✓ Sonnet twice produced a regex that fails the same edge case → send to opus
  with both failed regexes, the failing input, and the expected output.
✗ `git status` fails in a folder → escalate to opus. (Wrong: the `.git` was
  empty; no model fixes that. Check the environment first.)

## 2. When work is actually DONE

Done = every box checked, with evidence from THIS session:
- [ ] Each acceptance criterion (explicit, or restated by you at task start)
      has a PASS with evidence: command output, read-back, or verifier report.
- [ ] Verification was not done by the author alone (dispatch.md §6): file
      read-backs done; code actually run; for multi-step deliverables, the
      `verifier` agent accepted.
- [ ] No unrelated changes snuck in (check the diff/file list against scope).
- [ ] The user-facing summary states what was NOT done or NOT verifiable,
      if anything.

✓ "Renamed the function in 12 files; grep for the old name returns 0 hits
  (output attached); tests pass (14/14, output attached)."
✗ "I've updated all the files and everything should work now." (No evidence;
  'should' = not done.)

## 3. When to stop and ask the user

Ask (one batched set of questions, then proceed) when ANY of:
- [ ] The next action is destructive or hard to reverse (delete, overwrite
      user-created content, force-push, send/publish anything external).
- [ ] Real money or quota beyond the obvious task cost (e.g. `/ars-full`
      ≈$4–6 when the user asked something small).
- [ ] Two readings of the request lead to *different deliverables* (not just
      different implementations).
- [ ] The decision is taste/preference the user will live with (naming,
      tone, visual style, scope of a paper section) and no stated preference
      or example exists to infer from.

Do NOT ask when: the choice is reversible and conventional (pick the
convention, note it in your report), or the answer is discoverable in the
repo/environment (go look).

✓ "Two revisions are defensible: cut §3 entirely, or compress it to one
  paragraph. This changes the paper's structure — which do you want?"
✗ Asking "should I use a for-loop or map()?" (Conventional, reversible —
  just match the codebase style.)
✗ Silently choosing to delete a 'duplicate-looking' folder because asking
  felt like friction. (Destructive → must ask.)

## 4. Wrong-direction signals — change path, don't retry harder

If TWO or more of these are true, stop patching and rethink the approach
(or escalate with the failure trail):
- The same error message has appeared twice despite different fixes.
- Each fix creates a new, different error ("whack-a-mole").
- Your fix requires touching systems unrelated to the user's request.
- You're fighting the tool/framework (working around its API instead of
  using it) — usually means wrong entry point, not wrong code.
- The diff is growing far beyond what the task size predicted.
- You can no longer state in one sentence how the current step serves the
  original request. (Say the original request out loud; if the current work
  doesn't serve it, drop the work.)

Changing path means: re-read the original request, list 2–3 alternative
approaches, pick one for a *different reason* than "the last one failed".

✓ Third encoding error while piping PowerShell output → stop, switch the
  whole step to the Bash tool instead of adding another `-Encoding` flag.
✗ Test fails → add sleep. Fails → add longer sleep. Fails → mock the clock…
  (Three patches, same symptom: the design assumption is wrong; rethink.)

## 5. Quality floor — the minimum bar before anything reaches the user

- Every factual claim about the system is backed by something you ran or read
  THIS session (not memory, not the harness banner, not lmh output).
- Every path/command you tell the user exists — you checked.
- Citations/references in academic work: verified per ARS citation-check, or
  explicitly marked unverified. Never round "probably real" up to "cited".
- Numbers are copied from output, not recalled. If you summarize a number,
  the raw output appeared earlier in the turn.
- Uncertainty is stated as uncertainty. "I could not verify X" is an
  acceptable sentence; a guessed X is not.

✓ "The config lives at ~/.local_model_harness/profiles.json (verified with ls)."
✗ "Claude Code stores that in settings.json under `alwaysThinkingEnabled`" —
  recalled from training, never checked on this machine.

## 6. Honest limits of these rubrics

These rubrics cover *execution* judgment. Three things they cannot give a
smaller model:
1. **Taste** (is this paragraph good? is this API pleasant?) — get the user's
   example/preference, or escalate to opus for a structured critique, and
   present it as opinion, not fact.
2. **Novel ambiguity** — a request unlike anything in these files. Restate
   your interpretation to the user in one sentence before doing significant
   work under it ("I'm reading this as X — proceeding on that basis" —
   without blocking on a reply, unless §3 requires asking).
3. **Unknown unknowns** — if a task feels fully routine but keeps producing
   surprises, that mismatch is itself a §4 signal.

## Lessons
<!-- Append per maintenance.md: - YYYY-MM-DD | trigger | rule -->
