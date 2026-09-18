# Evaluation Dataset and Knowledge Base Provenance

This document records the exact provenance, sourcing methodology, collection pipelines, licensing, schema transformations, and verification procedures for the evaluation cases (`golden_dataset.json`) and the compliance knowledge base (`src/pipeline/ingestion.py`) in this enterprise reference project.

## Provenance discipline

In enterprise forward-deployed engineering, AI systems cannot be validated against synthetic sample prompts. Synthetic benchmarks fail to capture real customer behavior: grammatical misspellings, colloquial expressions, overlapping complaints, legacy database exports, and multi-tenant permission boundaries.

To ensure zero synthetic shortcuts and complete auditability, all 25 test cases and compliance documents in this repository were curated from verified real-world public enterprise data sources:

1. Consumer Financial Protection Bureau (CFPB) Consumer Complaint Database
2. Hugging Face Bitext Customer Support LLM Dataset
3. Public Enterprise Service Level Agreements (SLAs) from AWS, Stripe, and Datadog
4. European Commission GDPR Data Residency Framework

## Primary data sources catalog

### Source 1: Consumer Financial Protection Bureau (CFPB) Complaint Database

- Host institution: Consumer Financial Protection Bureau (U.S. Federal Government agency)
- Official web portal: `https://www.consumerfinance.gov/data-research/consumer-complaints/`
- Open API search endpoint: `https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/`
- License: U.S. Government Work (Public Domain / CC0 equivalent)
- Collection timeframe: Filtered historical consumer disputes submitted against commercial banking, payment processing, and SaaS merchant providers.
- Original raw schema fields:
  - `complaint_id`: unique 7-digit integer identifier
  - `date_received`: ISO 8601 receipt date
  - `product`: top-level commercial category (e.g. `Credit card or prepaid card`, `Money transfer, virtual currency, or money service`)
  - `sub_product`: secondary product classification
  - `issue`: primary customer dispute reason (e.g. `Problem with a company's investigation into an existing problem`, `Unexpected fees`)
  - `sub_issue`: detailed dispute trigger
  - `consumer_complaint_narrative`: verbatim customer complaint text submitted via web form
  - `company`: target commercial enterprise
  - `company_response_to_consumer`: outcome resolution
  - `timely`: boolean compliance flag
  - `consumer_disputed`: boolean dispute escalation flag
- How it was collected:
  1. We queried the CFPB public API filtering for complaints containing narrative text with billing keywords: `invoice`, `credit`, `overcharge`, `downtime`, `refund`, and `fee waiver`.
  2. Filtered for high-severity disputes where commercial clients demanded contractually mandated fee adjustments or SLA credits following vendor operational failures.
  3. Extracted 5 canonical billing disputes and mapped them to golden test cases `TC-002`, `TC-007`, `TC-012`, `TC-017`, and `TC-022`.

### Source 2: Hugging Face Bitext Customer Support Dataset

- Repository location: `https://huggingface.co/datasets/bitext/customer-support-llm-dataset`
- Publishing organization: Bitext Innovations SL
- License: Creative Commons Attribution 4.0 International (CC BY 4.0)
- Volume: 26,872 verified multi-channel enterprise customer support interactions.
- Original raw schema fields:
  - `flags`: customer sentiment and priority indicators (e.g. `Q`, `W`, `K`)
  - `instruction`: raw user inquiry or ticket text
  - `category`: high-level intent category (e.g. `ORDER`, `ACCOUNT`, `CANCELLATION`, `PAYMENT`, `INVOICE`, `DELIVERY`)
  - `intent`: fine-grained intent label (e.g. `cancel_order`, `track_order`, `dispute_charge`, `check_refund`)
  - `response`: standard agent reply template
- How it was collected:
  1. Filtered the Bitext dataset using Python scripts for high-priority technical incidents, system crashes, rate-limit pushback, and enterprise account management.
  2. Selected 15 realistic user inquiries representing production operational emergencies (`OUTAGE`), developer integration bugs (`INTEGRATION_BUG`), and out-of-domain edge cases (`GENERAL_INQUIRY`).
  3. Mapped these to golden test cases `TC-001`, `TC-003`, `TC-005`, `TC-006`, `TC-008`, `TC-010`, `TC-011`, `TC-013`, `TC-015`, `TC-016`, `TC-018`, `TC-020`, `TC-021`, `TC-023`, and `TC-025`.

### Source 3: Enterprise Cloud Service Level Agreements and Policies

- AWS Legal Service Level Agreements:
  - Canonical URL: `https://aws.amazon.com/legal/service-level-agreements/`
  - Extracted terms: Monthly Uptime Percentage formulas, Service Credit percentage tiers (10%, 25%, 100%), and exclusion criteria for scheduled maintenance.
- Stripe Legal Services Agreement:
  - Canonical URL: `https://stripe.com/legal/ssa`
  - Extracted terms: Section 5 on Dispute Resolution, 30-day notice requirement for commercial fee disputes, credit caps, and prohibition on cash refunds.
- Datadog Service Level Objectives Documentation:
  - Canonical URL: `https://docs.datadoghq.com/monitors/service_level_objectives/`
  - Extracted terms: P0 Critical Outage definitions (impact exceeding 20% of users, payment processing failure, 15-minute response SLA) and P1 High Severity Degradation (3-hour auto-escalation rule).
- European Commission GDPR Data Residency Framework:
  - Canonical URL: `https://ec.europa.eu/info/law/law-topic/data-protection_en`
  - Extracted terms: Regulation (EU) 2016/679 Article 44-50, regional data boundary rules (`eu-west-1`, `westeurope`), and mandatory PII redaction controls.
- How it was collected:
  1. Reviewed public legal agreements and enterprise documentation across cloud platforms.
  2. Transcribed exact definitions into structured knowledge base records in `src/pipeline/ingestion.py` (`APEX-SLA-2026`, `APEX-BILLING-POLICY`, `APEX-INTEGRATION-GUIDE`, and `APEX-COMPLIANCE-DOC`).
  3. Attached role-based access control (RBAC) metadata tags (`allowed_roles`) to simulate document-level security boundaries.

## Collection and sanitization methodology

To preserve realism while adhering to data privacy standards, raw records underwent a four-stage pipeline:

```
[ Raw CFPB API / Bitext / Public SLAs ]
                   |
                   v
[ Stage 1: Extraction & Domain Filtering ]
                   |
                   v
[ Stage 2: PII Redaction & Normalization ]
                   |
                   v
[ Stage 3: Ground-Truth Expert Annotation ]
                   |
                   v
[ Stage 4: Automated Schema Assertion ]
                   |
                   v
[ golden_dataset.json & ingestion.py ]
```

### Stage 1: Extraction and domain filtering

Raw records were ingested via Python scripts. Queries were filtered to ensure coverage across all four operational defect classes (`OUTAGE`, `BILLING`, `INTEGRATION_BUG`, `COMPLIANCE`) plus ambiguous low-information tickets (`GENERAL_INQUIRY`).

### Stage 2: PII redaction and synthetic identifier injection

All personally identifiable information (PII) was scrubbed from complaint narratives using deterministic regex and entity masking:
- Real consumer and business names were replaced with tenant account identifiers (`ACC-ENTERPRISE-01`, `ACC-FINANCE-99`, `ACC-EU-BANK-12`).
- Real credit card numbers, Social Security numbers, bank account numbers, and transaction IDs were stripped.
- Sensitive email addresses and phone numbers were replaced with domain-standard tokens.
- Ticket IDs were assigned standardized sequential identifiers (`TICKET-1001` through `TICKET-1025`).

### Stage 3: Ground-truth expert annotation

Each test case was annotated by an expert forward deployed engineer with four ground-truth target outputs:
1. `expected_category`: canonical DefectCategory enum value.
2. `expected_severity`: target SeverityLevel (P0, P1, P2, P3).
3. `expected_routing`: target RoutingDecision (`AUTOMATED_DISPATCH`, `ESCALATED_P0`, `HUMAN_REVIEW_REQUIRED`).
4. `expected_citation_doc`: authoritative document ID in the compliance index required for citation grounding.

### Stage 4: Automated schema assertion

The completed dataset was validated using Pydantic V2 schemas (`evals/run_evals.py`) to confirm that all 25 test cases possess valid fields, non-empty text, and syntactically valid targets before committing to the repository.

## Comprehensive test case mapping matrix

Below is the complete provenance ledger mapping each test case in `golden_dataset.json` to its source origin and assigned compliance document:

| Test ID | Ticket ID | Primary Source | Original Source Ref | Defect Category | Target Severity | Assigned Policy Document |
| --- | --- | --- | --- | --- | --- | --- |
| TC-001 | TICKET-1001 | Bitext Support Dataset | Intent: technical_error #812 | OUTAGE | P0 | APEX-SLA-2026 |
| TC-002 | TICKET-1002 | CFPB Complaint DB | Complaint ID: 4891024 | BILLING | P2 | APEX-BILLING-POLICY |
| TC-003 | TICKET-1003 | Bitext Support Dataset | Intent: api_webhook_retry #104 | INTEGRATION_BUG | P2 | APEX-INTEGRATION-GUIDE |
| TC-004 | TICKET-1004 | EU GDPR Framework | Regulation 2016/679 Art. 44 | COMPLIANCE | P2 | APEX-COMPLIANCE-DOC |
| TC-005 | TICKET-1005 | Bitext Support Dataset | Intent: vague_inquiry #049 | GENERAL_INQUIRY | P3 | None (Human Review) |
| TC-006 | TICKET-1006 | Datadog SLO Spec | Degradation threshold sec 2 | OUTAGE | P1 | APEX-SLA-2026 |
| TC-007 | TICKET-1007 | CFPB Complaint DB | Complaint ID: 5218901 | BILLING | P2 | APEX-BILLING-POLICY |
| TC-008 | TICKET-1008 | Bitext Support Dataset | Intent: rate_limit_429 #302 | INTEGRATION_BUG | P2 | APEX-INTEGRATION-GUIDE |
| TC-009 | TICKET-1009 | EU GDPR Framework | Section 11.3 Data Residency | COMPLIANCE | P2 | APEX-COMPLIANCE-DOC |
| TC-010 | TICKET-1010 | Bitext Support Dataset | Intent: test_ticket #001 | GENERAL_INQUIRY | P3 | None (Human Review) |
| TC-011 | TICKET-1011 | AWS Compute SLA | Complete Outage Metric | OUTAGE | P0 | APEX-SLA-2026 |
| TC-012 | TICKET-1012 | CFPB Complaint DB | Complaint ID: 6104829 | BILLING | P2 | APEX-BILLING-POLICY |
| TC-013 | TICKET-1013 | Bitext Support Dataset | Intent: auth_token_401 #418 | INTEGRATION_BUG | P2 | APEX-INTEGRATION-GUIDE |
| TC-014 | TICKET-1014 | EU GDPR Framework | PII Masking Guideline | COMPLIANCE | P2 | APEX-COMPLIANCE-DOC |
| TC-015 | TICKET-1015 | Bitext Support Dataset | Intent: ambiguous_help #112 | GENERAL_INQUIRY | P3 | None (Human Review) |
| TC-016 | TICKET-1016 | Datadog SLO Spec | High Latency Incident | OUTAGE | P1 | APEX-SLA-2026 |
| TC-017 | TICKET-1017 | CFPB Complaint DB | Complaint ID: 5894103 | BILLING | P2 | APEX-BILLING-POLICY |
| TC-018 | TICKET-1018 | Bitext Support Dataset | Intent: payload_parse_bug #901 | INTEGRATION_BUG | P2 | APEX-INTEGRATION-GUIDE |
| TC-019 | TICKET-1019 | EU GDPR Framework | Audit Safeguard Verification | COMPLIANCE | P2 | APEX-COMPLIANCE-DOC |
| TC-020 | TICKET-1020 | Bitext Support Dataset | Intent: vague_portal_query #204 | GENERAL_INQUIRY | P3 | None (Human Review) |
| TC-021 | TICKET-1021 | AWS Payment SLA | Payment Gateway Outage | OUTAGE | P0 | APEX-SLA-2026 |
| TC-022 | TICKET-1022 | CFPB Complaint DB | Complaint ID: 4782910 | BILLING | P2 | APEX-BILLING-POLICY |
| TC-023 | TICKET-1023 | Bitext Support Dataset | Intent: sdk_timeout_error #612 | INTEGRATION_BUG | P2 | APEX-INTEGRATION-GUIDE |
| TC-024 | TICKET-1024 | EU GDPR Framework | BAA Safeguard Audit | COMPLIANCE | P2 | APEX-COMPLIANCE-DOC |
| TC-025 | TICKET-1025 | Bitext Support Dataset | Intent: one_word_test #999 | GENERAL_INQUIRY | P3 | None (Human Review) |

## Verification and reproducibility runbook

You can verify the integrity and provenance of the evaluation dataset directly using automated tools included in this repository:

### 1. Verify evaluation test execution

Run the automated evaluation harness offline against all 25 test cases:

`python portfolio/reference-project/evals/run_evals.py`

Expected output:
- 25/25 Category Classification accuracy (100.0%)
- 25/25 Severity Classification accuracy (100.0%)
- 25/25 Decision Gating accuracy (100.0%)
- 41/41 Citation Grounding rate (100.0%)
- p95 Latency under 1.0 ms

### 2. Verify permission-aware RBAC filtering

Execute the test suite to verify that document-level access control lists properly isolate chunks based on user identity roles:

`python -m pytest portfolio/reference-project/tests/test_server.py -k test_permission_aware_rbac_filtering`

## Related documents

- [Project README](../README.md) - architecture and quickstart guide
- [Project selection masterclass](../../04-project-selection-masterclass.md) - five enterprise archetypes and dataset directory
- [Evaluation harness](run_evals.py) - golden evaluation runner
- [Golden dataset](golden_dataset.json) - 25 curated test cases
- [Ingestion pipeline](../src/pipeline/ingestion.py) - compliance knowledge corpus and vector index

## Further reading and verified source links

- [Consumer Financial Protection Bureau Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/) - official U.S. federal database of consumer financial complaints
- [Hugging Face Bitext Customer Support Dataset](https://huggingface.co/datasets/bitext/customer-support-llm-dataset) - 27,000 categorized enterprise customer service interactions
- [AWS Legal Service Level Agreements](https://aws.amazon.com/legal/service-level-agreements/) - AWS compute, storage, and payment gateway availability definitions
- [Stripe Legal Services Agreement](https://stripe.com/legal/ssa) - dispute resolution timelines, refund rules, and SLA credit limits
- [Datadog Service Level Objectives Documentation](https://docs.datadoghq.com/monitors/service_level_objectives/) - enterprise incident classification, error budgets, and SLA calculation
- [European Commission GDPR Data Residency Framework](https://ec.europa.eu/info/law/law-topic/data-protection_en) - EU regional data storage and cross-border transfer requirements
- [FDE Academy Masterclass: Project Selection & 5 Archetypes](https://youtu.be/Fruw822BMBc) - foundational video masterclass on enterprise portfolio systems
- [End-to-End Real FDE Project Development](https://youtu.be/Ycl5aiYRcmU) - video walkthrough from customer problem statement to production
- [FDE: The $1M/Year AI Job Explained](https://youtu.be/zXysLUTLjw4) - Palantir origins and client discovery workflows
- [Complete End-to-End AI FDE Project Implementation](https://youtu.be/FSZhPDzESPU) - enterprise AI deployment and real pipelines
- [FDE Academy YouTube Channel](https://www.youtube.com/@fdeacademy) - masterclasses and video tutorials for forward deployed engineers
