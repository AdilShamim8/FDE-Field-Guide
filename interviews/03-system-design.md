# System Design Rounds

This file is for candidates preparing for the design round of an FDE loop. You get why the round is customer-flavored, how it runs, the signals interviewers score, a seven-step framework with the constraint questions, two fictional worked examples, and the anti-patterns that sink otherwise strong candidates.

## The round is customer-flavored

FDE system design is never "design Twitter". The question arrives wearing a customer: design a document assistant for an insurance back office that will not let data leave its region, or a triage service for a company whose ops team is two people. The discipline under test is designing under constraints you did not choose, for an operator you must keep employed.

The evidence and patterns behind that framing:

- Reddit practitioner threads (2026, anecdotal) report loops that "care less about textbook distributed systems and more about whether you can reason about real-world" customer systems
- The Cohere practitioner account lists system context, scale assumptions, reliability decisions, and security constraints as the content of the design conversation ([gaijineer.co](https://gaijineer.co), April 2026, pattern tier)
- Anthropic's FDE posting requires building production applications inside customer systems ([greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/5302966008), 2026, observed evidence), which is the skill the round proxies

The full design method this round compresses is in [architecture for customer systems](../system-design/01-architecture-for-customer-systems.md); this file is the interview-length version.

## How the round runs

The shape is consistent across practitioner reports (pattern):

- Prompt - a customer scenario with named constraints: data volumes, compliance rules, existing systems, and how mature the ops team is
- Role-play - the interviewer plays a technical stakeholder and interjects mid-design: a new compliance rule, a hard deadline, a skeptical ops lead
- Time - 45-60 minutes, of which the constraint conversation should be a substantial fraction, not a preamble

The medium is usually a shared whiteboard or document. Draw coarse before fine: boxes and arrows first, technology names only where they are decisions rather than defaults. Thinking aloud is the norm here, and silence is scored as absence of reasoning even when your head is full of it - this is our interpretation, but it matches how every practitioner account describes the round.

If the prompt ships without constraints, that is the test: the missing constraints are yours to discover.

## What interviewers score

This list is our interpretation, drawn from how the round mirrors the job:

- Constraint discovery before designing - did you ask about their cloud, identity system, compliance regime, and data before drawing boxes
- Scoped requirements - did you pin down what "works" means and what is explicitly out of scope
- Fit to their estate - does the design use their stack and their ops model, or import the one from your last engagement
- Trade-offs named explicitly - cost against latency, build against buy, batch against real-time, said out loud
- Security and data boundaries raised unprompted - what leaves the customer boundary, and who approved it
- Evaluation and monitoring included - how quality is measured and watched after launch, not just whether it launches
- Rollout and rollback thinking - how the system lands in stages, and what happens when stage two fails
- Honest capacity assumptions - stated estimates with arithmetic, instead of "it scales"

## A framework for the round

We recommend this seven-step structure; it fits 45-60 minutes and covers the scoring list above:

1. Restate the problem and the success metric - one sentence each, and confirm them with the interviewer
2. Ask the constraint questions - the list below; do not start designing until the answers exist
3. Sketch the v1 boundary - what the first deployment includes and, out loud, what it excludes
4. Walk the request path end to end - one request through every box, including the failure path
5. Name the failure modes - the top three, each with a mitigation
6. Tell the rollout story - pilot scope, success criteria, promotion path, rollback trigger
7. Close with open questions - what you would need from the customer before build; this reads as experience, not weakness

### The constraint questions

- What cloud and accounts does this live in, and who administers them?
- What identity system must this integrate with, for users and for service auth?
- What data residency, compliance, or contractual rules apply, and where does the model run?
- Which existing systems must this read from or write to, and who owns them?
- What are the data volumes today, and at the horizon you care about?
- What latency do users actually need, and what would they tolerate?
- Who operates this after launch - how many engineers, and what on-call maturity?
- What is the cost ceiling, and who signs for it?
- What is the security review process, and how long does it take?
- What happens if this is wrong - what is the blast radius, and how reversible is a bad launch?

## Worked example: document Q&A under data residency

Fictional scenario: a 900-person insurance back office wants a question-answering assistant over its policy documents. Data residency rules are strict.

### The constraint questions to ask

Which region inference must run in; whether a hosted model with in-region processing satisfies the rule or self-hosted weights are required; what PII the documents contain and who may query what; how documents arrive and update; what the audit requirements are; who owns the corpus.

### The design shape

Scale changes the shape: 900 staff is a few requests per second at peak, so the interesting constraints are governance, not throughput. A typical shape: an ingestion pipeline into a document store, with per-document permissions carried through chunk metadata; retrieval over an in-region vector store; a model endpoint inside the customer's cloud region, via private endpoint or self-hosted weights depending on the residency answer; citations on every answer; and an audit log of queries. Evaluation: a golden set of 50-100 real questions with expected sources.

### The trade-offs to name

Hosted in-region model versus self-hosted weights (capability against compliance); index freshness against pipeline complexity; refusal behavior when retrieval misses, against the risk of confident wrong answers.

### The trap in the prompt

Designing a global-scale platform. The trap is spending the hour on sharding and multi-region replication for a system whose real risk is a permissions bug showing one policy document to the wrong employee.

## Worked example: ticket triage with two ops engineers

Fictional scenario: a SaaS company wants support-ticket triage - classify, prioritize, suggest a reply. The ops team is two people.

### The constraint questions to ask

What the current triage workflow is and where it lives; ticket volume and variance; what accuracy is acceptable before a misrouted ticket costs more than it saves; whether the team can tolerate operating a new service; what happens when the system fails today.

### The design shape

Boring technology wins: a queue-driven job that classifies new tickets with a hosted model, writes suggestions back into the existing helpdesk instead of building a new interface, and routes low-confidence cases to a human review queue. No Kubernetes, no new database where a table will do. Shadow mode first: suggestions logged but not applied, until accuracy is measured on real tickets.

### The trade-offs to name

Build versus buy (the helpdesk may already ship this); real-time versus batch, since triage is rarely latency-bound; per-ticket model cost against a cheaper batch window.

### The trap in the prompt

Ignoring who operates it. A system two people can run is the entire requirement; a technically superior design they cannot debug on a bad day fails the round regardless of its accuracy.

## Concrete capacity arithmetic for the round

Top-scoring candidates do not wave their hands and say it scales. They run back-of-the-envelope calculations aloud in the first fifteen minutes. We recommend memorizing these baseline sizing formulas:

### Ingestion throughput and vector storage

Scenario: 500,000 policy documents, average 10 pages per document.
- Raw text size: 500,000 docs * 10 pages * 3,000 characters per page = 15 GB raw text.
- Chunking strategy: 500 tokens per chunk with 10% overlap (50 tokens) yields approximately 8 chunks per page = 40,000,000 total chunks.
- Vector dimension: text-embedding-3-small (1536 dimensions) or text-embedding-3-large (3072 dimensions).
- Storage per vector: 1536 float32 values * 4 bytes = 6,144 bytes per chunk vector.
- Vector memory footprint: 40,000,000 chunks * 6.14 KB = approximately 245.7 GB of raw vector storage.
- With HNSW graph index overhead (M=16, efConstruction=64), budget an additional 1.2x to 1.5x RAM. Total RAM needed to keep index hot in memory: approximately 320 GB to 370 GB.
- Cost decision to state aloud: keeping 40 million vectors hot in RAM costs $1,200 to $1,800 per month on AWS or Azure. If query volume is low (e.g. 5 QPS during business hours), use pgvector with IVFFlat or disk-backed HNSW with SSD caches to cut infrastructure cost by 70%.

### Inference concurrency and token budget

Scenario: 2,000 concurrent insurance adjusters, generating 10 queries per minute per user at peak = 333 queries per second.
- Prompt token budget: System prompt (800 tokens) + 5 retrieved chunks (2,500 tokens) + conversation history (1,200 tokens) = 4,500 prompt tokens per request.
- Completion token budget: Structured answer with citations = 300 completion tokens.
- Total token throughput: 333 QPS * 4,800 tokens = approximately 1.6 million tokens per second.
- Architectural conclusion to state aloud: public LLM rate limits (e.g. Tier 5 limits of 500,000 TPM to 2M TPM) will throttle this traffic during spikes. You must provision dedicated provisioned throughput units (PTUs) or deploy a multi-region load-balanced gateway with regional rate limiters and token-bucket queuing.

## Enterprise blueprint 1: Private VPC agentic RAG under strict residency

### Architecture topology

```
[ Customer Browser ]
        |  (TLS 1.3 / Corporate SAML 2.0 / Okta)
        v
[ Enterprise API Gateway ] (Reverse Proxy + WAF + Mutual TLS)
        |
        +---> [ Query Rewriter & Intent Router ] (Small in-region LLM)
        |              |
        |              v
        +---> [ Hybrid Retrieval Engine ]
        |         |--> In-VPC BM25 Sparse Index (Elasticsearch/OpenSearch)
        |         +--> In-VPC Dense Index (pgvector / Qdrant)
        |              |
        |              v
        +---> [ Cross-Encoder Reranker ] (Cohere or BGE-Reranker in-VPC)
        |              |
        |              v
        +---> [ Generation & Citation Grounding Engine ] (In-Region LLM)
        |              |
        |              v
        +---> [ Guardrail & PII Redactor ] (Presidio / NeMo Guardrails)
        |
        +---> [ Append-Only Audit Ledger ] (S3 / Blob with WORM retention)
```

### Data boundary and security controls

- Data residency: zero customer text leaves the corporate AWS VPC or Azure subscription. Dedicated private endpoints (AWS PrivateLink or Azure Private Link) terminate model API traffic without traversing the public internet.
- Document-level access control: during ingestion, each document chunk inherits access control lists (ACLs) from the source repository (SharePoint, Google Workspace, or internal PostgreSQL). During retrieval, the user's active Active Directory groups are injected directly as SQL WHERE filters into the vector query, eliminating cross-tenant privilege escalation before the LLM prompt is assembled.
- Grounding verification: the generator must return exact source document IDs and character offsets. A deterministic validator verifies that every cited fact exists verbatim in the retrieved source text before presenting the answer to the user.

## Enterprise blueprint 2: Palantir-style operational ontology and triage

### What an operational ontology means in customer systems

In enterprise forward-deployed engagements, models do not interact directly with raw database tables. Instead, an ontology layer maps disconnected relational tables, object stores, and legacy APIs into concrete business entities: Customers, Invoices, Incidents, Facilities, and Actions.

```
+--------------------------------------------------------------------+
|                         ACTION LAYER                               |
|   Approve Invoice | Escalate Incident | Dispatch Field Technician   |
+--------------------------------------------------------------------+
                                 ^
                                 | (Validated Writeback with Human Gate)
+--------------------------------------------------------------------+
|                        ONTOLOGY LAYER                              |
|   Objects: Ticket, Account, Contract, Part, Technician             |
|   Links:   Account owns Ticket; Part belongs to Contract           |
|   Rules:   P0 incident requires VP notification within 15 min      |
+--------------------------------------------------------------------+
                                 ^
                                 | (Bi-directional Sync & Reconciliation)
+--------------------------------------------------------------------+
|                         DATA FOUNDATION                            |
|   Salesforce CRM | SAP ERP | Snowflake Warehouse | Zendesk Queue   |
+--------------------------------------------------------------------+
```

### Key architectural decisions for the ontology pattern

- Entity resolution: incoming events (e.g. an email from "Acme Intl" and a CRM record for "Acme Global") are resolved against a canonical entity registry using deterministic fuzzy matching and embedding nearest-neighbors.
- Writeback governance: the LLM never executes database INSERT or UPDATE statements directly. It proposes an Action with an explicit payload. If the action risk exceeds a defined threshold (e.g. modifying an invoice over $1,000), the action is routed to a human review inbox with a one-click approval interface and full diff visualization.
- Auditability: every state change records the prompt trace, the model ID, the active user session, and the human approver in an immutable event log.

## Rollout, rollback, and observability harness

Every credible system design response concludes with Day-2 operations.

### Rollout phases

1. Shadow phase (2 weeks): system ingests real requests, executes queries and classifications, logs recommendations to an internal telemetry database, but applies zero automated actions. Measures precision, recall, and latency against manual operator actions.
2. Assisted phase (4 weeks): system displays recommendations directly inside existing operator tooling (e.g. Zendesk sidebar or Salesforce widget). Operator accepts or overrides with one click, capturing direct feedback on misclassifications.
3. Autonomous low-risk phase: automated execution enabled only for transactions where confidence exceeds 0.92 and monetary or operational blast radius is under $250. High-risk transactions continue requiring human sign-off.

### Automated rollback triggers

- Error budget depletion: if 5xx HTTP responses exceed 0.5% over a rolling 10-minute window, traffic automatically fails over to the legacy rule engine or human-only queue.
- Hallucination canary: a background cron runs 20 synthetic golden queries every 5 minutes. If citation grounding verification fails on more than 1 canary query, the system switches to conservative refusal mode ("Service temporarily unable to ground response; routing to human specialist").

## Anti-patterns

- Designing for a billion users - the customer has 900 staff, and scale theater reads as not listening
- Ignoring who operates it - no owner, no runbook, and no on-call story means no design
- Forgetting model and data boundaries - where inference runs, what data leaves, and who approved it
- No rollback story - a rollout plan without a reverse gear is a bet, not a plan

All four anti-patterns share a root: answering the prompt as written instead of the customer behind it. The round rewards candidates who treat the scenario as a discovery artifact first and a design exercise second.

## Related documents

- [Coding round solutions](08-coding-solutions.md) - runnable implementations of integration and resiliency patterns
- [Architecture for customer systems](../system-design/01-architecture-for-customer-systems.md) - the full method this round compresses
- [Trade-offs and decision records](../system-design/03-trade-offs-and-decision-records.md) - how to name and record trade-offs
- [Deployment patterns](../deployment/02-deployment-patterns.md) - where the model runs, in depth
- [Evaluation and testing](../ai/03-evaluation-and-testing.md) - the evaluation half of a credible design
- [Customer scenario rounds](04-customer-scenarios.md) - when the design conversation meets stakeholder pushback
- [The interview process](01-interview-process.md) - where this round sits in the loop

## Further reading

- [AWS Architecture Blog: Exponential Backoff And Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/) - resilience in customer systems
- [gaijineer.co](https://gaijineer.co) - the Cohere practitioner account describing what the design conversation expects
- [Palantir Foundry Documentation](https://www.palantir.com/docs/foundry/) - operational ontology principles and entity modeling

