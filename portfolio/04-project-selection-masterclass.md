# FDE Project Selection Masterclass: Five Enterprise Archetypes and Reviewer Rubrics

This guide provides an authoritative, practitioner-grounded framework for selecting, architecting, and packaging portfolio projects that pass senior Forward Deployed Engineer hiring loops at frontier AI labs and enterprise software firms. It incorporates the framework from the FDE Academy Masterclass, analyzes the five core enterprise project archetypes, details verified public empirical datasets, provides a candidate background sequencing roadmap, and establishes the exact **five-pillar code review rubric** senior hiring managers use during portfolio walkthrough rounds.

---

## Why Basic AI Projects Get Candidates Rejected

Hiring managers at Palantir, Anthropic, OpenAI, Databricks, and enterprise AI startups consistently bypass candidates whose portfolios contain generic tutorial projects. Our [empirical job-market scrape dataset](../job-market/dataset/fde_market_data.json) of 146 deduplicated postings confirms that **90.4% of roles mandate deploying production systems**, **88.4% require customer-facing technical leadership**, and **0.0% are junior or entry-level positions**.

An analysis of industry evaluation rubrics reveals **seven fatal flaws** that disqualify applicant portfolios:

```
+-------------------------------------------------------------------------------+
|                 THE SEVEN FATAL PORTFOLIO FLAWS TO AVOID                      |
+-------------------+-----------------------------------------------------------+
| 1. TOY RAG FLAW   | Single-PDF script using default LangChain/LlamaIndex;     |
|                   | fails to handle OCR noise, multi-page tables, or scale.   |
+-------------------+-----------------------------------------------------------+
| 2. NO PERMISSIONS | Assumes all users see all data; ignores enterprise multi- |
|                   | tenancy, RBAC, and document Access Control Lists (ACLs).  |
+-------------------+-----------------------------------------------------------+
| 3. SYNTHETIC DATA | Evaluates on clean toy prompts; ignores dirty encodings,  |
|                   | missing primary keys, corrupted amounts, and malformed CSV|
+-------------------+-----------------------------------------------------------+
| 4. NO HUMAN LOOP  | Lets probabilistic models write directly to customers     |
|                   | without confidence gating, exception queues, or overrides.|
+-------------------+-----------------------------------------------------------+
| 5. NO EVAL HARNESS| Claims "it works" after 5 manual chat prompts; lacks an   |
|                   | automated golden evaluation runner on real test cases.    |
+-------------------+-----------------------------------------------------------+
| 6. ZERO RUNBOOKS  | Submits bare code with no Architecture Decision Record    |
|                   | (ADR), operations runbook, or Executive Handover Memo.    |
+-------------------+-----------------------------------------------------------+
| 7. NO COST/LATENCY| Ignores token budgeting, caching, and latency percentiles |
|    BUDGETS        | (p50, p90, p95, p99); invokes frontier models on every key|
+-------------------+-----------------------------------------------------------+
```

The FDE role is precisely the discipline of solving these seven failure modes. A project that ignores them proves only that you can follow a library tutorial.

---

## What an FDE Portfolio Must Prove

Senior hiring committees evaluate four core competencies across portfolio artifacts:

1. **Boundary and Permission Discipline**: Can you enforce data perimeters and access control lists so users never see unauthorized customer data?
2. **Ambiguity and Dirty Data Resilience**: Can you ingest malformed legacy data, state your assumptions in writing, and report every dropped record with an explicit defect accounting ledger?
3. **Closed-Loop Action and Workflow**: Does your system integrate into existing enterprise systems of record (CRM, ERP, ticketing queues) with governed writeback gates?
4. **Rigorous Deterministic Verification**: Do you verify every model citation verbatim against source documents and measure performance with an automated golden evaluation suite?

---

## The Five Enterprise Project Archetypes

Practitioner masterclasses converge on five distinct archetype systems that provide unambiguous evidence of customer-facing engineering capability:

---

### Archetype 1: Permission-Aware Enterprise Knowledge System
- **The Business Problem**: A multinational enterprise needs a unified question-answering assistant across internal Google Drive, SharePoint, and Confluence estates. However, internal documents carry strict security classifications: engineering staff cannot view HR salary bands, sales reps cannot access unreleased source code, and regional staff must adhere to regional data residency rules.
- **Architectural Components**:
  1. Identity and authorization gateway: Integrates with SAML 2.0 or OIDC identity providers to resolve user group memberships at query time.
  2. Metadata-tagged vector store: During ingestion, document chunks inherit parent document access control lists (ACLs), tenancy IDs, and classification tiers.
  3. Pre-retrieval security filtering: Vector queries execute SQL WHERE clauses or metadata filters that restrict cosine search exclusively to chunks authorized for the active user session.
  4. Deterministic citation grounding: Generated answers cite exact document IDs and section titles, verifying that quotes appear verbatim in retrieved text.
- **Verifiable Public Datasets**:
  - [SEC EDGAR System](https://www.sec.gov/edgar/searchedgar/companysearch): Official 10-K annual and 10-Q quarterly reports with real corporate disclosures.
  - [Enron Email Dataset](https://www.cs.cmu.edu/~enron/): Public archive of 500,000 corporate emails providing real organizational hierarchies.
- **Minimum Viable Bar**: Multi-user test harness demonstrating that querying the exact same prompt with two different user roles returns filtered, permission-isolated answers.

---

### Archetype 2: Intake-to-Resolution Enterprise Workflow (Reference Project)

> [!NOTE]
> **Complete Reference Project Available**: We have fully implemented Archetype 2 in [`portfolio/reference-project/`](reference-project/) featuring FastAPI, hybrid BM25 + dense search, golden evaluation harnesses, and an operations runbook.

- **The Business Problem**: A high-volume B2B enterprise receives thousands of support exceptions, payment disputes, and SLA credit claims daily across disparate channels. Support engineers spend hours manually categorizing tickets, reviewing policy manuals, and drafting replies.
- **Architectural Components**:
  1. Defensive ingestion API: REST and webhook receiver with idempotency key caching, payload checksum verification, and defensive schema parsing.
  2. Self-healing structured extraction: Extracts target fields (account ID, defect category, severity level, urgency score) with an automated repair loop that feeds validation errors back to the model.
  3. Hybrid knowledge index: BM25 keyword matching combined with dense vector retrieval to ground answers against official SLA and customer service handbooks.
  4. Human-in-the-loop exception queue: Tickets with confidence scores below 0.85 or P0 severity are routed to an operator review queue with one-click approval and override capture.
- **Verifiable Public Datasets**:
  - [Consumer Financial Protection Bureau (CFPB) Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/): Over 4 million real consumer financial disputes with company responses and resolution flags.
  - [Hugging Face Bitext Customer Support Dataset](https://huggingface.co/datasets/bitext/customer-support-llm-dataset): 27,000 categorized enterprise customer service interactions.
  - Sourcing documented in [`reference-project/evals/DATASET_PROVENANCE.md`](reference-project/evals/DATASET_PROVENANCE.md).
- **Minimum Viable Bar**: 25-case golden evaluation suite reporting 100% citation grounding and automated exception queue routing.

---

### Archetype 3: Document Intelligence and Multi-Stage Approval System
- **The Business Problem**: A logistics or insurance firm receives multi-page vendor invoices, bills of lading, and customs declarations in PDF and image formats. Legacy OCR produces fragmented tables, misread digits, and corrupted alphanumeric codes.
- **Architectural Components**:
  1. Layout-aware document parsing: Preserves table structures, key-value coordinate boundaries, and hierarchical sections.
  2. Strict schema validation: Parses extracted fields into typed Pydantic models with mathematical reconciliation (line items sum must match total invoice amount).
  3. Confidence thresholding and exception flagging: Flags records where OCR character confidence is low or arithmetic checks fail.
  4. Human supervisor sign-off interface: Displays side-by-side document views with bounding boxes, allowing human accountants to review and approve flagged discrepancies.
  5. Immutable audit ledger: Logs every field edit, model trace ID, and supervisor sign-off with WORM (write once, read many) integrity.
- **Verifiable Public Datasets**:
  - [CORD Dataset](https://huggingface.co/datasets/naver-clova-ix/cord-v2) & [RVL-CDIP Dataset](https://huggingface.co/datasets/rvl_cdip): Standardized business forms with layout annotations.
- **Minimum Viable Bar**: An extraction pipeline processing twenty multi-vendor invoices with an exception queue that surfaces arithmetic reconciliation errors.

---

### Archetype 4: Customer Data Onboarding and Schema Reconciliation Pipeline
- **The Business Problem**: Onboarding a new enterprise client requires migrating years of legacy database exports into your platform. The client exports messy CSV files with mixed character encodings (CP1252, Latin-1, UTF-8 with BOM), missing primary keys, non-standard timestamps, and duplicate customer records.
- **Architectural Components**:
  1. Multi-encoding stream reader: Detects byte order marks and attempts safe decoding cascades without crashing.
  2. Entity deduplication and fuzzy matching: Identifies duplicate records across varying company name spellings and addresses.
  3. Idempotent backfill engine: Allows multi-gigabyte ingestion jobs to pause, resume, and replay without duplicating rows or corrupting ledger state.
  4. Defect accounting report: Outputs an exact audit log detailing total records processed, valid rows, repaired entries, and dropped rows with line numbers and reasons.
- **Verifiable Public Datasets**:
  - [US Municipal Open Data Portals](https://data.cityofchicago.org/): City vendor expenditure exports containing dirty vendor names, inconsistent date formats, and missing departments.
- **Minimum Viable Bar**: A runnable pipeline that ingests a 100,000-row malformed export and outputs a structured Defect Accounting Report and clean database table.

---

### Archetype 5: Operations Command Center with an Action Loop
- **The Business Problem**: Enterprise operators need a system that does not merely answer questions, but takes governed operational actions: re-routing inventory, updating CRM deal stages, or dispatching field service personnel.
- **Architectural Components**:
  1. Operational ontology layer: Maps underlying relational tables, ERP endpoints, and warehouse schemas into canonical business objects (Accounts, Incidents, Technicians, Parts).
  2. Governed action execution engine: Models propose actions with structured JSON arguments; actions are validated against business rules (e.g. actions exceeding $500 require VP sign-off).
  3. Dual-phase commit and rollback mechanism: All state modifications support automated rollback if downstream webhooks or ERP transactions fail.
  4. Operator feedback capture: Every human override logs the original proposal and the operator modification, continuously enriching the golden test suite.
- **Verifiable Public Datasets**:
  - [MIMIC-IV Clinical Database Demo](https://physionet.org/content/mimiciv/): Anonymized hospital operational data and clinical event telemetry.
  - [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/): Production traces and prompt telemetry.
- **Minimum Viable Bar**: An operational event loop where the model proposes three distinct operational actions, with at least one requiring human supervisor sign-off before database commit.

---

## Senior Hiring Manager Portfolio Code Review Rubric

When hiring managers conduct a 45-minute portfolio walkthrough, they grade the repository against this 100-point rubric:

| Pillar | Weight | Strong Hire Standard | Fatal Elimination Trigger (No Hire) |
| :--- | :---: | :--- | :--- |
| **1. Architecture & Perimeter Discipline** | 25% | Clear separation of API, pipeline, validation, and storage; document ACL filtering; zero hardcoded credentials; pinned dependencies. | Flat monolithic script; hardcoded API keys; global unrestricted data access; no typed schemas. |
| **2. Boundary Defense & Defect Isolation** | 25% | Defensive parsing on dirty encodings/currencies; exponential backoff with full jitter; dead-letter defect accounting reports. | Pipeline crashes on malformed inputs; silent data drops with no audit trail; infinite retry loops. |
| **3. Empirical Evaluation Rigor** | 20% | Runnable evaluation script (`run_evals.py`); 25-case golden dataset from verified public data; reported precision/recall/latency. | Zero automated tests; evaluation claimed via 5 subjective chat screenshots; synthetic test data. |
| **4. Governance, ADRs & Handover Docs** | 20% | Architecture Decision Record (ADR) justifying trade-offs; operations runbook with alarm thresholds; Executive Handover Memo. | Empty README; no documentation of assumptions or trade-offs; commands fail on fresh clone. |
| **5. Production Readiness & Observability** | 10% | Reproducible `Dockerfile` and `docker-compose.yml`; structured JSON logging with trace IDs; health check endpoints. | Localhost-only dependencies; Jupyter notebook submission; zero logging or telemetry. |

---

## Candidate Background Selection Matrix

Map your current engineering background to the recommended project archetype to maximize interview conversion:

| Current Background | Recommended Archetype | Strategic Rationale |
| :--- | :--- | :--- |
| **Software Engineer** | **Archetype 2** (Intake-to-Resolution Workflow) | Your backend coding is strong; this proves customer discovery, probabilistic boundary handling, and human exception review design. |
| **Data Engineer** | **Archetype 4** (Customer Data Onboarding) or **Archetype 1** (Permission-Aware RAG) | Your pipeline skills are proven; this demonstrates metadata-driven access control, encoding resilience, and operational auditability. |
| **AI / ML Engineer** | **Archetype 5** (Operations Command Center) or **Archetype 2** (Intake-to-Resolution) | You already understand model architectures; this proves you can bind models to governed business actions and operational workflows. |
| **Solutions Engineer / Consultant** | **Archetype 3** (Document Intelligence) or **Archetype 2** (Intake-to-Resolution) | You have customer presence; this provides concrete code evidence of production software engineering and automated evaluation rigor. |

---

## The 90-Day Project Execution Roadmap

### Month 1: Discovery, Data Curation, and Architecture Specification (Weeks 1 to 4)
- Pick one archetype from the selection matrix. Do not build three at once.
- Source a real public enterprise dataset from the directory above (never synthetic data).
- Write the project brief as an enterprise sponsor would speak it (ambiguous and unpolished).
- Author `docs/ARCHITECTURE.md`, `docs/SOW.md`, and `docs/ADR-001.md` before writing application code.

### Month 2: Core Pipeline, Boundary Defense, and Exception Queue (Weeks 5 to 8)
- Build the ingestion engine with defensive parsing, encoding cascades, and idempotency key caching.
- Implement the model engine with self-healing schema validation and feedback repair loops.
- Construct the hybrid search index and enforce deterministic quote verification.
- Implement the human-in-the-loop review queue for low-confidence or high-severity cases.

### Month 3: Golden Evaluation Harness, Containerization, and Video Demo (Weeks 9 to 12)
- Build a golden dataset of at least 25 edge cases (clean, noisy, adversarial, out-of-domain).
- Author `run_evals.py` to calculate precision, recall, citation validity rate, and latency percentiles.
- Containerize the entire application with `Dockerfile` and `docker-compose.yml`.
- Record a three-minute technical walkthrough: demonstrate one happy path, one malformed input triggering automated repair, and one low-confidence ticket routed to the operator review queue.

---

## Related Documents

- [What to Build](01-what-to-build.md) - six portfolio principles and 3-tier rubrics
- [Project Ideas](02-project-ideas.md) - twelve enterprise customer briefs with hidden depth
- [Enterprise Reference Project](reference-project/README.md) - complete production implementation of Archetype 2
- [Reference Dataset Provenance](reference-project/evals/DATASET_PROVENANCE.md) - verified CFPB & Bitext dataset catalog
- [Presenting Projects](03-presenting-projects.md) - how to present this system to hiring managers
- [System Design Reference Architectures](../system-design/02-reference-architectures.md) - enterprise architecture patterns

---

## References & Further Reading

1. **Alexey Grigorev**: [AI Engineering Field Guide: FDE Responsibilities and Skills Analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)
2. **Anthropic**: [Forward Deployed Engineer Job Description & Fit Criteria](https://job-boards.greenhouse.io/anthropic/jobs/5302966008)
3. **Consumer Financial Protection Bureau (CFPB)**: [Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/)
4. **Hugging Face**: [Bitext Customer Support LLM Dataset](https://huggingface.co/datasets/bitext/customer-support-llm-dataset)
5. **SEC EDGAR**: [Company Financial Filings Search](https://www.sec.gov/edgar/searchedgar/companysearch)
6. **OpenTelemetry**: [Semantic Conventions for Generative AI Systems](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
7. **FDE Academy**: [YouTube Masterclass Series for Forward Deployed Engineers](https://www.youtube.com/@fdeacademy)
