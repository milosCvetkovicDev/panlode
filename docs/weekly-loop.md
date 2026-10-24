---
title: The weekly loop
nav_order: 5
description: "The minimum weekly routine for validating startup ideas with Panlode when client work or a day job comes first: one scouting run and two prospect contacts per experiment."
---

# The weekly loop
{: .no_toc }

No hour budget, only a floor that keeps the pipeline alive when other work comes first.
{: .fs-6 .fw-300 }

1. TOC
{:toc}

---

## The floor

- **One `/scout-online` run a week.**
- **At least two prospect contacts logged per running experiment**, with `/log-experiment`.

That is all. Everything else (shaping ideas, interviews, writing a landing page) happens when it can.
The floor exists because discovery dies quietly: nobody decides to stop, the next session just never
comes.

## How the workspace keeps you honest

The brief at every session start prints:

```text
Days since last signal: 9
Days since last log entry: 3
```

The workspace `CLAUDE.md` tells Claude to say so before anything else when either number passes 7.
Experiments past their deadline appear under `Overdue:` until they are closed.

## A 45-minute week

| When | What | Command |
|---|---|---|
| Monday, 20 min | Scout; keep the signals worth keeping | `/scout-online` (or with a focus) |
| Any day, 5 min each | Send or log two contacts per running experiment | `/log-experiment exp-NNNN <note>` |
| Friday, 15 min | Cluster new signals; close or extend experiments past their deadline; commit | `python3 scripts/engine.py check`, `git commit` |

## When to shape an idea

The `/scout-online` digest suggests it when a cluster holds three or more signals with evidence 3 or
more. Until then, a cluster of evidence-1 and evidence-2 signals is a lead for interviews, not an idea.
The fastest way to raise evidence is a conversation: one call that confirms the pain and its cost is
worth more than ten more forum threads.

## When to kill

When a dated kill criterion fires, or when an experiment ends below its metric and no pivot is more
promising than the next idea in line. Killing is the normal outcome; `git log` keeps the record, and a
killed idea's signals stay available for the next cluster.
