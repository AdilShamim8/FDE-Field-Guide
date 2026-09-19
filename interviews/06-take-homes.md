# Take-Home Assignments and Integration Briefs

This guide prepares candidates for the take-home technical assignment or asynchronous integration brief in a Forward Deployed Engineer loop. Rather than abstract algorithmic puzzles, FDE take-home assignments test the core habit of the job: **shipping a working, defensively coded integration system paired with production-grade client documentation inside a defined timebox**.

---

## Why FDE Loops Use Take-Homes

In forward deployed engineering, writing code is only half the deliverable; the other half is communicating architectural decisions, documenting failure boundaries, and providing an evaluation harness that proves the system works on messy customer data:

- **Startup & Enterprise AI Loops**: Evaluates the candidate's end-to-end engineering velocity, API design hygiene, and client deliverable standards ([Startup.jobs](https://startup.jobs/interview-questions/forward-deployed-engineer)).
- **Google & Scale AI Practice**: Tests whether a candidate can ingest ambiguous customer requirements, structure clean Pydantic data schemas, and produce an auditable system that non-technical operators can run ([YagyanshB Google FDE Guide](https://github.com/YagyanshB/google-fde-interview-guide)).
- **AI Engineering Field Standards**: Measures whether a candidate builds evaluation harnesses to quantify model accuracy rather than relying on lucky one-off demos ([Alexey Grigorev](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)).

Take-homes commonly span a **3 to 8-hour stated timebox** (or a 48 to 72-hour delivery window). The hiring committee evaluates the submitted artifact as a direct simulation of your first client deployment.

---

## Typical Take-Home Formats

Practitioner accounts converge on four recurring take-home shapes:

1. **Defensive Ingestion API & Normalizer**: Build an API service that ingests messy, malformed customer data (mixed encodings, dirty currency strings, missing keys), validates it against strict schemas, and emits an auditable defect report.
2. **Citation-Grounded Triage Prototype**: Ingest customer support queries or enterprise documents, execute hybrid retrieval (dense + sparse), and return structured answers with exact verbatim source citations or explicit refusal.
3. **Resilient Integration & Webhook Handler**: Build an idempotent webhook consumer that interacts with a rate-limited upstream API, featuring exponential backoff with full jitter, in-flight deduplication, and dead-letter queues.
4. **Architecture Review & Incident Remediation**: Review a flawed customer integration PR or outage transcript, identify security leaks (PII, secrets, SSRF), and deliver a working refactored codebase with a client-facing incident post-mortem.

---

## The 100-Point Hiring Committee Rubric

Hiring committees grade take-home submissions across five 20-to-25 point pillars. Submissions are scored into three explicit outcome bands:

```
+-------------------------------------------------------------------------------+
|                       TAKE-HOME EVALUATION SCORING BANDS                      |
+-------------------+-----------------------------------------------------------+
| STRONG HIRE       | 90 - 100 Points: Production-ready code, typed boundaries, |
|                   | runnable evaluation harness, ADR, and Executive Handover. |
+-------------------+-----------------------------------------------------------+
| HIRE              | 75 - 89 Points: Working implementation, basic unit tests, |
|                   | decent README, runs on fresh clone, minor edge-case gaps. |
+-------------------+-----------------------------------------------------------+
| NO HIRE           | < 75 Points: Fails to run on fresh clone, no tests, no    |
|                   | eval, hardcoded secrets, or unhandled boundary exceptions.|
+-------------------+-----------------------------------------------------------+
```

### Pillar 1: Code Architecture and Typing Hygiene (25 Points)
- Clean separation of concerns (API layer, ingestion engine, model client, validation layer).
- Comprehensive Python type annotations and strict Pydantic schemas.
- Zero committed credentials, tokens, or environment leaks.
- Pinned dependency management (`requirements.txt` or `pyproject.toml`).

### Pillar 2: Resilience and Boundary Defect Accounting (25 Points)
- Defensive parsing on malformed inputs, mixed encodings (UTF-8, UTF-8-BOM, CP1252), and dirty numeric strings.
- Client-side timeouts, circuit breakers, and exponential backoff with full jitter.
- Auditable defect ledgers: zero unhandled exceptions; every dropped or repaired record is accounted for.
- Idempotency guarantees on duplicate payloads.

### Pillar 3: Evaluation Rigor and Quality Measurement (20 Points)
- Runnable evaluation harness included in the repository (`python run_eval.py`).
- Golden test dataset covering at least 15 to 25 edge cases (clean, noisy, adversarial, out-of-domain).
- Concrete metric accounting: per-field precision, recall, citation accuracy, and schema failure rate.
- Transparent disclosure of model failure modes and refusal behavior.

### Pillar 4: Client Deliverables and Architecture Documentation (20 Points)
- Professional `README.md` functioning as an engineering specification.
- Architecture Decision Record (ADR) justifying technology trade-offs (e.g., SQLite vs. Postgres).
- One-page Executive Handover Memo written for business stakeholders.
- Working quickstart commands that execute cleanly on a fresh clone in under two minutes.

### Pillar 5: Production Readiness and Observability (10 Points)
- Clean `Dockerfile` and `docker-compose.yml` configuration.
- Structured JSON logging with request tracing IDs.
- Health check and metrics endpoint (`/health`, `/metrics`).

---

## Empirical Enterprise Take-Home Specification

Below is a representative take-home brief modeled on enterprise logistics and port customs triage challenges used across top AI platform loops.

### The Customer Problem Brief
> *"We are a global logistics enterprise receiving 15,000 shipment exception emails and customs queries per day across five regional ports. Support agents spend an average of four minutes per ticket manually reading PDFs, extracting invoice numbers, classifying defect urgency, and searching customs regulatory handbooks.
>
> Deliver a working prototype service that:
> 1. Ingests raw ticket payloads and attached markdown/text documents.
> 2. Extracts shipment ID, carrier, defect category, and urgency score with schema validation.
> 3. Provides an automated response grounded in our customs regulatory handbook, with exact document citations.
> 4. Routes low-confidence or high-severity cases to an exception review queue.
> 5. Ships with an automated test suite, an evaluation script demonstrating extraction precision, and client-facing architecture documentation."*

---

## Deliverables That Win the Loop

Top-scoring candidates submit a clean GitHub repository containing four distinct deliverables:

```
project-repo/
|-- src/                      # Clean modular source code
|   |-- api/                  # FastAPI / endpoint routes
|   |-- pipeline/             # Ingestion, parsing & rate-limiting
|   |-- models/               # Pydantic schemas & LLM client
|-- tests/                    # Pytest unit & integration suite
|-- evals/                    # Golden dataset & evaluation runner
|   |-- golden_dataset.json   # 25 verified test cases
|   |-- run_eval.py           # Automated evaluation script
|-- docs/
|   |-- ADR-001.md            # Architecture Decision Record
|   |-- HANDOVER.md           # Executive Handover Memo
|-- Dockerfile                # Reproducible container configuration
|-- README.md                 # Project specification & quickstart
```

---

### 1. The Architecture Decision Record (ADR) Template

Include an ADR in your submission (`docs/ADR-001.md`). Evaluators use this artifact to judge your technical decision-making:

```markdown
# ADR 001: Hybrid Search and In-Memory Vector Storage for Triage Prototype

## Status
Accepted

## Context
The customer requires sub-second response times across 15,000 daily tickets with strict adherence to port customs handbooks. Budget and engagement constraints require a lightweight footprint that can run on an existing on-premise server without provisioning expensive managed external cloud vector databases.

## Decision
We selected an in-process SQLite database paired with `sqlite-vec` for dense vector search and BM25 sparse keyword search, orchestrating extraction via strict Pydantic schemas.

## Consequences
Positive:
- Zero external cloud database dependencies; executes locally in a single Docker container.
- Sub-50ms hybrid retrieval latency on corpora under 50,000 document chunks.
- Deterministic Pydantic validation guarantees that zero malformed payloads reach downstream tables.

Negative:
- Horizontal scaling across multiple worker pods requires migrating from SQLite to PostgreSQL with `pgvector`.
- Memory usage scales linearly with chunk count, requiring an index partitioning strategy if the corpus exceeds 250,000 documents.
```

---

### 2. The Executive Handover Memo Template

Include a one-page business summary in your `README.md` or `docs/HANDOVER.md`:

```markdown
# Executive Handover: Automated Port Exception Triage Pipeline

## Engagement Summary
Over this initial engineering milestone, we developed an automated ingestion and document grounding service for port customs tickets. The system replaces manual triaging by automatically extracting invoice data, querying regulatory handbooks, and generating citation-grounded response drafts.

## Measured Performance Baseline
Across our 25-case golden verification suite:
- Field Extraction Precision: 96.2% on standard customs declarations
- Automated Routing Accuracy: 91.4% across five defect classifications
- Hallucination Rate: 0.0% (system cleanly refuses and routes to human operator when citations cannot be verified)
- Average End-to-End Latency: 840ms per ticket

## Recommended Next Steps
1. Deploy in shadow mode for two weeks alongside the Rotterdam port operations team to capture edge-case drift.
2. Integrate OAuth 2.0 service account credentials with the customer's active SAP shipment ledger.
3. Review human operator override logs weekly to continuously expand the golden evaluation suite.
```

---

## Time Budgeting Strategy

Manage your timebox strictly. The most frequent failure mode is spending 80% of the time tweaking prompt wording, running out of time, and submitting code with no tests and an empty README.

### 4-Hour Timebox Allocation
- **00:00 – 00:30 (30m)**: Read brief twice; write down assumptions, schema constraints, and out-of-scope boundaries.
- **00:30 – 01:30 (60m)**: Scaffold project structure; implement data schemas, parsing boundaries, and core pipeline.
- **01:30 – 02:30 (60m)**: Implement model extraction / retrieval logic with fallback and refusal handling.
- **02:30 – 03:15 (45m)**: Write unit tests (`pytest`) covering happy path and edge-case defect quarantine.
- **03:15 – 04:00 (45m)**: Write the evaluation runner, compile `README.md`, draft ADR, and verify clean run on fresh clone.

> [!TIP]
> If time runs short, **cut features first, never testing or documentation**. A clean, working subset of features with tests and an ADR scores higher than a sprawling, half-broken system.

---

## Pre-Submission Quality Checklist

Before pushing your final commit, verify each invariant:

- [ ] **Clean Clone Test**: Code runs end-to-end on a fresh machine with two commands (`pip install -r requirements.txt && python run_demo.py`).
- [ ] **Zero Hardcoded Secrets**: No API keys, passwords, or personal access tokens committed in code or git history.
- [ ] **Deterministic Testing**: `pytest` passes with 100% green tests in under 10 seconds.
- [ ] **Boundary Resilience**: Malformed JSON, missing fields, and bad encodings are caught cleanly and logged into an auditable report.
- [ ] **Runnable Eval**: An evaluation script (`run_eval.py`) executes against a golden dataset and outputs concrete accuracy metrics.
- [ ] **README as Specification**: The README clearly details architecture decisions, trade-offs, and Day-2 next steps.
- [ ] **Pinned Dependencies**: All packages in `requirements.txt` have explicit version pins.

---

## Related Documents

- [Coding and Technical Rounds](02-coding-and-technical.md) - live coding problem set and Google Vibe Coding timebox
- [Coding Round Solutions](08-coding-solutions.md) - runnable implementations of integration, retry, and rate-limiting patterns
- [Customer Scenario Rounds](04-customer-scenarios.md) - adversarial role-plays and de-escalation playbooks
- [System Design Rounds](03-system-design.md) - enterprise boundary architecture
- [Evaluation and Testing](../ai/03-evaluation-and-testing.md) - golden dataset construction and eval harnesses

---

## References & Further Reading

1. **Startup.jobs**: [Forward Deployed Engineer Interview Questions & Take-Home Briefs](https://startup.jobs/interview-questions/forward-deployed-engineer)
2. **YagyanshB**: [Google Forward Deployed Engineering Interview Prep Guide](https://github.com/YagyanshB/google-fde-interview-guide)
3. **Alexey Grigorev**: [AI Engineering Field Guide: FDE Responsibilities and Skills Analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)
4. **Nehal Vyas**: [Forward Deployed Engineer Interview Questions & Answers](https://fde.hinehal.com/blogs/fde-interview-questions)
5. **Pydantic**: [Data Validation and Settings Management for Python](https://docs.pydantic.dev/)
