---
id: <idea-NNNN from scripts/engine.py next-id idea>
type: idea
title: <short name of the offer>
status: <shaped | validating | go | parked | killed | building-elsewhere>
shape: <service | product | hybrid>
signals:
  - <sig-NNNN; at least one, each must exist>
segment: <who pays>
offer: <the first sellable thing, one sentence with a price shape>
product_path: <what the software version becomes; required for service and hybrid>
price_hypothesis: <e.g. 49 EUR per month per firm>
first_customer_days: <integer estimate of days to the first paying customer>
score_pain: <1-5>
score_reach: <1-5>
score_willingness: <1-5>
score_speed: <1-5>
score_fit: <1-5>
score_total: <sum of the five scores>
kill_criteria:
  - <YYYY-MM-DD condition that kills the idea; required when validating>
next: <exp-NNNN; required when validating>
archive_ref: <archive/ path for legacy ideas; optional>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---

## Problem

<The pain in one paragraph, citing the signals.>

## Who

<Segment, size, where they gather.>

## Why now

<Regulation, deadline, market shift.>

## Service version

<What can be sold by hand this month.>

## Product version

<What the software becomes once the service repeats.>

## Reaching twenty prospects

<Concrete places, lists and queries.>

## Competitors

- <name, URL, price, gap>

## Risks

- <the assumption most likely to be wrong>

## Founder fit

<Filter only: constraints from founder/ that this passes or breaks.>
