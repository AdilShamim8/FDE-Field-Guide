# Core Technical Skills

This document is for engineers deciding what to learn for forward deployed engineering,
and for working FDEs checking where their stack is thin. You get three things: the skill
stack weighted by evidence from real job postings, a calibration of how deep each skill
actually needs to go, and a self-audit that maps every gap to a document in this guide.

## The stack employers ask for

The strongest available evidence on what FDE employers want is an independent job-scrape
analysis of 146 unique FDE postings from 94 companies, collected between February and July
2026 ([the analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)).
Skill mentions across those postings:

- `Python` - 133 postings (91.0%)
- Prompt engineering - 80 postings (55.0%)
- RAG - 76 postings (52.0%)
- `AWS` - 69 postings (47.0%)
- LLMs - 63 postings (43.0%)
- AI agents - 61 postings (42.0%)
- `Docker` - 58 postings (40.0%)
- `GCP` - 55 postings (38.0%)
- `Kubernetes` - 51 postings (35.0%)
- `Azure` - 50 postings (34.0%)
- CI/CD - 50 postings (34.0%)
- `LangChain` - 48 postings (33.0%)

Percentages sum past 100% because postings list many skills. Counts are the nearest whole
posting to each reported percentage.

## How to read the stack

Three observations matter more than the raw ordering.

First, applied AI skills and classic delivery skills appear together. Python sits next to
Docker, three clouds, and CI/CD; prompt engineering sits a few points above Kubernetes.
This suggests employers are not hiring researchers or prompt hobbyists. They are hiring
engineers who can ship a containerized service into an environment they did not set up,
with the AI part expected on top.

Second, the three cloud numbers sit within 13 points of each other (AWS 47.0%, GCP 38.0%,
Azure 34.0%). You cannot assume the customer's stack. FDEs deploy into whatever already
exists, which is close to the definition of the job. Depth in one cloud plus reading
fluency in the other two is worth more than shallow familiarity with all three.

Third, `LangChain` at 33.0% tells you frameworks matter less than fundamentals. Two thirds
of postings name no framework at all. Learn the concepts frameworks wrap - retrieval, tool
calling, structured output, context limits - and you can pick up whichever framework the
customer already uses in about a week.

## Baseline versus differentiators

We recommend treating the stack as two tiers.

The baseline gets you considered. It is table stakes by the middle of any FDE interview
loop:

- Python - production packaging, testing, and typing, not notebook scripting
- One cloud, well - deploy a containerized service end to end, including networking and IAM basics
- `Docker` - build images, debug containers, glue a local stack together with `docker compose`
- Git and CI/CD - branch discipline, PR review, and a pipeline you did not have to invent
- SQL - real queries against schemas you did not design
- REST APIs - consuming, designing, and debugging them
- LLM API fundamentals - structured outputs, function calling, embeddings, context limits, cost per token

The differentiators get you picked. Postings list them less consistently, but interviews
and the first ninety days of the job test them hard:

- Evaluation discipline - proving a probabilistic feature works, to a skeptical customer (see [evaluation and testing](../ai/03-evaluation-and-testing.md))
- Integration craft - working against APIs and data systems you do not own (see [APIs and integrations](../engineering/02-apis-and-integrations.md))
- Debugging under pressure - finding root causes in an environment where you cannot read every line (see [debugging methodology](../troubleshooting/01-debugging-methodology.md))
- Security review literacy - answering a customer security questionnaire without guessing (see [security and compliance](../engineering/05-security-and-compliance.md))
- Technical writing - specs, decision records, and status updates a stranger can act on

The pattern: the baseline is about building, the differentiators are about building inside
someone else's organization. That is the FDE difference, and it is why the rest of this
guide spends so much time on the second tier.

## How deep each skill needs to go

Postings do not tell you depth. Here is the calibration we recommend for FDE work.

### Python

Production-grade: packaging with `pyproject.toml`, tests with `pytest`, type hints, config
and secret handling, and structured logging. FDE code often becomes the customer's code
after handover, so it has to survive their review. Notebook skills alone do not clear the
91.0% bar.

### SQL

Beyond `SELECT` and `JOIN`: window functions, CTEs, reading a query plan, and walking into
an unfamiliar schema and finding your way. Most customer data still lives in a relational
database somebody else designed (see [data pipelines](../engineering/03-data-pipelines.md)).

### Docker

Build a sensible image, keep it small and debuggable, use `docker compose` to stand up a
local stack with a database and a vector store, and read container logs fluently.

### Kubernetes

Read and debug manifests: deployments, services, config maps, probes, resource limits. Use
`kubectl describe` and `kubectl logs` to diagnose a crash loop. Stop before cluster design,
multi-tenant platform engineering, and CKA-level detail - most FDE roles operate clusters,
they do not build them.

### Terraform and infrastructure as code

Read and extend existing modules. The customer's platform team usually owns the
infrastructure code; you add a service following their patterns. Writing modules from
scratch is a senior-level differentiator, not an entry requirement.

### One cloud well, the others on sight

Pick the cloud you can actually access - often AWS given the posting numbers - and go end
to end: compute, storage, a managed database, secrets, and IAM policies that get tested by
something real. In the other two clouds, be able to navigate the console, read their
equivalent of a VPC and an IAM policy, and map concepts across clouds quickly.

### LLM APIs

Framework-free first: structured outputs with schema validation (`pydantic` and friends),
function and tool calling, embeddings, token and context limits, streaming, and cost math
per thousand requests. This is what the prompt engineering line at 55.0% translates to in
practice: a disciplined API user with an evaluation habit, not a prompt-collection hobbyist.

### RAG and agents

Build one of each end to end at small scale: chunking, embedding, retrieval, reranking,
and citation for RAG; a tool-calling loop with a stop condition for agents. Know when each
is the wrong answer (see [LLM application patterns](../ai/01-llm-application-patterns.md)
and [agents and tools](../ai/02-agents-and-tools.md)).

## Skill-gap self-audit

Run this quarterly, or before an interview. Each unchecked box links the guide document
that closes the gap.

- [ ] I can package, test, and type-check a Python service so another engineer could maintain it
- [ ] I have deployed a containerized service end to end on a cloud I would claim on my CV (see [cloud and infrastructure](../engineering/04-cloud-and-infrastructure.md))
- [ ] I can write a window-function query, read its query plan, and navigate an unfamiliar schema
- [ ] I can diagnose a crash-looping pod from manifests and logs without guessing
- [ ] I can call an LLM API with structured outputs and tool calling, without a framework
- [ ] I have built a small RAG pipeline end to end and can defend every retrieval decision (see [LLM application patterns](../ai/01-llm-application-patterns.md))
- [ ] I can build an evaluation set and a regression harness for a probabilistic feature (see [evaluation and testing](../ai/03-evaluation-and-testing.md))
- [ ] I can integrate with an API I do not own, including auth, retries, and rate limits (see [APIs and integrations](../engineering/02-apis-and-integrations.md))
- [ ] I can hold up my half of a customer security review (see [security and compliance](../engineering/05-security-and-compliance.md))
- [ ] I can write a one-page spec and a decision record a stranger could act on (see [requirements to spec](../customer/02-requirements-to-spec.md))

If more than three boxes are unchecked, start with the first three - they unblock
everything else.

## Related documents

- [Responsibilities](../role/02-responsibilities.md) - the work these skills are for, backed by the same posting evidence
- [Prototyping and PoCs](../engineering/01-prototyping-and-pocs.md) - the first place new technical skills get tested under customer constraints
- [Evaluation and testing](../ai/03-evaluation-and-testing.md) - the top differentiator, in full
- [Cloud and infrastructure](../engineering/04-cloud-and-infrastructure.md) - deploying into AWS, Azure, or GCP environments that already exist
- [From Software Engineer](../learning-paths/from-software-engineer.md) - if the baseline is solid and the customer-facing half is the gap
- [From AI/ML Engineer](../learning-paths/from-ai-ml-engineer.md) - if the AI half is solid and delivery is the gap

## Further reading

- [The job-scrape analysis behind the numbers](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md) - 146 postings, 94 companies, February-July 2026
- [Anthropic FDE job description](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) - a benchmark posting; note how its requirements match the baseline-plus-differentiators shape ($280,000-$320,000, 2026)
- [Anthropic documentation](https://docs.anthropic.com) - structured outputs, tool use, and context windows, framework-free
