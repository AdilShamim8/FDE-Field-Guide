# FDE Project Selection Masterclass: The Five Enterprise Archetypes

This file provides an authoritative, practitioner-grounded guide to selecting, architecting, and packaging portfolio projects that pass senior FDE hiring loops at AI labs and enterprise software firms. It incorporates the framework from the FDE Academy Masterclass (FDE Academy, 2026), documents the five core enterprise project archetypes, details verified public datasets with zero hallucination, and provides a candidate background sequencing roadmap.

## Why basic AI projects get candidates rejected

Hiring managers at Palantir, OpenAI, Anthropic, Databricks, and enterprise software firms consistently bypass candidates whose portfolios contain generic tutorial projects. An analysis of industry evaluation rubrics reveals seven fatal flaws that disqualify applicant portfolios:

1. The single-document toy RAG flaw: building a script that loads one PDF into an in-memory vector store via a high-level framework wrapper (LangChain or LlamaIndex) without handling real-world document scale, mixed layouts, tables, or OCR noise.
2. The missing permission boundary: assuming all users have global access to all data. Real enterprise deployments require multi-tenant isolation, role-based access control (RBAC), and document-level access control lists (ACLs) injected into retrieval filters.
3. Synthetic clean data: training or evaluating models on pristine, pre-curated benchmark datasets. Enterprise reality is dirty CSV exports, missing primary keys, corrupted timestamps, and conflicting character encodings.
4. Absence of human-in-the-loop oversight: letting probabilistic LLM generations communicate directly with end users without confidence thresholding, exception queues, or supervisor approval gates.
5. Lack of deterministic evaluation: claiming a system works because five manual prompts looked reasonable in a chat interface, rather than publishing an automated evaluation harness with golden datasets, precision, recall, and citation validity scores.
6. Zero operational artifacts: submitting code without an operational runbook, disaster recovery kill-switch, service level agreements (SLAs), or Architecture Decision Records (ADRs).
7. Ignoring cost and latency budgets: designing systems that invoke expensive frontier models on every keystroke without token budgeting, caching, or latency percentiles (p50, p90, p95, p99).

The FDE role is precisely the discipline of solving the seven problems above. A project that ignores them proves only that you can follow a library tutorial.

## What an FDE portfolio must prove

Senior interview loops evaluate four competencies across portfolio artifacts:

- Boundary and permission discipline: can you enforce data perimeters and access control lists so users never see unauthorized customer data?
- Ambiguity and dirty data resilience: can you ingest malformed legacy data, state your assumptions in writing, and report every dropped record with an explicit defect accounting ledger?
- Closed-loop action and workflow: does your system integrate into existing enterprise systems of record (CRM, ERP, ticketing queues) with governed writeback gates?
- Rigorous deterministic verification: do you verify every model citation verbatim against source documents and measure performance with an automated golden evaluation suite?

## The five enterprise project archetypes

The FDE Academy Masterclass defines five distinct archetype systems that provide unambiguous evidence of customer-facing engineering capability.

### Archetype 1: Permission-aware enterprise knowledge system

- The business problem: a multinational enterprise needs a unified question-answering assistant across internal Google Drive, SharePoint, and Confluence estates. However, internal documents carry strict security classifications: engineering staff cannot view HR salary bands, sales reps cannot access unreleased source code, and regional staff must adhere to regional data residency rules.
- Architectural components:
  1. Identity and authorization gateway: integrates with SAML 2.0 or OIDC identity providers to resolve user group memberships at query time.
  2. Metadata-tagged vector store: during ingestion, document chunks inherit parent document access control lists (ACLs), tenancy IDs, and classification tiers.
  3. Pre-retrieval security filtering: vector queries execute SQL WHERE clauses or metadata filters that restrict cosine search exclusively to chunks authorized for the active user session.
  4. Deterministic citation grounding: generated answers cite exact document IDs and section titles, verifying that quotes appear verbatim in retrieved text.
- Verifiable public datasets:
  - SEC EDGAR financial filings: quarterly 10-Q and annual 10-K filings with real financial disclosures across multiple corporate entities.
  - Enron email corpus: a public archive of 500,000 corporate emails providing real enterprise email threads with organizational hierarchy.
- Minimum viable bar: multi-user test harness demonstrating that querying the exact same prompt with two different user roles returns filtered, permission-isolated answers.

### Archetype 2: Intake-to-resolution enterprise workflow

- The business problem: a high-volume B2B enterprise receives thousands of support exceptions, payment disputes, and SLA credit claims daily across disparate channels. Support engineers spend hours manually categorizing tickets, reviewing policy manuals, and drafting replies.
- Architectural components:
  1. Defensive ingestion API: REST and webhook receiver with idempotency key caching, payload checksum verification, and defensive schema parsing.
  2. Self-healing structured extraction: extracts target fields (account ID, defect category, severity level, urgency score) with an automated repair loop that feeds validation errors back to the model.
  3. Hybrid knowledge index: BM25 keyword matching combined with dense vector retrieval to ground answers against official SLA and customer service handbooks.
  4. Human-in-the-loop exception queue: tickets with confidence scores below 0.85 or P0 severity are routed to an operator review queue with one-click approval and override capture.
- Verifiable public datasets:
  - Consumer Financial Protection Bureau (CFPB) complaint database: over 4 million real consumer financial complaints with company responses, dispute flags, and product categories.
  - Hugging Face Bitext customer support dataset: 27,000 categorized enterprise customer service interactions with intent tags and sentiment ratings.
- Minimum viable bar: see the complete reference implementation in `portfolio/reference-project/` featuring FastAPI, hybrid retrieval, a 25-case golden evaluation harness, and operations runbooks.

### Archetype 3: Document intelligence and multi-stage approval system

- The business problem: a logistics or insurance firm receives multi-page vendor invoices, bills of lading, and customs declarations in PDF and image formats. Legacy OCR produces fragmented tables, misread digits, and corrupted alphanumeric codes.
- Architectural components:
  1. Layout-aware document parsing: preserves table structures, key-value coordinate boundaries, and hierarchical sections.
  2. Strict schema validation: parses extracted fields into typed Pydantic models with mathematical reconciliation (e.g. line items sum must match total invoice amount).
  3. Confidence thresholding and exception flagging: flags records where OCR character confidence is low or arithmetic checks fail.
  4. Human supervisor sign-off interface: displays side-by-side document views with bounding boxes, allowing human accountants to review and approve flagged discrepancies.
  5. Immutable audit ledger: logs every field edit, model trace ID, and supervisor sign-off with WORM (write once, read many) integrity.
- Verifiable public datasets:
  - DocVQA and CORD datasets: public datasets of receipts, invoices, and business forms with layout annotations.
  - Open customs declaration forms: standardized international trade documents from public regulatory authorities.
- Minimum viable bar: an extraction pipeline processing twenty multi-vendor invoices with an exception queue that surfaces arithmetic reconciliation errors.

### Archetype 4: Customer data onboarding and schema reconciliation pipeline

- The business problem: onboarding a new enterprise client requires migrating years of legacy database exports into your platform. The client exports messy CSV files with mixed character encodings (CP1252, Latin-1, UTF-8 with BOM), missing primary keys, non-standard timestamps, and duplicate customer records.
- Architectural components:
  1. Multi-encoding stream reader: detects byte order marks and attempts safe decoding cascades without crashing.
  2. Entity deduplication and fuzzy matching: identifies duplicate records across varying company name spellings and addresses.
  3. Idempotent backfill engine: allows multi-gigabyte ingestion jobs to pause, resume, and replay without duplicating rows or corrupting ledger state.
  4. Defect accounting report: outputs an exact audit log detailing total records processed, valid rows, repaired entries, and dropped rows with line numbers and reasons.
- Verifiable public datasets:
  - US Municipal open data portals: government vendor expenditure exports (e.g. City of Chicago or New York City open data) containing dirty vendor names, inconsistent date formats, and missing departments.
  - Open public ERP test databases: anonymized ERP database dumps with relational foreign-key anomalies.
- Minimum viable bar: a runnable command-line or API pipeline that ingests a 100,000-row malformed export and outputs a structured Defect Accounting Report and clean database table.

### Archetype 5: Operations command center with an action loop

- The business problem: enterprise operators need a system that does not merely answer questions, but takes governed operational actions: re-routing inventory, updating CRM deal stages, or dispatching field service personnel.
- Architectural components:
  1. Operational ontology layer: maps underlying relational tables, ERP endpoints, and warehouse schemas into canonical business objects (Accounts, Incidents, Technicians, Parts).
  2. Governed action execution engine: models propose actions with structured JSON arguments; actions are validated against business rules (e.g. actions exceeding $500 require VP sign-off).
  3. Dual-phase commit and rollback mechanism: all state modifications support automated rollback if downstream webhooks or ERP transactions fail.
  4. Operator feedback capture: every human override logs the original proposal and the operator modification, continuously enriching the golden test suite.
- Verifiable public datasets:
  - MIMIC-IV Clinical Database Demo: anonymized intensive care unit records providing realistic operational events, patient telemetry, and protocol actions.
  - Public supply chain logistics data: shipment dispatch logs with carrier assignments, port dwell times, and exception events.
- Minimum viable bar: an operational dashboard and event loop where the model proposes three distinct operational actions, with at least one requiring human supervisor sign-off before database commit.

## Real-world public dataset sourcing directory

To ensure your portfolio contains zero synthetic shortcuts, use verified public enterprise datasets. Below are primary sources:

- Consumer Financial Protection Bureau (CFPB) Complaint Database (`https://www.consumerfinance.gov/data-research/consumer-complaints/`): real consumer financial disputes against banks and credit bureaus. Ideal for Archetype 2 and Archetype 4.
- SEC EDGAR System (`https://www.sec.gov/edgar/searchedgar/companysearch`): official 10-K annual and 10-Q quarterly reports. Ideal for Archetype 1 and Archetype 3.
- Hugging Face Enterprise Support Datasets: `bitext/customer-support-llm-dataset` and `banking77`. Ideal for classification, intent routing, and evaluation benchmarking.
- Enron Email Dataset (`https://www.cs.cmu.edu/~enron/`): historical corpus of real corporate email interactions. Ideal for identity mapping, thread extraction, and permission boundary simulation.
- Public Enterprise SLA handbooks: official terms from AWS Service Level Agreements, Stripe Legal Service Agreements, and Datadog SLA terms. Ideal for knowledge grounding and compliance citation indices.

## Candidate background selection matrix

Map your starting background to the recommended project archetype to maximize interview conversion:

- Transitioning from Software Engineer: build Archetype 2 (Intake-to-resolution workflow). Your coding baseline is strong; this proves customer discovery, probabilistic boundary handling, and human exception review design.
- Transitioning from Data Engineer: build Archetype 4 (Customer data onboarding pipeline) or Archetype 1 (Permission-aware knowledge system). Your pipeline skills are proven; this demonstrates metadata-driven access control and operational reliability.
- Transitioning from AI/ML Engineer: build Archetype 5 (Operations command center) or Archetype 2 (Intake-to-resolution workflow). You already understand model training; this proves you can bind models to governed business actions and operational workflows.
- Transitioning from Solutions Engineer or Consultant: build Archetype 3 (Document intelligence) or Archetype 2 (Intake-to-resolution workflow). You have customer presence; this provides concrete code evidence of production engineering ownership.

## The 90-day project execution roadmap

### Month 1: Discovery, data curation, and architecture specification (Weeks 1 to 4)
- Pick one archetype from the selection matrix. Do not build three at once.
- Source a real public enterprise dataset from the directory above.
- Write the project brief as a customer would speak it (ambiguous and unpolished).
- Author `docs/ARCHITECTURE.md`, `docs/SOW.md`, and `docs/ADR-001.md` before writing application code.

### Month 2: Core pipeline, boundary defense, and exception queue (Weeks 5 to 8)
- Build the ingestion engine with defensive parsing, encoding cascades, and idempotency key caching.
- Implement the model engine with self-healing schema validation and feedback repair loops.
- Construct the hybrid search index and enforce deterministic quote verification.
- Implement the human-in-the-loop review queue for low-confidence or high-severity cases.

### Month 3: Golden evaluation harness, containerization, and video demo (Weeks 9 to 12)
- Build a golden dataset of at least 25 edge cases (clean, noisy, adversarial, out-of-domain).
- Author `run_evals.py` to calculate precision, recall, citation validity rate, and latency percentiles.
- Containerize the entire application with `Dockerfile` and `docker-compose.yml`.
- Record a three-minute technical walkthrough: demonstrate one happy path, one malformed input triggering automated repair, and one low-confidence ticket routed to the operator review queue.

## Related documents

- [What to build](01-what-to-build.md) - six portfolio principles that separate deployment systems from tutorials
- [Project ideas](02-project-ideas.md) - twelve customer briefs with hidden depth
- [Enterprise reference project](reference-project/README.md) - complete production implementation of Archetype 2
- [Presenting projects](03-presenting-projects.md) - how to present this system to hiring managers
- [System design reference architectures](../system-design/02-reference-architectures.md) - enterprise architecture patterns

## Further reading

- [FDE Academy Masterclass](https://youtu.be/Fruw822BMBc) - video breakdown of what FDE portfolios must prove
- [fde.academy](https://fde.academy) - forward deployed engineering curriculum and community
- [CFPB Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/) - public enterprise customer disputes
