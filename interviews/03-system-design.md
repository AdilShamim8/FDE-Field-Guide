# System Design Rounds and Enterprise Boundary Architecture

This guide prepares candidates for the system design round of a Forward Deployed Engineer loop. Unlike general software engineering design interviews that emphasize consumer web scale ("design Twitter" or "design Netflix"), FDE system design tests your ability to architect production systems **under enterprise constraints you did not choose, inside legacy customer IT estates, for operators you must keep employed**.

---

## Why FDE System Design Is Different

In enterprise AI and platform engineering, the design challenge is rarely raw request volume; it is **governance, security boundaries, organizational legacy, and operational viability**:

- **Anthropic FDE Loop**: Focuses on designing production integrations directly inside customer cloud environments, handling strict egress limitations, and building robust human-in-the-loop workflows ([Anthropic Careers](https://job-boards.greenhouse.io/anthropic/jobs/5302966008)).
- **Cohere FDE Accounts**: Evaluates real-world system context, data residency, capacity budgeting, and on-call maintainability over abstract distributed theory ([Gaijineer](https://gaijineer.co)).
- **Palantir Deployment Philosophy**: Emphasizes operational ontologies, governed writebacks, and zero-egress VPC topologies over simple prompt wrappers.

The discipline under test is designing under constraints: What leaves the customer boundary? Who signs off on the data flow? How does the system fail safely? What happens at 3:00 AM when the upstream model provider degrades?

---

## What Interviewers Score

Interviewers evaluate candidates across eight core competencies:

| Competency | Strong Hire Signal | No Hire Signal |
| :--- | :--- | :--- |
| **Constraint Discovery** | Asks about identity (SAML/Okta), VPC peering, compliance (SOC 2, HIPAA), and data residency before drawing boxes. | Begins drawing microservice architectures before asking where the data lives or who operates the system. |
| **Estate Fit** | Reuses the customer's existing cloud services, databases, and logging infrastructure. | Insists on deploying a bespoke Kubernetes cluster and three new databases for an enterprise with two ops engineers. |
| **Data Boundary Discipline** | Explicitly defines private endpoints (AWS PrivateLink / Azure Private Link), VPC boundaries, and PII redaction gates. | Sends raw customer documents over the public internet to third-party SaaS endpoints without encryption or BAA agreements. |
| **Permission Inheritance** | Enforces document-level Access Control Lists (ACLs) at vector retrieval time, preventing cross-department data leaks. | Indexes all company documents into a single flat vector index, allowing any user prompt to retrieve executive payroll data. |
| **Capacity Arithmetic** | Calculates concrete vector memory footprints, QPS, token throughput, and GPU/PTU infrastructure costs aloud. | Hand-waves capacity with generic statements (*"We will just auto-scale on AWS"*). |
| **Explicit Trade-Offs** | Articulates trade-offs between hosted APIs vs. in-VPC weights, in-memory HNSW vs. disk-backed pgvector, and batch vs. real-time. | Treats technical choices as obvious defaults without stating cost, latency, or operational implications. |
| **Rollout & Rollback Story** | Designs phased rollouts (shadow mode -> assisted mode -> autonomous execution) with automated canary rollback triggers. | Proposes a big-bang cutover without fallback to legacy systems or automated failure containment. |
| **Day-2 Observability** | Builds structured JSON telemetry, correlation IDs, grounding validators, and dead-letter queues into the core design. | Treats logging and monitoring as an afterthought (*"We will add Datadog later"*). |

---

## The 7-Step Enterprise System Design Framework

Top candidates structure the 45–60 minute session using this seven-step cadence:

```
+-------------------------------------------------------------------------------+
|                 7-STEP ENTERPRISE SYSTEM DESIGN CADENCE                       |
+-------------------+-----------------------------------------------------------+
| 1. RESTATE & LOCK | Restate the business problem, user personas, and target   |
|    SUCCESS METRIC | SLA (e.g. 95th percentile latency < 2.5s, zero PII leak)  |
+-------------------+-----------------------------------------------------------+
| 2. DISCOVER ESTATE| Probe cloud VPC, IAM/Okta, compliance, existing DBs, and  |
|    & CONSTRAINTS  | on-call team size before drawing any architecture         |
+-------------------+-----------------------------------------------------------+
| 3. CAPACITY SIZING| Run back-of-the-envelope calculations aloud (RAM, QPS,    |
|    ARITHMETIC     | token budget, vector index bytes, infrastructure cost)    |
+-------------------+-----------------------------------------------------------+
| 4. SKETCH CORE V1 | Draw the end-to-end request flow with explicit data       |
|    BOUNDARY       | boundaries (private subnets, ingress WAF, audit ledger)   |
+-------------------+-----------------------------------------------------------+
| 5. DEEP DIVE &    | Address permission inheritance, grounding validation,     |
|    FAILURE MODES  | rate limiting, and circuit breaking                       |
+-------------------+-----------------------------------------------------------+
| 6. ROLLOUT & DAY-2| Detail shadow deployment, canary eval checks, automated   |
|    OPERATIONS     | rollbacks, and runbook hand-off                           |
+-------------------+-----------------------------------------------------------+
| 7. OPEN QUESTIONS | List unknown customer dependencies to resolve in discovery|
+-------------------+-----------------------------------------------------------+
```

### The 10 Essential Constraint Probes
1. **Cloud & Tenant Estate**: What cloud provider and region does this live in, and who holds root administrator access?
2. **Identity & Auth**: What identity provider must this integrate with (Okta, Azure AD, SAML 2.0), and how are permissions structured?
3. **Data Residency**: Does compliance or contract forbid customer text from leaving their private VPC or geographic region?
4. **Model Execution**: Can we call an external managed endpoint via private endpoint, or must we host open weights in-VPC?
5. **Existing Systems of Record**: Which ERPs, CRMs, or data lakes must this read/write, and what are their rate limits?
6. **Throughput & Concurrency**: What is the peak QPS and average document length today and in 12 months?
7. **Latency Tolerances**: Is this an interactive chat experience (< 2 seconds to first token) or an asynchronous background pipeline?
8. **Ops Team Maturity**: Who carries the pager after we leave—a 24/7 global SRE team or two systems administrators?
9. **Budget Ceiling**: What is the monthly infrastructure and token expenditure ceiling?
10. **Blast Radius of Inaccuracy**: What happens if the system hallucinates or errors—a minor inconvenience or an SEC/HIPAA regulatory fine?

---

## Concrete Capacity Arithmetic for the Interview

Top-scoring candidates do not wave their hands and say "it scales." They perform back-of-the-envelope calculations aloud in the first fifteen minutes.

### 1. Ingestion Throughput and Vector Storage Sizing
**Scenario**: 500,000 policy documents, average 10 pages per document.
- **Raw Text Size**:  
  $$500{,}000 \text{ docs} \times 10 \text{ pages} \times 3{,}000 \text{ chars/page} = 15 \text{ GB raw text}$$
- **Chunking Strategy**: 500 tokens per chunk with 10% overlap (50 tokens) yields $\approx 8$ chunks per page:  
  $$500{,}000 \times 10 \times 8 = 40{,}000{,}000 \text{ total chunks}$$
- **Vector Dimension**: `text-embedding-3-small` (1,536 dimensions) or `text-embedding-3-large` (3,072 dimensions).
- **Storage per Vector**:  
  $$1{,}536 \text{ float32 values} \times 4 \text{ bytes} = 6{,}144 \text{ bytes (6.14 KB) per vector}$$
- **Raw Vector Footprint**:  
  $$40{,}000{,}000 \times 6.14 \text{ KB} \approx 245.7 \text{ GB raw vector data}$$
- **HNSW Graph Memory Overhead**: With $M=16$ and $efConstruction=64$, budget an additional $1.2\times$ to $1.5\times$ RAM overhead. Total RAM to keep the index hot in memory: $\approx 320 \text{ GB}$ to $370 \text{ GB}$.
- **Architectural Conclusion to State Aloud**:  
  *"Keeping 40 million vectors hot in RAM requires a multi-node cluster (e.g. 3x `r6i.4xlarge` on AWS) costing $\approx \$1{,}800/\text{month}$. If peak query volume is low (e.g. 5 QPS during business hours), we should use PostgreSQL with `pgvector` and IVFFlat or disk-backed HNSW with SSD caching to cut infrastructure cost by over 70%."*

### 2. Inference Concurrency and Token Throughput Sizing
**Scenario**: 2,000 concurrent enterprise claim adjusters generating 10 queries/hour per user at peak = $\approx 6 \text{ QPS}$ average, $25 \text{ QPS}$ peak burst.
- **Prompt Token Budget**: System prompt (800 tokens) + 5 retrieved chunks (2,500 tokens) + conversation history (1,200 tokens) = $4{,}500 \text{ prompt tokens/request}$.
- **Completion Token Budget**: Structured JSON answer with exact citations = $300 \text{ completion tokens/request}$.
- **Total Token Throughput at Peak (25 QPS)**:  
  $$25 \text{ QPS} \times 4{,}800 \text{ tokens} = 120{,}000 \text{ tokens/sec} = 7{,}200{,}000 \text{ tokens/minute (TPM)}$$
- **Architectural Conclusion to State Aloud**:  
  *"Public cloud managed model tiers (standard 1M–2M TPM limit) will throttle us during 25 QPS peak bursts. We must either provision dedicated throughput units (e.g. Azure OpenAI PTUs or AWS Bedrock Provisioned Throughput) or implement a multi-region load-balanced gateway with client-side token-bucket rate limiting."*

---

## Enterprise Blueprint 1: Private VPC Agentic RAG Under Strict Data Residency

> [!NOTE]
> **Verified Source**: [Dr. Sundeep Teki](https://www.sundeepteki.org/advice/the-definitive-guide-to-forward-deployed-engineer-interviews-in-2026) | **Dataset ID**: `FDE-ARCH-001`  
> **Target Scenario**: 900-person insurance back office requiring strict zero-egress document Q&A over sensitive policy files.

### Architecture Topology

```
[ Enterprise User / Browser ]
             |  (TLS 1.3 / Corporate Okta SAML 2.0)
             v
[ Enterprise Ingress WAF & API Gateway ] (Rate Limiter + Mutual TLS)
             |
   +---------+-----------------------------------------+
   | PRIVATE CUSTOMER VPC / CLOUD TENANT               |
   |                                                   |
   |  [ Query Router & Intent Classifier ]             |
   |               |                                   |
   |               v                                   |
   |  [ Hybrid Retrieval Engine ]                      |
   |    |--> In-VPC BM25 Sparse Index (OpenSearch)     |
   |    +--> In-VPC Dense Index (pgvector / Qdrant)    |
   |               |  (Enforces AD Group ACL Filters)  |
   |               v                                   |
   |  [ Cross-Encoder Reranker ] (In-VPC BGE-Reranker) |
   |               |                                   |
   |               v                                   |
   |  [ Inference Engine ]                             |
   |    +--> Option A: AWS PrivateLink to In-Region Bedrock
   |    +--> Option B: Self-Hosted vLLM on EC2 G5/P4d   |
   |               |                                   |
   |               v                                   |
   |  [ Deterministic Grounding & Citation Validator ] |
   |               |                                   |
   |               v                                   |
   |  [ Append-Only Audit Ledger ] (S3 WORM Bucket)    |
   +---------------------------------------------------+
```

### Data Boundary and Security Controls
1. **Zero Data Egress**: All data remains inside the customer's private VPC. Ingress terminates via corporate reverse proxy with SAML authentication. Model calls route over AWS PrivateLink or Azure Private Link without traversing the public internet.
2. **Document-Level Permission Inheritance (ACL Filtering)**:
   - During ingestion, each document chunk inherits access control metadata (e.g., `department: "underwriting"`, `clearance_level: 3`).
   - At query time, the user's validated Active Directory groups are injected as mandatory SQL filters into the vector search query:
     ```sql
     SELECT id, content, vector <-> query_vector AS distance
     FROM document_chunks
     WHERE allowed_groups && ARRAY['underwriting_staff', 'claims_lead']
     ORDER BY distance LIMIT 10;
     ```
   - This eliminates cross-tenant data leakage before the LLM prompt is assembled.
3. **Deterministic Grounding Verification**: Every claim in the LLM response must map to a verbatim citation string in the retrieved context. If character-level citation verification fails, the response is downgraded to a safe refusal.

### 3-Tier Evaluation Rubric
- **Strong Hire**: Probes data residency constraints upfront; designs hybrid BM25 + dense retrieval; enforces AD group ACL filtering at database query level; sizes vector RAM accurately; establishes deterministic citation verification and append-only audit logging.
- **Hire**: Outlines a clean RAG pipeline; mentions private endpoints; includes vector search and prompt engineering; acknowledges data privacy concerns.
- **No Hire**: Proposes sending raw enterprise data to a public SaaS endpoint without private networking; stores vectors in a flat unindexed table; ignores access control and document permissions.

### Trade-Off Narration Script
> *"We face a trade-off between a managed in-region model via AWS PrivateLink versus self-hosting open weights (e.g. Llama-3-70B on vLLM). The managed endpoint via PrivateLink provides lower operational overhead and automatic scaling while satisfying data residency. However, if contractual compliance strictly prohibits any third-party multi-tenant hardware, we must pivot to self-hosted vLLM on dedicated in-VPC GPU instances, trading higher infrastructure management for absolute hardware isolation."*

---

## Enterprise Blueprint 2: Integration Gateway Under Lean Ops Constraints

> [!NOTE]
> **Verified Source**: [Nehal Vyas](https://fde.hinehal.com/blogs/fde-interview-questions) | **Dataset ID**: `FDE-ARCH-002`  
> **Target Scenario**: Automated support ticket categorization and triage for a SaaS company with an operations team of only two engineers.

### Architecture Topology

```
[ Inbound Support Webhooks ] (Zendesk / Salesforce / Email)
             |
             v
[ Idempotent Webhook Receiver ] (SHA-256 Deduplication + Redis TTL)
             |
             v
[ Managed Message Queue ] (AWS SQS / RabbitMQ with Dead Letter Queue)
             |
             +-----------------------+
             |                       |
             v (Worker Pool)         v (Dead Letter Quarantine)
[ Stateless Triage Worker ]      [ Failed Message Ledger ]
  - Pydantic Schema Validation     - Alert to On-Call Slack
  - Model Inference + Retry        - 14-day Replay Window
  - Low-Confidence Filter (<0.85)
             |
             +-----------------------+
             | (High Confidence)     | (Low Confidence)
             v                       v
[ Writeback to Helpdesk ]        [ Human Review Queue ]
  - Tags ticket & routes group     - Populates draft with reasoning
  - Updates priority               - Human clicks "Approve"
```

### Key Architectural Decisions for Lean Ops
1. **Boring Technology Wins**: Two operations engineers cannot maintain a bespoke Kubernetes cluster, distributed Kafka cluster, or custom vector database. Use managed services (AWS SQS, Serverless Lambda or simple ECS tasks, and managed PostgreSQL).
2. **Defensive Dead-Letter Queues (DLQ)**: If a webhook payload fails schema parsing or an upstream API returns 500, the message routes to an SQS DLQ with full payload preservation and alerts the team on Slack. No silent drops.
3. **Draft-Only Assisted Mode**: For the first 30 days, the system never closes or auto-routes tickets. It populates a draft recommendation in the operator's sidebar. The operator reviews and confirms with one click, gathering live evaluation data.

### 3-Tier Evaluation Rubric
- **Strong Hire**: Prioritizes operational simplicity; avoids infrastructure bloat; designs queue-driven backpressure with dead-letter replay; implements assisted human-in-the-loop triage before automation; provides single-dashboard metrics.
- **Hire**: Proposes a queue and worker architecture; handles basic retries; acknowledges that two ops engineers require managed services.
- **No Hire**: Proposes complex distributed infrastructure (Kafka clusters, custom Kubernetes operators, self-hosted LLM training) that overwhelms a two-person ops team.

### Trade-Off Narration Script
> *"Because the ops team is only two engineers, operational simplicity is our primary design constraint. We deliberately choose AWS SQS over Apache Kafka: Kafka requires partition rebalancing, cluster zookeeper/KRaft management, and disk provisioning, whereas SQS is fully managed, provides built-in dead-letter handling, and requires zero cluster maintenance. We trade microsecond latency for zero maintenance overhead."*

---

## Enterprise Blueprint 3: Palantir-Style Operational Ontology & Governed Writeback

> [!NOTE]
> **Verified Source**: [Om Bharatiya](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/15-role-guides/forward-deployed-engineer.md) | **Dataset ID**: `FDE-ARCH-003`  
> **Target Scenario**: Cross-system enterprise automation (SAP ERP, Salesforce, Snowflake) where models recommend business actions with financial consequences.

### Architecture Topology

```
+--------------------------------------------------------------------+
|                         ACTION LAYER                               |
|   Approve Invoice | Escalate Incident | Dispatch Field Technician   |
+--------------------------------------------------------------------+
                                  ^
                                  | (Validated Writeback with Human Gate)
+--------------------------------------------------------------------+
|                        ONTOLOGY LAYER                              |
|   Objects: Customer, Contract, Invoice, Facility, Part             |
|   Links:   Customer owns Contract; Invoice bills Customer          |
|   Rules:   Invoice > $5,000 requires Director-level sign-off       |
+--------------------------------------------------------------------+
                                  ^
                                  | (Bi-directional Sync & Reconciliation)
+--------------------------------------------------------------------+
|                         DATA FOUNDATION                            |
|   Salesforce CRM | SAP ERP | Snowflake Warehouse | Zendesk API     |
+--------------------------------------------------------------------+
```

### Key Architectural Decisions
1. **Decoupling Models from Raw Schemas**: The model does not write SQL against production database tables. It interacts with an **Ontology Layer** that defines business objects, valid relationships, and allowable actions.
2. **Governed Human-in-the-Loop Writeback**:
   - The model generates a structured `ActionProposal` with parameters and confidence scores.
   - Low-risk actions (e.g. tagging a ticket) execute automatically.
   - High-risk actions (e.g. issuing a credit memo or cancelling an enterprise contract) route to a human approval inbox displaying an explicit before/after diff.
3. **Immutable Audit Ledger**: Every action execution records the prompt, retrieved context, model version, human approver identity, and ERP transaction ID in a write-once audit log.

### 3-Tier Evaluation Rubric
- **Strong Hire**: Understands the ontology pattern; decouples models from direct database writes; establishes risk-tiered human-in-the-loop action gates; implements bi-directional sync reconciliation and immutable audit trails.
- **Hire**: Mentions that models should not write directly to databases; uses an approval queue for sensitive actions; implements structured outputs.
- **No Hire**: Allows an LLM to generate and execute direct SQL `UPDATE` or `DELETE` statements against production ERP databases.

### Trade-Off Narration Script
> *"Allowing an LLM to write directly to enterprise databases creates catastrophic reliability and compliance risks. We implement a strict Action Proposal architecture: the model can only emit typed action intents against our ontology. Actions with monetary impact over \$500 are held in a staging state requiring human sign-off. This trades instantaneous execution speed for absolute enterprise auditability and zero accidental financial writebacks."*

---

## System Design Architecture Cross-Reference

| Dataset ID | Stage / Category | Verified Primary Source | Core Tension & Architecture Pattern |
| :--- | :--- | :--- | :--- |
| `FDE-ARCH-001` | System Design | [Dr. Sundeep Teki](https://www.sundeepteki.org/advice/the-definitive-guide-to-forward-deployed-engineer-interviews-in-2026) | Private VPC agentic RAG under strict data residency; AD group ACL filtering |
| `FDE-ARCH-002` | System Design | [Nehal Vyas](https://fde.hinehal.com/blogs/fde-interview-questions) | Integration gateway & ticket triage under lean ops constraints; queue DLQ backpressure |
| `FDE-ARCH-003` | System Design | [Om Bharatiya](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/15-role-guides/forward-deployed-engineer.md) | Palantir-style operational ontology & governed writeback action system |

---

## Anti-Patterns That Fail the Round

1. **Scale Theater**: Spending 30 minutes designing multi-region sharding for an enterprise tool serving 500 internal adjusters. The real risk is security, ACL permissions, and latency, not 100,000 QPS.
2. **Ignoring Who Operates It**: Designing an architecture that requires three Kubernetes specialists when the customer has two generalist IT administrators.
3. **Blind Public SaaS Endpoints**: Sending confidential customer documents to external model APIs without inquiring about data retention, BAA agreements, or private networking.
4. **No Reverse Gear**: Failing to describe what happens when the model hallucinates or an upstream service degrades. Every rollout plan must include an automated rollback trigger.

---

## Related Documents

- [Customer Scenario Rounds](04-customer-scenarios.md) - adversarial role-plays and de-escalation playbooks
- [Coding Round Solutions](08-coding-solutions.md) - runnable implementations of integration, retry, and rate-limiting patterns
- [Question Bank](07-question-bank.md) - round-by-round interview directory
- [Market Overview](../job-market/01-market-overview.md) - empirical job market analysis and employer breakdown

---

## References & Further Reading

1. **Dr. Sundeep Teki**: [The Definitive Guide to Forward Deployed Engineer Interviews in 2026](https://www.sundeepteki.org/advice/the-definitive-guide-to-forward-deployed-engineer-interviews-in-2026)
2. **Nehal Vyas**: [Forward Deployed Engineer Interview Questions & Answers](https://fde.hinehal.com/blogs/fde-interview-questions)
3. **Om Bharatiya**: [AI Engineer Interview Questions: Forward Deployed Engineer Guide](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/15-role-guides/forward-deployed-engineer.md)
4. **Alexey Grigorev**: [AI Engineering Field Guide: FDE Responsibilities and Skills Analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)
5. **Marc Brooker**: [AWS Architecture Blog: Exponential Backoff And Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
6. **Palantir Foundry Documentation**: [Operational Ontology Principles & Entity Action Architecture](https://www.palantir.com/docs/foundry/)
7. **Gaijineer**: [Behind the Cohere Forward Deployed Engineer Interview Loop](https://gaijineer.co)
