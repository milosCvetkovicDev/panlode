---
title: Concepts
nav_order: 3
description: "Signals, the 1-5 evidence rubric, clusters, idea shapes, the five scores, dated kill criteria and cheap experiments: the vocabulary of Panlode."
---

# Concepts
{: .no_toc }

Five record types and one rule of thumb: score what you saw, not what you hope.
{: .fs-6 .fw-300 }

1. TOC
{:toc}

---

## Signal

One observed pain, with its source: who does what painful thing, how often, what they do about it today
and whether they already pay for it. A signal lives in `signals/YYYY-MM-DD-<slug>.md`.

- `ref` is a URL that was opened or seen in a search result, an `interviews/` path, or an `archive/` path
  for an older idea list. Never a constructed or guessed URL.
- `pain` is one paraphrased sentence of at most 200 characters. The body holds at most one verbatim quote
  of 15 words or fewer, with its link.
- Businesses and public roles only: no names, emails or profiles of private individuals.
- Status: `new` → `clustered` → `promoted` (it fed an idea) or `dismissed`.

### Evidence rubric

| Score | Meaning |
|---|---|
| 1 | One anonymous complaint, or a legacy idea with no observed demand |
| 2 | Several independent complaints from the same kind of source |
| 3 | Complaints plus a paid workaround: a job post, a freelancer gig, a badly reviewed tool people still pay for |
| 4 | A direct conversation confirming the pain and its cost in hours or money |
| 5 | A stated price they would pay, or proof they already pay for a worse alternative |

When unsure between two scores, take the lower one. Online scouting alone rarely gets past 3; scores 4
and 5 come from conversations and pre-sales.

## Cluster

A short slug shared by signals that describe the same pain in the same kind of segment. Clustering is a
judgment, written into each signal's `cluster` field; the `/scout-online` digest suggests clusters, and
proposes shaping one into an idea once it holds three or more signals with evidence 3 or more.

## Idea

A sellable offer built on observed signals, in `ideas/<slug>/idea.md`. Other files in the folder are
free-form research notes.

- **At least one signal.** No signal, no idea. When an idea is written, its signals become `promoted`.
- **Two versions.** `offer` is the service you can sell by hand this month; `product_path` is the
  software it becomes. `shape` is `service`, `product` or `hybrid`; `service` and `hybrid` need a
  `product_path`.
- **Five scores, 1 to 5:** `score_pain`, `score_reach` (judged against `founder/channels.md`),
  `score_willingness` to pay, `score_speed` to the first paying customer, `score_fit` (judged against
  `founder/profile.md`). `score_total` must equal their sum.
- **Status:** `shaped` → `validating` → `go`, or `parked`, `killed`, `building-elsewhere`. Closed ideas
  keep their file and say why.

### Kill criteria

An idea in `validating` needs `kill_criteria`: a list of conditions, each carrying a date (by
convention at the start), under which the idea dies. For example: `2026-11-07 fewer than 3 of 20 firms reply`. Writing them before the
experiment starts keeps the decision honest when the results come in.

### WIP limit

At most three ideas are `validating` at once. A fourth is an error, not a warning.

## Experiment

The cheapest test of an idea's riskiest assumption, in `experiments/exp-NNNN-<slug>.md`.

- `method`: `outreach`, `interviews`, `landing-page`, `pre-sale`, `concierge`, `fake-door` or `other`.
- `hypothesis` and a `success_metric` (numeric where possible: "3 of 10 confirm a paid workaround").
- `budget_eur` at most 100 and a `deadline` at most 14 days after `created`. Breaking either is a
  warning, so it is allowed as a conscious choice, written in the body.
- The body ends with `## Log`: one dated line per contact or result, newest last, written by
  `/log-experiment`.
- `done` requires `result` (with numbers) and `decision`: `continue`, `pivot` or `kill`.

## Interview

A [Mom Test](https://www.momtestbook.com/) note in `interviews/YYYY-MM-DD-<slug>.md`: past behaviour and
money spent, not opinions about a pitch. It records the channel (`in-person`, `call`, `chat`, `email`)
and whether the person agreed to notes being kept, holds a first name and role at most, and can promote
new signals. A direct conversation that confirms the pain and its cost is what earns evidence 4.

## Founder files

`founder/profile.md`, `constraints.md` and `channels.md` describe what you can build, what you will not
do (the vetoes) and where you can reach people. They **filter** ideas and inform three scores; they are
never a source of ideas. An idea that breaks a veto is killed with the veto named.

## Ranking

Ideas are compared by **speed to the first paying customer** (`score_speed`, `first_customer_days`),
then by total score. That comparison is yours to make; `INDEX.md` lists ideas by status, then by
`score_total`. A solo founder runs out of time before running out of market.
