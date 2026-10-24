---
name: log-experiment
description: Append a dated entry to an experiment's log, update its result when the note carries counts, and force a continue, pivot or kill decision once its deadline has passed or its success metric is met.
disable-model-invocation: true
argument-hint: "<exp-id> <note>"
allowed-tools: Read, Edit, Glob, AskUserQuestion, Bash(python3 scripts/engine.py *)
---

# /log-experiment

Arguments: `$ARGUMENTS` — the first word is the experiment id (`exp-NNNN`), the rest is the note.

## 1. Find the experiment

Glob `experiments/<exp-id>-*.md`. If there is no match, or the arguments have no note, say so and stop.
Read the file and its idea (`ideas/*/idea.md` whose `id` equals the experiment's `idea`).

## 2. Append the entry

- Add `- <today YYYY-MM-DD> <note>` as the last line under `## Log` (newest last). Keep the note's
  wording; translate nothing.
- If the note carries counts (messages sent, replies, calls, pre-sales, euros), update `result` in the
  frontmatter to the running totals, e.g. `result: 8 contacted, 2 replies, 0 calls`.
- If `status` is `planned`, set it to `running`.
- Set `updated` to today.

## 3. Decide when it is time

It is time when the `deadline` is before or equal to today, or the `result` meets `success_metric`.
Then ask with AskUserQuestion: "exp-NNNN: continue, pivot or kill?", one option each, with a one-line
summary of the result against the metric. Apply the answer:

| Answer | Experiment | Idea |
|---|---|---|
| kill | `status: done`, `decision: kill`, `result` filled | `status: killed`; add the reason to its body |
| pivot | `status: done`, `decision: pivot`, `result` filled | `status: shaped`; remove `next`; add the reason and the new angle to its body |
| continue | `status: done`, `decision: continue`, `result` filled | stays `validating`; propose the next experiment |

For `continue`, draft the next experiment from `templates/experiment.md` for the riskiest open
assumption and show it; write it only after the user agrees, then point the idea's `next` at it (write
order in `.claude/rules/experiments.md`). If the user declines it, set the idea to `shaped` and remove
`next`, so no `validating` idea points at a finished experiment.

Set `updated` to today on every record you change.

## 4. Check

Run `python3 scripts/engine.py check`; it must exit 0. Report in the conversation language set in
`CLAUDE.md`, in at most five lines: the entry added, the result, and the decision if one was made.
