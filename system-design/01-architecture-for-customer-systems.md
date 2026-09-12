# Architecture for Customer Systems

For FDEs designing systems that must live inside an organization they did not build. FDE
system design is architecture under constraints you did not choose: their network, their
identity provider, their ops maturity, their compliance regime. The skill is fitting a
good system into a real organization - and our position is that the best architecture is
the one the customer's team can operate after you leave.

## The constraint inventory

Capture the constraints before designing anything. In customer work the inventory, not
the idea, determines the design:

- Cloud estate and network topology - which cloud, which accounts, VPC layout, egress
  rules, and the pre-approved patterns security already signed off once
- Identity provider and SSO reality - which IdP, whether automated provisioning exists,
  how service accounts are governed
- Data volumes and refresh - sizes, growth rates, batch windows, and what freshness
  actually means to the users
- Latency budgets - interactive versus batch, measured at their peak load, not yours
- Compliance regimes - which of HIPAA, PCI DSS, FedRAMP, or GDPR apply, and the data
  residency rules attached to them
- Ops maturity - who is on-call, what they already run, what they can realistically
  learn in the engagement window
- Change-freeze calendars - quarter-end, fiscal year, peak season; the launch date
  negotiates with these, not the other way around
- Existing vendor stack - what is already bought, under what contracts, and who
  maintains it

The raw material comes from discovery - the interview bank and shadowing method are in
[discovery and requirements](../skills/02-discovery-and-requirements.md). Two practices
make the inventory useful rather than decorative: write it as a shared, versioned
artifact the customer can correct, and date every answer, because constraint answers go
stale as reorganizations and vendor renewals land. This suggests treating the inventory
as an engagement deliverable, not a private notebook.

Two constraints deserve special caution because they surface late. Identity surprises -
no automated provisioning, manual account creation, a shared service account inherited
from the last vendor - turn launch week into account-creation week. Egress rules
discovered late invalidate model choices already built against. Ask for evidence rather
than assurances: the actual auth flow of the last integration, the written policy, the
real timeout on provisioning requests.

## Designing for the operator

Prefer boring technology - the industry phrase, and the right default. A queue the
customer's team has run for five years beats a superior queue they have never seen,
because the second one comes with a learning curve you will not be there to supervise.

- Components they already run beat components they would have to learn - matching their
  compute pattern, their secrets manager, their observability stack costs less than it
  looks and saves an argument with every reviewer
- The ops-maturity rule - every new operational concept you introduce, whether a queue,
  a cache, or a vector database, needs a named owner, a runbook, and training on the
  customer side, or it becomes shelfware
- The shelfware test - if the customer cannot name who owns a component two weeks after
  handover, the design overreached

This is the interpretation tier, but it is consistent with how FDE roles are defined:
Anthropic's FDE job description requires building production applications inside
customer systems and codifying repeatable deployment patterns (greenhouse posting,
2026). Systems that only the builder can operate do not repeat; they regenerate
consulting hours. Design for the operator the customer actually has, not the operator
you wish they had.

A concrete illustration of the ops-maturity rule: if the customer runs everything on
`Kubernetes` with a platform team behind it, your service lands there, even where a
serverless function would be cheaper; if they have never operated a message queue, the
pipeline starts as scheduled jobs and earns its queue later. Each of those choices can
look like the wrong engineering answer on paper and still be the right answer for the
organization.

## Boundaries and blast radius

Draw the trust boundaries explicitly before drawing anything else: the customer tenant,
vendor services, and the model provider, with every crossing marked. This is the same
data-flow diagram the security review will demand (see
[security and compliance](../engineering/05-security-and-compliance.md)), so draw it
once, well, and let it drive both the design and the review.

Then design for failure across those boundaries:

- External dependencies degrade, never break - when the model provider is down, the
  workflow falls back to rules, caching, or queue-and-wait; it does not become a hard
  outage of the customer's business process
- Idempotent, replayable processing as the default - every pipeline stage re-runs for
  the same input without double effects, which is what makes backfills, retries, and
  incident recovery possible at all
- Blast radius thinking - for each component, answer what the customer loses when it
  fails: one workflow, or the tenant? Keep the answer to the first wherever the
  constraints allow

Give every boundary crossing a timeout, a retry budget, and a stated fallback; the
pattern catalog is in [APIs and integrations](../engineering/02-apis-and-integrations.md).
Check each fallback against the customer's business process before promising it - a
queue-and-wait fallback assumes the process has a queue, and many do not. A fallback
nobody can operate is a failure mode with better marketing.

## The architecture conversation with the customer

Present options, not the answer. Two or three architectures with trade-offs, each on a
single page, beat one confident proposal - the customer's engineers know constraints you
do not, and a single proposal invites them to approve rather than to think. Size the
room deliberately: the sponsor decides, their engineers correct, and your job is to keep
both in the conversation. A design reviewed only by executives gets approved faster and
dies later.

The whiteboard flow that works:

1. Constraints first - replay the constraint inventory and collect corrections;
   disagreement here is cheap now and expensive after components are chosen
2. Shapes next - boxes, arrows, and where the data-boundary crossings sit, before any
   technology is named
3. Components last - only after the shape is agreed do tools enter the conversation,
   and each one arrives with its operational cost attached

A useful test inside the conversation: walk their ops lead through a failure scenario
in each option and watch which one they can imagine debugging at 2am. The option they
can narrate is usually the right one to build.

Capture every choice that had a real alternative in a decision record - the format and
the recurring trade-offs are in
[trade-offs and decision records](03-trade-offs-and-decision-records.md). Decisions that
live only in the meeting deck get re-litigated for the rest of the engagement.

## Evolution

V1 is a beachhead. Design the seams where v2 will plug in - stable interfaces between
stages, versioned APIs, an abstraction at the model boundary - without pretending to
build v2. Concretely:

- Avoid premature generality - the second system you imagine rarely arrives in the
  imagined shape, and speculative flexibility is paid for in every review and every
  incident until then
- Keep the seams honest - a versioned interface between ingestion and processing costs
  a day and buys the ability to replace either side; a "pluggable everything" framework
  costs a quarter and buys complexity
- Expect drift between the diagram and reality, and update the diagram - the customer's
  operators inherit both

A practical seam inventory for LLM systems has three entries: the model boundary, where
provider and model are swappable; the retrieval boundary, where corpus and store are
swappable; and the integration boundary, where their systems are swappable. Version all
three and the v2 conversation becomes a component swap instead of a project.

Beware the rewrite temptation. Integrations that work age better than rewrites: the
running system accumulates the customer's trust, edge cases, and data history, and a
rewrite resets all three to zero. Working inside customer environments teaches the same
lesson at the ground level - integrate before you rewrite (see
[working in customer environments](../customer/03-working-in-customer-environments.md)).
If the seams themselves are wrong - rarely, but it happens - make that case in a
decision record with the evidence, not in a hallway.

## Related documents

- [Reference architectures](02-reference-architectures.md) - four starting shapes to adapt into the constraints you inventoried
- [Trade-offs and decision records](03-trade-offs-and-decision-records.md) - how the choices made in the architecture conversation get captured
- [Discovery and requirements](../skills/02-discovery-and-requirements.md) - where the constraint inventory comes from
- [Cloud and infrastructure](../engineering/04-cloud-and-infrastructure.md) - the estate-level realities behind the constraints
- [Working in customer environments](../customer/03-working-in-customer-environments.md) - the ground truth that keeps designs honest
- [The engagement lifecycle](../customer/01-engagement-lifecycle.md) - the phase 5 gate: a plan the customer's ops team believes

## Further reading

- [Chip Huyen's writing](https://huyenchip.com) - the GenAI platform design posts; a useful mirror for platform-level architecture choices
- [Site Reliability Engineering](https://sre.google) - Google's SRE book; the operational discipline "designing for the operator" points at
