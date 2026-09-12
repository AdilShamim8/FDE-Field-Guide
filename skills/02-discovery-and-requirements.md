# Discovery and Requirements Gathering

This document is for FDEs at the start of an engagement, when the customer knows it wants
"AI" but cannot yet say what for, and for engineers preparing for discovery-stage
interview rounds. Discovery is the highest-leverage skill in the job: decisions made here
are cheap to change, and the same decisions after the first demo cost weeks. You get a
question bank you can use tomorrow, a method for watching real work, a clean handoff into
requirements, and the failure modes that quietly sink engagements.

## The evidence: discovery is engineering

Two independent sources frame this skill.

In an independent job-scrape analysis of 146 unique FDE postings from 94 companies
(February-July 2026), scoping requirements and discovery appears in 52.0% of postings -
the same band as RAG (52.0%) and ahead of Kubernetes (35.0%)
([the analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)).
OpenAI's FDE postings put it first in the sentence: "lead technical discovery,
architecture, implementation, evaluation, productionization, and handoff"
([openai.com/careers](https://openai.com/careers)).

Meanwhile, the MIT NANDA report on enterprise GenAI found that roughly 95% of pilots
deliver no measurable P&L impact, and that the pilots which succeed are integrated into
specific business workflows rather than bolted on top of them (Fortune, August 2025)
([coverage](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo)).

This suggests the market treats discovery as engineering, not pre-sales. The failure it
prevents - building a good system for the wrong problem - is the most expensive failure an
FDE can cause, and no amount of late engineering skill repairs it.

## The discovery mindset

You are not there to pitch the product you came with. You are there to extract the real
problem from the people who live with it, at a level of detail where you could do their
job for a day. Two habits follow:

- Bias toward stories over opinions. "What do you think the problem is?" gets you a
  committee-approved answer. "Walk me through the last time this happened" gets you the
  workflow.
- Treat every meeting as evidence-gathering: write down what you observed about how the
  organization actually works, not just what was said.

## The stakeholder interview framework

Run interviews as 45-minute 1:1s where possible, with two people from your side: one
asks, one takes notes. Record with permission. Close every session by reading back what
you heard and resolving contradictions in the room - ambiguity left in notes is a defect.

The questions below are grouped by theme. Ask them roughly as written; the wording is
chosen to pull specifics instead of positions.

### Current state

- Walk me through the last time this problem happened, from the moment it started to the moment somebody closed it out.
- What does the person doing this work use today - which screens, spreadsheets, scripts, and group chats?
- If I sat next to your team for a day, what would surprise me?

### Pain and cost

- What does this cost per week, in hours, money, or customers affected? A rough range is fine - what does it include?
- Which part hurts most: the volume, the uncertainty, or the rework afterwards?
- What happens if nothing changes for a year?

### Volume and edge cases

- How many cases come through per day, and how does that move across the month?
- What share of the cases is weird? What were your three weirdest last month?
- Which cases will always need a human, no matter how good the system gets?

### Success metrics

- Ninety days after go-live, what number tells you this worked?
- If you are not in the room when someone asks that question, who answers it?
- What would make you call this project a failure even if it shipped on time?

### Constraints

- What data exists, where does it live, and who is allowed to use it for what?
- Which compliance or privacy rules apply - SOC 2, HIPAA, GDPR, internal policy?
- What systems would this have to live inside, and who owns those systems?
- What is the deadline, and what real-world event is it attached to?

### Decision structure

- Who decides whether this ships? Who can veto it? Who pays for it?
- Whose sign-off did the last similar project need that nobody planned for?

### Prior attempts

- What has been tried before, and why did it stop or stall?
- What did the last vendor or internal team get wrong?
- Is there a postmortem, ticket export, or proposal from that attempt I can read?

The last theme is the one teams skip and later regret. Prior attempts tell you where the
organizational antibodies are and what "here we go again" sounds like.

## Watching the workflow

Interviews tell you what people believe; shadowing shows you what they do. Spend at least
one session watching the actual work happen - the morning triage, the queue review, the
escalation call. Request the artifacts while you are there:

- Database schemas and table row counts - where the data actually lives and how messy it is
- Anonymized sample records - the real shapes of real data, including the broken ones
- Ticket or case exports - volumes, categories, resolution times, and the free-text field nobody fills in
- Call transcripts or chat logs - the language customers and operators actually use
- Existing dashboards - what management watches, which is not always what matters
- Prior vendor proposals - what was promised before, and what it cost

Why the demo environment lies: curated data, a happy path, no backlog, no concurrent
users, no escalation queue, and no nulls in the demo data. The distance between the demo
and the production workflow is exactly where pilots die (see
[failure stories](../case-studies/03-failure-stories.md)); measure that distance during
discovery, not after go-live.

## From discovery to requirements

Discovery ends with documents, not impressions. Three artifacts cover most engagements.

The problem statement, in four lines:

```
<Who> needs <what capability> so that <measurable outcome>.
Today they <current workaround>, which costs <quantified pain>.
Success in 90 days: <metric> moves from <baseline> to <target>.
Out of scope: <explicit non-goals>.
```

User stories with acceptance criteria, one per workflow. For example:

- As a duty manager, I want overnight exceptions grouped by likely cause, so that I can assign the top ten before 07:00.
  - Acceptance: given the last 24 hours of exception records, all exceptions above $1,000 impact are grouped, each group links to its source records, and groups below 80% confidence are flagged for human review.

Non-functional requirements, negotiated rather than assumed:

- Latency - what response time does the workflow tolerate?
- Privacy - what data may leave the customer environment, and to which providers?
- Uptime - what happens to the business when the system is down for an hour?
- Rollout control - can operators switch the feature off per team or per workflow?
- Cost ceiling - what monthly spend keeps this worth doing?

Scope-in and scope-out lists. The out list is the valuable one: it is what stops the slow
creep nobody notices until week eight.

The full spec skeleton - sections, sign-offs, sequencing - lives in
[requirements to spec](../customer/02-requirements-to-spec.md); discovery feeds it its
opening problem statement, its testable acceptance criteria, and its risks section.

## Discovery failure modes

Each of these is common, and each is avoidable with a habit.

- Skipping the data walkthrough. Requirements written without seeing the data assume the
  happy path. The first `SELECT *` on the real table rewrites half the spec.
- Trusting the champion's summary over the operators' reality. Champions compress;
  operators live in the exceptions. When the two disagree, believe the operator and tell
  the champion gently.
- Ignoring the approver who was never in the room. Security, legal, and data governance
  can veto in week six what they would have waved through in week one. Find them early
  (see [stakeholder management](04-stakeholder-management.md)).
- Capturing requirements from people with time to talk instead of people who do the work.
  Availability correlates inversely with operational knowledge. Go to the floor.
- Leaving ambiguity in the notes. "Support bulk uploads" is not a requirement until
  someone says how many, how big, and how often. Resolve it before the meeting ends.

## Worked scenario: the shipment exceptions dashboard

A fictional but typical example, in the standard scenario format.

### Situation

A mid-size logistics company asks for "an AI dashboard for shipment exceptions". The
sponsor is the VP of operations, who saw a competitor demo and has budget for a six-week
pilot. You have never seen their data.

### Constraints

Exception data lives in a ten-year-old transportation management system (TMS). Overnight
exception handling happens in email and a spreadsheet. The ops team is twelve people with
no data team behind them. Any data leaving their VPC needs a security review that takes
about three weeks.

### What good looks like

Not a dashboard. By the end of the first week: a one-line problem statement the sponsor
recognizes as their own problem, one baseline number, an open-questions log with owners
and dates, and a thin slice agreed for the first demo.

### Move-by-move walkthrough

1. Ask the sponsor for three recent concrete exceptions and the people who handled them.
   You learn that "exceptions" means overnight shipments that missed delivery windows,
   triaged by a duty manager every morning at 06:00 from a spreadsheet exported from the
   TMS.
2. Shadow the duty manager for one morning. You learn the first hour of the day is
   triage: the cost is not missing information, it is 45 minutes to sort signal from
   noise, and the misses that reach customers become credits and complaints.
3. Request the artifacts: the TMS exception table schema, the last 90 days of records,
   the spreadsheet, and two weeks of complaint logs. You learn there are roughly 60
   exceptions per night, five recurring causes cover most of them, and the worst failures
   repeat a pattern the TMS already flags but nobody watches overnight.
4. Interview the finance delegate and the customer support lead. You learn credits are
   the measurable cost and first-response time is the metric support already tracks.
5. Write and read back the problem statement: duty managers need overnight exceptions
   ranked by customer impact and likely cause before 06:30, so they can prevent credits
   and complaints. Today they sort a raw export by hand, which costs about 45 minutes
   every morning and still misses preventable escalations. Success in 90 days is handling
   time and preventable credits, baselined together in week one. Out of scope: rerouting,
   carrier scorecards, real-time tracking.
6. Agree the thin slice: not a dashboard but a 06:00 ranked digest posted to the channel
   the duty manager already uses, with links back to TMS records, reviewed together each
   morning for two weeks.

The ask moved from "AI dashboard" to a ranked morning digest with a baseline and a
metric. The AI part is now attached to a workflow instead of floating.

### Failure modes

- Taking the dashboard literally and building it. You would ship a chart nobody acts on,
  and the pilot dies at the first steering meeting.
- Demoing on the raw export without checking data quality. The TMS export has free-text
  cause fields, duplicates, and timezone traps; the demo would surface all of them.
- Promising the 06:30 digest before seeing the data. If the overnight job fails
  silently twice in week two, the digest is a liability instead of a deliverable.

## Related documents

- [Requirements to spec](../customer/02-requirements-to-spec.md) - the spec skeleton this document feeds into
- [Stakeholder management](04-stakeholder-management.md) - the decision-structure questions continue as engagement-long alignment
- [Managing expectations](../customer/04-managing-expectations.md) - what to do when discovery changes what the customer thought it bought
- [Data pipelines](../engineering/03-data-pipelines.md) - the data walkthrough usually exposes the real integration work
- [The engagement lifecycle](../customer/01-engagement-lifecycle.md) - where discovery sits from kickoff to handover
- [Failure stories](../case-studies/03-failure-stories.md) - what happens when discovery is skipped

## Further reading

- [Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) - lists strong communication for discovery as an explicit fit criterion (2026 posting)
- [The New Stack on FDE teams](https://thenewstack.io/forward-deployed-engineers-ai) - why AI labs treat discovery and integration as one job (May 2026)
