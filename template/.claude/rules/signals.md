---
paths:
  - "signals/**"
  - "interviews/**"
---

# Signals and interviews

A signal is one observed pain, with its source. Write it from `templates/signal.md`; an interview note from
`templates/interview.md`.

- **IDs and names.** `python3 scripts/engine.py next-id sig` gives the id;
  `python3 scripts/engine.py slug '<title>'` gives the ASCII slug (single quotes; first delete every
  `'`, `"`, `$`, backtick and backslash from the title, which the slug drops anyway). File:
  `signals/<captured>-<slug>.md`. Never invent an id or type one with non-ASCII letters.
- **Real sources only.** `ref` is a URL you or a scout opened or saw in a search result (say which in
  Context), an `interviews/` path, or an `archive/` path for a legacy idea. Never construct, guess or
  shorten a URL.
- **Paraphrase.** `pain` is one sentence in the customer's words, paraphrased, at most 200 characters.
  The body holds at most one verbatim quote of 15 words or fewer, with its link. Everything else is in
  your own words.
- **Businesses and public roles only.** No names, emails or profiles of private individuals. Interview
  notes keep a first name and role at most, and `consent` records whether notes were agreed to.
  `interviews/targets-<segment>.md` lists business names, public websites and public contact channels only.
- **Status.** `new` → `clustered` (set `cluster`) → `promoted` (set `cluster` and `ideas`) or `dismissed`.

## Evidence rubric

| Score | Meaning |
|---|---|
| 1 | One anonymous complaint, or a legacy idea with no observed demand |
| 2 | Several independent complaints from the same kind of source |
| 3 | Complaints plus a paid workaround: a job post, a freelancer gig, a badly reviewed tool people still pay for |
| 4 | A direct conversation confirming the pain and its cost in hours or money |
| 5 | A stated price they would pay, or proof they already pay for a worse alternative |

Score what you saw, not what you expect. When unsure between two scores, take the lower one.
