# Stakeholder Management

This document is for FDEs whose technical work keeps getting stalled, re-decided, or
vetoed by people they have never met. On customer engagements, the system you are running
has more stakeholders than services, and technical wins die in the organizational gaps
between them. You get a mapping method, the incentive questions that predict stalls, a
cadence that keeps approvals from becoming surprises, and the escalation and repair
patterns that protect trust.

## Mapping stakeholders

Six roles cover almost every engagement:

| Role | They win when | They fear |
| --- | --- | --- |
| Sponsor | the project moves their number | being attached to a visible failure |
| Owner | their problem shrinks | owning a system they cannot support |
| Operators | the daily work gets less painful | retraining, replacement, another tool |
| Approvers | nothing bad happens on their watch | surprise data, risk, or spend they never signed off |
| Blockers | the risk of saying yes goes away | being wrong in public |
| Champions | being right about you | their credibility spent on your pilot |

Approvers - security, legal, data governance, procurement - deserve a special warning:
they can veto the project without ever appearing in a planning meeting. The most common
organizational failure in customer deployments is discovering the real approver in week
six (see [security and compliance](../engineering/05-security-and-compliance.md) for the
technical half of that conversation).

For every person on the map, two questions matter: what do they win, and what do they
fear. Ask both in the first 1:1. The answers predict where an engagement stalls better
than any org chart - the sponsor's fear tells you what news you must never surprise them
with, and the operators' fear tells you why adoption will stall unless they help shape
the rollout.

In practice: if the sponsor wins when handling costs drop and fears a failed audit, you
lead every update with cost movement and flag anything that touches audit before it
happens. If the operators fear another tool to learn, you deliver into the channel they
already use instead of asking them to open one more dashboard. The map is cheap to make
and expensive to skip.

## Aligning incentives

- Find whose KPI moves. If no measured number improves when you succeed, nobody fights
  for the project when it becomes inconvenient. Find that KPI in week one and tie your
  success metrics to it (see
  [discovery and requirements](02-discovery-and-requirements.md) for the questions that
  surface it).
- Surface conflicts early. The ops team that must support what you build did not choose
  it, and engagements commonly stall when that team first hears about the system at
  go-live. Give them a named role in the design and a say in the rollout while changes
  are still cheap. If your system auto-closes tickets, bring the support team the metric
  change and the opt-out lever before they discover both in production.
- Pre-wire the big decisions. A pattern borrowed from consulting and enterprise delivery:
  meet each decider 1:1 before the meeting where the decision formally happens, fold
  their edits into the proposal, and let the meeting confirm rather than debate. This is
  not politics; it is respecting that people need to change their minds in private.
- Treat blockers as approvers without an exit. A blocker usually fears being wrong in
  public, so give them a cheap way to say yes: a sandbox, a time box, a rollback plan.
  Most blockers convert once the downside is bounded.

## Cadence

Who gets what, at what frequency - the defaults we recommend:

- Sponsor - a bottom-line update every one to two weeks; full detail only on request. A
  sponsor update is three lines: trajectory, the one number that matters this week, and
  any decision you need. Everything else goes where the owner reads it.
- Owner - a weekly working session with decisions and blockers, not a status read.
- Operators - daily contact during rollout weeks, then as needed; they should hear about
  changes before their users do.
- Approvers - at engagement gates and on any change touching their domain. The goal: no
  approval is ever a surprise, so no approval ever needs a meeting of its own.

Steering committees typically run every two to four weeks on an engagement. We recommend
asking for the slot at kickoff, so the rhythm exists before it is needed. Bring
decisions, not status: a steering meeting that ends without a decision made was a status
email with worse formatting. The standing agenda: what changed since last time, what
needs deciding today, what we need from the people in the room. Twenty minutes of
decisions beats an hour of demo theater.

## Conflict and escalation

- Escalate with options, not problems. Bring two paths with trade-offs and your
  recommendation: "data access is delayed. Option A ships aggregated-only in two weeks;
  option B waits for full access and ships in four. We recommend B if per-record
  attribution matters for the pilot metric."
- Follow the ladder: raise it with the individual first; then both managers together;
  then the sponsors. Skip steps only for safety, security, or legal issues.
- Never escalate by surprise. Tell the person you are escalating, why, and what you will
  ask for. A surprise escalation reads as an attack, and you will be working with that
  person long after the issue is forgotten.

Escalation done this way is a service to the customer, not a complaint about them: you
are surfacing a conflict the organization needs to resolve anyway, and making it cheap
to resolve.

Most conflicts on engagements are structural, not personal: two teams measured on
numbers that move in opposite directions. Naming the structural conflict out loud -
"support is measured on response time and we are asking them to absorb triage work" -
turns a fight into a design problem, and someone senior can usually solve design
problems.

## Trust repairs

Two repairs come up on almost every engagement.

When you break something in production, the note follows four beats: facts, impact, fix,
prevention. Send it within a day, in that order, with no adjectives doing the work of
evidence:

```
Subject: <service> incident - resolved <date>
What happened: one sentence, plain facts.
Impact: who felt it, for how long, what it cost.
Fix: what changed and when it resolved.
Prevention: the concrete change, and when it ships.
```

The technical side is covered in
[debugging customer systems](../troubleshooting/02-debugging-customer-systems.md).

When a date slips, say it early with a recovery plan, not late with an excuse. The
message has four parts: the new date, the reason in one sentence, what you cut or added
to hit it, and what you need from the customer. A slip announced at the deadline removes
every option except anger; a slip announced early with a plan is just a status update.

Our read of enterprise relationships is that trust accrues less through the absence of
incidents than through their handling - which makes the repair note a career skill, not
a chore.

## Related documents

- [Managing expectations](../customer/04-managing-expectations.md) - the customer-facing discipline of scope and bad news
- [Discovery and requirements](02-discovery-and-requirements.md) - the decision-structure questions that build the map
- [Security and compliance](../engineering/05-security-and-compliance.md) - the approver most engagements meet too late
- [Debugging customer systems](../troubleshooting/02-debugging-customer-systems.md) - the technical work before and after a trust-repair note
- [The engagement lifecycle](../customer/01-engagement-lifecycle.md) - where each stakeholder conversation belongs in the arc

## Further reading

- The Trusted Advisor (David Maister) - the trust equation is the cleanest model for why credibility and intimacy outweigh the technical pitch
- Never Split the Difference (Chris Voss) - tactical empathy for the escalation and negotiation conversations
