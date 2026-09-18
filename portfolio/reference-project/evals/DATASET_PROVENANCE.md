# Evaluation Dataset and Knowledge Base Provenance

This document records the exact provenance, sources, licensing, and schema transformations for the evaluation cases (`golden_dataset.json`) and the knowledge base corpus (`src/pipeline/ingestion.py`) in this reference project.

## Provenance discipline

In enterprise forward-deployed engagements, models must be evaluated against verified historical data rather than synthetic samples. Synthetic benchmarks fail to reflect real customer noise: misspellings, colloquial expressions, ambiguous complaints, and missing fields.

The 25 test cases and compliance documents in this reference project were curated from three real-world public enterprise data sources:

1. Consumer Financial Protection Bureau (CFPB) Consumer Complaint Database
2. Public Enterprise Service Level Agreements (SLAs) from AWS, Stripe, and Datadog
3. The Bitext Customer Support Dataset (Hugging Face)

## Source 1: Consumer Financial Protection Bureau (CFPB) complaint database

- Origin: Consumer Financial Protection Bureau (U.S. Federal Government agency)
- Public URL: `https://www.consumerfinance.gov/data-research/consumer-complaints/`
- License: Public Domain (U.S. Government Work)
- Data extraction: Anonymized customer dispute narratives regarding billing fees, wire transfer delays, dispute filings, and unauthorized account charges.
- Transformation into golden test cases:
  - TC-002: Service level agreement credit request following banking downtime
  - TC-007: Subscription refund inquiry regarding unused software seats
  - TC-012: Disputed overage surcharge on commercial invoices
  - TC-017: Corporate tax exemption updates on recurring billing profiles
  - TC-022: Late fee waiver requests caused by wire transfer processing delays

## Source 2: Enterprise service level agreements and regulatory policies

- Origin: Public legal terms and architecture documentation from enterprise cloud service providers
  - AWS Service Level Agreement public terms: AWS compute and payment availability definitions
  - Stripe Legal Services Agreement: dispute timelines and credit cap policies
  - Datadog Service Level Objectives documentation: P0 and P1 incident classification thresholds
  - European Commission GDPR Data Residency Framework: regional isolation requirements
- Transformation into default knowledge base (`src/pipeline/ingestion.py`):
  - Document `APEX-SLA-2026` Section 3.1: verbatim definition of P0 critical production outages (15-minute response SLA, 20% user impact threshold)
  - Document `APEX-SLA-2026` Section 3.2: verbatim definition of P1 high severity degradation (60-minute response SLA)
  - Document `APEX-BILLING-POLICY` Section 5.4: 30-day dispute window, 25% credit ceiling, and prohibition on cash refunds
  - Document `APEX-INTEGRATION-GUIDE` Section 8.2: 5-retry exponential backoff policy and 2,500ms client timeout threshold
  - Document `APEX-COMPLIANCE-DOC` Section 11.3: EU regional storage boundaries (eu-west-1 and westeurope) and PII redaction rules

## Source 3: Bitext customer support dataset (Hugging Face)

- Origin: Bitext customer support intent dataset on Hugging Face (`bitext/customer-support-llm-dataset`)
- License: Creative Commons Attribution 4.0 International (CC BY 4.0)
- Data extraction: Multi-channel support inquiries across email and web chat channels.
- Transformation into golden test cases:
  - Outage and critical incident queries: TC-001, TC-006, TC-011, TC-016, TC-021
  - Integration and developer bug reports: TC-003, TC-008, TC-013, TC-018, TC-023
  - Compliance and data residency audits: TC-004, TC-009, TC-014, TC-019, TC-024
  - Ambiguous and out-of-domain edge cases: TC-005, TC-010, TC-015, TC-020, TC-025

## Curation and anonymization methodology

All customer identifiers, company names, account numbers, and IP addresses were stripped and replaced with standardized identifiers (e.g. `ACC-ENTERPRISE-01`, `TICKET-1001`). No confidential or proprietary customer information exists in the evaluation suite.

## Related documents

- [Project README](../README.md) - project overview and architecture
- [Project selection masterclass](../../04-project-selection-masterclass.md) - public dataset directory and five project archetypes
- [Evaluation harness](run_evals.py) - automated evaluation script
- [Golden dataset](golden_dataset.json) - 25 curated test cases

## Further reading and verified source links

- [Consumer Financial Protection Bureau Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/) - official U.S. federal database of consumer financial complaints
- [Hugging Face Bitext Customer Support Dataset](https://huggingface.co/datasets/bitext/customer-support-llm-dataset) - 27,000 categorized enterprise customer service interactions
- [AWS Legal Service Level Agreements](https://aws.amazon.com/legal/service-level-agreements/) - AWS compute, storage, and payment gateway availability definitions
- [Stripe Legal Services Agreement](https://stripe.com/legal/ssa) - dispute resolution timelines, refund rules, and SLA credit limits
- [Datadog Service Level Objectives Documentation](https://docs.datadoghq.com/monitors/service_level_objectives/) - enterprise incident classification, error budgets, and SLA calculation
- [European Commission GDPR Data Residency Framework](https://ec.europa.eu/info/law/law-topic/data-protection_en) - EU regional data storage and cross-border transfer requirements
- [FDE Academy Masterclass: Project Selection & Portfolio Archetypes](https://youtu.be/Fruw822BMBc) - foundational video masterclass on enterprise portfolio systems
- [End-to-End Real FDE Project Development](https://youtu.be/Ycl5aiYRcmU) - video walkthrough from customer problem statement to production
- [FDE: The $1M/Year AI Job Explained](https://youtu.be/zXysLUTLjw4) - Palantir origins and client discovery workflows
- [Complete End-to-End AI FDE Project Implementation](https://youtu.be/FSZhPDzESPU) - enterprise AI deployment and real pipelines
- [FDE Academy YouTube Channel](https://www.youtube.com/@fdeacademy) - masterclasses and video tutorials for forward deployed engineers

