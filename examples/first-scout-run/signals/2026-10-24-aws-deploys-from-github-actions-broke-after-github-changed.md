---
id: sig-0016
type: signal
title: AWS deploys from GitHub Actions broke after GitHub changed the OIDC subject claim
source: forum
ref: https://dev.to/aws-builders/github-changed-its-oidc-subject-claims-and-broke-my-aws-deploys-for-new-repos-2cfp
captured: 2026-10-24
segment: small to mid dev teams deploying to AWS (CDK) from GitHub Actions with OIDC federation
pain: New repos get an ID-based subject claim, so slug-based IAM trust policies stop matching and deploys fail with AssumeRoleWithWebIdentity errors.
frequency: event-driven
workaround: Edit every trust policy to accept both claim formats; find the rejected identity in CloudTrail
pays_today: Engineer time, about an afternoon per incident
trigger: GitHub issued the new claim format for new and renamed repos from 2026-07-15
evidence: 2
status: new
---

## Context

A DEV Community post dated 2026-07-20, opened by the forums scout and again in the 2026-10-24 spot
check, which confirmed the July 15th change, the AssumeRoleWithWebIdentity error and the lost afternoon.
Two readers commented that they hit it or that the fix worked. Search results also showed a GitHub
changelog entry, a Japanese blog post and a PyPI checker tool on the same break. The post says GCP, Azure
and Vault federation face the same change.

## Quote

"Hopefully this saves you the afternoon it cost me." ([DEV](https://dev.to/aws-builders/github-changed-its-oidc-subject-claims-and-broke-my-aws-deploys-for-new-repos-2cfp))

## Why it matters

A fresh, dated trigger: existing repos may move to the new format later, so more teams will hit it.

## Open questions

- How many teams find out only when a deploy fails, and would they pay for a pre-flight check?
