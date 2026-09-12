# The Production Readiness Checklist

For the engagement lead running the go/no-go review before any customer system takes
live traffic. Every item is a question with a yes or a no, and every "no" is either
fixed, waived in writing by the accountable owner, or it blocks launch. We recommend
running this as a scheduled review two to three weeks before the target date, so there
is time to fix what it finds.

## How to use this checklist

The waiver rule: every unchecked item needs an owner and a date, or a written waiver
from the accountable owner on the customer side. Launch is a decision, not a hope. A
waived item is not a hidden one - the waiver names the risk, the owner accepting it, and
when it will be revisited. We recommend pasting the checklist into the launch ticket and
resolving items inline, so the decision trail survives the launch.

Check against the spec, not against memory: the thresholds are the ones signed in
`requirements.md`, and the review's job is to verify the system matches them. The
readiness review sits in phase 9 of the
[engagement lifecycle](../customer/01-engagement-lifecycle.md); this checklist is what
that review runs.

## The checklist

### Data

- [ ] Data refresh runs on schedule in production, unattended
- [ ] Backfills complete, with historical data validated against source counts
- [ ] PII scoping verified: what is read, stored, logged, and sent externally matches the spec
- [ ] Schema drift alarm exists, and a named person receives it
- [ ] Target volumes reconcile with the source: row and document counts checked after load

### Quality

- [ ] Eval thresholds met on the golden set, measured by the agreed method
- [ ] Error taxonomy reviewed with the customer, with known failure classes named
- [ ] Known-limitations list shared with users and support before launch

The quality bar is whatever the spec says it is; the measurement methodology lives in
[evaluation and testing](../ai/03-evaluation-and-testing.md).

### Access and security

- [ ] SSO and user provisioning done end to end, with a test account from each user group
- [ ] Service identities least-privilege; no shared human credentials anywhere
- [ ] Secrets live in the customer's secrets manager; none in code, config files, tickets, or chat
- [ ] Security review passed, or waived in writing with conditions; the review's demands are in
  [security and compliance](../engineering/05-security-and-compliance.md)

### Operations

- [ ] Dashboards live, showing what the runbook says they show
- [ ] Alerts routed to a named on-call, with response expectations agreed
- [ ] Runbook written and rehearsed by someone who did not build the system
- [ ] Rollback tested - actually executed in a non-production environment, not theoretically possible
- [ ] Kill switch tested: flipping it demonstrably stops the system, and flipping it back works
- [ ] Monitoring covers the probabilistic failure modes - drift, quality regressions, cost - not
  just uptime; see [monitoring and reliability](../ai/04-monitoring-and-reliability.md)

### Support

- [ ] Support path agreed: who calls whom, for what, with what response times
- [ ] Escalation contacts named on both sides, with backups
- [ ] Incident comms template exists, and the sponsor has seen it before the first incident;
  the comms patterns are in [managing expectations](../customer/04-managing-expectations.md)

### Cost and capacity

- [ ] Budget approved by the person who owns it
- [ ] Spend alerts set at fractions of the budget, routed to someone who can act
- [ ] Load estimate compared against reality: peak traffic modeled, and at least one test at
  scaled load
- [ ] Unit cost per workload inside the ceiling stated in the spec, measured on pilot traffic

### Ownership

- [ ] Post-launch owner named on the customer side for every component
- [ ] Support boundaries signed by both sides - who calls whom, for what, when
- [ ] Handover date agreed, with the unaided-operation window defined
- [ ] The customer-side owner has accepted the role in writing, not by silence

## Launch day

A short runbook for the day itself.

Who is in the room: the FDE, the customer-side owner, the on-call for the first week,
and a sponsor who is reachable but not watching over shoulders. Too many observers turns
an incident into a performance.

What is watched: traffic and error rates, latency percentiles, queue depth, model-call
success rate and cost per hour, and the support inbox - one dashboard, on a screen
everyone can see.

First-hour checks, in order:

1. Smoke-test the primary path end to end with a production-shaped request
2. Verify alert routing by firing a test alert and confirming a human receives it
3. Confirm the data refresh ran, or the ingest queue is draining
4. Check cost metering is actually reporting - billing surprises should happen in hour
   one, not month one
5. Post the first status note even if nothing has happened, because silence reads as
   concealment

The rollback trigger is agreed in advance and written where everyone can see it: the
condition under which the kill switch gets pulled - for example, error rate above the
agreed threshold for the agreed duration, or any data-boundary violation, which is
automatic and carries no debate. Rehearse who pulls it. The rollout mechanics behind
the switch are in [deployment patterns](02-deployment-patterns.md).

Keep a smaller version of the room booked for the first week: a daily 15-minute check on
the same dashboard, until the numbers and the support inbox are boring. Boring is the
launch goal.

## Related documents

- [Prototype to production](01-prototype-to-production.md) - the plan this checklist gates
- [Deployment patterns](02-deployment-patterns.md) - the rollout mechanics, flags, and kill switch the checklist assumes
- [Monitoring and reliability](../ai/04-monitoring-and-reliability.md) - what "dashboards live" and "alerts routed" mean in detail
- [Security and compliance](../engineering/05-security-and-compliance.md) - the review behind the access and security group
- [The engagement lifecycle](../customer/01-engagement-lifecycle.md) - where the readiness review sits (phase 9) and what follows it
- [Managing expectations](../customer/04-managing-expectations.md) - the support and incident-comms conversations this checklist forces

## Further reading

- [Site Reliability Engineering](https://sre.google) - Google's SRE book; production readiness reviews and runbooks as formal practice
- [Prometheus documentation](https://prometheus.io) - alerting and dashboarding basics for the operations items
