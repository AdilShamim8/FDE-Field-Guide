# LLM Application Patterns

For engineers deciding how to solve a customer problem with an LLM. This is the pattern
catalog: the seven shapes most FDE deployments take, when to reach for each, and how each
one fails. The vocabulary is confirmed by hiring data - prompt engineering appears in
55.0% of FDE postings, RAG in 52.0%, LLMs in 43.0% (146 postings scraped February-July
2026, [independent job-scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)).
Knowing the catalog - and the failure mode of each pattern - is the difference between a
designed system and an improvised one.

## The pattern catalog

Seven patterns cover most engagements. Pick by task shape and operating cost, not by
novelty. Most customer systems combine two or three: extraction feeding a workflow,
retrieval feeding a chat surface, classification feeding a queue.

### Single-shot extraction

Document or text in, structured fields out: invoice totals from PDFs, parties and dates
from contracts, entities and actions from tickets. This is the highest-ROI enterprise
pattern because it maps onto a measurable manual task - data entry, triage prep, records
coding - and the baseline you compete against is a human's error rate and time, both of
which are easy to measure and easy to beat. The classic failure is silent hallucination:
the model fills a plausible-looking date or ID for a field it cannot find instead of
returning nothing. We recommend treating "not found" as a first-class output and
validating field formats against the source.

### Structured output

The contract that makes any LLM output usable downstream: constrain the model to a schema
(provider JSON modes or constrained decoding), then validate the result with `pydantic`
at the boundary, retrying once with the validation error attached if the first attempt
fails. Reach for it in every pattern where code consumes the output - extraction,
routing, tool arguments. The failure mode is validation as an afterthought: the parse
succeeds but the semantics fail, because the model returned a real-looking string where
the business needs one of three allowed values, or a date outside the ledger's range.
Validate schema and semantics: enums, ranges, cross-field rules. The general
boundary-validation discipline for integrations is in
[APIs and integrations](../engineering/02-apis-and-integrations.md).

### Classification and routing

Labels, sentiment, urgency, queue routing. Usually the cheapest pattern - a small model
at low latency handles high volume - and often the first one a customer accepts, because
"suggestions with override" is a low-risk rollout. The failure mode is threshold drift
across categories: overall accuracy looks healthy while one rare, expensive class quietly
degrades - escalation-grade tickets routed to the general queue for weeks. We recommend
per-class metrics and a standing review of confusion on the expensive class, rather than
a single accuracy number; the measurement detail is in
[evaluation and testing](03-evaluation-and-testing.md).

### Retrieval-augmented generation

RAG grounds answers in a customer corpus: chunk documents, embed the chunks, store the
vectors (`pgvector` inside the Postgres they already run, or dedicated stores such as
`qdrant`, `weaviate`, or `pinecone`), retrieve the top matches at question time, and
generate an answer with citations. Reach for it when answers must reflect documents you
will not retrain on - policies, contracts, wikis, manuals. It fails three ways: retrieval
misses, where the right chunk never reaches the model; stale corpora, where yesterday's
policy is quoted with full confidence; and bad chunks, where fluency turns wrong source
material into confident nonsense. Evaluate retrieval separately from generation, and put
the index freshness guarantee in writing - the pipeline side is covered in
[data pipelines](../engineering/03-data-pipelines.md).

### Summarization and drafting

Meetings into minutes, ticket threads into handover notes, long reports into briefs,
first drafts of replies. Reach for it when a human consumes and edits the output: the
tolerance for imperfection is high and the volume savings are real. The failure mode is
missing the point: a summary that is fluent and well-toned but omits the one decision the
meeting actually made, or a draft whose tone drifts away from the customer's voice over
weeks. Judge summarization by how little the human edits, not by how good the text
sounds, and keep a human in the loop for anything outbound.

### Conversation with memory

Support assistants and copilots: multi-turn state built from conversation history,
rolling summaries, and retrieved context. Reach for it when user problems are
follow-up-shaped - clarifications, iterations, partial information - and deflection of
routine tickets is worth the operating cost. The failure modes are context bloat and cost
creep: history accumulates, so latency and cost per turn grow over a session, and long
contexts degrade answer quality (see context engineering below). We recommend summarizing
or windowing old turns rather than appending everything, and budgeting sessions by turn
count and token count.

### Agentic workflows

The model decides which tools to call and iterates until the task is done: research,
reconciliation, multi-system actions. The most powerful pattern in the catalog, and the
most expensive to run, evaluate, and secure - it gets its own document:
[agents and tools](02-agents-and-tools.md).

## Context engineering

Over the life of an engagement, what goes into the context window matters more than how
the prompt is phrased. Prompts stabilize in week 2; context construction is where quality
is won and lost - and where the cost lives. A well-built context contains:

- Compact instructions - short, stable task directions, versioned like code, not a wiki
  pasted into every call
- Relevant retrieval - the few chunks that answer the question, not the top count the
  config happens to specify
- Structured context blocks - instructions, retrieved data, and conversation history in
  clearly separated, labeled sections, so the model can tell commands from material
- Only the state the task needs - the current turn plus what it references, not the full
  transcript by default

The reason for the discipline is context rot: answer quality degrades as inputs grow, so
stuffing everything into the window costs money, latency, and accuracy at the same time.
This is expert interpretation, but it matches most teams' production experience and
provider guidance ([Anthropic documentation](https://docs.anthropic.com),
[OpenAI documentation](https://platform.openai.com/docs)). We recommend treating context
construction as code: versioned, reviewed, and measured against the evaluation set like
any other change.

## Choosing a pattern for a customer problem

Work the questions in order and stop at the first pattern that fits:

1. Can part of the task be solved without a model - SQL, regex, rules, the customer's
   existing system? Do that part without a model; a model in a deterministic loop adds
   cost and variance and nothing else.
2. Is the task text or documents to structured fields? Single-shot extraction with
   structured output.
3. Is the task putting inputs into buckets or queues? Classification and routing.
4. Do answers need knowledge that lives in customer documents? Retrieval-augmented
   generation.
5. Is the output text for a human to edit? Summarization or drafting.
6. Does the task need actions across systems, with branching decisions? Only now:
   agents.

Two rules govern the choice. Start with the simplest pattern that could work, and upgrade
only when evaluation proves the need - a working extractor that misses 5% of fields is a
better system than a half-evaluated agent that misses 5% of tasks differently (see
[evaluation and testing](03-evaluation-and-testing.md)). And remember that operating cost
climbs steeply up the ladder: a classification call and an agent run differ by orders of
magnitude in latency, cost per task, and failure surface. Most "we need agents"
conversations we have seen resolve into "we need extraction plus a workflow engine" once
someone draws the actual branching.

## Model selection in customer environments

In customer environments, constraints bind before quality does: a model that cannot be
deployed is not a candidate, whatever the benchmark says. The constraints that usually
decide the shortlist:

- Data residency - data must stay in a region or jurisdiction; this rules out providers
  and serving regions outright
- Private networking - traffic must not traverse the public internet: VPC endpoints,
  private connectivity, or on-premises serving
- Cost ceilings - a cap per ticket or per query at the customer's volume; a brilliant
  model at the wrong price is a failed project
- Latency budgets - interactive routing needs hundreds of milliseconds; overnight batch
  coding can wait minutes
- Compliance regimes - healthcare, payments, and government work narrow the field before
  anyone discusses quality (see
  [security and compliance](../engineering/05-security-and-compliance.md))

The process we recommend: shortlist by constraints first, then evaluate quality on the
golden dataset. Compare by tier, not by name - frontier models for hard reasoning,
mid-size models for most production work, small models for high-volume classification and
extraction - because named models age fast and the tiers survive provider churn. Pin the
model version once chosen, and treat any provider upgrade as a change to be evaluated,
not an automatic improvement; the operating side of that is in
[monitoring and reliability](04-monitoring-and-reliability.md).

## Related documents

- [Agents and tools](02-agents-and-tools.md) - the agentic pattern in full: loops, tool design, MCP, guardrails
- [Evaluation and testing](03-evaluation-and-testing.md) - how you prove the chosen pattern meets the bar
- [Monitoring and reliability](04-monitoring-and-reliability.md) - operating the pattern after launch, including model upgrades
- [Data pipelines](../engineering/03-data-pipelines.md) - the corpus, vector branch, and freshness guarantees RAG depends on
- [Security and compliance](../engineering/05-security-and-compliance.md) - the data boundaries that constrain pattern and model choice
- [Reference architectures](../system-design/02-reference-architectures.md) - how these patterns compose into deployable customer architectures

## Further reading

- [Anthropic documentation](https://docs.anthropic.com) - structured outputs, tool use, embeddings, and context windows, framework-free
- [OpenAI platform documentation](https://platform.openai.com/docs) - structured outputs and function calling references
- [pgvector](https://github.com/pgvector/pgvector) - vectors inside the Postgres the customer already runs
- [Qdrant](https://qdrant.tech) - dedicated vector store for corpora that outgrow the database
- [Weaviate](https://weaviate.io) - vector database with hybrid search support
