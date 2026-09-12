# Debugging in Customer Systems

For FDEs embedded with customers and the engineers who back them. Half of FDE debugging
is technical; the other half is navigating an environment that was not built for you: no
console access, ticket-queue approvals for every change, logs you cannot read, and an
ops team with its own priorities and queue. The craft is making progress inside opaque
systems rather than waiting for perfect visibility that never arrives
(interpretation from practice).

## Seeing what you need

### The visibility ladder

Access arrives in layers, each usually behind a justification, a ticket, and a
signature. Request it in this order, and justify each request with a concrete blocked
bug rather than a general need for "better observability":

1. Your own application logs and traces - you control these; if they do not answer the
   question, instrument before escalating
2. The customer's dashboard screenshots - low effort for them and often decisive: their
   system's view of the same request
3. Ticket exports - the change history lives there: what their team touched, and when
4. Sampled request or response pairs, with written approval - a handful of concrete
   payloads beats a week of inference
5. Screen-shares with their operators - watching someone else reproduce the bug is the
   fastest way to learn the system's real behavior
6. Read access to their logs - the endgame; valuable, slow to approve, and rarely
   necessary once the first five rungs are used well

Each approved rung buys credibility for the next: "we cannot tell whether your webhook
reached us; three screenshots would answer it" gets approved faster than "we need
broader access".

## Working the process

### Working through other people's process

In customer organizations, everything is a ticket: diagnostic queries, config changes,
restarts. Add change freezes around fiscal events and four-eyes reviews on production
access, and a ten-minute fix becomes a two-week project. This is an industry pattern;
only the intensity varies.

The moves that work, from repeated pattern:

- Batch your diagnostic asks - one ticket with five queries beats five tickets with one
  query each, because it costs one review instead of five
- Pre-write the ticket text for the ops team - they approve faster what they do not have
  to compose; include the exact command, expected output, and blast radius
- Offer the diff and the rollback plan with every change request - "here is the one-line
  change, here is the one-command revert" converts an unknown risk into a bounded one
- Make the review trivial - small changes, clear titles, no bundled surprises; a
  reviewer who can approve in four minutes approves today

None of this is gaming their process; it is reducing the cost of helping you. The
engineer who respects the ops queue gets more help than the one who routes around it.

## Technical moves

### Debugging at the boundary

Most cross-organization bugs live at interfaces: the SSO handshake that stalls, the
webhook they are sure they send, the schema that drifted, the firewall rule that changed,
the service account permission that expired. When a bug crosses the trust boundary,
instrument your side completely first: log exactly what you sent and exactly what you
received, with request IDs and timestamps, kept long enough to matter.

Then hand their team evidence, not accusations. "Your system returned HTTP 403 at
14:03:22 UTC for request ID `a1b2c3`, here is the full response body" is actionable -
their engineer can search for the ID and find the cause in minutes. "Your API is broken"
is not, and it puts their team in defense mode. The boundary-logging design that makes
this possible is covered in
[APIs and integrations](../engineering/02-apis-and-integrations.md).

### The permission guessing game

When access fails, five suspects exist: your code, the credential, the scope, the
network path, or the policy. Work them in order of cheapness:

- [ ] Valid credential - has the token or key expired or been rotated? Check issuance
      time first
- [ ] Correct role or scope - the identity may exist but lack the action; compare the
      granted policy with the denied action line by line
- [ ] Network reachable - egress rules, firewalls, and network boundaries block
      silently; test the path with the simplest possible call first
- [ ] Resource exists in this environment - the staging-versus-production confusion is a
      classic: config pointing at the wrong tenant, or a table in one environment and not
      the other
- [ ] Quota not exhausted - a 429 reads like a permissions failure if you only look at
      the status family

The checklist is deliberately boring: the exciting hypothesis ("their IAM is
misconfigured") is usually checked first and correct last. The auth patterns behind the
first two items are in [APIs and integrations](../engineering/02-apis-and-integrations.md);
the network and identity topology behind the middle two is in
[cloud and infrastructure](../engineering/04-cloud-and-infrastructure.md).

## Operating together

### Shared on-call reality

After launch, incidents span both organizations: your service, their data, their users,
their change process. This is a pattern of the deployment model, not a sign of a
difficult customer, so agree the triage contract before go-live:

- Who pages whom, through what channel, for which severity
- Response windows per severity, in writing - "critical means a human from each side
  responds within 30 minutes" is a contract; "urgent" is a mood
- A joint war-room channel per incident, created from a template, archived afterwards
- A single incident commander per side, so decisions have one place to happen
- A blameless but precise incident write-up both parties can share upward

The write-up matters more across organizations than inside one, because the customer's
ops lead has management of their own reading it. Facts, timeline, cause, fix, prevention
- no blame, and no omission of what each side did. The readiness phase where this
contract gets agreed is the
[production readiness checklist](../deployment/03-production-readiness-checklist.md).

## A worked scenario: wrong answers on Mondays

Clearly fictional - company, names, and numbers are invented; the shape is common.

### Situation

A fictional retailer, Northline, runs a support assistant built on a retrieval corpus of
product policies. Three weeks after launch, their ops lead reports: "the assistant gives
wrong answers on Mondays" - wrong about refund windows, occasionally about prices.
Tuesday through Friday, nobody complains.

### Constraints

The corpus pipeline is owned by Northline's data team; changes to it go through their
ticket queue. You have logs on your side of the boundary only. Monday morning is their
peak support window, so a broken assistant on Monday is politically expensive. The
nightly eval runs at 22:00 against a 60-question golden set; it passed on Sunday night.

### Move-by-move walkthrough

1. Reproduce and classify. Monday 09:00, the failing questions reproduce; the same
   questions run clean on Friday. Correlation with the calendar is itself evidence:
   something weekly. Top suspects: a scheduled job, a weekly data event, or Monday load.
2. Pull failing examples. Every wrong answer cites refund policy text that
   predates last week's policy change. The error taxonomy says stale corpus, not bad
   retrieval or model reasoning.
3. Build the timeline. Sunday 23:40, a policy-corpus refresh job ran - visible in your
   ingestion logs, which record what Northline's export delivered and when. Usual Sunday
   load: about 40,000 chunks. This Sunday: 1.4 million.
4. Boundary evidence, not blame. The refresh delivered the raw ticket dump instead of
   the curated policy extract. Your ingestion job embedded everything it was given, so
   retrieval now surfaces thousands of near-duplicate ticket fragments, older policy
   text among them.
5. Mitigate first. Restore the corpus index from the Friday snapshot, re-run the
   golden-set eval, and tell the ops lead before Monday's peak. Root cause waits;
   customers bleeding do not.
6. Root cause. A ticket with Northline's data team reveals the rest: the curated extract
   query was edited two weeks ago by an analyst "temporarily" during a source schema
   change, and nobody re-reviewed the job. The change went live with no freshness or
   content check.
7. Fix and prevent. Three changes: a freshness check that alarms when the maximum source
   timestamp is older than the expected cadence; a golden-set eval run
   scheduled after the Sunday refresh window (the current 22:00 run finishes before the
   23:40 refresh, so it never sees the damage); and a runbook entry in both
   organizations' wikis: "Monday wrong answers - check Sunday refresh volume and content
   before touching the prompt."

### Outcome

The root cause was a data contract failure at a boundary, not a model failure - which is
why prompt tuning would have made it worse, and why the eval never fired. The
general lesson: periodicity in bug reports is diagnostic evidence. Day of week, month
end, quarter end - a calendar pattern points at scheduled jobs and data cycles before it
points at code. The drift and freshness alarms that would have caught this automatically
are covered in [monitoring and reliability](../ai/04-monitoring-and-reliability.md).

## Related documents

- [A debugging methodology](01-debugging-methodology.md) - the general method; this file
  is what it looks like inside someone else's organization
- [Monitoring and reliability](../ai/04-monitoring-and-reliability.md) - drift
  detection, freshness alarms, and the observability that shortens the visibility ladder
- [Working in customer environments](../customer/03-working-in-customer-environments.md)
  - the access friction and first-week playbook behind the ladder
- [APIs and integrations](../engineering/02-apis-and-integrations.md) - boundary
  logging, contract tests, and the auth patterns referenced throughout
- [Cloud and infrastructure](../engineering/04-cloud-and-infrastructure.md) - identity,
  network paths, and environment topology behind the permission checklist
- [Production readiness checklist](../deployment/03-production-readiness-checklist.md) -
  where the shared on-call contract gets agreed before go-live

## Further reading

- [OpenTelemetry](https://opentelemetry.io) - trace context propagation, which is what
  makes "request ID X" meaningful across two organizations
