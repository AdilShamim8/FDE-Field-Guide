# Reference Architectures for FDE Work

For FDEs who need a starting shape, not a blank page. Most engagements fit one of four
repeatable architectures, given here with diagrams, fit criteria, components, trade-offs,
and operational notes. Treat them as starting points to adapt to the customer's
constraints - not answers to paste.

## How to use these shapes

Three rules before the diagrams:

- Adapt, do not adopt - run the constraint inventory first (see
  [architecture for customer systems](01-architecture-for-customer-systems.md)); the
  shape is the last thing you choose, not the first
- The deployment pattern decides where it lands - the same logical architecture can be
  tenant-embedded, SaaS, hybrid, or air-gapped (see
  [deployment patterns](../deployment/02-deployment-patterns.md))
- Every shape inherits the same operational spine - monitoring, secrets, and config are
  covered once in the cross-cutting notes, not per diagram

The shapes are deliberately boring: queues, stores, services, and human gates, arranged
so each part can fail and be replaced alone. Novelty belongs in the model behavior, not
in the scaffolding around it.

## The four shapes

### Document intelligence pipeline

Ingest, parse, embed, retrieve, extract - the shape behind most document work.

```
sources (SharePoint, S3, email, exports)
        |
        v
  ingest queue --> parse and chunk --> embed --> vector store
        |                                           ^
        v                                           |
  failure queue                                     |
                                                    |
user query --> retrieve top-k --> llm with grounding and output schema
                                                    |
                                                    v
                                    structured output --> review UI
                                                    |
                                                    v
                                            downstream systems
```

- Fits - extraction, classification, and retrieval over document corpora: contracts,
  claims, filings, policies
- Components - ingest queue, parser, chunker, embedding step, vector store
  (`pgvector` or a dedicated store), retrieval service, LLM call with an output schema,
  review UI
- Trade-offs - chunking quality dominates outcomes, more than model choice does; a
  corpus that needs current answers requires an incremental per-document pipeline, not
  periodic full rebuilds
- Operational notes - route unparseable documents to a failure queue with a human
  path; keep per-document lineage (source, version, chunk set) so a bad parse or a
  model change can be purged and re-embedded in place

In practice, parsing is where the schedule goes: PDFs with tables, scans that need OCR,
and format drift between sources each consume days that chunking experiments do not.
Budget integration time for the parser accordingly, and evaluate retrieval and
extraction separately - a bad answer can be a retrieval miss or a chunking fault, and
the fixes differ. Freshness is an architecture property, not a feature: decide the
delete-and-reinsert path per document before the corpus grows, not after the customer
asks why yesterday's policy change is not in the answers.

### Customer-facing assistant (RAG chat)

Grounded question answering over a curated corpus, with citations.

```
user --> app service --> guardrails --> retrieval over curated corpus
                                           (metadata filters: team, locale)
                                                |
                                                v
                                     llm with grounding context
                                                |
                                                v
                                  response with citations --> user

feedback capture (ratings, reasons) --> weekly curation review
```

- Fits - support assistants and internal knowledge assistants over a corpus someone
  owns: help centers, runbooks, policy documents
- Components - app service, input and output guardrails, retrieval with metadata
  filters, LLM with grounding context, citations in the response, feedback capture
- Trade-offs - corpus curation is the real work: assistants fail because the corpus is
  stale, duplicated, or self-contradictory, not because retrieval is slow; grounding
  evaluation - how often the answer is supported by its cited sources - is the launch
  gate, and the method is in [evaluation and testing](../ai/03-evaluation-and-testing.md)
- Operational notes - guardrails cover both directions: input filtering against prompt
  injection (untrusted text is in the corpus too) and output filtering before send; the
  feedback loop must route to a person with time to act on it weekly, or it becomes a
  dashboard nobody reads

Cache what repeats: retrieval results for common questions, and full answers where a
staleness budget allows it, cut cost and latency at the same time. Ship the citation UX
early - users trust an assistant they can check - and treat "no supporting source" as a
designed answer rather than an error: telling the user the corpus does not cover it is
both the honest failure mode and the cheap one.

### Agentic workflow with human gates

A model-driven worker with scoped tools, wrapped in deterministic scaffolding.

```
task queue --> agent loop (scoped tools, step and cost budget)
                   |
                   +--> low-risk action ------> execute
                   |                               |
                   +--> risky action ------> approval gate --> human decision
                                                                      |
                                                                      v
                                                                  execute
                   |
                   +-------------> audit log (every proposed and executed action)
```

- Fits - operations automation with accountability: refunds, ticket resolution,
  provisioning, anything an auditor will ask about
- Components - task queue, agent with per-tool permissions, policy layer that decides
  what needs human approval, approval gate, audit log, step and cost budgets
- Trade-offs - agents multiply model calls, so cost per task needs a budget; permission
  scoping is the security conversation, especially the "what may the agent's database
  user do" question (see
  [security and compliance](../engineering/05-security-and-compliance.md)); evaluation
  must judge trajectories, not just final outcomes
- Operational notes - deterministic scaffolding around model decisions: the model
  proposes, the scaffolding validates against schemas and allowlists, then executes;
  every action must be replayable from the audit log alone. The agent-building detail
  is in [agents and tools](../ai/02-agents-and-tools.md)

Budgets are commonly expressed as a maximum step count and a maximum cost per task
(industry pattern); when either trips, the workflow hands the task back to a human with
the trajectory attached. Keep the tool surface small and named - every tool is an audit
line item and a review question - and log a reasoning summary alongside actions so a
reviewer can reconstruct why, within the customer's log-content rules.

### Batch enrichment and the data plane

Model calls as a warehouse-shaped workload, at volume.

```
source systems --> CDC or scheduled pulls --> staging tables
                                                    |
                                                    v
                                llm enrichment (structured output,
                                                cache keyed on input hash)
                                                    |
                                                    v
                                warehouse and targets --> dashboards
```

- Fits - back-office enrichment at volume: lead scoring, product classification,
  summarization across a table of records
- Components - change data capture or scheduled pulls, staging tables, enrichment step
  with structured output validation and a cache, warehouse targets, dashboards
- Trade-offs - idempotency is the design center: re-running a batch must not double
  effects or double spend; cost per record decides margins, so cache aggressively and
  route easy rows to smaller models; backfill strategy needs an answer before launch -
  when the prompt or model changes, re-enrich everything or only new rows, and version
  the outputs either way
- Operational notes - every output row carries model version and prompt version; state
  freshness expectations explicitly ("this is yesterday's data, by design") so nobody
  mistakes a batch shape for a broken real-time one. The ingestion patterns are in
  [data pipelines](../engineering/03-data-pipelines.md)

Watermark the pulls so an interrupted run resumes instead of repeating, and park
enrichment failures in a dead-letter table with the provider error attached - silent
drops are how backlogs become mysteries. Cost per record is measurable from day one;
publish it on the dashboard, because it is the number that decides whether the
enrichment survives the next budget cycle.

## Cross-cutting notes

Five things are true of every shape above:

- Monitoring, secrets, and config live outside the shapes - metrics and traces go to
  the customer's existing stack (`Prometheus` and `Grafana` or their equivalent), secrets
  come from their manager at runtime, and config differs per environment without code
  changes; the details are in
  [monitoring and reliability](../ai/04-monitoring-and-reliability.md)
- Each shape maps to deployment patterns - document pipelines and batch enrichment are
  commonly customer-tenant or hybrid, because they touch raw data; assistants run in
  any pattern depending on what the corpus contains; agents depend entirely on what
  their tools may touch
- Air-gapping changes specific components, not the shapes - hosted model calls become
  self-hosted open-weight serving, artifact mirrors replace registries, evaluation runs
  offline on customer hardware, and any step assuming internet egress (web-search tools,
  hosted rerankers) must be replaced or dropped
- The review UI is not optional - in all four shapes a human-facing surface for
  spot-checking outputs is the cheapest quality and trust instrument you can build
- The diagram is a contract - when the shape lands in their environment it gets
  redrawn with their components; treat that redraw as a design review and keep the
  diagram and the running system the same artifact by updating it at every change

## Related documents

- [Architecture for customer systems](01-architecture-for-customer-systems.md) - how to adapt these shapes to the constraint inventory
- [Deployment patterns](../deployment/02-deployment-patterns.md) - where each shape physically lands: tenant, SaaS, hybrid, air-gapped
- [LLM application patterns](../ai/01-llm-application-patterns.md) - the pattern catalog behind the LLM components in each shape
- [Evaluation and testing](../ai/03-evaluation-and-testing.md) - the launch gates each shape has to pass
- [Data pipelines](../engineering/03-data-pipelines.md) - the ingestion and quality layer most shapes stand on
- [Trade-offs and decision records](03-trade-offs-and-decision-records.md) - recording the adaptations you made and why

## Further reading

- [pgvector](https://github.com/pgvector/pgvector) - vector search inside `PostgreSQL`; the lowest-ops vector store for estates that already run it
- [Qdrant documentation](https://qdrant.tech) - a dedicated vector store option for the retrieval shapes
- [Anthropic documentation](https://docs.anthropic.com) - model APIs and tool use behind the LLM steps in these shapes
