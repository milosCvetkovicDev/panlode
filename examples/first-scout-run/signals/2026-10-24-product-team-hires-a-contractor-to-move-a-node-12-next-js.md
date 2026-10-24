---
id: sig-0009
type: signal
title: Product team hires a contractor to move a Node 12 Next.js app to current versions
source: upwork
ref: https://www.upwork.com/jobs/~022061317433783949984
captured: 2026-10-24
segment: small product team or agency running Node and Next.js on AWS EC2 with MongoDB
pain: A Node 12 app on deprecated node-sass needs Node 18+, current Next.js and Keystone 6, and a move off self-managed EC2 hosting.
frequency: event-driven
workaround: Hire an outside contractor for the upgrade
pays_today: unknown
trigger: Node 12 is end of life and node-sass is deprecated
evidence: 1
status: new
---

## Context

An Upwork job post seen only in a search-result snippet; the page returned 403 to the scout, so the
budget, the posting date and the client's history are not verified. The client also wants the frontend
moved to Vercel and MongoDB to a managed service.

## Why it matters

A concrete upgrade forced by runtime end of life, the kind of trigger a fixed-scope service can sell to.

## Open questions

- What budget do such Node end-of-life upgrades carry on Upwork when the page can be read?
