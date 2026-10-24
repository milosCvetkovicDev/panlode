---
id: sig-0017
type: signal
title: Azure admins lose SSO and integrations when an Entra secret or key expires unnoticed
source: forum
ref: https://learn.microsoft.com/en-us/answers/questions/2123648/problem-with-client-secrets-in-app-registrations
captured: 2026-10-24
segment: company IT admins on Entra ID or Azure AD B2C with Key Vault; SaaS vendors integrating with Entra
pain: A secret or policy key expires silently and SSO or an integration breaks, and nothing links the key to its Key Vault item or app.
frequency: event-driven
workaround: Rotate after the outage and add an expiry reminder; compare keys against Key Vault by hand
pays_today: Admin time, about a week in the Q&A case
trigger: Secrets have a maximum lifetime, so they expire on schedules nobody owns
evidence: 1
status: new
---

## Context

A Microsoft Q&A thread from 2024-11-27, opened by the forums scout and again in the 2026-10-24 spot check:
the error blamed an already-rotated client secret, while the cause was an expired B2C policy key with no
visible link to Key Vault or the app. One reporter only. The scout also saw, in search results only,
public status-page incidents with expired credentials as the cause: Xink (2026-04-03, about 7 hours, via
pingoru.io, whose page returned 403 to the spot check), Zendesk Sell (2025-02-14), Brevo (2026-07) and
Trengo (2026-01). Merged here because the pain and the segment are the same.

## Why it matters

Outages of hours from one forgotten date; each incident's follow-up was just an expiry alert.

## Open questions

- Open the status-page incidents directly; if they hold, the evidence rises to 2.
- Who owns credential expiry in a 5-50 person company?
