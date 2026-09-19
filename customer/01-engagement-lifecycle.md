# The Engagement Lifecycle

Every customer engagement is unique in its tech stack and organizational politics; the delivery
phases are not. This document is the master operational blueprint: ten disciplined phases spanning
the initial technical account review to the day the customer's engineering organization operates
the system autonomously.

Each phase establishes explicit **Inputs**, **Core Activities**, **Deliverable Artifacts**,
**Measurable Exit Criteria**, and **Failure Warnings**. Every other document in this customer
engineering section deepens one specific phase—read this master framework first to understand
where your engagement sits.

```
+---------------------------------------------------------------------------------------------------+
|                               THE 10-PHASE ENTERPRISE DELIVERY LIFECYCLE                          |
+---------------------------------------------------------------------------------------------------+
|  1. Pre-Engagement Context   --->   2. Kickoff & Charter   --->   3. Discovery & Shadowing        |
|                |                              |                              |                    |
|  4. Requirements to Spec     <---   5. Architecture & SecOps <---   6. Walking Skeleton & PoC     |
|                |                              |                              |                    |
|  7. Production Integration   --->   8. Evaluation & Pilot  --->   9. Production Launch & Control  |
|                                               |                                                   |
|                                    10. Handover & Upstream Feedback                               |
+---------------------------------------------------------------------------------------------------+
```

---

## The 10-phase enterprise delivery framework

Enterprise client engagements fail when teams drift forward without written alignment. While
technical discovery may inform architecture, and integration may reveal new data quirks,
**phase exits must never be informal**. Phase transitions require explicit, documented exit
criteria signed off by both vendor and customer stakeholders.

---

### 1. Pre-engagement context & technical feasibility check

- **Purpose**: Arrive with account history, political awareness, and a verified technical fit check—never a blank page.
- **Inputs**: Sales handoff notes, CRM history, preliminary RFP disclosures, customer public tech stack disclosures.
- **Core Activities**:
  - Review prior account history: past failed initiatives, vendor relationships, open escalations, and executive sponsors.
  - Run a technical feasibility check: verify that the customer's throughput, latency, and compliance requirements fall within your product's verified capabilities, rather than unvalidated sales promises.
  - Staffing alignment: establish who is deployed (Lead FDE, Data Engineer), for how many weeks, and who provides tier-2 internal engineering escalation.
- **Deliverable Artifacts**: Account Brief, Technical Feasibility Assessment, Engagement Staffing Charter.
- **Measurable Exit Criteria**: The Lead FDE can articulate the customer's core problem in one measurable sentence and identify the relationship owners and technical gatekeepers.
- **Failure Warning**: The FDE team arrives fluent in the product demo but completely blind to the customer's three previous failed vendor pilots.

---

### 2. Kickoff, governance charter, & access inventory

- **Purpose**: Convert high-level business intent into a signed delivery charter with named stakeholders, escalation cadences, and Day-1 access requests.
- **Inputs**: Executed Statement of Work (SOW), client organizational chart, Account Brief.
- **Core Activities**:
  - Define success metrics in writing: baseline error rates, target accuracy thresholds, latency budgets, and review milestones.
  - Establish the multi-stakeholder RACI matrix (Responsible, Accountable, Consulted, Informed) across technical leads, executive sponsors, and InfoSec.
  - Establish meeting cadence: weekly executive demos, daily standup channels, and emergency escalation paths.
  - File all access requests on Day 1 (repos, VPNs, bastions, data lakes, container registries) using the [Access Dependency Log](03-working-in-customer-environments.md#the-access-dependency-log).
- **Deliverable Artifacts**: Engagement Charter, RACI Matrix, Access Dependency Log, Shared Milestones Calendar.
- **Measurable Exit Criteria**: A signed Engagement Charter acknowledged in writing by the customer's executive sponsor.
- **Failure Warning**: Kickoff ends with enthusiastic smiles but zero written success metrics; later trade-offs and delays are judged by subjective executive memory.

---

### 3. Discovery, workflow shadowing, & data auditing

- **Purpose**: Replace sales-time assumptions with empirical data observed directly from operational floor workflows.
- **Inputs**: Current SOP documents, sample database exports, ticket queues, triage logs.
- **Core Activities**:
  - Shadow actual operational users: sit beside Tier-1 support operators, data analysts, or underwriters to observe edge cases, undocumented workarounds, and tribal spreadsheet habits.
  - Audit live data sources: evaluate schema completeness, null distributions, timestamp formats, and PII presence.
  - Quantify the operational baseline: measure current error rates, first-response latencies, and labor costs per ticket.
- **Deliverable Artifacts**: Workflow Journey Map, Data Quality Audit, Quantified Problem Statement.
- **Measurable Exit Criteria**: A Quantified Problem Statement accepted and verified by the customer's operational team leads.
- **Failure Warning**: Conducting discovery interviews exclusively with senior engineering managers, generating requirements for a theoretical workflow nobody actually executes on the floor.

---

### 4. Requirements alignment & executable spec signing

- **Purpose**: Transform discovery findings into an agreed, binding engineering contract settling scope, acceptance criteria, and non-goals.
- **Inputs**: Quantified Problem Statement, Data Quality Audit, Product Architecture Boundaries.
- **Core Activities**:
  - Draft the engineering specification following the standard [One-Page Spec Skeleton](02-requirements-to-spec.md#the-one-page-spec-skeleton).
  - Codify behavior criteria in executable Given/When/Then format (e.g. [ETISE Specification](02-requirements-to-spec.md#the-agreed-engineering-specification)).
  - Define explicit Non-Goals: write down what Phase 1 will *not* touch, protecting the schedule from silent scope creep.
  - Execute the 24-hour silent review ritual and capture all objections as assigned open questions.
- **Deliverable Artifacts**: Engineering Specification (`requirements.md` / `SPEC-2026-v1`), Executable Acceptance Criteria List, Open Question Log.
- **Measurable Exit Criteria**: Formally signed specification by the Lead FDE, Customer Tech Lead, and InfoSec Officer, with zero unassigned open questions.
- **Failure Warning**: The specification is circulated via Slack, praised verbally, but never signed; subsequent scope debates lack an agreed reference document.

---

### 5. Architecture, threat modeling, & SecOps clearance

- **Purpose**: Design the system inside the customer's architectural, network, and compliance boundaries before writing integration code.
- **Inputs**: Signed Engineering Specification, Customer Cloud Security Whitepapers, VPC Topology Diagrams.
- **Core Activities**:
  - Select deployment topology: customer-tenant VPC, private container enclave, hybrid gateway, or managed SaaS.
  - Formalize Architectural Decision Records (ADRs) documenting evaluated options, security trade-offs, and rejected paths.
  - Conduct security threat modeling: identify PII egress paths, secrets handling, data retention boundaries, and token expiration lifecycles.
  - Submit security architectures for SecOps and compliance clearance (SOC 2, GDPR Article 11.3, HIPAA).
- **Deliverable Artifacts**: Target Architecture Blueprint, Architectural Decision Records (ADRs), SecOps Clearance Package.
- **Measurable Exit Criteria**: Written SecOps and network architecture approval from the customer's security review board.
- **Failure Warning**: Developing an architecture that assumes open internet access, only to discover during deployment that the customer requires air-gapped container registries and private SSM bastions.

---

### 6. Walking skeleton, PoC gating, & risk de-risking

- **Purpose**: Eliminate the highest technical risk with a thin, end-to-end executable slice before investing in polish.
- **Inputs**: Approved Architecture Blueprint, Mock Contract Schemas, Sample Test Records.
- **Core Activities**:
  - Build the **Walking Skeleton**: an end-to-end pipeline connecting API ingress, ingestion, tokenization, mock model inference, and output queues (implemented in [`portfolio/reference-project/src/`](../portfolio/reference-project/README.md)).
  - Implement mock adapters to validate interface contracts while customer IAM/SSO approvals queue.
  - Demo the walking skeleton live to operational users, validating latency and data shapes.
- **Deliverable Artifacts**: Executable Walking Skeleton, Integration Test Suite, PoC Risk De-Risking Report.
- **Measurable Exit Criteria**: A functional end-to-end slice processing synthetic payloads across all architectural boundaries without crashing.
- **Failure Warning**: Spending two months polishing an isolated local UI while the core network connectivity and authentication pipeline remain unproven.

---

### 7. Production integration, auth/IAM, & pipeline hardening

- **Purpose**: Wire the proven prototype into real customer infrastructure, enterprise identity providers, and live databases.
- **Inputs**: Approved IAM credentials, VPC peering configurations, internal API endpoints.
- **Core Activities**:
  - Implement enterprise authentication: mutual TLS, OAuth2/OIDC service accounts, AWS IAM role assumption, and [RBAC header filtering](../portfolio/reference-project/tests/test_server.py).
  - Harden data ingestion: implement deterministic PII sanitization (masking SSNs, credit cards, IBANs), schema validation, and dead-letter exception queues.
  - Implement idempotency enforcement with SHA-256 tokens to prevent double-processing on network retries.
  - Run non-production integration stress testing against historical database dumps.
- **Deliverable Artifacts**: Production Integration Pipeline, IAM Configuration Manifests, Hardened Ingestion Engine.
- **Measurable Exit Criteria**: Unattended, automated processing of historical customer data batches in staging with zero unhandled exceptions.
- **Failure Warning**: Testing exclusively against pristine sample fixtures and experiencing total pipeline collapse when encountering unescaped nulls and corrupted encodings in real data.

---

### 8. Golden dataset evaluation, canary pilot, & quality gates

- **Purpose**: Statistically prove model accuracy, safety, and business value against written bars before declaring production readiness.
- **Inputs**: Staging Integration Pipeline, Curated Golden Evaluation Dataset.
- **Core Activities**:
  - Curate the Golden Dataset: 25+ canonical evaluation cases reflecting real-world distributions, adversarial inputs, and regulatory disputes ([`evals/DATASET_PROVENANCE.md`](../portfolio/reference-project/evals/DATASET_PROVENANCE.md)).
  - Execute automated evaluation benchmarks asserting hard statistical gates (Category Accuracy $\ge 88\%$, Severity Accuracy $\ge 90\%$, $100\%$ Citation Grounding) using [`portfolio/reference-project/evals/run_evals.py`](../portfolio/reference-project/evals/run_evals.py).
  - Launch a constrained canary pilot: deploy the system to a 10% user group in shadow or suggestion-only mode with operator override logging.
  - Conduct weekly joint evaluation reviews where both vendor and customer inspect identical telemetry.
- **Deliverable Artifacts**: Golden Evaluation Suite, Automated Evaluation Scorecards, Canary Pilot Review Report.
- **Measurable Exit Criteria**: The system meets or exceeds all statistical quality gates established in Phase 4 for two consecutive weeks.
- **Failure Warning**: Running a pilot without pre-agreed numerical success thresholds, allowing the pilot to terminate on executive fatigue rather than empirical proof.

---

### 9. Production launch, rollout control, & kill switches

- **Purpose**: Transition into live production operation with strict rollout controls, telemetry dashboards, and emergency rollback switches.
- **Inputs**: Successful Canary Pilot Sign-Off, Production Readiness Review.
- **Core Activities**:
  - Execute the [Production Readiness Checklist](../deployment/03-production-readiness-checklist.md): verify distributed tracing, alerts, Prometheus metrics, and automated backups.
  - Deploy behind feature flags (`ETISE_SHADOW_MODE=false`) enabling progressive volume scaling (10% $\rightarrow$ 25% $\rightarrow$ 50% $\rightarrow$ 100%).
  - Verify emergency kill switches: validate that flipping a configuration flag instantly reverts traffic to legacy systems without service downtime.
  - Establish 24/7 on-call coverage across both vendor and customer engineering rotations.
- **Deliverable Artifacts**: Production Deployment Runbook, Rollout Feature Flags, Live Telemetry Dashboards, Incident Escalation Matrix.
- **Measurable Exit Criteria**: System running at 100% production traffic within agreed latency and error SLAs, with telemetry actively monitored by both teams.
- **Failure Warning**: Launching the day before an enterprise corporate change freeze with untested rollback procedures, transforming the first transient bug into a Sev-0 trust crisis.

---

### 10. Operational handover, runbook validation, & upstream feedback

- **Purpose**: Transfer sustainable operational autonomy to the customer's engineering team and codify reusable architectural patterns for your core product.
- **Inputs**: Live Production System, Operational Runbooks, Training Curriculum.
- **Core Activities**:
  - Execute the **Operational Handover Triad**: runbooks, test suites, and named ownership.
  - Conduct reverse-shadowing operational shifts: customer on-call engineers triage live alerts and perform maintenance while the FDE observes silently.
  - Formulate SLA support boundaries: define Tier-1, Tier-2, and vendor Tier-3 escalation protocols and response time windows.
  - Feed architectural insights, edge cases, and missing platform features back to core product management.
- **Deliverable Artifacts**: Validated Operational Runbooks, Recorded Admin Training Sessions, Formal SLA Agreement, Product Feedback Whitepaper.
- **Measurable Exit Criteria**: Customer engineering manages production operations unaided for 30 consecutive calendar days with zero vendor interventions.
- **Failure Warning**: The FDE departs immediately after launch, leaving behind an undocumented, bespoke system that collapses during the first post-deployment schema migration.

---

## The phase-gate governance matrix

To prevent project drift, transitions between major phases require formal Phase-Gate reviews. If
a phase fails its gate criteria, the engagement must pause, remediate, or pivot—never stumble forward.

| Phase Transition | Gate Review Name | Required Artifacts | Approving Stakeholders | Stop / Pivot Condition |
|---|---|---|---|---|
| **Phase 2 $\rightarrow$ 3** | Charter Gate | Engagement Charter, Access Log | Customer VP, Lead FDE | Critical IAM access blocked $> 10$ days |
| **Phase 4 $\rightarrow$ 5** | Spec Gate | Signed `requirements.md`, Given/When/Then criteria | Customer Tech Lead, Lead FDE, InfoSec | Unagreed scope or missing baseline data |
| **Phase 5 $\rightarrow$ 6** | Architecture Gate | ADRs, Threat Model, SecOps Clearance | Customer SecOps, Vendor Architect | InfoSec rejection or tenant egress violation |
| **Phase 6 $\rightarrow$ 7** | PoC De-Risk Gate | Working Skeleton, Integration Test Suite | Customer Tech Lead, Lead FDE | Latency $> 5\times$ budget or unviable API |
| **Phase 8 $\rightarrow$ 9** | Quality Gate | Golden Eval Report, Canary Override Logs | Customer VP, Support Ops Lead | Category accuracy $< 88\%$ or hallucinated citations |
| **Phase 9 $\rightarrow$ 10** | Handover Gate | Validated Runbooks, Reverse-Shadowing Log | Customer Ops Lead, Lead FDE | Customer team cannot resolve simulated P1 alert |

---

## Why GenAI pilots fail: The MIT NANDA empirical reality

An authoritative investigation by the MIT NANDA initiative (covered extensively in Fortune,
August 2025) uncovered that approximately **95% of enterprise Generative AI pilots failed to deliver
measurable P&L impact**.

The root causes do not stem from model parameter size or token context windows; they cluster
overwhelmingly around **workflow integration and operational governance**:

```
                  MIT NANDA REPORT: ROOT CAUSES OF PILOT STALLS
+-------------------------------------------------------------------------------+
|  1. Workflow Mismatch (42%): AI isolated in a side-chat rather than embedded  |
|     directly into enterprise CRM, ERP, or ticketing systems of record.        |
|  2. Unenforced Evaluation Gates (28%): Pilots evaluated on subjective vibes   |
|     rather than statistically grounded golden benchmarks and edge cases.      |
|  3. Data Friction & Compliance Rejection (18%): Inadequate PII tokenization   |
|     and late-stage SecOps vetoes halting production deployment.               |
|  4. Handover Failure (12%): Systems requiring continuous vendor babying with  |
|     zero internal operational ownership post-launch.                          |
+-------------------------------------------------------------------------------+
```

The 10-phase lifecycle is explicitly engineered to neutralize these four failure modes:
- **Phase 3 (Discovery & Shadowing)** eliminates Workflow Mismatch by observing real floor processes.
- **Phase 4 (Requirements) & Phase 8 (Evaluation)** eliminate Subjective Evaluation via golden datasets and hard statistical gates.
- **Phase 5 (Architecture & SecOps)** prevents late-stage compliance vetoes via Day-1 threat modeling.
- **Phase 10 (Handover Triad)** eliminates Handover Failure via reverse-shadowing.

---

## The operational handover triad

An engagement is never complete at launch. Launch is an adrenaline-fueled milestone celebrated with
executives; handover is the quiet, disciplined transfer of operational responsibility to customer
engineers who did not build the codebase.

Enforce the **Handover Triad**—all three legs are mandatory:

```
                          THE HANDOVER TRIAD
                             +---------+
                             | Runbooks|
                             +----+----+
                                  |
                                  |
                        +---------+---------+
                        |                   |
                  +-----+-----+       +-----+-----+
                  |   Tests   |       | Ownership |
                  +-----------+       +-----------+
```

1. **Self-Contained Runbooks**: A customer engineer who has never seen the source code must be able
   to diagnose and resolve a simulated P1 incident (e.g. queue backup, token expiration, database
   reconnection failure) using step-by-step terminal commands without contacting the FDE.
2. **Automated Regression & Quality Tests**: The customer must be able to verify that an upstream
   API upgrade or model fine-tune introduced zero regressions by running local test suites
   ([`test_server.py`](../portfolio/reference-project/tests/test_server.py)) and automated golden
   evaluations ([`run_evals.py`](../portfolio/reference-project/evals/run_evals.py)).
3. **Named Customer Ownership & Reverse Shadowing**: Component ownership is mapped to specific
   customer individuals in PagerDuty/Opsgenie. During the final 30 days, the customer handles all
   tier-1 and tier-2 operational alerts while the FDE observes in silence.

---

## Weekly engagement health audit

Every Monday morning, the engagement lead must execute this 10-point operational health audit.
Any item remaining unchecked for two consecutive weeks represents an active schedule or delivery risk:

- [ ] We demonstrated working software to operational users this week (no slides-only demos).
- [ ] Every active issue and open question has a named owner and a concrete calendar due date.
- [ ] Access blockers are documented transparently in the executive dashboard, not absorbed privately.
- [ ] The written specification still matches 100% of what is actively being implemented in code.
- [ ] Customer engineering could execute a cold-restart and deploy the service if the FDE team vanished.
- [ ] The Lead FDE can state current benchmark evaluation accuracy numbers without checking notes.
- [ ] The executive champion received a concise, data-driven status broadcast this week.
- [ ] Architectural decisions and operational post-mortems are recorded while fresh.
- [ ] Next phase's formal exit criteria are documented and agreed upon before exiting the current phase.
- [ ] The reverse-shadowing handover calendar is scheduled and accepted by customer team leads.

---

## Direct codebase defense mappings

The phases of this lifecycle map directly to executable assets and test fixtures across this repository:

| Lifecycle Phase | Repository Asset / Defense Pattern | Operational Role |
|---|---|---|
| **Phase 3 & 4 (Spec & Discovery)** | [`customer/02-requirements-to-spec.md`](02-requirements-to-spec.md) | Formats Given/When/Then acceptance criteria and measurable baselines |
| **Phase 5 & 6 (Walking Skeleton)** | [`portfolio/reference-project/src/`](../portfolio/reference-project/README.md) | FastAPI walking skeleton with mock fallbacks and hybrid retrieval |
| **Phase 7 (Integration & Auth)** | [`portfolio/reference-project/tests/test_server.py`](../portfolio/reference-project/tests/test_server.py) | Verifies idempotency replays, RBAC role filtering, and exception queues |
| **Phase 8 (Golden Evaluation)** | [`portfolio/reference-project/evals/run_evals.py`](../portfolio/reference-project/evals/run_evals.py) | 25-case golden evaluation harness asserting $\ge 88\%$ accuracy and $100\%$ citations |
| **Phase 9 (Production Incident SRE)** | [`troubleshooting/01-debugging-methodology.md`](../troubleshooting/01-debugging-methodology.md) | 7-phase incident response lifecycle, Sev-0..Sev-3 SLA matrix, and post-mortems |
| **Phase 10 (Handover & Defense)** | [`troubleshooting/02-debugging-customer-systems.md`](../troubleshooting/02-debugging-customer-systems.md) | 6-tier visibility ladder and diagnostic commands for customer environments |

---

## Related documents

- [Requirements to spec](02-requirements-to-spec.md) - phase 4 in full detail: converting discovery notes into signed contracts
- [Working in customer environments](03-working-in-customer-environments.md) - tactical navigation of Day 1–5 onboarding and bastions
- [Managing expectations](04-managing-expectations.md) - calibrated de-escalation and the Trust Equation across the lifecycle
- [The FDE loop](../role/05-the-fde-loop.md) - the core operational mental model instantiated by these phases
- [Prototype to production](../deployment/01-prototype-to-production.md) - bridging the transition between Phase 6 and Phase 9
- [Discovery and requirements](../skills/02-discovery-and-requirements.md) - hands-on interview and shadowing toolkits for Phase 3

## Further reading

- [MIT NANDA Report: The GenAI Divide in Business](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo) -
  Fortune's investigation into why 95% of enterprise AI pilots fail without workflow integration
- [Site Reliability Engineering: Managing Incidents](https://sre.google/sre-book/managing-incidents/) -
  Google SRE principles for operational handover, on-call rotations, and post-mortem rituals
- [Anthropic Forward Deployed Engineer Guide](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) -
  canonical enterprise role expectations for end-to-end customer deployment lifecycles
