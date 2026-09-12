# From Data Engineer to FDE

Your skills map to the hardest 80% of AI deployments: getting data out of systems,
moving it, checking its quality, and landing it somewhere usable. Paul Farnsworth,
president of Dice, named the market problem in Fortune's September 2026 coverage:
companies are "struggling to turn those models into something that actually works inside
of their business, as connecting them to proprietary data, existent systems and specific
workflows can be a big roadblock to overcome" (observed evidence). That roadblock is
your home turf. What you add is the application layer above the pipelines and the
engagement arc around the work.

## What You Already Have

- SQL and data modeling - reading and querying schemas you did not design, which is most
  of what customer data work actually is
- Ingestion patterns - batch, incremental, change data capture: the plumbing that FDE
  deployments stand on and AI demos fall through
- Forensic patience - when two numbers disagree, you find out which one is lying before
  reporting either; production AI features need exactly this reflex
- Data quality instincts - you have been burned by silent nulls, stale partitions, and
  the source system that changed schema on a Friday
- Cloud infrastructure - warehousing, object storage, scheduling, IAM; `AWS` alone
  appears in 47.0% of the 146 FDE postings in the job-scrape analysis used across this
  guide (observed evidence)
- Stakeholder exposure - analysts, operations, and finance teams are already your users;
  you have taken requirements from business people and lived with the consequences

## What You Need to Learn

- The application layer - building services and APIs with `fastapi`; your pipelines feed
  systems today, and FDE work also builds the system on top (see
  [APIs and integrations](../engineering/02-apis-and-integrations.md))
- LLM patterns over your pipelines - RAG (52.0% of postings) and structured extraction,
  which are data problems wearing an AI costume (see
  [LLM application patterns](../ai/01-llm-application-patterns.md))
- Evaluation basics - golden sets and regression harnesses for AI features; your data
  testing instincts transfer faster than you expect (see
  [evaluation and testing](../ai/03-evaluation-and-testing.md))
- Discovery and requirements work - you know the data; discovery teaches you to extract
  the workflow it serves, including the spreadsheets around the system of record (see
  [discovery and requirements](../skills/02-discovery-and-requirements.md))
- The customer-engagement arc - specs, expectation management, and handover; internal
  data teams ship to colleagues, FDEs ship to customers (see
  [managing expectations](../customer/04-managing-expectations.md))

One warning from the field: the application layer will tempt you to stay in the data
layer because it is comfortable. The FDE gap for data engineers is almost never the
pipeline - it is the service, the interface, and the conversation about what the user
actually needs once the pipeline delivers. Budget your hours accordingly.

## What to Skip

- Streaming internals - how a message broker rebalances partitions rarely decides an
  engagement; know when streaming is the right pattern, not how to patch the broker
- Data-viz tool mastery - dashboards are a deliverable, not the job; build the one the
  customer needs and move on
- More orchestrator certifications - a third workflow-tool badge adds no FDE signal;
  you already prove orchestration by having run it in production
- Reverse-engineering exotic formats for fun - do it when an engagement demands it; as
  a portfolio strategy it reads as hobby, not delivery
- Building another pipeline framework - the world has enough; spend the hours on the
  application layer above instead

## Projects to Build

The theme is your data discipline underneath an AI application, in conditions messier
than any demo dataset. For twelve full specs, see
[project ideas](../portfolio/02-project-ideas.md).

### RAG over a genuinely messy corpus

Pick a corpus that is actually messy - scans, duplicates, three naming conventions,
stale versions - and build the full stack: ingestion pipeline, chunking, embedding,
retrieval, citations, plus an evaluation set of golden questions with expected answers.
It is FDE-shaped because retrieval quality is decided upstream in the data work, which
is exactly where you are strongest. It proves the union of your skills: a pipeline that
feeds a model, with evidence that the answers are right. Write down every data problem
the corpus surfaces; the list itself is evidence of the instinct this path monetizes.

### A structured extraction pipeline into a warehouse

Use an LLM to extract structured records from unstructured documents - invoices,
contracts, support tickets - landing them in a warehouse with quality checks, rejection
handling, and cost tracking per document. It is FDE-shaped because production extraction
is a data-quality problem with a model in the middle. It proves you can treat model
output with the same discipline as any upstream feed. Keep the model boring and the
checks strict; the value is in what gets rejected and why.

### The data plumbing for a real internal tool

Volunteer to build the data plumbing for an internal tool at work or for a volunteer
organization, and own the handover documentation, not just the pipeline. It is
FDE-shaped because handover is the phase data teams skip and engagements die without.
It proves you deliver for someone else's ownership, not just your own dashboard. Write
the handover for an engineer who has never met you, then test it on one.

## Suggested Path

1. Learn the application layer - wrap one of your existing pipelines in a `fastapi`
   service with auth, tests, and pagination; the shift from scheduled job to called
   service is the mental leap this path asks for
2. Add the LLM layer - structured outputs first, then RAG over the messy corpus above;
   notice how much of it is your existing discipline with new vocabulary
3. Build your first evaluation set - golden questions, expected answers, and a
   regression harness; reuse your data-testing instincts deliberately
4. Practice discovery - interview the actual users of one of your pipelines about what
   they do with the data downstream, and write a problem statement in their words
5. Run a small engagement arc - spec, build, expectation management, and handover on a
   real mini-project with a real user
6. Point your search at data-heavy FDE work - integrating models with proprietary data
   and existent systems is the named market roadblock, and verticals like finance and
   healthcare hire for exactly this profile

## Timeline

2-4 months, assuming 5-10 hours per week, an existing cloud data skillset, and a real
corpus to practice on (expert estimate). The application layer is the single biggest
lift; the engagement skills ride on stakeholder exposure you already have. Expect closer
to 2 months if your pipelines already serve an LLM feature in production, and closer to
4 if you have never built a user-facing service. Expect the messy-corpus project to
surface more data problems than model problems; that ratio is the argument for your
background, not against it. This is an estimate for focused preparation, not a
guarantee; the corpus project in particular refuses to be rushed.

## Your Advantage

Data reality checks are where AI engagements die, and you cannot be fooled by a clean
demo dataset. You ask where the data comes from, how fresh it is, who owns it, and what
happens when the source changes - the questions that surface the roadblock in week one
instead of month six. In a market where the named obstacle is connecting models to
proprietary data and existent systems (Dice, via Fortune, September 2026), the engineer
who has actually moved proprietary data is the one who gets believed in the technical
interview. Demos persuade; data lineage convinces.

## Related documents

- [Data pipelines](../engineering/03-data-pipelines.md) - your home turf, rewritten for
  customer environments
- [LLM application patterns](../ai/01-llm-application-patterns.md) - RAG and extraction
  on top of the pipelines you already build
- [Evaluation and testing](../ai/03-evaluation-and-testing.md) - the differentiator
  skill, adapted from data testing
- [Requirements to spec](../customer/02-requirements-to-spec.md) - the writing half of
  the engagement arc
- [Debugging customer systems](../troubleshooting/02-debugging-customer-systems.md) -
  where pipeline instincts meet unfamiliar environments
- [Trade-offs and decision records](../system-design/03-trade-offs-and-decision-records.md) -
  the artifact format for the architecture calls you will be making
