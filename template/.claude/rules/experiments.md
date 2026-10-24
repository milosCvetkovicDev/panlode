---
paths:
  - "experiments/**"
---

# Experiments

An experiment tests one idea's riskiest assumption, cheaply and fast. Write
`experiments/exp-NNNN-<slug>.md` from `templates/experiment.md`; log progress with `/log-experiment`.

- **IDs and names.** `python3 scripts/engine.py next-id exp` and
  `python3 scripts/engine.py slug '<title>'` (single quotes, as in `rules/signals.md`). The file name
  starts with the id.
- **Limits.** `budget_eur` at most 100; `deadline` at most 14 days after `created`. Both are warnings,
  so a breach is a conscious choice written in the body.
- **Metric.** `success_metric` is numeric where possible ("3 of 10 confirm a paid workaround").
- **Log.** The body ends with `## Log`; one line per entry, `- YYYY-MM-DD <note>`, newest last. Log at
  least two prospect contacts a week per running experiment.
- **Closing.** `status: done` needs `result` (what happened, with numbers) and `decision`
  (`continue`, `pivot` or `kill`). Then update the idea: a new experiment in `next`, or a new status.

## Write order (keeps every reference resolvable)

1. Idea with `status: shaped` (no `next` yet).
2. Experiment with `idea: idea-NNNN`.
3. Idea set to `validating`, with `next: exp-NNNN` and dated `kill_criteria`.

Writing them in another order makes the post-write check reject the file that points at a record that
does not exist yet.
