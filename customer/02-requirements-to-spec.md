# From Requirements to Spec

For the FDE turning discovery notes into an agreed document. The spec is where discovery
becomes a contract with the future: it is the artifact every later argument about scope,
quality, and dates gets settled against. Bad specs are the root cause of most failed
deliveries - and they fail quietly, weeks later, as rework, missed acceptance criteria,
and disputes with no reference document.

## Why specs fail

Four killers account for most spec failures. None announces itself at review time; all
surface during build, when they are expensive.

- Ambiguity - words that mean different things to different teams. "Handle the obvious
  errors" is a plan for a dispute: your engineer hears "retry and log", their QA lead
  hears "a documented recovery path per error class". Replace every such phrase with a
  number or a named example.
- Invisible assumptions - the ones you imported. Your spec says "nightly batch" because
  your last engagement was a nightly batch; their data team assumes streaming.
  Assumptions you do not write down cannot be corrected, only discovered.
- Moving stakeholders - the sponsor who signed the spec changes roles, and the successor
  reopens settled decisions. A spec without named sign-offs and a change process gives
  the successor nothing to inherit except an argument.
- Unbounded scope - "phase 1 should probably also..." with no non-goals section. Scope
  without explicit exclusions expands to fill the calendar; the non-goals list is the
  only sentence in the spec that buys you time.

## The one-page spec skeleton

Use this skeleton when there is nothing heavier to justify:

```
<Project> - Phase 1 spec - v<n> - <date>

## Problem statement
<One paragraph: the measurable problem, the current baseline,
and where the numbers came from.>

## Goals
- <Outcome with metric and target, e.g. "routing accuracy at
  least 90.0% on the pilot dataset, measured weekly">

## Non-goals
- <What this phase explicitly will not do>

## Scope
- In - <capabilities, systems, user groups, environments>
- Out - <neighboring systems and features we will not touch>

## User stories and acceptance criteria
- As a <role>, I need <capability>, so that <outcome>.
  - Given <state>, when <action>, then <observable result>
  - Given <edge case>, when <action>, then <observable result>

## Non-functional requirements
- Latency - <budget at stated load>
- Data handling - <what may be read, stored, logged, sent externally>
- Audit - <what must be reconstructable, and for how long>
- Rollout control - <flags, phased groups, kill switch>
- Cost - <ceiling per unit at stated volume>

## Architecture sketch
<One diagram or five lines: components, where they run, data flows.>

## Rollout plan
<Phases, user groups, success bar per phase, abort criteria.>

## Open questions
- <Question> - owner <name> - due <date>

## Glossary
- <Customer term> - <definition in the customer's words>

## Sign-off
- <Name, role, customer> - <date>
- <Name, role, vendor> - <date>
```

When is one page enough? The rule we recommend: the document grows when the blast radius
grows. A pilot inside one team, on mock data, with no external data flows is fine at one
page. A spec that touches production customer data, a second system of record, or a
compliance boundary needs every section expanded, plus decision records and a rollback
plan. Length follows consequence, not the seniority of the audience.

## Acceptance criteria that survive contact with QA

Write behavior criteria in given/when/then form:

```
Given a ticket classified as billing with confidence 0.85 or higher,
when it enters the routing queue,
then it lands in the billing queue within 60 seconds,
and the routing decision is logged with model version and timestamp.
```

Three rules make criteria survive QA:

- Measure, do not adjective - "accurate" is a mood; "at least 90.0% of routed tickets
  reach the correct queue on the pilot set" is a criterion. Attach the dataset, the
  threshold, and the measurement method.
- Edge cases are first-class citizens - empty inputs, expired tokens, tickets in a
  language the model handles badly, and the customer's own top failure cases from last
  year. Criteria covering only the happy path are marketing.
- Name the validator and the data - who signs off, on what dataset, by when. A criterion
  nobody has agreed to verify is a wish.

## Non-functional requirements that matter in customer environments

Customers rarely ask for these and always notice their absence:

- Latency budgets - a suggestion needed in 200 milliseconds is a different system than
  one needed in 8 seconds; interactive means interactive at their peak load, not yours
- PII handling - which fields the system may read, store, log, and send to external
  APIs; it is the first question their security team asks, so answer it in the spec
- Audit requirements - who must be able to reconstruct what happened, and for how long
  the records must live
- Uptime and support windows - what "down" means, who gets called, and whether your
  on-call covers their Monday morning
- Rollout control - feature flags, phased user groups, and a kill switch; the customer
  wants the system turn-off-able faster than it was turned on
- Cost ceilings - a cap per ticket or per query, because a system that works brilliantly
  at $4 per ticket is a failed project at their volume

## The review ritual

The review meeting is part of the spec. We recommend this shape:

1. Send the spec 24 hours ahead, and state that sign-off is the meeting's output
2. Open with 10 to 15 minutes of silent reading - the objections people write in the
   margins are not the ones they raise in the room
3. Walk the scope-out list first; that is where the disagreements live
4. Capture every objection as an open question with an owner and a date - tracked but
   open beats resolved by silence
5. Close with named sign-offs and dates in the document itself

An emailed "looks good, let's go" from the sponsor is a signature in practice: paste it
into the spec with the name and date attached. Do not wait for a formal signature process
to appear.

## Change management

The spec is versioned: `requirements.md` in the shared repo with a changelog at the top,
or a dated document ID if the customer lives in a document system. Changes after sign-off
go through a change request with three fields: what changes, why, and the impact
statement. Impact statements speak in the schedule's own language: "adds roughly 2 weeks
and moves the pilot start past the December change freeze, so first results land in
mid-January." That sentence lets a busy sponsor make a real decision; "it's a small
change" does not.

No silent scope: work agreed verbally in a corridor is work that will be contested at
acceptance. If you build it, write it into the spec first.

## Worked example

Fictional, but assembled from recurring shapes. The customer ask, verbatim from the first
meeting:

"We want AI to help with our support tickets."

Three facts from discovery:

- 40% of inbound tickets enter the wrong queue first, and re-routing adds a median 9
  hours to first response (ticketing system export, measured across one discovery week)
- The 60-agent support team runs a triage rota; automation must fit the rota, not
  replace it
- Ticket text contains customer names and account numbers that cannot leave the tenant

The resulting spec excerpt:

```
## Problem statement
40% of tickets enter the wrong queue (ticketing export, measured
2026-03-02 to 2026-03-06), adding a median 9 hours to first response.

## Goals
- Route at least 90.0% of new tickets to the correct queue on the
  pilot dataset, measured weekly by the support ops lead
- Fit the existing triage rota: suggestions only, agent can override

## Non-goals
- No auto-closing or auto-replying in phase 1
- No changes to the ticketing system itself; we consume its API
- No PII leaves the tenant: names and account numbers masked
  before any external model call

## Acceptance criteria (excerpt)
- Given a new ticket in any of the 12 supported categories,
  when it is created, then a queue suggestion is attached
  within 60 seconds
- Given a suggestion, when the agent overrides it, then the
  override is logged with a reason code for weekly review
- Phase 1 passes if 90.0% routing accuracy holds on the pilot
  dataset for 2 consecutive weeks; below that, phase 1 extends
  or stops, by joint decision
```

Note what the conversion did: it replaced a vibe ("help with tickets") with a measured
baseline, a written boundary, and a bar with a measurement plan and a stop condition.

## Related documents

- [The engagement lifecycle](01-engagement-lifecycle.md) - where this document sits:
  phase 4, with phases 6 through 9 standing on it
- [Discovery and requirements](../skills/02-discovery-and-requirements.md) - how to
  gather the raw material this spec is written from
- [Evaluation and testing](../ai/03-evaluation-and-testing.md) - how the acceptance
  thresholds get measured once the pilot starts
- [Trade-offs and decision records](../system-design/03-trade-offs-and-decision-records.md) -
  where the architecture constraints behind the spec get recorded and challenged
- [Managing expectations](04-managing-expectations.md) - the kickoff promises this
  document formalizes

## Further reading

- [Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) -
  lists strong discovery and communication among fit criteria; the spec is the artifact
  where those skills become enforceable
