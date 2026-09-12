# The Engagement Lifecycle

Every engagement is different; the phases are not. This document is the map: ten phases
from the first account read to the day the customer's team runs the system without you,
each with activities, artifacts, exit criteria, and a classic failure. Every other
document in this section zooms into one phase - read this first, then go deep where your
engagement currently sits.

## The phase model

Discovery bleeds into requirements; integration sends
you back to architecture. What must not overlap is the exit: we recommend enforcing exit
criteria in writing with the customer, even when the calendar argues for skipping ahead.

### 1. Pre-engagement context

Purpose: arrive with history and a fit judgment, not a blank page.

Key activities:

- Read the account history - prior engagements, open escalations, known complaints, and
  the politics you are walking into
- Run a product fit check - confirm the ask is something your product can genuinely do,
  not a sales promise wearing engineering clothes
- Confirm the team - who is deployed, for how long, and who backs them

Artifacts: account brief, fit assessment, engagement calendar.

Exit criteria: the assigned engineer can state the customer's problem in one sentence and
name the relationship owners.

Classic failure: the team arrives fluent in the demo and ignorant of the last three
escalations.

### 2. Kickoff

Purpose: convert intent into a signed-off plan with named people and a working cadence.

Key activities:

- Define success in writing - metrics, baselines, dates, owners, and what happens if
  they slip
- Map stakeholders - sponsor, operators, skeptics, and whoever grants approvals
- Agree cadence - demo schedule, status format, escalation path
- File access requests on day one - repos, data, clouds, environments - because
  approvals queue

Artifacts: engagement plan, stakeholder map, access requests, shared calendar.

Exit criteria: a signed-off engagement plan the sponsor has acknowledged in writing.

Classic failure: kickoff ends with enthusiasm and no written success definition, so
later disputes are judged by memory.

### 3. Discovery

Purpose: replace the sales-time problem statement with one grounded in observed work.

Key activities:

- Interview stakeholders - sponsors for outcomes, operators for how the work is done
- Shadow workflows - watch the process end to end, including the spreadsheets around it
- Walk the data - schemas, quality, volumes, freshness, and who owns each source

Artifacts: interview notes, workflow map, data inventory, draft problem statement.

Exit criteria: a problem statement the sponsor accepts as their own, in their words.

Classic failure: interviews with managers only, yielding requirements for a job nobody
does as described.

### 4. Requirements alignment

Purpose: turn discovery into a spec both sides sign.

Key activities:

- Write the spec - problem, goals, non-goals, scope in and out, acceptance criteria
- Run the review ritual - silent reading, objections as tracked questions, named
  sign-offs
- Baseline the exclusions - what phase 1 will not do, written down early

Artifacts: `requirements.md` or equivalent, acceptance criteria list, open question log.

Exit criteria: named individuals have signed the spec - an emailed acknowledgment
counts - and every open question has an owner and a date.

Classic failure: the spec is circulated, praised, never signed, and the later scope
argument has no reference document.

### 5. Architecture and planning

Purpose: design within the customer's constraints and produce a plan their operators
believe.

Key activities:

- Choose the deployment shape - where code and data live, what stays inside the customer
  tenant
- Write decision records - the options, trade-offs, and what was rejected and why
- Plan milestones with their ops team - not around them; they run the environments you
  ship into

Artifacts: architecture sketch, decision records, milestone plan, environment diagram.

Exit criteria: a plan the customer's ops team believes - reviewed by them, objections
resolved or logged.

Classic failure: an architecture ignoring their existing cloud posture, discovered
at integration time when changes are expensive.

### 6. Build and prototype

Purpose: answer the biggest technical risk with a thin end-to-end slice before polishing
anything.

Key activities:

- Build the walking skeleton - one slice end to end with real interfaces, everything
  else stubbed
- Gate the PoC - define in advance what evidence it must produce and by when
- Demo early to operators - not only sponsors; operators see what breaks

Artifacts: working skeleton, PoC results, demo recording, updated risk list.

Exit criteria: a PoC decision made with data - continue, pivot, or stop - against the
gate from phase 5.

Classic failure: three months polishing a happy-path demo while the risky part goes
untested until integration.

### 7. Integration

Purpose: connect the prototype to the customer's real systems, identities, and data.

Key activities:

- Wire APIs and auth - service accounts, secrets handling, token lifetimes, rate limits
- Build the data pipelines - ingestion, validation, and the schema drift you will
  actually get
- Prove it in non-production - end to end, unattended, with customer-shaped data

Artifacts: integrated build, pipeline runs, integration log of credentials and
endpoints.

Exit criteria: end-to-end runs on real data in a non-production environment without you
in the loop.

Classic failure: trusting the pristine test dataset and meeting real volumes, nulls, and
duplicates at launch.

### 8. Evaluation and pilot

Purpose: prove quality and value against written bars, with real users, before anyone
promises production.

Key activities:

- Build the golden dataset - cases from real traffic plus known edge cases, agreed with
  the customer
- Run the user pilot - a defined group, a defined period, defined thresholds
- Review results jointly - the customer sees the same numbers, at the same time

Artifacts: golden dataset, evaluation reports, pilot findings, go/no-go recommendation.

Exit criteria: the metrics meet the written bar from phase 4; if not, the phase loops
back to build instead of drifting into a launch.

Classic failure: a pilot with no thresholds, ending when patience runs out rather than
when evidence arrives.

### 9. Production launch

Purpose: go live deliberately, with rollout control and an owner for every failure mode.

Key activities:

- Run the readiness checklist - logging, alerting, rollback, support boundaries, load
- Plan the rollout - phased user groups, feature flags, a kill switch everyone knows how
  to pull
- Name the alerting owner - yours until handover, theirs after; both know the day it
  changes

Artifacts: readiness review, rollout plan, dashboards, on-call arrangement.

Exit criteria: live in production, with alerting wired and a named owner for every
component.

Classic failure: launching before the customer's change freeze with no rollback plan, so
the first incident becomes a trust incident.

### 10. Handover and feedback loop

Purpose: make yourself unnecessary, and send what you learned back into the product.

Key activities:

- Write runbooks - for the failures that actually happened, not the ones convenient to
  document
- Train the customer team - on operations, not just features
- Set support boundaries - who calls whom, for what, with what response times
- Codify patterns - feed reusable findings back to your product and engineering teams

Artifacts: runbooks, training sessions, support matrix, pattern write-up for your own
org.

Exit criteria: the customer team runs the system unaided for a defined period - most
teams use 2 to 4 weeks - with you watching, not driving.

Classic failure: celebrating at launch and leaving behind a system only you can operate.

## Timeline realism

Industry pattern tier - treat these as commonly reported shapes, not laws. Mid-size
engagements commonly run 6 to 16 weeks from kickoff to first production value, with
pilots of 4 to 8 weeks inside that. Regulated industries commonly run longer, mostly in
phases 7 and 9, where security review and change approval live. A startup can compress
the arc into weeks; an enterprise with procurement can spend that long in phase 1
alone.

The observed backdrop makes patience rational: roughly 95% of enterprise GenAI pilots
delivered no measurable P&L impact (MIT NANDA report, via Fortune, August 2025), with
causes clustering around workflow integration - what phases 3, 7, and 8 exist to get
right. This suggests planning around phase exits rather than one end date: a phase that
refuses to exit tells you early whether the real constraint is access, data, or
sign-off.

## The handover problem

Engagements fail at handover more often than at launch. Launch is a shared adrenaline
event with executives watching; handover is a quiet transfer of operational weight to
people who did not build the system and have their own queue.

We recommend treating handover as a triad - all three, or it is not a handover:

- Runbooks - a person who did not build the system can execute the recovery steps
  without calling you
- Tests - the customer can verify a routine change broke nothing, without you
- Ownership - named people on the customer side own each component, and they know it

A missing leg means the engagement is paused, not ended, until the first incident. The
[FDE loop](../role/05-the-fde-loop.md) ends at customer impact rather than deployment
for this reason, and the
[production readiness checklist](../deployment/03-production-readiness-checklist.md)
forces the ownership conversation weeks before go-live.

## The engagement health checklist

A weekly self-audit for the engagement lead. Any item unchecked two weeks running is a
schedule risk, whatever the status update says.

- [ ] We demoed something this week, even if rough
- [ ] Every open question has an owner and a date
- [ ] Access blockers are in the status update, not absorbed privately
- [ ] The spec still matches what we are building
- [ ] Someone on the customer side could run the system if we disappeared
- [ ] We know the current evaluation numbers without opening a document
- [ ] The sponsor heard from us directly this week
- [ ] Lessons are being captured while fresh, not queued for the wrap-up deck
- [ ] Next phase's exit criteria are written before we enter it

## Related documents

- [From requirements to spec](02-requirements-to-spec.md) - phase 4 in full; phases 6
  through 9 stand on it
- [Working in customer environments](03-working-in-customer-environments.md) - what the
  early phases feel like on the ground
- [Managing expectations](04-managing-expectations.md) - the work that runs across every
  phase
- [The FDE loop](../role/05-the-fde-loop.md) - the mental model these phases instantiate
- [Prototype to production](../deployment/01-prototype-to-production.md) - where
  engagements stall between phases 8 and 9
- [Discovery and requirements](../skills/02-discovery-and-requirements.md) - the phase 3
  interview and shadowing toolkit

## Further reading

- [The GenAI Divide: State of AI in Business 2025](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo) -
  Fortune's coverage of the MIT NANDA finding that ~95% of enterprise GenAI pilots show
  no measurable P&L impact; why phase 8 has exit criteria
- [Site Reliability Engineering](https://sre.google) - Google's SRE book; the runbook
  and postmortem practices phase 10 depends on
