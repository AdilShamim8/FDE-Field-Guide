# Deployment Patterns

For the FDE deciding where a customer's system physically runs. Where the system lives
shapes everything else: security scope, latency, cost, and who can operate it at 2am.
This catalog gives four patterns that cover most engagements, the model-serving options
inside each, and the rollout strategies that get real traffic flowing without betting
the engagement on launch day.

## Where the system lives

The deployment pattern is the first architecture decision, and in customer work it is
rarely yours to make freely. It is usually decided by the customer's constraints - data
boundaries, existing cloud estate, compliance regime - before your preferences arrive.
The decision determines which security reviews apply, how much of their network policy
you inherit, what latency users feel, who pays for what, and who gets paged when it
breaks. It is also expensive to reverse once data flows exist, which is why the
constraint interview at the end of this document comes before any design work.

The four-pattern catalog below is expert interpretation, grounded in the way major FDE
organizations codify their deployment practice: Anthropic's FDE job description names
"identify and codify repeatable deployment patterns" and feeding insights back to
product and engineering as core responsibilities (greenhouse posting, 2026). Treat the
four as the recurring shapes such codification produces, not as a closed set.

## The four patterns

### Customer-tenant deployment

The shape: your stack - services, pipelines, storage - runs inside the customer's cloud
account or VPC. Data never leaves their tenant, and model inference either runs on
private endpoints inside the tenant or is excluded from the design.

When it fits: regulated customers in healthcare, finance, and defense; data-residency
requirements; security reviews that reject any external data flow.

Trade-offs: their constraints become your constraints - allowed regions, service
allowlists, tagging policies, change freezes, and their incident process. Velocity
drops; trust and auditability rise. The operational realities of building inside someone
else's estate are in
[cloud and infrastructure](../engineering/04-cloud-and-infrastructure.md).

Watch-outs: approval lead times for new service types, measured in weeks; the temptation
to ship your own parallel tooling instead of using theirs; GPU quota, which enterprises
ration by account and region. Costs shift onto their ledger - usually a political
advantage, since their budget and their tags carry it - but their procurement cycle now
governs your capacity changes.

### Vendor-hosted SaaS integration

The shape: your product runs in your cloud, and you integrate with their systems through
APIs, webhooks, and scoped credentials. Their data flows to you under contract.

When it fits: customers without heavy residency constraints, and products that are
genuinely multi-tenant SaaS. This is commonly the fastest path to first value.

Trade-offs: you operate on your own stack with your own tooling and your own on-call.
The costs are on the boundary: data-egress approvals - security review, data processing
agreements, the subprocessor list - and shared on-call boundaries where "whose alert is
this" must be answered before the first incident, not during it. The review side is in
[security and compliance](../engineering/05-security-and-compliance.md).

Watch-outs: the data boundary is contractual, not physical, so every new data type you
ingest is a new review; per-tenant isolation and rate limits become your problem at
their scale. Their feature requests also flow into your product roadmap through the
integration, which is an advantage only if your product team is listening.

### Hybrid data plane

The shape: the negotiation zone. Data stays in the tenant while compute or model calls
go out - or the reverse: payloads are anonymized, masked, or reduced before they reach
your cloud for embedding or inference, and results flow back.

When it fits: customers who accept derived data leaving the tenant but not raw data;
LLM workloads where the customer wants frontier-model quality but their policy bans raw
content in external APIs.

Trade-offs: flexible middle ground, and often the only design that satisfies both the
sponsor and the security team. But every hybrid design needs its own data-flow diagram,
threat model, and review, and the anonymization step becomes a load-bearing, tested
component - a bug there is a breach, not a bug.

Watch-outs: latency adds up across the boundary; derived data such as embeddings is
commonly treated as personal data in its own right by reviewers; the boundary you
negotiated can tighten mid-engagement when policy changes, so design the reduction step
to be re-tunable. A common variant: embeddings and retrieval run inside the tenant, and
only masked or aggregated payloads travel out for the generation step.

### On-prem and air-gapped

The shape: hardware you cannot resize, networks with no internet egress, artifact
mirrors, bastion hosts, internal registries. Every model weight, container, and
dependency is carried in through a controlled gate.

When it fits: defense, banks, healthcare, and government - environments where the
security posture forbids external calls entirely.

Trade-offs: everything takes longer. Installs, upgrades, and debugging all move at the
speed of the gate; capacity planning is physical; nobody "just adds a node" over a
weekend.

Watch-outs: verify model-serving options in week 1, because which models can be
licensed and served on their hardware determines the entire product surface; plan
artifact transfer times generously; access comes in shift windows and disappears during
holidays, so batch your changes. A model refresh that takes an afternoon in your cloud
can take a quarter of gate approvals in theirs, so schedule upgrades against their
calendar, not your release notes.

## Model serving options in customer environments

Three options cover the field:

- Hosted model API - your service calls the provider's API. Best quality, least
  operations, but every call crosses the data boundary, so it needs the data-boundary
  review - retention and training-use policies - before the first request
- VPC-private model endpoints - provider models exposed inside the customer's cloud
  account, so prompts never cross the tenant boundary while the provider still operates
  the hardware. Commonly the compromise for regulated-but-reasonable customers
- Self-hosted open-weight models - open-weight models served on customer hardware. The
  only option inside air gaps; buys full data control at the price of a serving stack,
  GPU capacity planning, and an upgrade treadmill most customer teams have never run

Decision factors, in the order that usually eliminates options: data residency first,
then cost per token at their volume, then latency budgets, then the ops maturity of
whoever will run it after handover. The LLM-side selection criteria are in
[LLM application patterns](../ai/01-llm-application-patterns.md).

## Rollout strategies

- Feature flags - every customer-facing behavior sits behind a flag you can flip
  without a deploy; the kill switch is a flag, pre-agreed, that everyone knows how to
  pull
- Shadow mode - the system runs on real traffic but does not act: outputs are logged
  and compared against what the humans did, and nobody's work depends on it
- Canary user groups - one team, then a department, then the organization; each stage
  has pre-agreed promotion criteria. Pick the canary group for workflow fit, not for
  friendliness: a group whose work the system must actually serve produces signal, and
  a group chosen for goodwill produces praise
- Staged rollout with promotion criteria - the schedule advances when the numbers say
  so, not when the calendar says so

Shadow mode deserves special attention for LLM systems: run the model alongside the
human process and compare before switching. It produces the evaluation dataset and the
trust evidence at the same time, and it is the least political rollout step because
nobody's work is at risk while it runs. The comparison methodology is in
[evaluation and testing](../ai/03-evaluation-and-testing.md).

## Choosing a pattern

Run the constraint interview before designing anything:

- Data boundaries - what may leave the tenant, in what form, to which subprocessors?
  This alone usually eliminates half the patterns
- Existing cloud estate - which cloud, which accounts, and which pre-approved vendor
  patterns already exist
- Compliance regimes - which of HIPAA, PCI DSS, FedRAMP, or GDPR apply, and what each
  constrains
- Who operates post-launch - the team's skills, on-call structure, and appetite; your
  components join someone's rotation
- Outage tolerance - whether a 4-hour outage is an inconvenience or a contractual event

In practice the customer's answers decide the pattern before your preferences arrive: a
bank with a no-egress policy has chosen on-prem for you; a startup that already buys
your SaaS has chosen vendor-hosted. Your job is to confirm the constraints in writing,
then design the best system the chosen pattern allows. The wider design process - how to
turn these constraints into an architecture the customer's team can operate - is in
[architecture for customer systems](../system-design/01-architecture-for-customer-systems.md).

## Related documents

- [Prototype to production](01-prototype-to-production.md) - the crossing these patterns serve, and why it kills pilots
- [The production readiness checklist](03-production-readiness-checklist.md) - the go/no-go gate that applies regardless of pattern
- [Cloud and infrastructure](../engineering/04-cloud-and-infrastructure.md) - landing inside their estate: accounts, identity, IaC, cost
- [Architecture for customer systems](../system-design/01-architecture-for-customer-systems.md) - designing under the constraints that chose the pattern
- [LLM application patterns](../ai/01-llm-application-patterns.md) - the model-selection criteria behind the serving options
- [Security and compliance](../engineering/05-security-and-compliance.md) - the review that decides what may cross the boundary

## Further reading

- [Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) - the codify-repeatable-deployment-patterns mandate this catalog instantiates
- [Anthropic documentation](https://docs.anthropic.com) - hosted API options and data-handling terms for the model-serving decision
- [Terraform documentation](https://terraform.io) - infrastructure as code for tenant-embedded deployments
