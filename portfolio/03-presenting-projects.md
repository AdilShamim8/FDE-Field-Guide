# Presenting Portfolio Projects to Reviewers and Hiring Committees

This guide prepares candidates to present deployment-shaped portfolio projects to senior hiring managers, technical interviewers, and field leads. In competitive hiring loops, reviewers spend **less than three minutes** on a candidate's GitHub profile before deciding whether to advance them to an onsite interview. The presentation layer—the README architecture, the recorded failure demonstration, the evaluation scorecard, and the verbal walkthrough—determines whether your engineering depth is recognized.

---

## The 2-Minute Reviewer Filter

Hiring managers scan candidate repositories looking for signals that distinguish enterprise engineers from tutorial learners:

```
+-------------------------------------------------------------------------------+
|                      THE 2-MINUTE REVIEWER SCAN SEQUENCE                      |
+-------------------+-----------------------------------------------------------+
| 00:00 - 00:30     | Scans the README top fold: Is there an architectural      |
|                   | diagram, a clear problem statement, and quickstart setup? |
+-------------------+-----------------------------------------------------------+
| 00:30 - 01:15     | Inspects the evaluation scorecard: Are metrics reported   |
|                   | on real empirical data, or does it claim 100% accuracy?   |
+-------------------+-----------------------------------------------------------+
| 01:15 - 01:45     | Checks boundary resilience: Are there Pydantic schemas,   |
|                   | encoding handlers, rate limiters, and pytest suites?      |
+-------------------+-----------------------------------------------------------+
| 01:45 - 02:30     | Inspects the operations handover: Is there an ADR and a   |
|                   | runbook, or just a generic "how to install" section?      |
+-------------------+-----------------------------------------------------------+
```

If your repository passes this 2-minute filter, the reviewer examines your code in depth and enters the technical interview predisposed to advocate for your hiring.

---

## The High-Converting Write-Up Structure

Every portfolio repository should structure its `README.md` and documentation around these eight sections in strict sequence:

1. **Problem Statement & Enterprise Persona**: The customer problem stated in raw, operational terms before technical cleanup (e.g. *"Support engineers spend 4 minutes per ticket reading PDFs across five regional ports"*).
2. **Discovered Constraints**: Non-negotiable enterprise boundaries you did not choose (e.g. zero cloud data egress, PII redaction, 2.5s latency ceiling, legacy CP1252 character encodings).
3. **Architecture Topology**: A clean ASCII or Mermaid diagram depicting component boundaries, private subnets, WAF ingress, and storage tiers.
4. **Architecture Decision Records (ADR)**: Three to five explicit technical trade-offs documenting rejected alternatives, rationale, and accepted costs (linking to [`docs/ADR-001.md`](reference-project/docs/ADR-001.md)).
5. **Empirical Evaluation on Real Data**: Dataset provenance, golden dataset size, precision, recall, citation grounding rate, and latency percentiles (p50, p90, p95, p99).
6. **Production Deployment & Observability**: Containerized deployment instructions (`docker-compose up`), structured JSON telemetry, and health check endpoints.
7. **Measurable Outcomes & Business ROI**: Quantified performance baselines committed before build and validated post-deployment (e.g. 78% automated resolution, 0.0% hallucination rate).
8. **Technical Post-Mortem & Future Roadmap**: Concrete technical lessons, known failure modes, and what you would architect differently in Phase 2.

---

## The 3-Minute Video Walkthrough Script

Do not rely exclusively on live deployment URLs. Cloud links can cold-start, 404, or hit external API rate limits during an evaluation. Embed a crisp, 3-minute Loom or unlisted YouTube technical walkthrough at the very top of your `README.md`.

```
+-------------------------------------------------------------------------------+
|                    3-MINUTE TECHNICAL WALKTHROUGH SCRIPT                      |
+-------------------+-----------------------------------------------------------+
| 00:00 - 00:45     | The Operational Context & Live Containerized Deployment   |
| 00:45 - 01:45     | The Ingress Boundary & The Deliberate Failure Path        |
| 01:45 - 02:30     | The Automated Golden Evaluation Harness on Real Data      |
| 02:30 - 03:00     | Architecture Trade-Offs (ADR) & Operations Handover       |
+-------------------+-----------------------------------------------------------+
```

### Minute 00:00–00:45: Problem & Containerized Architecture
> *"Hi, I'm walking through our automated port customs and exception triage service. In enterprise logistics, support staff manually process 15,000 shipment exception tickets daily across five ports. The core challenge is extracting structured data from malformed vendor emails, grounding answers in customs regulatory handbooks, and preventing ungrounded hallucinations.
>
> Here you see the application running inside Docker Compose. Notice that our FastAPI service exposes `/health` and `/metrics` endpoints and connects to an in-process SQLite instance with `sqlite-vec` for dense vector search."*

### Minute 00:45–01:45: The Recorded Failure Path (The Highest-Signal Minute)
> *"Now let us demonstrate how the system behaves under failure. In enterprise FDE engagements, anyone can demo the happy path; the real engineering is boundary defense.
>
> I will send an intentionally corrupted ticket payload: missing mandatory carrier IDs, a dirty European currency figure `€1.450,50`, and an ambiguous customs inquiry. Notice that rather than crashing with an unhandled exception or hallucinating a response, our Pydantic validation catches the missing ID, normalizes the currency, and flags the ticket with an 0.62 confidence score.
>
> Because confidence is below our 0.85 SLA threshold, the pipeline routes this ticket directly to our Human Exception Review Queue with an auditable defect ledger entry. An operator can review the before/after diff and resolve it with one click."*

### Minute 01:45–02:30: The Automated Evaluation Harness
> *"Rather than relying on subjective chat prompts, we evaluate this system against a verified 25-case golden dataset curated from public CFPB financial disputes and Bitext customer support tickets.
>
> Let's run `python evals/run_evals.py`. In less than 500 milliseconds, the harness evaluates all 25 cases against our compliance engine, reporting 100% citation grounding, 96.2% extraction precision, and a p95 latency of 0.28 milliseconds. Every claim is strictly backed by verbatim handbook quotes."*

### Minute 02:30–03:00: Architecture Decisions & Handover
> *"Finally, in `docs/ADR-001.md`, we documented our decision to use in-process SQLite vector search over managed cloud databases to satisfy on-premise air-gapped constraints. Our operations runbook details alarm thresholds and rollback procedures. Thank you."*

---

## The 90-Second Verbal Interview Pitch (STAR+P)

When an interviewer opens with: *"Tell me about your portfolio project"*, deliver this disciplined 90-second STAR+P summary:

> **[Situation]**: *"I built an automated intake-to-resolution pipeline modeled after high-volume logistics and customs triage operations receiving 15,000 daily exception tickets.*  
> **[Tension]**: *The operational bottleneck was that tickets arrived as dirty multi-format text with missing keys and corrupted currencies, while customs answers required 100% quote grounding without hallucination.*  
> **[Action]**: *I engineered a FastAPI service with Pydantic boundary parsing, an in-process hybrid search engine (BM25 sparse keyword matching plus cosine vector similarity), and a deterministic citation verification engine. If model confidence fell below 0.85, the system routed the ticket to a human review queue.*  
> **[Result]**: *Across our 25-case golden evaluation suite curated from public CFPB complaint data, the pipeline achieved 96.2% extraction precision, 100% citation grounding, and an 840ms average response time.*  
> **[Prevention]**: *To prevent production data corruption, I introduced an automated defect accounting ledger that records every repaired and quarantined record, and packaged an operations runbook for client hand-off."*

---

## The 5 Defensive Interview Follow-Up Probes

Expect interviewers to probe deeply into technical decisions. Rehearse these defensible responses:

### Probe 1: "Why did you choose in-process SQLite with vector extensions over Postgres or Pinecone?"
> *"I evaluated three options: Pinecone, PostgreSQL with pgvector, and SQLite with sqlite-vec. Managed cloud vector stores like Pinecone violate strict enterprise air-gapped data residency rules and introduce network egress costs. Dedicated PostgreSQL clusters were over-engineered for our initial corpus of 50,000 chunks. In-process SQLite executes in-memory within a single Docker container, delivers sub-50ms hybrid retrieval, and eliminates external database dependencies. As documented in our ADR, if chunk count exceeds 250,000, we migrate to PostgreSQL with pgvector."*

### Probe 2: "What happens when the model hallucinates or returns malformed JSON?"
> *"Our architecture enforces two deterministic guardrails: first, structured output is validated via Pydantic; if validation fails, our self-healing loop feeds the exact schema error back to the model for up to two repair turns. Second, generated answers pass through a deterministic citation validator that checks whether cited quotes exist verbatim in the retrieved source text. If character-level verification fails, the response is downgraded to an explicit refusal and routed to human review."*

### Probe 3: "How does this pipeline behave if customer traffic spikes 10x?"
> *"Inbound webhooks are immediately ingested by a token-bucket rate limiter that enforces client-side concurrency caps to prevent gateway saturation. If traffic bursts exceed capacity, excess requests receive HTTP 429 with calculated `Retry-After` headers and queue into an asynchronous worker pool backed by SQS or Redis. No records are dropped silently."*

### Probe 4: "What would the customer's on-call operator complain about on Day 30?"
> *"The operator's primary friction point would be review queue backlog management during unexpected document schema changes. If an upstream supplier updates their invoice layout, low-confidence routings spike. Our operations runbook addresses this by providing a one-click bulk-reclassification tool and an automated pipeline to add resolved exceptions directly into the golden evaluation dataset."*

### Probe 5: "How did you build the golden evaluation dataset without introducing bias?"
> *"We eliminated synthetic prompt generation entirely. As documented in our `DATASET_PROVENANCE.md`, test cases were curated from verified public enterprise sources: 15 technical support tickets from the Hugging Face Bitext dataset, 5 high-severity billing disputes from the Consumer Financial Protection Bureau (CFPB) complaint database, and 5 edge cases derived from public cloud SLAs (AWS, Stripe). Every case has deterministic ground-truth labels."*

---

## Empirical Data Provenance Hygiene

Run this quality audit on your portfolio repository before submitting it to employers:

- [ ] **Empirical Data Only**: All datasets are sourced from public domain or Creative Commons repositories (CFPB, Bitext, SEC EDGAR, Grants.gov); zero synthetic or unverified benchmark shortcuts.
- [ ] **Zero Confidential PII**: No private customer data, real passwords, or proprietary client business secrets in source code or git history.
- [ ] **Clean Clone Reproducibility**: Fresh clones install and run with two commands (`pip install -r requirements.txt && pytest`).
- [ ] **Automated Evaluation Runner**: Includes a standalone script (`python evals/run_evals.py`) that executes without external API keys (using mocked fixtures or local embeddings).
- [ ] **Documented Trade-Offs**: Contains at least one formal Architecture Decision Record (`docs/ADR-001.md`) documenting rejected alternatives and accepted trade-offs.
- [ ] **Handover Memo**: Contains an executive-ready business summary (`docs/HANDOVER.md`) detailing performance baselines and deployment next steps.

---

## Related Documents

- [What to Build](01-what-to-build.md) - six non-negotiable portfolio principles and 3-tier rubrics
- [Project Ideas](02-project-ideas.md) - twelve enterprise customer briefs with empirical dataset recommendations
- [Project Selection Masterclass](04-project-selection-masterclass.md) - five deployable archetypes and reviewer rubrics
- [Reference Project Implementation](reference-project/README.md) - complete runnable implementation of Archetype 2
- [Reference Dataset Provenance](reference-project/evals/DATASET_PROVENANCE.md) - verified CFPB & Bitext dataset catalog

---

## References & Further Reading

1. **Chip Huyen**: [Designing Machine Learning Systems & LLM Evaluation in Production](https://huyenchip.com)
2. **Alexey Grigorev**: [AI Engineering Field Guide: FDE Responsibilities and Skills Analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)
3. **Anthropic**: [Forward Deployed Engineer Job Description & Fit Criteria](https://job-boards.greenhouse.io/anthropic/jobs/5302966008)
4. **Consumer Financial Protection Bureau (CFPB)**: [Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/)
5. **Hugging Face**: [Bitext Customer Support LLM Dataset](https://huggingface.co/datasets/bitext/customer-support-llm-dataset)
