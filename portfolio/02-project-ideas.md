# Portfolio Project Ideas: 12 Enterprise Deployment Briefs

This guide provides twelve production-grade project specifications modeled on real-world forward deployed engineering engagements across enterprise AI platforms, fintech, logistics, and healthcare. Each specification reflects how customer briefs arrive in the field: **deliberately ambiguous on the surface, with the critical technical, security, and operational constraints hidden underneath**.

To eliminate synthetic shortcuts, every brief includes recommended **verified public empirical datasets** and concrete depth markers that separate a passing prototype from a production system.

---

## How to Use These Briefs

- **The Brief**: Written from the customer's operational perspective. Resist the urge to clean it up before writing down your requirements; translating messy human intent into a technical specification is the core work of an FDE.
- **The Ambiguity Line**: Identifies the unstated assumptions you must resolve through discovery documentation.
- **Empirical Dataset**: Real-world public data sources you can ingest immediately without creating synthetic toy prompts.
- **Skills Demonstrated**: Maps directly to production architecture and engineering competencies.
- **Depth Markers**: The specific criteria hiring managers use to distinguish a senior deployment from an amateur demo.
- **Hidden Operational Iceberg**: The operational failure mode that ruins the project if ignored.

> [!TIP]
> Pick **one project, not five**. A single end-to-end deployment with a container, a golden evaluation suite, an Architecture Decision Record (ADR), and an operations runbook carries significantly more weight than multiple shallow GitHub repositories.

---

## The Twelve Enterprise Briefs

---

### 1. Support-Ticket Triage for Mid-Size SaaS (Reference Implementation)

> [!NOTE]
> **Complete Reference Project Available**: We have fully implemented this brief in [`portfolio/reference-project/`](reference-project/) with FastAPI, hybrid BM25 + dense search, golden evaluation harnesses, and an operations runbook.

- **The Customer Brief**: *"Our support queue is a firehose and everything lands in one unprioritized pile. We need incoming tickets classified automatically, urgent SLA-breach tickets escalated instantly, and draft answers prepared from our compliance and SLA handbooks."*
- **The Ambiguity**: Nobody has defined the severity taxonomy or routing classes; nobody has stated what happens when model confidence is low ($<0.85$); nobody has designed the operator feedback loop.
- **Empirical Dataset**:
  - [CFPB Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/) (U.S. Federal Government agency)
  - [Hugging Face Bitext Customer Support Dataset](https://huggingface.co/datasets/bitext/customer-support-llm-dataset) (26,872 multi-channel enterprise tickets)
  - Cloud Service Level Agreements (AWS, Stripe, Datadog)
  - Complete catalog documented in [`reference-project/evals/DATASET_PROVENANCE.md`](reference-project/evals/DATASET_PROVENANCE.md).
- **Skills Demonstrated**: Pydantic schema validation, hybrid retrieval, confidence gating, human-in-the-loop exception queues, automated golden evals.
- **Depth Markers**: Per-class precision/recall on a 25-case golden set, deterministic citation verification (zero ungrounded claims), and a one-click operator resolution queue.
- **Hidden Operational Iceberg**: The human review queue and confidence thresholding *are* the product. The LLM is just a component; operator override feedback is what prevents model drift.

---

### 2. Regulatory Document Q&A with Verbatim Citation Receipts

- **The Customer Brief**: *"Our legal and compliance analysts spend hours checking insurance contracts against regional regulatory statutes. Build an assistant that answers policy coverage questions and attaches exact paragraph receipts."*
- **The Ambiguity**: Which documents are legally binding versus superseded; how to handle conflicting clauses across policy addendums; how to structure an absolute refusal when context is missing.
- **Empirical Dataset**:
  - [SEC EDGAR 10-K & 10-Q Financial Filings](https://www.sec.gov/edgar/searchedgar/companysearch) (public corporate disclosure filings)
  - [EUR-Lex European Union Regulations & Directives](https://eur-lex.europa.eu/) (official European legal texts)
- **Skills Demonstrated**: Token-aware sliding chunking, document-level ACL metadata, hybrid dense/sparse search, deterministic character-level citation verification.
- **Depth Markers**: Automated evaluation measuring citation grounding precision; explicit refusal mode when retrieval fails; handling amended and superseded document versions.
- **Hidden Operational Iceberg**: Confident hallucinations on legal clauses create regulatory liability. A system that cleanly refuses when uncertain scores higher than one that guesses.

---

### 3. Multi-Vendor Invoice Extraction & Defect Ledger

- **The Customer Brief**: *"Our accounts payable department manually keys 5,000 PDF invoices per month into SAP. Extract the line items, validate the math, and flag discrepancies."*
- **The Ambiguity**: Missing purchase order numbers, multi-page tables, currency format inconsistencies (comma decimals vs. period decimals), and non-standard tax calculations.
- **Empirical Dataset**:
  - [Document Understanding CORD Dataset](https://huggingface.co/datasets/naver-clova-ix/cord-v2) (receipt and invoice layout annotations)
  - [RVL-CDIP Document Image Dataset](https://huggingface.co/datasets/rvl_cdip) (scanned enterprise business documents)
- **Skills Demonstrated**: Multi-modal document parsing, Pydantic data normalization, arithmetic reconciliation assertions, dead-letter defect accounting.
- **Depth Markers**: Defect ledger accounting for every dropped or repaired line; regex normalization of European and US currencies; zero unhandled parsing exceptions.
- **Hidden Operational Iceberg**: A silent 2% error rate in accounts payable causes accounting reconciliation failure. Loud, auditable defect quarantine is mandatory.

---

### 4. Meeting-Notes-to-CRM Governed Updater with Rollback Gates

- **The Customer Brief**: *"Sales reps take messy free-form notes during client calls, but never update Salesforce. Automatically parse meeting transcripts and update the deal stage, ARR, and next steps in the CRM."*
- **The Ambiguity**: Which fields an automated worker is authorized to overwrite; how to prevent overwriting manual human updates made during the call; how to handle ambiguous customer names.
- **Empirical Dataset**:
  - [HubSpot Developer Sandbox API](https://developers.hubspot.com/) & Public CRM Datasets
  - [Enron Email Corpus / Business Communication Archives](https://www.cs.cmu.edu/~enron/) (real enterprise communications)
- **Skills Demonstrated**: Tool-calling agents, stateful idempotency, entity resolution, governed human approval gates, audit trails.
- **Depth Markers**: Write-policy matrix (autonomous update for low-risk notes vs. human-gated approval for deal amount changes $> \$5{,}000$); replay-safe idempotency; full before/after diff visualization.
- **Hidden Operational Iceberg**: Unconditional write access to production CRMs will corrupt the sales pipeline. Write governance and one-click undo are non-negotiable.

---

### 5. High-Scale Data-Warehouse Free-Text Enrichment

- **The Customer Brief**: *"Our data warehouse has 250,000 legacy account rows with unstructured text notes. Enrich them with industry classification, company size, and tech stack tags so marketing can segment."*
- **The Ambiguity**: Rate limits on model APIs; cost ceiling for processing a quarter-million rows; reconciling enrichment with existing human tags; backfill checkpointing.
- **Empirical Dataset**:
  - [Kaggle Enterprise B2B Company Profiles](https://www.kaggle.com/) (real firmographic enterprise datasets)
  - [SEC EDGAR Company Profiles](https://www.sec.gov/edgar/searchedgar/companysearch)
- **Skills Demonstrated**: Batch LLM processing, token-bucket client-side rate limiting, resume-from-checkpoint state machines, cost budgeting.
- **Depth Markers**: A backfill script that can be paused, killed, and resumed without re-processing records; defensible cost calculation ($\text{cost/row} \le \$0.002$); schema validation on output.
- **Hidden Operational Iceberg**: Network hiccups midway through a 10-hour batch run. Without idempotent checkpointing, you either duplicate charges or lose progress.

---

### 6. Compliance-Review Assistant for Regulated Grant Processing

- **The Customer Brief**: *"Staff review regional research grant applications against a complex federal compliance handbook. Build a tool to assist reviewers in identifying non-compliant budget items and eligibility gaps."*
- **The Ambiguity**: Determining whether the AI assists or decides; legal liability for missed disqualifications; handling contradictory federal guidance.
- **Empirical Dataset**:
  - [Grants.gov Uniform Guidance (2 CFR 200)](https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200) (official federal grant compliance regulations)
  - [National Science Foundation (NSF) Public Award Summaries](https://www.nsf.gov/awardsearch/)
- **Skills Demonstrated**: Regulatory RAG, immutable audit logging, assistive-only UI boundaries, strict quote attribution.
- **Depth Markers**: Audit trail recording prompt version, model version, and exact regulatory clause cited; clear assistive disclaimers; deterministic failure fallbacks.
- **Hidden Operational Iceberg**: If the system makes autonomous decisions, it breaches federal administrative compliance. The assistive-only boundary must be enforced in architecture.

---

### 7. Multi-Source Financial Reconciliation Ingest

- **The Customer Brief**: *"We process transactions across Stripe, Adyen, and internal ledger exports. The numbers never match at the end of the month. Ingest all three sources and generate an automated reconciliation report."*
- **The Ambiguity**: Different source schemas, time-zone alignment on midnight transactions, differing rate limits per gateway, and resolving conflicting transaction statuses.
- **Empirical Dataset**:
  - [Stripe Developer Sandbox & Mock API Fixtures](https://stripe.com/docs/api)
  - Synthetic and anonymized banking ledgers
- **Skills Demonstrated**: Third-party API integration, exponential backoff with full jitter, deterministic transaction matching, scheduled reconciliation pipelines.
- **Depth Markers**: Reconciliation report detailing matched transactions, unmatched items, and floating-point rounding adjustments; handling gateway 429 retries.
- **Hidden Operational Iceberg**: Time-zone offsets between payment gateways cause transactions near midnight to record on different calendar days. Normalization must precede matching.

---

### 8. Voice-of-Customer Multi-Label Classifier over Public App Reviews

- **The Customer Brief**: *"Our product team receives 10,000 mobile app reviews per month across Google Play and iOS. Classify user sentiment, extract bug reports, and track feature complaints across app versions."*
- **The Ambiguity**: Reviews containing multiple conflicting sentiments; slang, sarcasm, and typos; highly imbalanced class distributions (many general complaints, few specific crashes).
- **Empirical Dataset**:
  - [Hugging Face App Store & Google Play Reviews](https://huggingface.co/datasets/app_reviews) (public scraped app feedback)
- **Skills Demonstrated**: Multi-label classification, data drift detection, precision/recall threshold optimization, weekly trend reporting.
- **Depth Markers**: Per-class precision and recall metrics detailing weak categories; automated drift detector flagging novel error keywords; version-stratified trend analytics.
- **Hidden Operational Iceberg**: Global accuracy metrics hide minority-class failures. A classifier with 92% overall accuracy might catch 0% of critical security bug reports.

---

### 9. Internal-Wiki RAG with Incremental Ingestion & Freshness Canaries

- **The Customer Brief**: *"Our engineering wiki has 8,000 pages, and half of them contain outdated architectural guidelines. When engineers ask technical questions, ensure answers prioritize the freshest documentation."*
- **The Ambiguity**: Defining what constitutes a "stale" document; resolving conflicting guidance between old and new RFCs; executing incremental ingestion without full index re-indexing.
- **Empirical Dataset**:
  - [Wikimedia Foundation Public Dumps](https://dumps.wikimedia.org/) or enterprise Confluence markdown archives
- **Skills Demonstrated**: Incremental embedding updates, document versioning graphs, staleness scoring heuristics, background freshness canaries.
- **Depth Markers**: Webhook-driven incremental chunk updates; freshness metadata displayed in query citations; automated canary tests alerting on stale retrieved documents.
- **Hidden Operational Iceberg**: Re-indexing 8,000 documents on every git commit is computationally unfeasible. Incremental CDC (Change Data Capture) is mandatory.

---

### 10. Multi-Format Order-Email Parser with Exception Queue

- **The Customer Brief**: *"Wholesale customer purchase orders arrive as unstructured emails, attached CSVs, or scanned PDFs. Convert them into clean database orders and route ambiguous orders to a human dispatcher."*
- **The Ambiguity**: Incomplete SKU descriptions, ambiguous quantities ("three boxes" vs. "three units"), conflicting delivery addresses, and duplicate email resends.
- **Empirical Dataset**:
  - [Enron Email Dataset](https://www.cs.cmu.edu/~enron/) or public e-commerce Shopify webhook test payloads
- **Skills Demonstrated**: Defensive parsing, Pydantic schema validation, hash-based deduplication, dispatcher exception queue.
- **Depth Markers**: Exception queue with assigned owner and priority SLA; daily audit digest; idempotent replay protection for re-sent emails.
- **Hidden Operational Iceberg**: An order processed twice due to email retries causes duplicate physical shipments. Idempotent deduplication keys must be derived from payload content.

---

### 11. Self-Hosted Model Deployment in a Locked-Down Air-Gapped Network

- **The Customer Brief**: *"Our security policy mandates that zero data can leave our private on-premise infrastructure. No external cloud APIs, no package downloads, and no internet access. Deploy a local model pipeline."*
- **The Ambiguity**: Package dependencies cannot be downloaded via `pip` at runtime; model weights must be pre-packaged; telemetry cannot use cloud dashboards.
- **Empirical Dataset**:
  - Open-source enterprise compliance guidelines ([NIST SP 800-53 / DISA STIG](https://csrc.nist.gov/))
  - Local open weights (e.g. Llama-3-8B or Qwen-2.5 on local vLLM / Ollama)
- **Skills Demonstrated**: Local containerized inference (vLLM / Ollama), offline Docker image bundling, local Prometheus/Grafana telemetry, air-gapped evaluation.
- **Depth Markers**: Fully functional deployment executed with networking disabled (`docker run --network none`); local vector index; offline test and eval suite.
- **Hidden Operational Iceberg**: Modern AI libraries assume active internet access for huggingface token downloads. Building fully hermetic offline containers is the engineering test.

---

### 12. Production Observability & Automated Eval Harness for Upstream Models

- **The Customer Brief**: *"Our product engineering team deployed an LLM-based customer onboarding assistant. It works well today, but we have no visibility into latency, cost, token drift, or when model accuracy degrades."*
- **The Ambiguity**: Negotiating telemetry instrumentation with an engineering team that did not ask for oversight; establishing acceptable error budget thresholds.
- **Empirical Dataset**:
  - [OpenTelemetry Semantic Conventions for Generative AI](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
  - Real production traces and prompt logs
- **Skills Demonstrated**: OpenTelemetry instrumentation, Prometheus metric export, automated golden canary evaluation cron, alert routing.
- **Depth Markers**: Structured JSON traces containing prompt tokens, completion tokens, latency percentiles, and cost; automated hourly canary query testing grounding accuracy.
- **Hidden Operational Iceberg**: Logging full prompt payloads to central aggregators leaks customer PII and violates privacy regulations. Automatic PII masking before trace export is required.

---

## How to Select and Execute Your Project

1. **Leverage Existing Domain Knowledge**: If you have a background in finance, pick Brief 3 or 7; if healthcare or compliance, pick Brief 2 or 6; if DevOps or SRE, pick Brief 11 or 12.
2. **Commit to the Six Principles**: Verify your project against the six principles in [What to Build](01-what-to-build.md).
3. **Use Real Empirical Data**: Never build against synthetic sample data. Ingest one of the verified public datasets listed above.
4. **Study Our Reference Project**: Use [`portfolio/reference-project/`](reference-project/) as your architectural template for FastAPI structure, Pydantic schemas, and pytest evaluation harnesses.

---

## Related Documents

- [Reference Project Implementation](reference-project/README.md) - complete runnable implementation of Brief 1
- [Reference Dataset Provenance](reference-project/evals/DATASET_PROVENANCE.md) - verified CFPB & Bitext dataset documentation
- [What to Build](01-what-to-build.md) - six non-negotiable portfolio principles and 3-tier rubrics
- [Presenting Projects](03-presenting-projects.md) - writing up architecture and demonstrating depth
- [The FDE Loop](../role/05-the-fde-loop.md) - walking the project through discovery, build, and production

---

## References & Further Reading

1. **Alexey Grigorev**: [AI Engineering Field Guide: FDE Responsibilities and Skills Analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)
2. **Consumer Financial Protection Bureau (CFPB)**: [Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/)
3. **Hugging Face**: [Bitext Customer Support LLM Dataset](https://huggingface.co/datasets/bitext/customer-support-llm-dataset)
4. **SEC EDGAR**: [Company Financial Filings Search](https://www.sec.gov/edgar/searchedgar/companysearch)
5. **OpenTelemetry**: [Semantic Conventions for Generative AI Systems](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
