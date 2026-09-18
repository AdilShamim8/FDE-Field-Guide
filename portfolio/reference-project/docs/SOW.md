# Statement of Work: Enterprise Ticket Intelligence Pilot

This document defines the formal scope of work, technical boundaries, delivery milestones, and acceptance criteria for the forward-deployed deployment of the Enterprise Ticket Intelligence and Grounded Synthesis Engine (ETISE).

## Engagement summary

- Customer: Apex Enterprise Cloud Services
- Provider: Forward Deployed Engineering Practice
- Timeline: 6-week pilot engagement
- Primary objective: Automate the categorization, triage, and policy-grounded draft response synthesis for 12,000 daily incoming support tickets, achieving at least an 85% reduction in manual triage latency while maintaining zero hallucinated citations.

## Scope boundaries

### In scope

- Ingestion of incoming support tickets via REST API and webhook endpoints.
- Extraction and schema validation of key fields: Account ID, Severity Level (P0 to P3), Defect Category, Affected System, and Summary.
- Automated knowledge grounding against the Apex Customer Service & SLA Handbook (PDF and Markdown formats).
- Human-in-the-loop exception queue for low-confidence classifications (< 0.85) and P0 incidents.
- Operational metrics dashboard tracking triage precision, recall, latency, and operator override rate.
- Golden evaluation harness with at least 25 edge-case scenarios.

### Explicitly out of scope

- Direct automated dispatch of responses to external end-customers without human review during Phase 1.
- Direct automated writebacks or schema alterations to customer enterprise ERP database tables.
- Ingestion of audio or telephony streams (deferred to Phase 2).
- Modification of existing customer Active Directory or Okta identity infrastructure.

## Deliverables and milestones

### Milestone 1: Discovery and environment validation (Week 1 to 2)

- Delivery of signed Architecture and Threat Model document.
- Ingestion pipeline running locally and verified against historical anonymized ticket sample.
- Acceptance criteria: Ingestion pipeline correctly parses 1,000 historical tickets with zero unhandled exceptions.

### Milestone 2: Core extraction and knowledge grounding engine (Week 3 to 4)

- Self-healing structured extraction module with automated schema repair.
- Hybrid search index over Apex SLA and Policy documentation.
- Acceptance criteria: Automated evaluation harness demonstrates field extraction precision above 90% and citation verification rate of 100% on golden dataset.

### Milestone 3: Operational queue and shadow deployment (Week 5)

- Exception review queue operational for support supervisors.
- System running in shadow mode alongside human triage team.
- Acceptance criteria: 99th percentile end-to-end processing latency under 1,500ms; zero disruption to existing ticket queues.

### Milestone 4: Handover and operational runbook sign-off (Week 6)

- Final delivery of production Docker containers, operations runbook, and staff training session.
- Executive Handover Memo presented to executive sponsors.
- Acceptance criteria: Formal sign-off on operations runbook by customer operations lead.

## Acceptance criteria sign-off matrix

- Performance: p95 latency <= 1,200ms across all ticket sizes up to 10,000 tokens.
- Precision: classification precision >= 88.0% across all defect classes.
- Citation integrity: 100% of generated citations match source policy text verbatim; zero ungrounded policy citations permitted.
- Reliability: 99.9% uptime of API ingestion endpoint during shadow phase.

## Related documents

- [Project README](../README.md) - project architecture and quickstart guide
- [Enterprise architecture](ARCHITECTURE.md) - component and threat model specifications
- [Operations runbook](SLA_RUNBOOK.md) - alert thresholds, on-call runbook, and rollback plans
- [The engagement lifecycle](../../customer/01-engagement-lifecycle.md) - field guide on engagement lifecycle phases

## Further reading

- [Requirements to spec](../../customer/02-requirements-to-spec.md) - converting customer conversations into binding specifications
- [Managing expectations](../../customer/04-managing-expectations.md) - scope boundaries and delivery contracts
