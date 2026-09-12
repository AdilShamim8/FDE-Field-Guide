# Failure Stories

The industry publishes almost no failure postmortems, which makes failures the most
valuable thing this guide can document carefully. This file separates what is documented
(sourced) from what is pattern (labeled as such), walks the failure modes that recur across
engagements, tells one clearly fictional composite failure story end to end, and closes
with the questions that keep your own engagement off this page. The engineering catalog of
the same failures, told by technical tell and fix, lives in
[common failure modes](../troubleshooting/03-common-failure-modes.md); this file is the
engagement-level view.

## What is documented

The factual spine is a measured statistic. The MIT NANDA report "The GenAI Divide: State of
AI in Business 2025" found that approximately 95% of enterprise GenAI pilots deliver no
measurable P&L impact (Fortune coverage, August 18, 2025,
[Fortune](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo)).
The report ties the surviving ~5% to workflow integration, domain specificity, and buying
external tools rather than building internal. Read the inverse way, and with the caution
that this inverse reading is interpretation: pilots stall where the tool does not fit the
workflow it was dropped into, where the domain specificity was never built, and where teams
undertook customization and context-heavy builds that never converged.

The role itself has a documented criticism, which is a failure story about the FDE motion
rather than the customer's system: Wikipedia notes that some engineers consider the role
undesirable because of travel requirements and pressure to solve problems on short
timelines ([Wikipedia](https://en.wikipedia.org/wiki/Forward_deployed_engineer)). The
documented pattern is clear even though individual cases are not: the role's own failure
mode is burnout, and an FDE team that burns out takes the customer relationship down with
it. Staffing, rotation, and travel expectations are engineering constraints of the
engagement, not personal weaknesses.

## The documented failure modes

What follows is pattern tier: these recur across practitioner reporting and match the
drivers in the measured evidence, but no public source names names. [Prototype to
production](../deployment/01-prototype-to-production.md) turns each into a prevention plan;
here they are as they present in the room.

- The pilot that ran on curated data - a clean extract, hand-loaded, one snapshot in time.
  The demo was excellent because the data was excellent, and production arrived with
  refreshes, drift, and volume the extract never represented. The tell is quality that
  degrades the first time real data flows. Prevention: scheduled refresh and quality gates
  from day one, per [data pipelines](../engineering/03-data-pipelines.md).
- The shadow-workflow pilot nobody adopted - the system ran beside the real process, and
  nobody changed how they work. Usage decays after launch week, and the P&L never moves,
  which is exactly the outcome the NANDA statistic counts. Prevention: adoption planning as
  an engagement phase with exit criteria, per
  [the engagement lifecycle](../customer/01-engagement-lifecycle.md).
- The undefined quality bar - "works" was never measured against a threshold, so the pilot
  ends when patience or funding runs out rather than when evidence arrives, and every
  quality debate is re-litigated from memory. Prevention: a golden set and agreed
  thresholds during requirements, per
  [evaluation and testing](../ai/03-evaluation-and-testing.md).
- The integration debt surprise - SSO, permissions, data refresh, and handoffs to
  neighboring systems were deferred as "launch details", and the crossing ends up costing
  more than the build. The prototype hardcoded what production has to negotiate. Prevention:
  integration contracts and honest hardening estimates, per
  [APIs and integrations](../engineering/02-apis-and-integrations.md).
- The cost surprise - unit economics that looked trivial at pilot volume are a budget line
  at production volume, and an unapproved budget line gets cut along with the system
  attached to it. Prevention: cost visibility, alerts, and an approved budget before
  go-live, per the [production readiness checklist](../deployment/03-production-readiness-checklist.md).
- The missing owner at handover - the first production failure lands on a person who does
  not exist, and an unrepaired failure teaches users to route around the system
  permanently. Prevention: the handover triad of named owner, runbook, and support
  boundary, per [the engagement lifecycle](../customer/01-engagement-lifecycle.md).

## The composite failure story

What follows is a fictional composite. The company does not exist, the engagement did not
happen, and every detail is assembled from the documented failure modes above. It is told
in the guide's scenario format so it can be compared against working scenarios elsewhere in
the guide.

### Situation

Calloway Mutual, a fictional mid-size insurer, buys a claims-document Q&A assistant from a
vendor. Two FDEs are assigned. The statement of work defines success as "assistant
deployed" - a phrase nobody interrogates. The executive sponsor wants it live before the
annual board review.

### Constraints

- Data - twelve years of claims documents, scanned, mixed quality, PII throughout
- Security - PII cannot leave the tenant, and the claims network has no internet egress
- People - no named owner on the insurer side; the sponsor sits in the CIO's office, the users sit in claims operations
- Timeline - ten weeks, set by the board review rather than by any engineering estimate

### Move-by-move

1. Weeks 1-2 - discovery is compressed into two calls; the team samples 300 recent, closed claims because they are the cleanest documents available, and nobody asks what a data refresh would look like because the pilot is scoped as a snapshot
2. Week 3 - the demo lands well: five hand-picked questions answered fluently with citations; the sponsor books the board review; the quality bar is now, implicitly, "as good as the demo"
3. Weeks 4-7 - integration realities arrive: SSO, PII redaction, and egress rules consume the weeks the plan reserved for evaluation; the golden set is deferred to "after launch"
4. Week 8 - launch to 40 adjusters; usage peaks at 60 questions in week one and then decays; adjusters route around the assistant because its answers cite the 2023 procedure manual while the workflow moved on - the snapshot aged
5. Week 9 - a scheduled claims-system migration changes document IDs; ingestion breaks silently; the assistant keeps answering from a stale index; nothing is monitored, so nobody is paged and nothing is logged
6. Week 10 - the sponsor asks for board metrics; the team has usage logs but no outcomes; the meeting becomes a blame exchange - the vendor blames data access, operations blames the tool - and the sponsor cancels round two

### Outcome

The pilot ends at the deadline with no evaluation, no owner, no adopters, and no evidence
either way about whether the system could have worked. Every documented failure mode above
appears in one engagement, and none of them is the model. A rerun - still fictional, a year
later, by a new team - did five things differently:

- Named a business owner in claims operations before the statement of work was signed
- Built the golden set from the insurer's own historical questions and misanswers, before the prototype
- Ran on refreshed data with a freshness alarm from week one
- Defined the quality bar as citation-grounded answers above an agreed threshold on the golden set
- Launched to five adjusters with a weekly review, then scaled by evidence rather than by calendar

The lessons, one per miss: the demo that oversold was the cheapest moment to add honesty
and the most expensive to skip ([managing expectations](../customer/04-managing-expectations.md));
the eval gap turned every later dispute into memory versus memory
([evaluation and testing](../ai/03-evaluation-and-testing.md)); the stale index was a
freshness check that cost an afternoon and was never written
([data pipelines](../engineering/03-data-pipelines.md)); and the missing owner meant the
silent breakage had nowhere to land ([prototype to production](../deployment/01-prototype-to-production.md)).

## Reading failures well

We recommend running these questions on your own engagement every two weeks, in writing,
with the answers dated. They are cheap, and every one maps to a failure mode above.

- What are we not measuring? - every unmeasured claim is a future dispute conducted from memory
- Who owns this after we leave? - if the answer is a role rather than a name, it is nobody
- What happens when the data refreshes? - the question the composite pilot never asked, and the one that ages systems silently
- What would make us kill this pilot? - if nothing would, the pilot cannot produce evidence, only demo theater
- Which part of the demo would not survive real data? - name it now and fix it before launch, or schedule the failure

The two-week cadence is deliberate: it is frequent enough to catch the quiet drifts -
stale data, decaying usage, an owner who left - before they compound into the blame
meeting.

## Related documents

- [Common failure modes](../troubleshooting/03-common-failure-modes.md) - the engineering catalog of the same failures, by tell and fix
- [Prototype to production](../deployment/01-prototype-to-production.md) - the crossing, its pilot-failure taxonomy, and the prevention plan
- [Evaluation and testing](../ai/03-evaluation-and-testing.md) - the practice that prevents the eval gap in the composite
- [Managing expectations](../customer/04-managing-expectations.md) - the demo honesty and bad-news discipline the composite lacked
- [Documented LLM deployment cases](02-llm-deployment-cases.md) - the sourced evidence this file reads against the grain
- [The engagement lifecycle](../customer/01-engagement-lifecycle.md) - the phase exits the composite skipped

## Further reading

- [Fortune: MIT report on GenAI pilots](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo) - the measured failure rate behind this file's factual spine (August 2025)
- [Wikipedia: Forward deployed engineer](https://en.wikipedia.org/wiki/Forward_deployed_engineer) - the documented criticisms of the role itself
