# Enterprise Forward Deployed Engineer Roadmap and Delivery Package

This directory contains the foundational reference documentation and production-grade delivery artifacts for forward deployed AI engineering. It includes the complete 24-week engineering roadmap and the end-to-end specification package for Vaayu Pumps and Systems Ltd, prepared by AtliQ Technologies.

## Document inventory

The four documents in this directory represent the standard document chain produced by forward deployed engineering teams during enterprise engagements:

- `FDE_Roadmap_2026.pdf` - Codebasics Forward Deployed AI Engineer Roadmap 2026 (19 pages). Comprehensive 24-week curriculum covering technical competencies, product management, soft skills, and 12 core operating principles derived from practitioner interviews.
- `01_BRD_VaayuPumps_FieldServiceAI_v1.1.pdf` - Business Requirement Document v1.1 (25 pages). Baselined specification defining business context, manual process bottlenecks, measurable success metrics, MoSCoW functional requirements, and acceptance criteria.
- `02_TDD_VaayuPumps_FieldServiceAI_v1.0.pdf` - Technical Design Document v1.0 (25 pages). Low-level implementation specification defining supervised multi-agent pipeline topology, Pydantic schemas, API contracts, routing logic, decision tables, and developer testing rubrics.
- `03_SDD_VaayuPumps_FieldServiceAI_v1.0.pdf` - Solution Design Document v1.0 (33 pages). High-level and low-level architecture defining system boundaries, component models, technology selection rationale, on-premise and VPC hybrid topology, egress security, and telemetry.

## Enterprise client context: Vaayu Pumps and Systems Ltd

The specification suite models an authentic industrial equipment manufacturer operating under tight physical and contractual constraints:

- Corporate profile - Founded 1994, headquartered in Pune, manufacturing industrial centrifugal pumps and compressors with annual revenue of 840 crore INR.
- Service operational volume - Installed base of approximately 11,000 industrial pumps across 1,400 customer sites, supported by 42 field service technicians operating from six regional depots.
- Intake bottleneck - 180 service complaints received weekly across three uncontrolled channels (unmonitored email inbox, WhatsApp Business account, and regional depot phone logs).
- Baseline performance - Average triage latency of 47 minutes per ticket, 31.0% initial diagnosis error rate, and annual liquidated damages exceeding 1.4 crore INR due to contractual SLA breaches on critical continuous-process pump installations.

## The enterprise specification hierarchy

Enterprise deployments fail when teams jump directly from executive slide decks to source code. Professional forward deployed engineering follows a four-tier document contract where each tier answers one fundamental question and is signed off by specific customer stakeholders:

1. Business Requirement Document (BRD) - Answers what the business needs, why, and what measurable criteria determine commercial acceptance. Signed off by the client executive sponsor (COO/VP Service).
2. Solution Design Document (SDD) - Answers what the system is made of, where each component runs, why specific technologies were selected over alternatives, and how cross-cutting concerns (security, latency, data residency) are satisfied. Signed off by client enterprise architecture and security leadership.
3. Technical Design Document (TDD) - Answers how the system behaves at the boundary and component level, specifying API contracts, schema validations, error recovery state machines, and routing thresholds. Signed off by the engineering delivery lead.
4. Source code and automated test suite - Implements the verified contracts and proves conformance against the traceability matrix.

## Core technical architecture summary

The Vaayu Pumps Field Service Command Centre (`VPS-FSCC-2026`) implements a supervised multi-agent pipeline with deterministic guardrails:

- Ingestion agent - Validates channel payload, extracts unstructured complaint narrative, deduplicates against open work orders, and executes customer account lookup.
- Diagnosis agent - Analyzes failure symptoms against equipment master records (SAP PM `IE03`), historical fault logs, and pump telemetry to generate root cause hypotheses with confidence scores.
- Dispatch agent - Evaluates technician proximity, regional depot spare parts availability (SAP MM `MMBE`), and technical certification matrices to calculate optimal work order assignments.
- Memory and routing agent - Evaluates overall system confidence against a 0.85 threshold. Ingests human supervisor overrides into a dynamic memory layer to prevent recurring misclassifications.
- Deterministic enterprise integration - Emits validated service order mutations directly to SAP S/4HANA via Cloud Platform Integration (SAP CPI) using standard Remote Function Calls (`BAPI_ALM_ORDER_MAINTAIN`), maintaining SAP as the single system of record.

## Related documents

- [The 24-Week Enterprise FDE Roadmap](../learning-paths/24-week-enterprise-fde-roadmap.md) - complete week-by-week implementation guide based on `FDE_Roadmap_2026.pdf`
- [Enterprise Manufacturing Case Study](../case-studies/05-enterprise-manufacturing-vaayu-pumps.md) - exhaustive operational walkthrough of the Vaayu Pumps deployment
- [From Requirements to Spec](../customer/02-requirements-to-spec.md) - detailed methodology for writing testable BRD and TDD contracts
- [APIs and Integrations](../engineering/02-apis-and-integrations.md) - enterprise ERP and SAP integration architecture
- [Supervised Multi-Agent Systems](../ai/02-agents-and-tools.md) - implementation patterns for human-in-the-loop agent workflows

## Further reading

- [SAP BAPI Documentation: Plant Maintenance](https://help.sap.com) - official technical reference for maintenance order function modules
- [Codebasics FDE Roadmap Video](https://youtu.be/uE4HTkDtp48) - end-to-end video walkthrough of the forward deployed engineer learning pathway
