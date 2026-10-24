# Example: the first scouting run

This folder is a workspace after one `/scout-online` run on 2026-10-24: the signals as they were
written, plus the generated [`INDEX.md`](INDEX.md). It shows what a run produces when the evidence is
still thin. Every signal links to the public page it came from; follow any of them to check the
paraphrase.

```bash
python3 template/scripts/engine.py --root examples/first-scout-run check   # 0 error(s), 0 warning(s)
python3 template/scripts/engine.py --root examples/first-scout-run brief
```

## What the run found

The run focused on delivery pain in small software teams. Three scouts, one per recipe (forums,
review sites, freelance and job posts), brought back 19 candidates. Two were dropped in review (one
described an enterprise-sized buyer, one was a feature request rather than a pain) and two describing
the same expiry problem were merged, which left 16 signals:
10 with evidence 2 (several people describe the same problem) and 6 with evidence 1 (one post). None
reached 3, which takes complaints plus a paid workaround such as a job post or a freelance gig.
The ids start at `sig-0007` because the first six signals came from an earlier batch that is not
published here.

Read side by side, they fall into three clusters. The clusters are not recorded in the signals yet
(every `status` is still `new`), because clustering is the next step a person takes, not the scout.

| Cluster | Signals | The pain, in short |
|---|---|---|
| Debugging CI pipelines | [sig-0007](signals/2026-10-24-app-owner-pays-a-freelancer-to-fix-a-failing-github-actions.md), [sig-0012](signals/2026-10-24-circleci-users-struggle-to-debug-failed-pipelines-and-hand.md), [sig-0013](signals/2026-10-24-github-actions-teams-find-failing-workflows-and-token-setup.md), [sig-0014](signals/2026-10-24-small-company-cto-restarts-self-hosted-gitlab-every-few-days.md), [sig-0016](signals/2026-10-24-aws-deploys-from-github-actions-broke-after-github-changed.md), [sig-0018](signals/2026-10-24-developers-debug-ci-by-committing-again-and-again-because.md), [sig-0019](signals/2026-10-24-teams-re-run-flaky-ci-builds-by-hand-and-accept-flakiness-as.md) | Failing and flaky pipelines are debugged by pushing commits and re-running builds, because the pipeline cannot be run locally. |
| Secrets and credentials | [sig-0010](signals/2026-10-24-small-consultancy-pays-for-a-secrets-manager-but-still.md), [sig-0011](signals/2026-10-24-devops-teams-on-gitguardian-chase-leaked-secret-alerts-by.md), [sig-0015](signals/2026-10-24-small-startups-find-hashicorp-vault-too-complex-and-costly.md), [sig-0017](signals/2026-10-24-azure-admins-lose-sso-and-integrations-when-an-entra-secret.md) | Small teams rotate secrets and chase leak alerts by hand, and an expired key takes down sign-in. |
| Upgrading legacy JavaScript | [sig-0008](signals/2026-10-24-small-business-pays-a-freelancer-to-strip-deprecated.md), [sig-0009](signals/2026-10-24-product-team-hires-a-contractor-to-move-a-node-12-next-js.md), [sig-0020](signals/2026-10-24-developers-returning-to-old-node-projects-lose-hours-to.md), [sig-0021](signals/2026-10-24-teams-with-half-finished-multi-framework-frontends-face.md), [sig-0022](signals/2026-10-24-companies-hire-contractors-for-year-long-angularjs-to.md) | Old Node and AngularJS code drifts until someone is hired to move it to current versions. |

## Why no idea yet

An idea needs a sellable offer and a reason to believe someone will pay this month. Evidence 1-2 says
the pain exists, not that anyone pays to remove it. The freelance and job posts (sig-0007, sig-0008,
sig-0009, sig-0022) come closest, since someone hired help, but each is a single post. The next step
for any cluster is not code: it is a handful of conversations with the people who wrote posts like
these, or a small paid offer, recorded as an experiment.
