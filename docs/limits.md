---
title: Limits
nav_order: 6
description: "What Panlode cannot do: the bias of public sources, non-reproducible web search, fixed limits, a minimal YAML subset and other known boundaries."
---

# Limits
{: .no_toc }

Knowing where a tool stops is part of using it well.
{: .fs-6 .fw-300 }

1. TOC
{:toc}

---

## Evidence

- **Public text is biased.** Forums and review sites over-represent developers, larger companies and
  loud complaints. Many paying customers never post anything.
- **Scores 1 and 2 are leads, not demand.** Online scouting rarely reaches evidence 3; 4 and 5 need
  conversations, pre-sales or proof of an existing spend.
- **Paraphrase loses nuance.** Signals store one paraphrased sentence and at most one short quote, by
  design. Open the `ref` before acting on a signal.

## Scouting

- **Not reproducible.** Web search and fetch results vary by region, day and the tools' own limits. Two
  runs with the same focus will differ.
- **A handful of pages per run.** Each scout reads a few pages and returns at most eight candidates.
  This is sampling, not market research at scale.
- **Some sites refuse automated fetches.** The scouts can still report a search result they saw, marked
  as such, but cannot read the page behind it.
- **No personal data.** Scouts record businesses and public roles only. Leads that only exist as private
  individuals are dropped.

## Engine

- **Fixed limits.** 100 € per experiment, 14 days per experiment and three validating ideas are
  constants (`MAX_BUDGET_EUR`, `MAX_EXPERIMENT_DAYS` in `scripts/ideaengine/schema.py`, `MAX_VALIDATING`
  in `workspace.py`), not settings. Budgets are in euros.
- **A small YAML subset.** Flat keys, inline lists and block lists. Nested maps and multi-line block
  values are rejected with an error that names the file, rather than half-parsed. Anchors, aliases and
  flow maps (`{k: v}`) are not interpreted: they are kept as plain text.
- **Shell writes skip the per-write check.** Records written through Bash are only checked by the
  `Stop` hook and by `engine.py check`.
- **One workspace, one person.** There is no locking or merge logic beyond git.

## Platform

- **Claude Code 2.1.295 or later** for scouting, skills and hooks (the hooks use its `onFailure`
  setting; this release was tested with 2.1.310). The engine and the records work without it.
- **Python 3.10 or newer as `python3`.** If `python3` is missing or older, the engine cannot start: the
  installer warns, the `PreToolUse` hook blocks every Write and Edit in the workspace, and the other hooks
  show a hook error notice.
- **macOS and Linux.** On Windows, use WSL.
