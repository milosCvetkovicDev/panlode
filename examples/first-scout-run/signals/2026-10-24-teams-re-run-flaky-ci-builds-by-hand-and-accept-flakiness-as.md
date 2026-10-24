---
id: sig-0019
type: signal
title: Teams re-run flaky CI builds by hand and accept flakiness as a cost of merging
source: hn
ref: https://news.ycombinator.com/item?id=20028057
captured: 2026-10-24
segment: software teams of any size with browser or end-to-end heavy CI
pain: Intermittent test failures mean re-running builds; hours go to retries instead of fixes, and trust in the CI signal erodes.
frequency: daily
workaround: Retry up to three times, quarantine flaky tests, or run them in a separate suite before release
pays_today: Developer time; a 2024 industrial case study measured at least 2.5% of productive developer time
evidence: 2
status: new
---

## Context

A Hacker News thread from 2019, seen by the forums scout in search results only, so it shows a
long-standing pain rather than a fresh one. The scout also saw the same pain in a 2024 ICST industrial
case study on the cost of flaky tests and in a newer HN thread (around 2026-02) saying retries and
quarantine hide the problem. Vendor cost figures were modelled, so they are not used here.

## Why it matters

A measured, recurring cost in developer time, but the market for flaky-test tools is crowded.

## Open questions

- Find a fresh (last 12 months) small-team complaint with hours or money attached.
