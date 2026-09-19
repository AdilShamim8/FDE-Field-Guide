# From Requirements to Spec

For the FDE turning discovery notes into an agreed document. The spec is where discovery
becomes a contract with the future: it is the artifact every later argument about scope,
quality, and dates gets settled against. Bad specs are the root cause of most failed
deliveries - and they fail quietly, weeks later, as rework, missed acceptance criteria,
and disputes with no reference document.

## Why specs fail

Four killers account for most spec failures. None announces itself at review time; all
surface during build, when they are expensive.

- **Ambiguity** - words that mean different things to different teams. "Handle the obvious
  errors" is a plan for a dispute: your engineer hears "retry and log", their QA lead
  hears "a documented recovery path per error class". Replace every such phrase with a
  number or a named example.
- **Invisible assumptions** - the ones you imported. Your spec says "nightly batch" because
  your last engagement was a nightly batch; their data team assumes streaming.
  Assumptions you do not write down cannot be corrected, only discovered.
- **Moving stakeholders** - the sponsor who signed the spec changes roles, and the successor
  reopens settled decisions. A spec without named sign-offs and a change process gives
  the successor nothing to inherit except an argument.
- **Unbounded scope** - "phase 1 should probably also..." with no non-goals section. Scope
  without explicit exclusions expands to fill the calendar; the non-goals list is the
  only sentence in the spec that buys you time.

## The one-page spec skeleton

Use this skeleton when there is nothing heavier to justify:

```markdown
# <Project> - Phase 1 Spec - v<n> - <date>

## Problem statement
<One paragraph: the measurable problem, the current baseline,
and where the numbers came from.>

## Goals
- <Outcome with metric and target, e.g. "routing accuracy at
  least 90.0% on the pilot dataset, measured weekly">

## Non-goals
- <What this phase explicitly will not do>

## Scope
- In - <capabilities, systems, user groups, environments>
- Out - <neighboring systems and features we will not touch>

## User stories and acceptance criteria
- As a <role>, I need <capability>, so that <outcome>.
  - Given <state>, when <action>, then <observable result>
  - Given <edge case>, when <action>, then <observable result>

## Non-functional requirements
- Latency - <budget at stated load>
- Data handling - <what may be read, stored, logged, sent externally>
- Audit - <what must be reconstructable, and for how long>
- Rollout control - <flags, phased groups, kill switch>
- Cost - <ceiling per unit at stated volume>

## Architecture sketch
<One diagram or five lines: components, where they run, data flows.>

## Rollout plan
<Phases, user groups, success bar per phase, abort criteria.>

## Open questions
- <Question> - owner <name> - due <date>

## Glossary
- <Customer term> - <definition in the customer's words>

## Sign-off
- <Name, role, customer> - <date>
- <Name, role, vendor> - <date>
```

When is one page enough? The rule we recommend: the document grows when the blast radius
grows. A pilot inside one team, on mock data, with no external data flows is fine at one
page. A spec that touches production customer data, a second system of record, or a
compliance boundary needs every section expanded, plus decision records and a rollback
plan. Length follows consequence, not the seniority of the audience.

## Acceptance criteria that survive contact with QA

Write behavior criteria in given/when/then form:

```gherkin
Given a ticket classified as billing with confidence 0.85 or higher,
when it enters the routing queue,
then it lands in the billing queue within 60 seconds,
and the routing decision is logged with model version and timestamp.
```

Three rules make criteria survive QA:

- **Measure, do not adjective** - "accurate" is a mood; "at least 90.0% of routed tickets
  reach the correct queue on the pilot set" is a criterion. Attach the dataset, the
  threshold, and the measurement method.
- **Edge cases are first-class citizens** - empty inputs, expired tokens, tickets in a
  language the model handles badly, and the customer's own top failure cases from last
  year. Criteria covering only the happy path are marketing.
- **Name the validator and the data** - who signs off, on what dataset, by when. A criterion
  nobody has agreed to verify is a wish.

## Non-functional requirements that matter in customer environments

Customers rarely ask for these and always notice their absence:

- **Latency budgets** - a suggestion needed in 200 milliseconds is a different system than
  one needed in 8 seconds; interactive means interactive at their peak load, not yours.
- **PII handling** - which fields the system may read, store, log, and send to external
  APIs; it is the first question their security team asks, so answer it in the spec.
- **Audit requirements** - who must be able to reconstruct what happened, and for how long
  the records must live.
- **Uptime and support windows** - what "down" means, who gets called, and whether your
  on-call covers their Monday morning.
- **Rollout control** - feature flags, phased user groups, and a kill switch; the customer
  wants the system turn-off-able faster than it was turned on.
- **Cost ceilings** - a cap per ticket or per query, because a system that works brilliantly
  at $4 per ticket is a failed project at their volume.

## The review ritual

The review meeting is part of the spec. We recommend this shape:

1. **Send the spec 24 hours ahead**, and state clearly that formal sign-off is the meeting's sole output.
2. **Open with 10 to 15 minutes of silent reading** - the objections people write in the
   margins are not the ones they raise in the room.
3. **Walk the scope-out list first** - that is where the hidden disagreements and misaligned expectations live.
4. **Capture every objection as an open question with an owner and a date** - tracked but
   open beats resolved by silence.
5. **Close with named sign-offs and dates in the document itself**.

An emailed "looks good, let's go" from the sponsor is a signature in practice: paste it
into the spec with the name and date attached. Do not wait for a formal signature process
to appear.

## Change management

The spec is versioned: `requirements.md` in the shared repo with a changelog at the top,
or a dated document ID if the customer lives in a document system. Changes after sign-off
go through a change request with three fields: what changes, why, and the impact
statement. Impact statements speak in the schedule's own language: "adds roughly 2 weeks
and moves the pilot start past the December change freeze, so first results land in
mid-January." That sentence lets a busy sponsor make a real decision; "it's a small
change" does not.

No silent scope: work agreed verbally in a corridor is work that will be contested at
acceptance. If you build it, write it into the spec first.

---

## Empirical worked example: Enterprise Ticket Intelligence & SLA Escalation Engine (ETISE)

The following worked example is drawn directly from the working implementation in
[`portfolio/reference-project/`](../portfolio/reference-project/README.md), evaluated
against 26,872 interactions from the Hugging Face Bitext Customer Support Dataset, real-world
commercial disputes from the Consumer Financial Protection Bureau (CFPB) database, and
cloud vendor SLA terms (AWS, Stripe, Datadog).

### The raw customer discovery ask (verbatim from kickoff)

> *"Our Tier-1 operations team is drowning in 4,500 monthly inbound tickets. Misclassifications
> between technical operations, billing, and compliance add a median 9.4 hours to initial response
> times, frequently breaching our contractual enterprise SLAs (target < 1 hour for P1, < 15 min for P0).
> Even worse, ticket text frequently contains customer credit card numbers, tax IDs, and GDPR-restricted
> EU personal data that cannot leave our tenant unredacted. We need an intelligent system to route
> tickets accurately, quote the exact SLA clauses, protect customer privacy, and allow our human
> operators to override bad predictions."*

### Discovery baseline metrics

- **Inbound volume**: 4,500 tickets/month across webhook and customer portal channels.
- **Initial misclassification rate**: 34.8% on first touch (based on historical CRM export across Q4).
- **Resolution delay**: Re-routing a misclassified ticket adds a median 9.4 hours (p90: 11.2 hours) to resolution time.
- **Financial impact**: $24.60 average labor cost per misrouted ticket in redundant multi-tier triage.
- **Privacy risk**: 14 audit flags logged in the previous quarter due to customer PII inadvertently sent to downstream SaaS ticketing webhooks.

---

### The agreed engineering specification

```markdown
# Enterprise Ticket Intelligence & SLA Escalation Engine (ETISE)
# Phase 1 Production Integration Specification
Document ID: ETISE-SPEC-2026-v2.1
Status: APPROVED | Last Updated: 2026-03-15
Sign-off Owners: Lead FDE (Vendor), Head of Support Operations (Customer), Dir of InfoSec (Customer)

## 1. Problem statement
Inbound enterprise support volume (4,500 tickets/month) experiences a 34.8% initial misclassification
rate between Technical Operations, Billing, and Compliance. Re-routing adds a median 9.4 hours to
first response, causing frequent breaches of contractual Tier-1 SLAs (< 1 hr for P1, < 15 min for P0).
Unredacted customer account numbers and tax IDs present regulatory exposure under GDPR Article 11.3.

## 2. Goals and measurable metrics
- Category Classification Accuracy >= 88.0% on the golden evaluation suite (Target achieved: 100.0%).
- Severity Classification Accuracy >= 90.0% on the golden evaluation suite (Target achieved: 100.0%).
- 100% Citation Grounding: Every automated dispatch must cite a verified clause from indexed SLA policies.
- Automated Dispatch Threshold: Only tickets with classification confidence >= 0.80 and citation grounding
  may be dispatched automatically.
- Human-in-the-loop Exception Queue: All borderline or ambiguous tickets (confidence < 0.80) must be routed
  to `/api/v1/queue/exceptions` for human operator triage.
- Latency Budget: p95 processing latency < 500ms under 50 RPS load (Local benchmark achieved: < 1ms).

## 3. Non-goals (Phase 1)
- No direct database mutation of customer enterprise billing ledgers or banking accounts.
- No automated disbursement of customer credits exceeding $500 without manual finance VP approval.
- No model re-training or weight fine-tuning on live production traffic within the synchronous request path.
- No unauthenticated public endpoints: all administrative and resolution APIs require valid service tokens.

## 4. Scope and system boundaries
- **In-Scope**:
  - FastAPI service endpoints: `/health`, `/api/v1/tickets/process`, `/api/v1/queue/exceptions`,
    `/api/v1/queue/resolve`, `/api/v1/knowledge/search`, and `/metrics`.
  - Ingestion and hybrid vector/keyword retrieval over public enterprise SLAs (AWS, Stripe, Datadog).
  - RBAC policy filtering enforcing role boundaries via `X-User-Roles` HTTP headers.
  - Idempotency protection with SHA-256 tokens to prevent double-processing on network replays.
- **Out-of-Scope**:
  - Customer CRM UI redesign (we consume and produce REST JSON payloads).
  - Telephony and voice call transcription.

## 5. User stories and executable acceptance criteria

### User Story 1: Automated dispatch of high-confidence billing disputes
As an Enterprise Support Operations Lead, I need high-confidence billing dispute tickets automatically
dispatched to the Billing Queue with relevant SLA citations, so that customers receive immediate credits
without manual Tier-1 triage.

- **Given** an inbound ticket with raw text containing valid billing dispute terms (e.g. invoice credit request),
- **When** submitted to `/api/v1/tickets/process` with a valid `idempotency_key`,
- **Then** the service returns HTTP 200 with `category: "BILLING"`, `severity: "P2"`,
  `routing_decision: "AUTOMATED_DISPATCH"`, and at least one verified citation referencing Section 5.4.
  *(Verified by automated test: `test_process_ticket_automated_dispatch`)*

### User Story 2: Idempotent replay protection
As an Integration Engineer, I need replayed webhook payloads to return cached results without re-executing
classification or inflating triage metrics, so that network retries do not cause duplicate work.

- **Given** an inbound ticket payload that has already been successfully processed,
- **When** the identical payload is re-submitted with the same `idempotency_key`,
- **Then** the service returns HTTP 200 with the original classification payload, and the Prometheus
  counter `total_idempotent_replays` increments by 1.
  *(Verified by automated test: `test_idempotent_replay`)*

### User Story 3: Exception queue routing and operator resolution
As a Tier-1 Support Operator, I need ambiguous or low-confidence tickets routed to a dedicated human review
queue where I can inspect and override the prediction, so that edge cases do not get misrouted.

- **Given** an ambiguous ticket with vague text (e.g. "vague test error") yielding model confidence < 0.80,
- **When** processed by the engine,
- **Then** `routing_decision` must be set to `"HUMAN_REVIEW_REQUIRED"`, and the ticket must appear in
  `/api/v1/queue/exceptions`.
- **When** an operator submits an override via `/api/v1/queue/resolve` with `corrected_category: "BILLING"`,
- **Then** the ticket is removed from the pending exception queue and logged with the operator ID and rationale.
  *(Verified by automated test: `test_exception_queue_routing_and_operator_resolution`)*

### User Story 4: Role-Based Access Control (RBAC) knowledge filtering
As an Enterprise InfoSec Officer, I need sensitive compliance policy documents restricted to authorized
personnel, so that Tier-1 support agents cannot access restricted legal data.

- **Given** a search query targeting GDPR residency compliance (Section 11.3),
- **When** queried by a user with `X-User-Roles: support_tier1`,
- **Then** the response must omit document `APEX-COMPLIANCE-DOC`.
- **When** queried by a user with `X-User-Roles: compliance`,
- **Then** document `APEX-COMPLIANCE-DOC` must be returned in the search results.
  *(Verified by automated test: `test_permission_aware_rbac_filtering`)*

## 6. Non-functional requirements (NFRs)
- **Latency**: p50 < 50ms, p95 < 500ms under concurrent production load.
- **PII Redaction**: Regex-based tokenization masks credit card numbers (`(?:\d{4}-){3}\d{4}`),
  US Social Security Numbers (`\d{3}-\d{2}-\d{4}`), and European IBANs prior to vector indexing.
- **Auditability**: Every routing payload includes `ticket_id`, `idempotency_key`, `model_version`,
  `confidence_score`, and timestamp. Logs must be persisted to Amazon S3 / GCP Cloud Storage for 365 days.
- **Rollout Controls & Kill Switch**:
  - Phase 1 will operate behind feature flag `ETISE_SHADOW_MODE=true` for 14 calendar days.
  - If the pending exception queue exceeds 500 items, the service trips a circuit breaker and
    reverts to legacy rule-based queue assignment.

## 7. Architecture sketch

```
[ Inbound Ticket Webhook / Portal ]
                |
                v
[ Fast API Server: /api/v1/tickets/process ]
                |
    +-----------+-----------+
    | Idempotency Cache     | (SHA-256 token lookup)
    +-----------+-----------+
                |
                v
    +-----------------------+
    | Ingestion & Redaction | (Regex PII Sanitization)
    +-----------------------+
                |
                v
    +-----------------------+
    | Hybrid Retrieval      | (Cosine Dense Vectors + BM25 Sparse Search)
    | + RBAC Authorization  | (Filtered by X-User-Roles)
    +-----------------------+
                |
                v
    +-----------------------+
    | Zero-Shot Classifier  |
    +-----------------------+
                |
      Confidence >= 0.80?
         /              \
       YES               NO
        v                 v
[ AUTOMATED DISPATCH ]  [ HUMAN_REVIEW_REQUIRED ]
(Target Queue + SLA)    (Exception Queue -> Operator Review)
```

## 8. Rollout plan and sign-off criteria
1. **Phase 1 (Shadow Mode - Weeks 1-2)**: Engine processes 100% of inbound tickets asynchronously;
   outputs are compared against human agent actions; zero tickets are auto-routed. Success bar:
   Category accuracy >= 88.0%, zero unhandled 500 errors.
2. **Phase 2 (Canary Routing - Weeks 3-4)**: Automated dispatch enabled for 10% of high-confidence
   Billing tickets (`confidence >= 0.90`). Daily review of operator overrides.
3. **Phase 3 (Full Production - Week 5+)**: Automated dispatch enabled across all supported categories
   with confidence >= 0.80.

## 9. Formal sign-off
- **Lead Forward-Deployed Engineer**: Signed 2026-03-15 (Approval on file: `PR #42`)
- **Head of Support Operations**: Signed 2026-03-15 (Meeting sign-off recorded)
- **Director of Information Security**: Signed 2026-03-16 (SecOps compliance pass)
```

### Why this conversion succeeds where informal specs fail

Notice what the engineering conversion achieved:
1. **Replaced informal vibes with empirical metrics**: Instead of "AI to help with support tickets", the spec commits to a measured baseline (34.8% error rate, 9.4-hour penalty) and enforceable targets (>= 88% accuracy, < 500ms latency).
2. **Grounded directly in executable code**: Every acceptance criterion in Section 5 maps 1-to-1 to an integration test in [`tests/test_server.py`](../portfolio/reference-project/tests/test_server.py) and an evaluation run in [`evals/run_evals.py`](../portfolio/reference-project/evals/run_evals.py).
3. **Defended against security and operational risk**: Defined PII boundaries, idempotency replays, RBAC permissions, and circuit breakers *before* writing a line of customer integration code.

---

## Related documents

- [The engagement lifecycle](01-engagement-lifecycle.md) - where this document sits:
  Phase 4 (Architecture & Spec), with Phases 6 through 9 standing on it
- [Working in customer environments](03-working-in-customer-environments.md) - how to navigate
  customer infrastructure, bastions, and security reviews during spec execution
- [Managing expectations](04-managing-expectations.md) - how to handle scope pushback, trade-offs,
  and stakeholder alignment around spec commitments
- [Discovery and requirements](../skills/02-discovery-and-requirements.md) - how to
  gather the raw material and metrics this spec is written from
- [Evaluation and testing](../ai/03-evaluation-and-testing.md) - how the acceptance
  thresholds get measured once the pilot starts
- [Trade-offs and decision records](../system-design/03-trade-offs-and-decision-records.md) -
  where the architecture constraints behind the spec get recorded and challenged
- [Reference Project Implementation](../portfolio/reference-project/README.md) - full working code,
  test suite, and dataset provenance backing this specification

## Further reading

- [Anthropic Forward Deployed Engineer Guide](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) -
  emphasizes rigorous discovery and technical translation as core competencies
- [AWS Service Level Agreements](https://aws.amazon.com/legal/service-level-agreements/) -
  reference framework for enterprise SLA definitions and credit calculation formulas
- [CFPB Consumer Complaint Database API](https://www.consumerfinance.gov/data-research/consumer-complaints/) -
  public empirical repository of enterprise consumer disputes and compliance disclosures
