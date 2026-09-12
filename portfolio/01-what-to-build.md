# What to Build: Portfolio Principles

For engineers assembling evidence that they can do FDE work before anyone pays them to do
it. This file defines the six principles that make a portfolio project FDE-shaped, explains
why tutorial projects actively hurt an application, and tells you what to do when you
cannot get access to a real customer. An FDE portfolio has one job: demonstrate that you
can walk the full loop from ambiguous problem to deployed system with measurable outcomes.
Tutorial projects fail that test; deployment-shaped projects pass it.

## What the portfolio has to prove

The [FDE loop](../role/05-the-fde-loop.md) runs from a vague customer problem through
discovery, requirements, integration, evaluation, and production to measurable customer
impact. The posting evidence says employers screen for exactly that arc: in an
[independent job-scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)
of 146 FDE postings (February-July 2026), 90.0% mention building or deploying production
systems, 88.0% describe direct customer-facing work, and 64.0% mention integrating systems,
APIs, or data. This suggests hiring managers are not screening for coding ability alone;
they are screening for engineers who can carry a system across every stage of the loop in
an environment they do not control.

A portfolio project therefore passes when it shows all of the loop, not just the build
stage. The six principles below are what that looks like in practice.

## The six principles

We recommend treating these as a bar, not a menu: a project that misses three of them is a
tutorial with extra steps, whatever the write-up claims.

### Ambiguous requirements, resolved by you

Start from a vague ask, the way a real customer gives one: "our support queue is a
firehose", "nobody can find anything in our documents". Then document how you turned that
ask into a spec - the questions you asked, the assumptions you killed, the scope you cut.
The before-and-after of requirements is the FDE work; the code is downstream of it. A
project that begins with a clean problem statement has already skipped the stage most
interviewers want to probe. [Discovery and requirements](../skills/02-discovery-and-requirements.md)
is the skill being demonstrated.

### A real integration

Your system must talk to at least one API or data source you did not create, with real
authentication, real rate limits, and real failure modes. Handling the third party's 429s,
retrying safely, and degrading when it goes down is where integration skill becomes
visible. A system that only talks to data you prepared yourself proves nothing about
working inside someone else's estate. [APIs and integrations](../engineering/02-apis-and-integrations.md)
covers the patterns the integration should show.

### Production deployment

The system must run somewhere real - a cloud account, a VPS, a container host - with
monitoring, and it must still be running when a reviewer looks. A localhost notebook or a
screenshot of a terminal is not a deployment. The deployment does not need to be impressive;
it needs to be operational: restarts on failure, logs you can read, a URL or endpoint that
works. This is the cheapest principle to satisfy and the one most portfolios skip.

### Evaluation with numbers

Build a golden set before you build the system, agree on a threshold, and report quality
against it - including the failures. "It works well" is not evidence; "86% correct
routings on 412 real tickets, with the failures concentrated in multi-intent messages" is.
Reporting the failure modes honestly is itself an FDE signal, because probabilistic systems
are sold and judged by their error profiles. [Evaluation and testing](../ai/03-evaluation-and-testing.md)
defines the practice.

### Measurable outcomes

Decide what "worked" means before you build, and report it after. The measure does not need
to be revenue; time saved per ticket, percentage of invoices needing human review, or
questions answered with citations all count - as long as the metric existed before the
code did. A project that reports outcomes chosen after the fact has the epistemics of a
marketing page. This principle is the portfolio-scale version of the loop's customer-impact
stage.

### A handover artifact

Write a README and runbook complete enough that another engineer can operate the system
without you: how to deploy it, how to read the dashboards, what to do when each alarm
fires, and where the known sharp edges live. Anthropic's FDE job description asks its
engineers to "codify repeatable deployment patterns" precisely because operating knowledge
that lives in one head does not survive handover
([Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008)).
The handover artifact is the FDE signature: it converts a project you did into a system
someone else can run.

## The tutorial trap

Portfolios full of completed course capstones, Kaggle notebooks, and clone apps are common,
and they hurt an FDE application. The reason is what they prove: that you can follow
instructions in an environment where the requirements, the data, and the evaluation criteria
were already decided by someone else. The FDE role is precisely the part that was decided
for you in a tutorial - the ambiguous ask, the messy data, the undefined quality bar, the
question of whether anyone adopts the thing. This suggests a tutorial-heavy portfolio
signals the opposite of the role's core skill, however strong the engineering inside it.

There is a second, more practical problem: uniqueness. A hiring manager reviewing FDE
applications has seen the same five tutorial projects many times. Identical projects are
indistinguishable, and indistinguishable projects compete on nothing. The deployment-shaped
project, built against constraints you had to resolve, is different by construction.

## Quality over quantity

We recommend one deep deployment-shaped project over five shallow ones. Depth signals are
cumulative inside a project, not across projects, and interviewers probe depth: two
follow-up questions collapse a shallow project and deepen a real one. The signals that
read as depth:

- A problem statement that starts vague and ends specific, with the rejected versions visible
- Decision records that name the alternative, the reason, and the accepted cost
- An evaluation table with dataset size, thresholds, and the failures you did not fix
- An incident log: what broke in operation, how you found out, and what changed
- A runbook that someone other than you has actually executed

A project with those five artifacts is a story an interviewer can spend an hour inside.
A project without them is a demo, and demos are what FDEs are paid to move past.

## What if you cannot access real customers

Most engineers building a portfolio do not have a customer. We recommend simulating the
constraints instead of waiting for permission. The options, in rough order of realism:

- Messy public data - municipal records, grant filings, court dockets, regulatory filings,
  and app-store reviews are dirty, duplicated, and versioned, which is the point
- A nonprofit as your first client - small organizations have real workflows, real
  constraints, and real gratitude; the data is real even when the budget is zero
- An internal team - the team down the hall at your current employer has the same dynamic
  as a customer: requirements you do not control and success you do not define alone
- A friend's business - a real operator with a real queue of email, invoices, or tickets
  gives you adoption stakes no synthetic project can

Whichever you choose, run the constraint simulation checklist before building:

- [ ] The brief came from someone who is not you, or is written the way a customer would write it
- [ ] At least one data source you did not clean or curate
- [ ] At least one external API or system with real authentication and rate limits
- [ ] One constraint you did not choose: PII handling, no egress, a latency budget, or a cost cap
- [ ] Someone other than you has used the system, and their feedback is logged
- [ ] The quality bar and the outcome metric were defined in writing before the build started

Six checked boxes and the project is deployment-shaped regardless of who paid for it.

## Related documents

- [Project ideas](02-project-ideas.md) - twelve briefs engineered around these six principles
- [Presenting projects](03-presenting-projects.md) - how to make the depth visible to a reviewer
- [The FDE loop](../role/05-the-fde-loop.md) - the sequence a passing project has to walk
- [Discovery and requirements](../skills/02-discovery-and-requirements.md) - the skill behind principle one
- [Evaluation and testing](../ai/03-evaluation-and-testing.md) - the practice behind principle four
- [Prototype to production](../deployment/01-prototype-to-production.md) - the professional-scale version of the same crossing

## Further reading

- [Independent job-scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md) - what 146 FDE postings actually ask for (February-July 2026)
- [Fortune: MIT report on GenAI pilots](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo) - why deployment-shaped evidence, not model skills, is what the market pays for (August 2025)
