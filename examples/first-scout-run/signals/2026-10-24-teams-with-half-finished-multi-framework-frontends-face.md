---
id: sig-0021
type: signal
title: Teams with half-finished multi-framework frontends face patch deadlines
source: hn
ref: https://news.ycombinator.com/item?id=43422368
captured: 2026-10-24
segment: teams with large legacy frontends (jQuery, Backbone, Angular, React), including enterprise ones
pain: Started migrations never finish, leaving stacked frameworks and deprecated tooling that must still meet security patch deadlines.
frequency: monthly
workaround: Pin dependencies with TODO comments, keep deprecated CLIs, or leave the apps alone
pays_today: unknown
trigger: Security patch deadlines; one team must patch critical vulnerabilities within 48 hours or shut the app down
evidence: 1
status: new
---

## Context

A Hacker News thread from 2025-03-20, opened by the forums scout (first 100,000 of about 182,000
characters read). No hours or money are given; the thread is mostly opinion and not specific to small
teams.

## Why it matters

Patch deadlines turn a slow migration into an urgent one.

## Open questions

- Are there small companies (not enterprises) in this position, and what would they pay to finish?
