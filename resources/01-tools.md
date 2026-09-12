# The FDE Toolbox

If you are assembling a working toolkit for FDE work, or deciding what to learn first, this file lists the tools by the job's phases rather than by category, with the job each tool does. Tools change constantly, so this list favors boring, widely adopted choices over fashionable ones, and explains the reasoning so you can substitute sensibly. We recommend boring tools deliberately: you are not the one maintaining them long-term - the customer's team is.

## Build

- Python - the default, named in 133 of 146 scraped postings (91.0%) (observed evidence); production packaging and testing, not notebook scripting
- `fastapi` - the default way to put a model or pipeline behind an HTTP API; boring, documented, and everywhere ([fastapi.tiangolo.com](https://fastapi.tiangolo.com))
- `pydantic` - boundary validation for messy customer inputs and structured output schemas for LLM calls ([pydantic.dev](https://pydantic.dev))
- A SQL client you like - you will spend real hours reading customer schemas; fluency matters more than the tool, and any competent client works
- `docker` - build images and glue local stacks together with `docker compose`; the customer's environment will not match yours, and containers shrink the surprise ([docker.com](https://www.docker.com))
- Git, on their terms - you will work in the customer's repositories under their branching and review rules; assume their conventions rather than importing yours

The depth calibration for each of these - what "knows Python" means in an FDE interview - is in [core technical skills](../skills/01-core-technical-skills.md).

## The AI application layer

- Provider SDKs and documentation as first-class tools - the model docs ([Anthropic](https://docs.anthropic.com), [OpenAI](https://platform.openai.com/docs)) are primary sources; capabilities move monthly and changelogs are where the truth arrives first
- Vector stores - `pgvector` when Postgres already exists in the customer estate ([github.com/pgvector/pgvector](https://github.com/pgvector/pgvector)); `qdrant` ([qdrant.tech](https://qdrant.tech)) or `weaviate` ([weaviate.io](https://weaviate.io)) when a dedicated store fits the workload; `pinecone` ([pinecone.io](https://pinecone.io)) when the customer wants the operation managed for them
- Embedding pipelines - boring ETL under a new name: chunking, metadata, and a refresh schedule; the retrieval quality is decided here more than in the store choice
- Prompts under version control - prompt and context files live in the repository like code, with diffs and review, because "what changed in the prompt" is a question you will need to answer to the customer and to yourself
- Agent frameworks - learn the concepts first (retrieval, tool calling, structured output, context limits), then adopt whichever framework the customer already runs; `LangChain` appears in 33.0% of scraped postings, and the other two thirds name no framework at all (observed evidence)

The pattern-level decisions - which retrieval design, when an agent is the wrong answer - are covered in [LLM application patterns](../ai/01-llm-application-patterns.md) and [agents and tools](../ai/02-agents-and-tools.md).

## Deploy

- Cloud console fluency - one cloud deep, two reading-fluent; AWS is named in 47.0% of scraped postings, GCP at 38.0%, Azure at 34.0%, and you cannot pick the customer's (observed evidence)
- `terraform` - infrastructure as code; in customer estates, IaC is often the change-control mechanism that lets a review board say yes ([terraform.io](https://www.terraform.io))
- CI/CD - whatever the customer runs; the FDE job is using their pipeline, not importing yours, so learn to read all the common ones
- Containers and `kubernetes` - named in 35.0% of scraped postings; the need is deploy-and-debug fluency, not cluster administration ([kubernetes.io](https://kubernetes.io))
- Secrets managers - the cloud-native secret stores; credentials never live in code or notebooks in customer environments, a rule with consequences described in [security and compliance](../engineering/05-security-and-compliance.md)
- A load-test script - a plain script driving realistic traffic against the endpoint before go-live; the first load test should not be the customer's launch day

The deployment-context decisions - embedding in their estate, environments, cost visibility - are in [cloud and infrastructure](../engineering/04-cloud-and-infrastructure.md).

## Evaluate

- A golden set in a notebook - a spreadsheet of inputs and expected outcomes is a legitimate evaluation harness and the right starting point; discipline first, tooling second, and a notebook version makes the first fifty cases easy to share with the customer for review
- `mlflow` - experiment tracking once runs multiply and you need to compare them ([mlflow.org](https://mlflow.org))
- Purpose-built evaluation platforms - a fast-growing category; adopt one only after the golden-set habit exists, and pick based on what the customer's team can operate, because an evaluation platform only you can operate becomes shelfware
- The methodology - what to measure, how to build the set, how to judge outputs - is the hard part, and it lives in [evaluation and testing](../ai/03-evaluation-and-testing.md); the tools above are bookkeeping around it

## Observe

- `opentelemetry` - tracing across your code and vendor calls; the LLM call is just another span, which is exactly what you want when a customer asks why an answer took eleven seconds ([opentelemetry.io](https://opentelemetry.io))
- `prometheus` and `grafana` - metrics and dashboards an ops team can keep running after you leave ([prometheus.io](https://prometheus.io), [grafana.com](https://grafana.com))
- A log platform - the customer usually has one; learn theirs rather than arguing for yours, because logs are where their on-call lives
- Uptime checks - a scheduled request against the customer-facing endpoint, agreed with their operations team; simple, and it catches the failures dashboards miss

Monitoring and reliability for probabilistic systems - what to alert on, what drift looks like - is in [monitoring and reliability](../ai/04-monitoring-and-reliability.md).

## Collaborate

- Shared documents - engagement notes, decision records, and runbooks live where the customer can read them, not in your private wiki
- Ticketing - the work happens in the customer's tracker; importing your own splits the record of what was promised
- Whiteboarding - architecture conversations with mixed technical and executive rooms need a shared surface more than they need a slide deck
- Screen recording - a three-minute recording of a failing integration, narrated, replaces an hour of meetings across time zones; the cheapest trust-builder on this list
- Decision records - short, dated notes on what was decided and why, in the format of [trade-offs and decision records](../system-design/03-trade-offs-and-decision-records.md); they outlive every meeting and settle most disputes

## The boring-tools principle

Prefer what the customer's team can operate after you leave. A stack of fashionable tools is a liability you hand over at handover: every novel component is one their on-call cannot debug at 2am. The full operator-first design argument is in [architecture for customer systems](../system-design/01-architecture-for-customer-systems.md). When you must introduce a new tool, introduce it with a runbook and a named owner, or do not introduce it.

Concretely: `pgvector` on the customer's existing Postgres usually beats a new dedicated vector database, because their team already backs up, monitors, and patches Postgres. The same test applies to every row above.

## A starter stack

For a first portfolio project, this is enough to demonstrate every phase of [the FDE loop](../role/05-the-fde-loop.md) end to end (recommendation):

- Python with `fastapi` and `pydantic`
- One provider SDK, used against its official documentation
- `pgvector` on a local Postgres for retrieval
- `docker compose` to run the whole thing on one command
- A golden set of 30-50 cases in a notebook, with pass rates tracked
- `opentelemetry` traces emitted to a local collector

Resist adding more until a real requirement demands it; the demonstration value is in the working whole, not the component count. Every addition should trace to a requirement from a simulated customer, not to curiosity.

## Related documents

- [LLM application patterns](../ai/01-llm-application-patterns.md) - where the AI-layer tools fit into the pattern catalog
- [Evaluation and testing](../ai/03-evaluation-and-testing.md) - the methodology behind the evaluation tooling
- [Cloud and infrastructure](../engineering/04-cloud-and-infrastructure.md) - deploying into estates that already exist
- [Core technical skills](../skills/01-core-technical-skills.md) - the evidence-weighted skill list behind these picks
- [Architecture for customer systems](../system-design/01-architecture-for-customer-systems.md) - the operator-first argument in full

## Further reading

- [Anthropic documentation](https://docs.anthropic.com) - the model and tooling docs worth reading as a primary source
- [OpenAI platform documentation](https://platform.openai.com/docs) - same role for the OpenAI stack
- [OpenTelemetry](https://opentelemetry.io) - the tracing standard referenced throughout the observability section
