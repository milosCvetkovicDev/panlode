---
title: Home
layout: home
nav_order: 1
description: "Panlode is an open-source Claude Code workspace for validating startup ideas before you build: scout real customer pain, score the evidence, run cheap experiments, kill weak ideas early."
permalink: /
---

# Evidence before code
{: .fs-9 }

Panlode is an open-source Claude Code workspace that finds real customer pain, turns it into startup
ideas and kills the weak ones with cheap experiments, before you build anything.
{: .fs-6 .fw-300 }

[Get started](getting-started.md){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View on GitHub](https://github.com/milosCvetkovicDev/panlode){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## The idea in one minute

Building got cheap; knowing what to build did not. Panlode points Claude Code at the step most
builders skip:

1. **Scout.** `/scout-online` sends three read-only `signal-scout` subagents to public forums, review
   sites and freelance or job boards. They bring back **signals**: someone describing a recurring
   problem, ideally one they already pay to work around, each with its source link.
2. **Score.** Every signal gets an evidence score from 1 (one anonymous complaint) to 5 (proof they
   already pay for a worse alternative).
3. **Shape.** Signals that cluster around one sellable offer become an **idea**: a service you can sell
   by hand this month, the product it can become, five scores and dated kill criteria.
4. **Test.** Each idea runs **one experiment at a time**, at most 100 € and 14 days: outreach,
   interviews, a landing page, a pre-sale or a concierge test. It ends in `continue`, `pivot` or `kill`.
5. **Hand off.** An idea that reaches `go` is built in a separate repository. This workspace refuses
   product code.

Ideas are ranked by **speed to the first paying customer**, not by the size of the market.

## Why it holds up

The rules are not just in the prompt. A dependency-free Python engine runs from four Claude Code hooks
and checks every record as it is written: ids resolve, scores add up, at most three ideas are in
validation, every experiment has a deadline and every finished one a decision. The session brief at
start tells you how many days have passed since the last signal and the last contact.

## Where to next

| If you want to | Read |
|---|---|
| install it and run the first scouting pass | [Getting started](getting-started.md) |
| understand signals, evidence, ideas and kill criteria | [Concepts](concepts.md) |
| see how the engine, hooks, rules, agents and skills fit | [Architecture](architecture.md) |
| keep it going with a small weekly floor | [The weekly loop](weekly-loop.md) |
| know what it cannot do | [Limits](limits.md) |
| see how it compares with idea generators, canvases and listening tools | [Compared with other approaches](comparison.md) |
| find a quick answer | [FAQ](faq.md) |
