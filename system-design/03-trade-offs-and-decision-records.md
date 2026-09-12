# Trade-offs and Decision Records

For FDEs making architecture decisions that must survive scrutiny - by the customer's
security team, by your own product team, and by whoever inherits the system. Customer
engagements accumulate decisions that outlive the meeting where they were made; decision
records make them legible, reviewable, and reversible. The format adapts the industry
architecture-decision-record practice to the engagement context.

## The decision record format

Use this template, one record per decision, in the shared engagement repo:

```
Decision record - <ID> - <title> - <date>

Status - proposed, accepted, or superseded by <ID>

Context - the constraint that forced the choice: what the customer's
environment, policy, deadline, or data ruled out, and where that
evidence came from.

Decision - what we will do, in one sentence, then the specifics.

Consequences - what this costs, what we gave up, what becomes harder,
and who inherits the burden.

Revisit - the date or trigger that reopens this decision, and what
would change our mind.
```

The field people skip is the field that matters. A decision without consequences is a
press release: "consequences" is where you write down what you gave up, which is
exactly what a reviewer - or an auditor, or your successor - reads to check whether the
decision was made with open eyes. It is also the field that prevents the quiet rehash:
when someone proposes the rejected option three weeks later, the consequences section is
where the conversation starts instead of from zero.

Keep records short. If a record needs two pages, the decision inside it is probably
three decisions, and each deserves its own record with its own revisit date.

## The recurring FDE trade-offs

Seven decisions almost every engagement hits. Each is written here the way it should
appear in a record: the tension, the signal that tips it, and the framing worth
recording.

### Build or buy inside the customer estate

The tension: building gives control and fits the constraint; buying gives speed and
someone else's roadmap - and inside a customer estate, anything you build also becomes
something they must maintain after handover. Build when the capability is the point of
the engagement and no vendor fits the data boundary; buy when the capability is
commodity and the customer's team cannot absorb another component to operate. Record
the ownership consequence either way: "we build the parser in-tenant because no vendor
meets the residency constraint; the customer's data team accepts ownership of it from
handover."

### Hosted model API or self-hosted serving

The tension: hosted APIs buy frontier quality with no serving operations; self-hosting
buys data control and predictable unit economics at the price of a serving stack, GPU
capacity, and an upgrade treadmill. Host externally when the data boundary allows it
and quality differences are material; self-host under air gaps, residency rules, or at
volumes where per-token pricing distorts the business case. Record the data-boundary
evidence, the cost per unit at the customer's stated volume, and who operates serving
after handover - the last point is where this decision usually fails.

### Their stack or your stack

The tension: adapting to their queue, database, and observability lowers operational
risk but is slower and constrains the design; introducing your own is faster to build
but adds a component they must run and a reviewer must approve. Adapt when the "their"
component runs in production with a named team behind it; introduce when the gap is
real and nothing on their side owns the need. Record every introduced component with
its post-handover owner by name - a component with no owner is a defect in the design,
not a detail.

### Event-driven or batch

The tension: event-driven buys freshness and decoupling at the price of infrastructure
and harder debugging; batch buys simplicity, replayability, and cheap recovery at the
price of staleness. Go event-driven when users act on updates within minutes and the
trigger is a real business event; go batch when hours of staleness are acceptable and
the workflow is reconciliation-shaped. Record the freshness requirement from the spec
and the accepted failure mode - late data or lost events - because they are different
incidents with different on-call behavior.

### Real-time or cached

The tension: real-time answers are fresh but pay per request in latency and model cost;
cached answers are instant and cheap but respond to a world that has moved on. Cache
when queries repeat and a staleness budget exists; go real-time when freshness or
personalization is the product. Record the staleness budget - how old an answer may be
- and the assumed hit rate, which is the number the cost model quietly depends on.

### One tenant-wide system or pilot-group-first

The tension: tenant-wide launch captures value now but bets everything on launch
quality; pilot-group-first spends weeks to buy evidence and champions. Choose
pilot-first when the quality bar is unproven, the workflow change is large, or the
operator base is skeptical; go tenant-wide when shadow-mode evidence exists and the
workflow is additive rather than replacing. Record the promotion criteria between
stages - the [rollout strategies](../deployment/02-deployment-patterns.md) and the
evaluation gates in
[evaluation and testing](../ai/03-evaluation-and-testing.md) define what "promoted"
means, so the launch cannot drift on enthusiasm.

### Cheapest model with evals or best model by default

The tension: the best model by default maximizes quality per request and cost; the
cheapest model behind evaluations maximizes margin and forces the eval discipline the
engagement needs anyway. Start cheap when the task is narrow, measurable, and high
volume; default to the strongest model when the task is long-tail, eval coverage is
weak, or errors are expensive in customer trust. Record the eval set that gates the
cheap model, the fallback path when it fails in production, and the cost-per-unit
difference at their volume - that last number is what the sponsor actually decides on.

## Writing trade-offs for the customer

Translate the trade into their vocabulary: risk, cost, time, compliance. Throughput and
percentiles are engineer vocabulary; the sponsor decides on "this option keeps all data
inside the tenant but adds two weeks and a component your team will operate". Every
option in the memo should be expressible in those four currencies, or it is not yet a
real option.

The one-page decision memo, for decisions that need customer sign-off:

- Context - three lines: the constraint, the deadline, the evidence
- Options - one paragraph each, stated in risk, cost, time, and compliance terms
- Recommendation - one sentence, and what you would watch that would prove it wrong
- Consequences - what each party gives up and who owns what afterwards
- Sign-off - named individuals and dates

Who signs off: the accountable owner on the customer side - the person whose budget,
risk, or compliance exposure the decision touches - plus your engagement lead. Where it
lives: the engagement repo, versioned alongside the spec, with the same discipline as
`requirements.md` (see
[from requirements to spec](../customer/02-requirements-to-spec.md)). An unversioned
decision record is a rumor with formatting.

## Reversibility

Classify decisions when you write them, using the one-way and two-way door distinction
the industry borrowed from Amazon's decision-making practice. Two-way doors - model
choice behind an abstraction, feature flags, a caching layer - can be made quickly and
revisited cheaply; give them a short record and a fast decision. One-way doors - the
data model, the deployment pattern, a tenant-wide rollout - get the full record, a slow
decision, and the accountable owner's signature.

The revisit date is a feature, not an admission of doubt. Writing "we re-decide this on
evidence at this date" makes the decision easier to accept now, because it tells the
people who disagreed that the door is not welded shut. Recording what would change your
mind - a cheaper model passing the golden set for four consecutive weeks, a vendor
finally meeting the data boundary - turns the record into a standing offer, and gives
the next engagement a head start on the same decision.

## Related documents

- [Architecture for customer systems](01-architecture-for-customer-systems.md) - the design context these decisions emerge from
- [Reference architectures](02-reference-architectures.md) - the shapes the trade-offs modify
- [From requirements to spec](../customer/02-requirements-to-spec.md) - where decisions are versioned and signed alongside the spec
- [Communication and storytelling](../skills/03-communication-and-storytelling.md) - presenting the technical narrative the records feed
- [Managing expectations](../customer/04-managing-expectations.md) - saying no with a documented, dated reason

## Further reading

- [Chip Huyen's writing](https://huyenchip.com) - platform and model-choice trade-off analysis that maps well onto the hosted-versus-self-hosted decision
