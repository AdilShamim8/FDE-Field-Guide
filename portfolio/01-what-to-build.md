# What to Build: Enterprise Portfolio Principles

This guide defines the six core engineering principles that make a portfolio project Forward Deployed Engineer-shaped. An FDE portfolio has one primary objective: **demonstrate that you can walk the full loop from an ambiguous customer problem to a containerized, defensively coded, and empirically evaluated production deployment with measurable business impact**.

---

## What the Empirical Market Data Proves

The [FDE loop](../role/05-the-fde-loop.md) runs from a vague customer pain point through discovery, requirements, integration, evaluation, and production deployment to customer business impact. Empirical hiring data confirms that employers screen for this exact end-to-end arc:

According to our verified [empirical job-market scrape dataset](../job-market/dataset/fde_market_data.json) of 146 deduplicated FDE job postings across 94 companies (February–July 2026):
- **90.4% (132 / 146 postings)** explicitly mandate **building and deploying production systems**.
- **88.4% (129 / 146 postings)** require **direct customer-facing technical work**.
- **64.4% (94 / 146 postings)** require **integrating disparate customer systems, APIs, or data streams**.
- **0.0% (0 / 146 postings)** are entry-level or junior positions.

This demonstrates that hiring committees do not evaluate candidates on raw coding or toy notebook experiments; they screen for engineers who possess the senior judgment to carry software across enterprise security perimeters and operational boundaries.

---

## The Six Non-Negotiable Portfolio Principles

Treat these six principles as a strict bar, not an optional menu. A project that misses three of them is a tutorial project with extra steps, regardless of how polished the code looks:

```
+-------------------------------------------------------------------------------+
|                       THE SIX FDE PORTFOLIO PRINCIPLES                        |
+-------------------+-----------------------------------------------------------+
| 1. AMBIGUOUS      | Start from a messy, conflicting customer ask; document how|
|    REQUIREMENTS   | you resolved ambiguities, killed assumptions, and scoped. |
+-------------------+-----------------------------------------------------------+
| 2. REAL THIRD-    | Must integrate with external systems with real auth, rate |
|    PARTY APIS     | limits (HTTP 429), timeouts, and token-bucket flow control|
+-------------------+-----------------------------------------------------------+
| 3. CONTAINERIZED  | Must run inside Docker / Docker Compose with healthchecks,|
|    DEPLOYMENT     | environment variable isolation, and clean restart policies|
+-------------------+-----------------------------------------------------------+
| 4. EMPIRICAL EVAL | Build an automated evaluation harness on a verified golden|
|    ON REAL DATA   | dataset; report per-field precision, recall, and refusal. |
+-------------------+-----------------------------------------------------------+
| 5. MEASURABLE     | Define what "worked" before building (e.g. 42% latency cut|
|    OUTCOMES       | or $180k SLA credits saved) and report post-deployment.   |
+-------------------+-----------------------------------------------------------+
| 6. HANDOVER       | Ship an Architecture Decision Record (ADR), an operations |
|    ARTIFACTS      | runbook, and a one-page Executive Handover Memo.          |
+-------------------+-----------------------------------------------------------+
```

### 1. Ambiguous Requirements, Resolved by You
Start from a vague operational ask, the way an enterprise sponsor delivers it: *"Our support queue is a firehose and everything lands in one unprioritized pile"* or *"Nobody can find anything in our regulatory documents."* Document the discovery process: the questions you asked, the assumptions you invalidated, and the scope you deliberately cut. A project that opens with a clean, pre-packaged schema has already skipped the discovery phase interviewers want to evaluate.

### 2. A Real Integration with Boundary Resiliency
Your system must interact with at least one external data source or API with real authentication and strict rate limits. Handling HTTP 429 Too Many Requests, implementing exponential backoff with full jitter, and isolating third-party outages with circuit breakers is where enterprise engineering skill becomes visible. A project that only interacts with static local files proves nothing about surviving inside a client's IT estate.

### 3. Containerized Production Deployment
The application must execute reliably inside a containerized environment (`Dockerfile` and `docker-compose.yml`) with automated restart policies, structured JSON logging, and `/health` and `/metrics` endpoints. A localhost Jupyter Notebook or a screenshot of a terminal is not a deployment.

### 4. Empirical Evaluation with Verifiable Numbers
Build an automated evaluation runner before writing application logic, agree on a quality threshold, and report precision, recall, and failure distributions. Do not use synthetic AI prompts. In our reference project ([`portfolio/reference-project/`](reference-project/)), we curate test cases directly from verified public sources:
- **CFPB Consumer Complaint Database** (U.S. Federal Government agency)
- **Hugging Face Bitext Customer Support Dataset** (26,872 verified interactions)
- **Enterprise Cloud SLAs** (AWS, Stripe, Datadog)
- Complete sourcing documented in [`reference-project/evals/DATASET_PROVENANCE.md`](reference-project/evals/DATASET_PROVENANCE.md).

### 5. Measurable Customer Outcomes
Define your success metric before building, and measure it post-implementation. Valid metrics include:
- Percentage reduction in ticket triage latency (e.g. from 4 minutes to 840ms).
- Ratio of tickets successfully routed without human intervention ($>91\%$).
- Hallucination rate locked to $0.0\%$ via strict citation verification and safe refusal.

### 6. Production Handover Artifacts
Write documentation that enables another engineer or operator to run the system without your assistance:
- **Architecture Decision Record (ADR)**: Justifies technology choices and accepted trade-offs (e.g., SQLite + `sqlite-vec` vs. managed cloud vector databases).
- **Operations Runbook**: Explains dashboard alerts, failure remediation, and rollback triggers.
- **Executive Handover Memo**: A one-page business briefing summarizing performance baselines and recommended next steps for executive sponsors.

---

## 3-Tier Hiring Manager Portfolio Evaluation Rubric

Hiring managers at top AI labs evaluate candidate portfolio projects across three distinct scoring bands:

| Evaluation Tier | Characteristics & Observed Signals | Hiring Outcome |
| :--- | :--- | :--- |
| **Strong Hire** (Top 5%) | Containerized repository runs on fresh clone with two commands (`docker-compose up` or `pytest`); runnable evaluation harness reporting concrete precision/recall on a verified dataset; documented ADR with rejected alternatives; defensive boundary handling (encoding detection, rate limits, schema validation); one-page Executive Handover Memo. | **Fast-track to technical screen / onsite loop** |
| **Hire** (Competitive) | Functional application with clear documentation; basic unit tests covering the happy path; typed schemas (Pydantic); runs cleanly; basic evaluation script; minor omissions in failure boundary testing or deployment runbooks. | **Standard technical screen** |
| **No Hire** (Default) | Single-file script or Jupyter Notebook; toy Streamlit prompt wrapper; hardcoded API keys or environment leaks; zero automated tests; synthetic sample prompts; claims "it scales" without capacity arithmetic; no evaluation harness. | **Immediate rejection** |

---

## The Tutorial Trap: Why Course Capstones Hurt Your Candidacy

Portfolios filled with course capstones, Kaggle notebooks, and cloned tutorial apps actively hurt an FDE application. The reason is structural: **tutorials eliminate everything the FDE role exists to do**.

In a tutorial:
- The requirements are pre-defined and unambiguous.
- The dataset is pre-cleaned with zero encoding anomalies.
- The evaluation criteria are already fixed.
- The system never has to survive customer security reviews or on-call hand-offs.

A tutorial-heavy portfolio signals that an engineer can follow instructions in an idealized sandbox, but reveals nothing about how they behave when an upstream API returns malformed JSON or a client CISO vetoes cloud data egress.

Furthermore, hiring managers have reviewed the same five tutorial projects hundreds of times. A deployment-shaped project built against messy real-world constraints stands out immediately by construction.

---

## The Five Deployable FDE Archetypes

Senior practitioner masterclasses converge on five archetype systems that provide incontrovertible proof of forward deployed engineering capability:

```
+-------------------------------------------------------------------------------+
|                       THE FIVE DEPLOYABLE ARCHETYPES                          |
+-------------------+-----------------------------------------------------------+
| 1. PERMISSION-    | Document-level ACL inheritance; Active Directory group    |
|    AWARE RAG      | filtering injected into vector SQL; zero cross-tenant leak|
+-------------------+-----------------------------------------------------------+
| 2. INTAKE-TO-     | Multi-channel ingestion, schema extraction, confidence    |
|    RESOLUTION     | gating, human review queue, and automated evaluation.     |
|    (Our Ref Proj) | (Full runnable code: portfolio/reference-project/)        |
+-------------------+-----------------------------------------------------------+
| 3. DOCUMENT       | Complex layout PDF/invoice processing, field extraction,  |
|    INTELLIGENCE   | OCR artifact repair, one-click diff approval interface.   |
+-------------------+-----------------------------------------------------------+
| 4. CUSTOMER DATA  | Dirty legacy ERP ingestion, BOM encoding detection,       |
|    ONBOARDING     | deduplication, and auditable defect accounting reports.   |
+-------------------+-----------------------------------------------------------+
| 5. OPERATIONS     | Palantir-style ontology, entity resolution, governed      |
|    COMMAND CENTER | action writeback with human approval, and audit logs.     |
+-------------------+-----------------------------------------------------------+
```

### Complete Reference Implementation: Archetype 2
We provide a complete, production-grade reference implementation of Archetype 2 in [`portfolio/reference-project/`](reference-project/):
- **FastAPI Core Service**: REST endpoints for ticket processing, health, and operator review.
- **Defensive Boundary Processing**: Pydantic schema validation, payload hash deduplication, and exception queue routing.
- **Hybrid Grounding Engine**: BM25 sparse keyword search combined with dense cosine vector similarity over enterprise SLAs and compliance handbooks.
- **Enterprise Eval Suite**: Automated 25-case evaluation runner ([`evals/run_evals.py`](reference-project/evals/run_evals.py)) verified against CFPB and Bitext data.
- **Complete Test Suite**: Comprehensive pytest suite ([`tests/test_server.py`](reference-project/tests/test_server.py)) running in under 0.5s.

---

## What If You Cannot Access Real Customers?

Most engineers building a portfolio do not have active enterprise clients. You do not need to wait for permission; you can simulate enterprise constraints using public assets:

1. **Messy Public Data**: Use municipal complaint portals, regulatory dockets, SEC 10-K filings, or CFPB consumer complaint databases. They contain dirty formatting, duplicate entries, and versioning conflicts.
2. **Nonprofit Client Engagements**: Offer to automate an intake or document workflow for a local nonprofit or community organization. They have real operational pain, real data, and genuine gratitude.
3. **Internal Team Tooling**: Automate a workflow for an adjacent department (sales, legal, operations) at your current employer. You encounter the same dynamic as a customer: unmanaged requirements and shared operational stakes.

Before building, verify the **Constraint Simulation Checklist**:
- [ ] The brief is written from an external stakeholder's operational perspective.
- [ ] At least one data source that you did not clean or prepare manually.
- [ ] At least one external API with authentication, rate limits, and network failure modes.
- [ ] One non-negotiable constraint you did not choose (e.g., zero data egress, PII masking, or strict latency budget).
- [ ] At least one real operator has tested the system and provided documented feedback.
- [ ] The evaluation metrics and acceptance criteria were committed in writing before writing code.

---

## Related Documents

- [Project Ideas](02-project-ideas.md) - twelve enterprise briefs engineered around these six principles
- [Presenting Projects](03-presenting-projects.md) - how to present depth to reviewers and hiring managers
- [Reference Project README](reference-project/README.md) - complete runnable implementation
- [Reference Dataset Provenance](reference-project/evals/DATASET_PROVENANCE.md) - verified CFPB & Bitext dataset catalog
- [Market Overview](../job-market/01-market-overview.md) - empirical job market analysis and compensation benchmarks

---

## References & Further Reading

1. **Alexey Grigorev**: [AI Engineering Field Guide: FDE Responsibilities and Skills Analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)
2. **Anthropic**: [Forward Deployed Engineer Job Description & Fit Criteria](https://job-boards.greenhouse.io/anthropic/jobs/5302966008)
3. **Fortune / MIT Report**: [Why 95% of Enterprise Generative AI Pilots Fail](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo)
4. **Consumer Financial Protection Bureau (CFPB)**: [Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/)
5. **Hugging Face**: [Bitext Customer Support LLM Dataset](https://huggingface.co/datasets/bitext/customer-support-llm-dataset)
