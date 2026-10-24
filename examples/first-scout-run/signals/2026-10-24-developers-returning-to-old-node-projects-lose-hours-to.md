---
id: sig-0020
type: signal
title: Developers returning to old Node projects lose hours to dependency drift
source: hn
ref: https://news.ycombinator.com/item?id=42175316
captured: 2026-10-24
segment: developers and small teams maintaining older Node, Vue or Express apps
pain: Old projects fail on native addons, removed packages and unrecorded Node versions, and the upgrade path can take days.
frequency: event-driven
workaround: Install the old Node version, pin it with .nvmrc or Docker, commit lockfiles, or rewrite into a simpler stack
pays_today: Hours to days of developer time; the poster gave up after about 2 hours
trigger: Node 16 and Node 18 are past end of life (Node 18 since 2025-04-30)
evidence: 2
status: new
---

## Context

A Hacker News thread from 2024-11-18, opened by the forums scout. Many independent commenters confirm the
problem, with times from minutes to days; one Svelte 3 to 5 upgrade took about 90 minutes with an AI
assistant. Older than 12 months and mostly general developer venting; no budget is shown.

## Why it matters

Runtime end of life keeps creating this pain for every app nobody touched in a while.

## Open questions

- Who pays to fix it: the developer's own time, or a client who owns an abandoned app?
