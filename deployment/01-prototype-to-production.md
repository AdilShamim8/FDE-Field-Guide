# Prototype to Production

For the FDE holding a working prototype that now has to survive contact with a real
business. This document covers the documented failure pattern of enterprise AI pilots,
the gap between what a prototype is and what production requires, and a plan for crossing
deliberately: sequencing prerequisites, hardening the system, designing the pilot, and
handing over.

## The documented cliff

The pilot-to-production cliff is the best-documented failure pattern in enterprise AI.
Roughly 95% of enterprise GenAI pilots deliver no measurable P&L impact, according to the
MIT NANDA report "The GenAI Divide: State of AI in Business 2025" (Fortune coverage,
August 2025), based on 150 leadership interviews, a 350-employee survey, and analysis of
300 public AI deployments. The same coverage found the ~5% that succeed share three
traits: the system is integrated into real workflows, it is domain-specific, and it is
commonly bought and adapted rather than built internally. None of the three is about
model quality.

The FDE role exists largely to walk systems across this cliff. In an
[independent job-scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)
of 146 FDE postings (February-July 2026), 90.0% mention building or
deploying production systems. Anthropic's FDE job description centers on production
applications inside customer systems with white-glove deployment support. On the demand
side, Paul Farnsworth, president of Dice, described the roadblock: companies struggle to
turn models into "something that actually works inside of their business", because
connecting them to proprietary data, existing systems, and specific workflows "can be a
big roadblock to overcome", and forward-deployed engineers "can help fill that gap"
(Fortune, September 2026).

This suggests the cliff is not an engineering inconvenience at the end of a project; it
is the project. The rest of this document treats it that way.

## Why pilots die

Seven failure modes account for most pilot deaths. None of them is the model.

- Toy data - the pilot ran on a curated extract: clean rows, a fixed snapshot, one
  region. Production arrives with dirty, refreshed, growing data, and the query that
  produced the extract was never designed to run on a schedule.
- Shadow workflow - the system ran beside the real process and nobody changed how they
  work. Adoption was never part of the pilot, so the P&L never moved. Since the MIT
  NANDA findings tie success to workflow integration, this suggests it is the single
  most common cause.
- Missing owner - nobody was assigned to operate the system after the demo. The first
  production failure lands on a person who does not exist yet, and an unrepaired failure
  teaches users to route around the system permanently.
- Undefined quality bar - "works" was never measured against a threshold. The pilot ends
  when patience or funding runs out rather than when evidence arrives, and every later
  disagreement is judged from memory.
- Integration debt - SSO, permissions, data refresh, and handoffs to neighboring systems
  were never built. The prototype hardcoded what production has to negotiate: identity,
  access, and both sides of the boundary.
- Change-management void - users were never trained or consulted, so production week one
  is resistance. Operators who discover a system after it ships treat it as something
  done to them.
- Cost surprise - finance sees the bill at scale. Unit costs that look trivial at 100
  queries a day are a budget line at 100,000, and an unapproved budget line gets cut
  along with the system attached to it.

## The production gap checklist

Use this table in the architecture phase, with the customer in the room. Each production
requirement becomes a work item with an owner; rows left undiscovered become the failure
modes above.

| Concern | Prototype state | Production requirement |
| --- | --- | --- |
| Data | Curated extract, loaded by hand | Scheduled refresh, backfills, schema drift alarms |
| Auth | Hardcoded keys, one test user | SSO, service identities, least-privilege roles |
| Quality bar | "Looks good" in demos | Thresholds on a golden set, measured on a schedule |
| Monitoring | Eyeballed in a terminal | Dashboards, alerts, a named on-call |
| Deployment | Runs from a laptop | Packaged service, CI/CD, tested rollback |
| Ownership | The builder is the operator | Named owners on the customer side, runbooks |
| Docs | In the builder's head | Runbook, training, support boundaries |
| Cost | Invisible | Approved budget, spend alerts, unit cost per workload |

## Planning the crossing

Plan backwards from the launch date, not forwards from the prototype. Pick the date,
then schedule the boring prerequisites first: access, SSO, data refresh, security
review. They have the longest lead times and the least schedule flexibility - code
compresses, approval queues do not. The infrastructure realities live in
[cloud and infrastructure](../engineering/04-cloud-and-infrastructure.md), and the
security review that gates production is in
[security and compliance](../engineering/05-security-and-compliance.md).

Build the milestone plan with customer-side names on every external dependency: who
provisions the service account, who approves the data feed, who signs the security
review. A milestone without a customer-side owner is a wish. The phase model in the
[engagement lifecycle](../customer/01-engagement-lifecycle.md) attaches exit criteria to
each phase; use those rather than inventing your own.

Pin the definition of done to the spec, not to anyone's current enthusiasm: the
acceptance criteria and non-functional requirements signed in
[from requirements to spec](../customer/02-requirements-to-spec.md). If the launch date
and the definition of done disagree, change one of them explicitly, in writing. Never
let one quietly redefine the other - that trade, made silently, is where quality dies.

## Hardening the system

The distance from notebook to service is unglamorous and non-negotiable:

- Packaging - the system builds and starts from a clean checkout with one command; if
  setup lives in your head, it is not deployable
- Configuration - environments differ by configuration, not by code branches; keep
  config out of the image and out of the repo
- Secrets - injected at runtime from the customer's secrets manager, with rotation
  designed to be a non-event
- Migrations - schema changes are scripted, versioned, and reversible; "I ran it in the
  console" is not a migration, it is a future incident
- CI/CD - tests run on every change and deploys are repeatable by someone other than
  you; in many customer estates you propose the change and a customer engineer applies
  it, so keep changes small and reviewable

Then close the two gaps the prototype always hides:

- Load - the pilot's 10 friendly users say nothing about launch week. Write down the
  expected peak and test at it, or at a defensible fraction of it, before launch day.
  The first real load test should not be production.
- Failure behavior - decide what happens when the model times out, the queue backs up,
  or the data goes stale: degrade to the human process, retry with backoff, or fail
  loudly. Silence is the one wrong answer. Making these failures visible is the job of
  [monitoring and reliability](../ai/04-monitoring-and-reliability.md).

## The pilot design

A pilot is a production rehearsal, not a longer demo. The differences are structural:
real users doing real work, real data at production volumes, a real support path with a
number to call, and thresholds agreed before the pilot started.

We recommend pre-agreeing the exit decision with the sponsor before the pilot begins: it
ends in scale, fix, or kill, and the criteria for each branch are written in the spec. A
pilot without a pre-agreed exit drifts into a permanent shadow system that nobody funds
and nobody is brave enough to turn off.

The rehearsal checklist:

- Real users - the people whose workflow will change, not volunteers who owe you a favor
- Real data - the scheduled refresh, the real volumes, the dirty edges
- Real support path - who gets called, with what response expectation
- Pre-agreed thresholds - measured on an agreed schedule against the golden set; the
  methodology is in [evaluation and testing](../ai/03-evaluation-and-testing.md)
- An explicit exit decision - scale, fix, or kill, made jointly against the numbers

On length: most teams run pilots in weeks, not months - commonly 4 to 8 weeks (industry
pattern). Length does not buy signal; traffic and thresholds do.

Killing a pilot well is a core FDE skill, not an admission of failure. Document the
reasons against the original thresholds, preserve the learnings - what the data taught
you, which integrations blocked progress, what a fixed attempt needs - and run no blame
ritual. At a ~95% base rate, a cleanly killed pilot keeps the customer relationship and
the budget line intact for the next attempt; a quietly shelved, unmeasured pilot burns
the organization's appetite for the idea.

## Handover

Launch is not done. Done is the handover triad from the
[engagement lifecycle](../customer/01-engagement-lifecycle.md): runbooks for the failures
that actually happened, tests the customer can run after routine changes, and named
owners on the customer side who know they own each component. The practical standard for
"done": the customer runs the system unaided for a defined window - most teams use 2 to
4 weeks - with you watching rather than driving.

Then close the loop that FDE job descriptions make explicit: Anthropic's posting names
"identify and codify repeatable deployment patterns" and feeding insights back to
product and engineering as core responsibilities. The write-up of what worked, what the
customer's constraints forced, and what should become a product feature is part of the
engagement, not an afterthought. The [deployment patterns](02-deployment-patterns.md)
catalog is what that responsibility looks like as a document.

## Related documents

- [Deployment patterns](02-deployment-patterns.md) - where the system physically lands once the crossing is committed
- [The production readiness checklist](03-production-readiness-checklist.md) - the go/no-go gate for the launch this document plans
- [The engagement lifecycle](../customer/01-engagement-lifecycle.md) - the phase model, exit criteria, and the handover triad
- [From requirements to spec](../customer/02-requirements-to-spec.md) - where the definition of done and pilot thresholds get written
- [Evaluation and testing](../ai/03-evaluation-and-testing.md) - how pilot thresholds are measured and proven to a skeptic
- [Monitoring and reliability](../ai/04-monitoring-and-reliability.md) - the observability that hardening assumes

## Further reading

- [Fortune: MIT report on GenAI pilots](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo) - the ~95% finding and why success correlates with workflow integration
- [Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) - white-glove deployment and the codify-patterns mandate, as posted 2026
- [Site Reliability Engineering](https://sre.google) - Google's SRE book; the runbook and postmortem practices handover depends on
