# Recipe: freelance job posts

Repeated paid tasks are the strongest online signal: someone already pays a person to do the work by
hand. Each post is demand proof and a price benchmark.

## Where

- Upwork job listings (`upwork.com/freelance-jobs/`, public job pages)
- Freelancer.com and PeoplePerHour project listings
- Job boards with contract roles that exist to do manual work (data entry, reconciliation, reporting)

## Search patterns

- `site:upwork.com/freelance-jobs "<focus>" (manual OR "every week" OR "every month" OR ongoing)`
- `site:upwork.com "<task> specialist" "long term"`
- `site:peopleperhour.com "<focus>"` and `site:freelancer.com/projects "<focus>"`
- `"looking for someone to" "<task>" "every week"` (any site)
- Without a focus, start from repetitive back-office tasks: invoice entry, bank reconciliation, report
  building, catalogue updates, CRM clean-up, CI or deployment fixes.

## What counts as a signal

- The same task posted repeatedly, or one post for ongoing or recurring work.
- A stated budget or hourly rate (record it in `pays_today`).
- The tool stack named in the post (tells you what the workaround sits on).

## Evidence hints

- 3: a paid recurring task (a budget or rate is visible), or the same task from several businesses.
- 2: one-off posts for the same task from different businesses, no rate visible.
- 1: a single one-off post.

## Known noise

- Agencies reposting the same job across boards; count it once.
- "Build me an app like X" posts: a product request, not a pain.
- Job pages behind a login: use the search result snippet and say so.

## Caps

At most 15 searches and 8 candidates.
