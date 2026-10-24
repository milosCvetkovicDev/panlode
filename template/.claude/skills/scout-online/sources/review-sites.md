# Recipe: review sites

Low-star reviews of tools people keep paying for show a paid workaround with a gap. The complaint names
the gap; the subscription proves the willingness to pay.

## Where

- G2 (`g2.com/products/<tool>/reviews`), Capterra (`capterra.com`), Trustpilot (`trustpilot.com/review/<domain>`)
- Filter for 1–3 star reviews and the "cons" or "what do you dislike" sections.

## Search patterns

- `site:g2.com "<category>" reviews "what do you dislike"`
- `site:capterra.com "<category>" reviews cons "manual"`
- `site:trustpilot.com "<tool>" "still have to"`
- Find the category leaders first (`"best <category> software" <year>`), then read their worst reviews.
- Phrases that mark a gap: "still have to", "manually", "export to Excel", "workaround", "no way to",
  "support said".

## What counts as a signal

- A reviewer who still uses and pays for the tool but does part of the job by hand.
- The same missing capability across several reviews or several tools in one category.
- The reviewer's company size and role, when shown (record in `segment`).

## Evidence hints

- 3: a paying user describes a manual workaround for the gap (a paid tool plus hours).
- 2: several independent reviews name the same gap.
- 1: a single complaint without a workaround.

## Known noise

- Complaints about price, support tone or onboarding only: not a product gap.
- Incentivised or vendor-replied reviews that read like marketing.
- Reviews older than two years unless the gap is still listed in recent ones.

## Caps

At most 15 searches and 8 candidates.
