---
paths:
  - "ideas/**"
---

# Ideas

An idea is a sellable offer built on observed signals. Write `ideas/<slug>/idea.md` from
`templates/idea.md`; other files in the folder (research, plans) are free-form notes.

- **IDs and names.** `python3 scripts/engine.py next-id idea` and
  `python3 scripts/engine.py slug '<title>'` (single quotes, as in `rules/signals.md`). Never invent an
  id.
- **Signals first.** `signals` lists at least one existing `sig-NNNN`. No signal, no idea: capture the
  signal first. When an idea is written, set each of its signals to `promoted` with `cluster` and `ideas`.
- **Founder fit is a filter, never a generator.** `founder/` says which ideas you can sell and
  deliver; it is never a source of ideas. Ideas come from signals.
- **Two versions.** Every idea names the service that can be sold by hand this month and the product it
  becomes. `shape: service` or `hybrid` needs `product_path`.
- **Scores.** `score_pain`, `score_reach`, `score_willingness`, `score_speed`, `score_fit` are 1–5 and
  `score_total` is their sum; the check rejects a mismatch. Rank by speed to the first paying customer.
- **Validating.** At most three ideas are `validating` at once. A validating idea needs dated
  `kill_criteria` (each item starts with `YYYY-MM-DD`) and `next` pointing at an existing experiment.
  Follow the write order in `.claude/rules/experiments.md`.
- **Closed ideas.** `killed` and `parked` keep their file and say why in the body. `building-elsewhere`
  means it left this workspace to be built elsewhere; never re-propose it.
