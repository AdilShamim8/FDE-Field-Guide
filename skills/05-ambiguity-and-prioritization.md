# Working with Ambiguity and Prioritization

This document is for FDEs handed problems that arrive as one sentence and one
expectation. Ambiguity is the default state of the job: Anthropic's FDE posting asks for
"high agency with an ability to navigate ambiguity present in complex organizations"
([the posting](https://job-boards.greenhouse.io/anthropic/jobs/5302966008), 2026). On
customer engagements, requirements are outputs of the work, not inputs to it. You get a
triage method for ambiguous situations, a decision framework, prioritization patterns
that survive pressure, and a definition-of-done habit that keeps slices shippable.

## The ambiguity triage

When everything feels undecided, sort every open item into three buckets:

- Knowable now - go find out. Most ambiguity is an unasked question, not a hard one.
  Schedule the conversation this week and name the person who has the answer.
- Decidable now - decide and write it down. If the item affects the next two weeks and
  you already hold most of the information you will ever get, decide, record the decision
  and its reasoning, and move. A rough decision written down beats a precise one that
  never arrives.
- Must stay open - schedule the decision date and the owner. Some questions genuinely
  cannot be answered yet: approvals pending, budgets in cycle, data access in flight.
  Park them somewhere visible.

The standing artifact is the open-questions log, with four fields per row: question,
owner, decision date, and impact if unresolved. A real-looking example:

| Question | Owner | Decision date | Impact if unresolved |
| --- | --- | --- | --- |
| Which model provider is approved for customer data? | Customer security lead | Week 3 | Blocks all prototype work beyond fake data |
| Does the pilot include the EU region? | Sponsor | Week 4 | Expands privacy review by weeks |
| Is the morning digest email or in-app? | Duty manager | Week 2 | One hour of rework, no downstream effect |

The log does two jobs: it keeps must-stay-open items from leaking into the sprint, and
it shows the sponsor that ambiguity is being managed rather than ignored.

## Reversible versus irreversible decisions

A framing popularized at Amazon: two-way doors are decisions you can walk back through;
one-way doors are expensive or impossible to reverse. Two-way doors deserve speed, and
one-way doors deserve ceremony.

Most FDE decisions are two-way doors wearing one-way costumes. The model choice, the
vector store, even the chunking strategy are all swappable before customer data and
operator habits get attached to them. The genuinely one-way decisions are few: where
data lives, what gets written into systems of record, what operators are trained on, and
what gets promised contractually.

Two corollaries we recommend:

- Spend discovery effort proportionally. A week of interviews to choose a chunking
  strategy is overkill; a week to decide where customer data may flow is not.
- Default to reversible when the customer panics. Under pressure, customers reach for
  one-way doors: long contracts, big platform commitments, permanent data copies. Offer
  the two-door version - a two-week pilot on fake data before the platform decision -
  and you convert fear into a schedule.

## Prioritization under pressure

- Value versus effort, roughly sorted. Do the high-value, low-effort quadrant first.
  Avoid the high-effort, unclear-value quadrant no matter how interesting it is;
  interesting is not a value.
- Track two lists explicitly: customer-visible work and system-critical work. A backlog
  that is all plumbing never demos; one that is all demos never ships. The classic FDE
  failure is letting the demo list eat the whole week before an integration deadline.
- Price the integration tax out loud. Anything touching a system you do not own costs
  multiples of the estimate: auth, environments, test data, change freezes (see
  [APIs and integrations](../engineering/02-apis-and-integrations.md)). Say it during
  planning: "the model work is two days; the SSO integration is two weeks." Customers
  respect the number; they resent the surprise.
- Cut scope in a fixed order without killing trust: thin slice first, then breadth, then
  depth. The thin slice is one workflow on real data, end to end. Breadth is more
  workflows on the same rails. Depth is quality, latency, and edge cases. Cut depth
  before breadth, and breadth before the slice - never the slice itself, because the
  slice is the only part that produces learning.

## Definition of done

- Negotiate what "working" means before building. "It works" from a sponsor and "it
  works" from the operator running it at 06:00 are different claims, and only one of
  them survives contact with the workflow.
- Write acceptance criteria a skeptical operator would accept: given the last 24 hours
  of real records, the digest posts by 06:30, every item links to its source record, and
  anything below 80% confidence is flagged for human review. The full method for turning
  decisions into criteria lives in
  [requirements to spec](../customer/02-requirements-to-spec.md).
- Use demo checkpoints as ambiguity insurance. A demo every one to two weeks converts
  ambiguity into feedback before too much gets built on a guess. Say out loud that a
  checkpoint is not a promise of polish - it is a promise of evidence.

## Worked scenario: "just build something with our data"

A fictional but typical week one, in the standard scenario format.

### Situation

Week one at a mid-market insurance company. The sponsor, a COO with budget and
impatience, says: "just build something with our claims data and we'll know it when we
see it." Your team is you plus one customer data analyst at 30% time.

### Constraints

Claims data sits in a legacy DB2 warehouse. The analyst has read access to de-identified
text only. Any external data flow needs a security review that takes at least three
weeks. The claims operations team is skeptical - a previous vendor pilot failed quietly.
The sponsor's attention span is one demo.

### What good looks like

By the end of week one: an open-questions log with owners and dates, a shortlist of
three candidate thin slices with one chosen, one baseline number, and a demo booked for
week three. Nobody has built anything yet, and that is the point.

### Move-by-move walkthrough

1. Run the triage on everything ambiguous. For the knowable-now items, book
   conversations this week: the analyst walks you through the warehouse tables and which
   ones are trusted; the operations lead shows you the worst hour of their week.
2. Decide the decidable-now items and write each down: the pilot uses de-identified
   claim text only; the demo environment is your sandbox, not their network; the
   operations team sees everything before the COO does.
3. Park the must-stay-open items with dates and owners: provider approval with security
   by week three; the production deployment pattern by week six.
4. Pick the thin slice from what the walkthrough revealed: adjusters spend hours
   summarizing claim files by hand, so a draft-summary assist over 50 real de-identified
   claims is small, reversible, and uses access you already have.
5. Baseline one number with the analyst: minutes per summary today, timed over ten real
   summaries. This is the number the week-three demo will move.
6. Book a 20-minute week-three demo with the COO, framed in advance: "one workflow,
   real data, one number that moved - and you decide whether we go wider."

The sponsor's sentence stayed vague, but the engagement now has decisions, dates, and a
slice. "Know it when we see it" became "judge this number at week three."

### Failure modes

- Building the dashboard the COO pictures at night instead of the slice the workflow
  supports. It demos well once and changes nothing.
- Waiting for the security review before touching any data. Three weeks of goodwill
  burn while you "prepare". De-identified data you already have access to is the
  reversible door.
- Promising production at the week-three demo. The pilot has no deployment pattern, no
  monitoring, and no approver yet; the promise converts your week-six decision into a
  week-four obligation.

## Related documents

- [Discovery and requirements](02-discovery-and-requirements.md) - where the answers to knowable-now questions come from
- [Requirements to spec](../customer/02-requirements-to-spec.md) - how decisions become acceptance criteria
- [Prototyping and PoCs](../engineering/01-prototyping-and-pocs.md) - the thin slice, run properly
- [The engagement lifecycle](../customer/01-engagement-lifecycle.md) - how decision gates pace an engagement
- [Prototype to production](../deployment/01-prototype-to-production.md) - the one-way doors that get created here

## Further reading

- [Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) - the high-agency-in-ambiguity criterion in its original context (2026 posting)
