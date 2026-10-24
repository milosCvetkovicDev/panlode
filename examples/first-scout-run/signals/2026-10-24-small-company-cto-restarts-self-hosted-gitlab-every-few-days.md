---
id: sig-0014
type: signal
title: Small-company CTO restarts self-hosted GitLab every few days as CI runners stall
source: other
ref: https://www.peerspot.com/products/gitlab-pros-and-cons
captured: 2026-10-24
segment: CTO at a small company; engineers at 201-500 employee software vendors
pain: Self-hosted GitLab slows under load and needs restarts every few days, and runners start slowly or stall when several merges run.
frequency: weekly
workaround: Restart the self-hosted instance by hand; keep it on a single VM to avoid deployment complexity
pays_today: Self-hosted infrastructure and admin time
trigger: Concurrent merges and load growth
evidence: 2
status: new
---

## Context

PeerSpot pros-and-cons page for GitLab, opened by the review-sites scout. Independent reviews dated
2025-05-06, 2025-11-25 and 2026-03-27 report the same stalled-CI and load problems; only 5 of about 95
cons were visible.

## Why it matters

Self-hosting saves licence money but moves the cost into recurring admin time for a small team.

## Open questions

- Would these teams pay for managed upkeep of their self-hosted GitLab, or would they rather move to SaaS?
