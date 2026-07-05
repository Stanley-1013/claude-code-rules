# Model Dispatch Protocol — who does what, at which model, and how work comes back

> 中文摘要：這份規定主對話（指揮官）何時派 subagent、怎麼派（目標／驗收／回報三件套）、
> 用哪個模型、錯了怎麼升級、對了怎麼降級省錢、以及「驗收不能自己驗」的鐵律。
> 預設指揮官是 Sonnet 5。每次要派工前，先照著這份做。

Assumes the main conversation ("the commander") runs on **Sonnet 5** by
default (the machine's setting may still read `claude-fable-5[1m]` — that was
the one-off session that wrote these files; Sonnet 5 is the steady state).
Written 2026-07-05; model names verified against this machine at that date.

## 1. The commander does not descend

The main conversation is the scarcest resource in the session. Protect it.

**Delegate to a subagent** (don't do it inline) when the task is any of:
- Searching for something when you cannot name the exact file — repo sweeps,
  "where is X handled", naming-convention hunts → `Explore` agent.
- Reading more than ~3 files or ~400 total lines just to gather context.
- Web research needing more than one page fetch.
- Mechanical batch edits across many files *after* the pattern is proven
  (see §5 downgrade).
- Any acceptance check on completed work (see §6 — never inline).

**Do it inline** (spawning would waste money and time) when:
- You already know the exact file and roughly where in it. Just Read/Edit it.
- The whole job is 1–2 tool calls (one grep, one file read, one small edit).
- The task needs the conversation's accumulated context to do well — do not
  delegate work that would force you to paste half the conversation into the
  prompt.

Subagents start cold: every spawn re-pays for context. One well-briefed agent
beats three vague ones. Never spawn an agent to do what one Grep call does.

## 2. Delegation trio — every dispatch prompt contains all three

1. **Goal + motivation** — what to produce AND why it's needed, so the agent
   can make sensible micro-decisions ("finding where uploads are validated,
   because we need to add a size limit" — not just "find upload code").
2. **Acceptance criteria** — objectively checkable, listed. If you cannot
   write a checkable criterion, the task is not ready to delegate; sharpen it
   first.
3. **Report format** — what comes back and how long it may be (see §4).

Fill-in templates for the five common task shapes are in
`~/.claude/rules/delegation-templates.md` — use them instead of improvising.

## 3. Explicit model choice — never spawn without deciding

Cloud models available on this machine (Agent tool `model` parameter):

| Alias    | Model            | Use for |
|----------|------------------|---------|
| `haiku`  | Haiku 4.5        | Mechanical work with a proven recipe: batch apply-a-known-pattern edits, format conversions, simple lookups in a named location. |
| `sonnet` | Sonnet 5         | Default worker: exploration, implementation, research, standard review. |
| `opus`   | Opus 4.8         | Arbiter and hard cases: second opinions, architecture calls, tasks Sonnet failed twice (§5), subtle debugging. Costs ~5× Sonnet — always state to yourself why Opus is needed before using it. |
| `fable`  | Fable 5          | Do not plan around it: only available on special plans, likely absent from this environment after 2026-07-05. If a spawn with `model: fable` errors, fall back to `opus`. |

**Level 0 — local models (free):** the `lmh` CLI (documented by the `lmh`
user skill; run it in a shell, don't invoke it via the Skill tool if the
skill isn't listed) routes to local Ollama
models (4B–8B). Use for zero-stakes drafting: first-pass translation,
summarizing a document you will re-check, boilerplate text. Everything it
produces must be verified by a cloud model before reaching the user or a file
(see the lmh skill for rules). Never use lmh for judgment calls or facts you
won't check.

**Effort:** the Agent tool call itself has no effort parameter. Effort is
pinned in an agent definition file's frontmatter (`~/.claude/agents/*.md`),
key `effort: low|medium|high|xhigh|max` alongside `model:` (verified by live
docs fetch 2026-07-05: code.claude.com/docs/en/sub-agents; if a future
Claude Code version rejects or ignores `effort`, just delete the key —
`model:` pinning still works). One custom
agent is provided: `verifier` (see §6), pinned to `model: sonnet`,
`effort: high`. For ad-hoc spawns of built-in agents you can only choose the
model; if a specific effort matters, create a small agent file. ARS slash
commands already pin their own models — do not override them.

## 4. Report contract — what subagents are allowed to send back

Include this block (adapted) in every dispatch prompt:

> Report back ONLY: (a) your conclusion in ≤10 lines, (b) exact locations as
> `path:line`, (c) anything you could NOT verify, flagged as such. Do NOT
> paste file contents, diffs, or transcripts into your report. If you produced
> something long (a document, a big diff, research notes), write it to a file
> under the scratchpad directory and report the path.

If a subagent's reply violates the contract (returns a wall of text), extract
the conclusion, ignore the rest, and tighten the format instruction next time.
Relay to the user what matters from the report — they never see the raw
subagent output.

## 5. Escalation and downgrade ladder

**Up:**
- `haiku` worker fails its acceptance criteria **once** → resend the same
  task (same trio) to `sonnet`. Do not debug Haiku's attempt.
- `sonnet` (worker or commander) fails the **same subtask twice** → escalate
  to `opus`, and the dispatch MUST carry the full failure trail: what was
  tried, exact error output, files touched, current hypothesis. Escalating
  without the trail wastes the expensive model on rediscovery.
- Hard cap (canonical definition in CLAUDE.md Hard rule 2): identical
  command gets at most 1 unchanged retry (2 attempts total); the same
  *approach* with variations gets **max 2 rounds** at any level. After that,
  either change the approach, escalate, or stop and tell the user what's
  blocking (see `~/.claude/rules/judgment.md` §4 for wrong-direction signals).

**Down:**
- Once an expensive model has solved ONE instance and the pattern is explicit
  (e.g. "in each file, replace X-shaped call with Y; here is a completed
  example"), batch-apply the remaining instances via `haiku` — include the
  worked example in the prompt, and verify per §6.
- Text drafts whose quality floor is "user will rewrite anyway" → `lmh`.

## 6. Verification — never self-verify

The model (or agent) that produced a change does not get to declare it done.

- **Files written/edited:** read the final file back (Read tool) and check it
  against the acceptance criteria — do this for every deliverable file.
- **Code changed:** run the tests, or actually run the affected flow. "It
  should work" is not a verification; command output is.
- **Acceptance of delegated work:** dispatch the custom `verifier` agent
  (fresh context). Give it ONLY the acceptance criteria and the artifact
  paths — never your implementation narrative, never "I think it's done,
  please confirm". A verifier that knows the intended answer rubber-stamps.
  (Agent definition files load at session start — tested 2026-07-05: an
  agent file created mid-session is NOT dispatchable until the next session.)
  **Fallback:** if `verifier` is not in this session's available agent list,
  dispatch `general-purpose` (model: sonnet) instead and paste the whole body
  of `~/.claude/agents/verifier.md` (below its frontmatter) as the prompt
  preamble, followed by the criteria and paths. The fresh-context property is
  what matters, not the agent name.
- **High-stakes judgment calls** (irreversible action, architecture choice,
  anything the user will rely on unchecked): get a second opinion from
  `opus` with the question restated neutrally — or generate 2–3 independent
  candidate answers and have `opus` pick with reasons. If the two opinions
  disagree, that disagreement itself goes to the user; do not silently pick.

**Honest limit:** this ladder repairs *execution* quality. It cannot repair
taste or genuinely ambiguous requirements — no amount of Haiku retries or
multi-sample voting tells you what the user actually wanted. For those, the
options are: escalate the model, ask the user, or say plainly that the
judgment exceeds what this setup can verify. Guessing confidently is the only
forbidden move.

## Lessons
<!-- Append per maintenance.md §4: - YYYY-MM-DD | trigger | rule -->
