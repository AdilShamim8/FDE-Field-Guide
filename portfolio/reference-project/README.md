# Enterprise Ticket Intelligence and Grounded Synthesis Engine (ETISE)

This directory contains a complete, production-grade reference project designed to demonstrate forward deployed engineering competence end to end. It transforms an ambiguous customer brief into a resilient, evaluated, and client-operable system.

## The customer problem

A high-growth B2B enterprise receives 12,000 incoming support tickets and policy exceptions per day across email, web forms, and external webhooks. Support engineers spend an average of 4.5 minutes per ticket manually reading text, categorizing defects, checking internal compliance manuals, and drafting responses.

Customer pain points identified during discovery:
- Unsorted firehose: high-severity P0 outages sit in the same queue as general billing questions.
- Unreliable triage: manual classification errors exceed 18%, leading to misrouted tickets and delayed SLAs.
- Compliance risk: support reps copy-paste outdated policy clauses from local notes rather than official documentation.
- Mistrust of pure AI: operations leadership refuses to allow ungrounded LLM generation to communicate directly with Tier-1 accounts.

## The architecture solution

ETISE addresses these constraints through five deterministic components:

1. Defensive ingestion: receives incoming tickets via REST API with idempotency key deduplication, payload checksum validation, and schema enforcement via Pydantic.
2. Self-healing structured extraction: extracts target fields (urgency score, defect category, customer account, affected system) with an automated repair loop that feeds validation errors back to the model.
3. Hybrid grounding engine: performs dense semantic search and keyword retrieval over an embedded compliance corpus, requiring verbatim quote matching before any citation is presented.
4. Human-in-the-loop exception review queue: tickets with confidence scores below 0.85 or P0 severity are routed to an operator review queue with one-click approval and override capture.
5. Automated evaluation harness: measures extraction accuracy, citation integrity, schema failure rate, and latency over a curated 25-case golden dataset.

## System topology

```
[ Incoming Webhook / Email ]
             |
             v
[ API Layer: FastAPI with Idempotency Guard ]
             |
             +---> [ Ingestion & Defensive Normalizer ]
             |
             v
[ Engine: Self-Healing Structured Extraction ]
             |
             +---> [ Hybrid Knowledge Retrieval & Citation Grounding ]
             |
             v
[ Confidence & Policy Gate ]
      |
      +---> Confidence >= 0.85 & Non-P0: [ Automated Draft & Direct Route ]
      |
      +---> Confidence < 0.85 or P0:     [ Operator Exception Review Queue ]
                                                           |
                                                           v
                                            [ Human Feedback Ledger ]
```

## Quickstart and local execution

### 1. Requirements

- Python 3.10+
- pip or uv

### 2. Environment setup

Clone the repository and install dependencies:

`pip install -r portfolio/reference-project/requirements.txt`

Copy the sample environment file:

`cp portfolio/reference-project/.env.example portfolio/reference-project/.env`

### 3. Run the evaluation suite

Validate the system against the 25-case golden dataset:

`python portfolio/reference-project/evals/run_evals.py`

### 4. Run the unit and integration tests

`python -m pytest portfolio/reference-project/tests/ -v`

### 5. Start the API server

`python -m uvicorn portfolio.reference-project.src.api.server:app --port 8000 --reload`

Once started, the API docs are accessible at `http://localhost:8000/docs`.

## Project artifacts in this directory

- `docs/ARCHITECTURE.md` - comprehensive architecture, threat model, and data boundary specification
- `docs/SOW.md` - Statement of Work detailing scope boundaries, deliverables, and acceptance criteria
- `docs/SLA_RUNBOOK.md` - operational runbook, alert thresholds, and rollback procedures
- `docs/ADR-001.md` - Architecture Decision Record justifying hybrid search, dense embeddings, and local validation
- `evals/DATASET_PROVENANCE.md` - exact provenance and licensing documentation for evaluation cases and handbook corpus
- `src/` - production source code (FastAPI server, extraction engine with vector similarity, hybrid retrieval with RBAC ACLs, Pydantic schemas)
- `evals/` - golden evaluation dataset and automated scoring harness
- `tests/` - unit and regression test suite
- `docker-compose.yml` & `Dockerfile` - containerized deployment setup

## Related documents

- [Project selection masterclass](../04-project-selection-masterclass.md) - the five enterprise archetypes, dataset directory, and candidate sequencing
- [What to build](../01-what-to-build.md) - portfolio principles that separate deployment systems from tutorials
- [Project ideas](../02-project-ideas.md) - twelve customer briefs with hidden depth
- [Presenting projects](../03-presenting-projects.md) - how to present this system to hiring managers
- [System design rounds](../../interviews/03-system-design.md) - system design interview frameworks

## Further reading

- [CFPB Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/) - public enterprise dispute data
- [Hugging Face Bitext Dataset](https://huggingface.co/datasets/bitext/customer-support-llm-dataset) - real-world customer support intents
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - production Python web frameworks
- [Pydantic Documentation](https://docs.pydantic.dev/) - data validation and settings management
