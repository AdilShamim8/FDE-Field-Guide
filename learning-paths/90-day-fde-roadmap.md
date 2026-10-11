# The 90-Day FDE Transition Roadmap

This is a recommended twelve-week project plan for engineers who already write basic code. It is not an authenticated employer curriculum or a guarantee of readiness in ninety days. Implementation descriptions were checked against this repository on 2026-10-11. Start with the [foundations lessons](foundations/README.md) if you cannot yet read JSON, query a table, or debug an HTTP request.

The plan develops defensive data handling, evaluation, and customer-facing discovery. The local reference demonstrates a subset of these skills. Tasks involving learned embeddings, model calls, durable databases, authentication, deployment, or customer acceptance are extensions you must implement and verify.

## Structure of the 90 days

The program is structured into three consecutive 30-day blocks:

- Month 1 (Weeks 1 to 4): Enterprise Engineering, Defensive Ingestion, and Infrastructure Foundations
- Month 2 (Weeks 5 to 8): Production AI Systems, RBAC Permissions, and Deterministic Evaluation
- Month 3 (Weeks 9 to 12): Enterprise System Design, Customer Scenarios, and Interview Execution

## Month 1: Enterprise Engineering and Data Plumbing (Weeks 1 to 4)

Goal: Master production Python, defensive parsing, idempotency, rate limiting, and containerized operational hygiene.

### Week 1: Production Python and Defensive Ingestion

- Core focus: moving past naive scripting to defensive data engineering.
- Key skills:
  - Strong typing with `mypy` and runtime schema enforcement using `pydantic` V2.
  - Multi-encoding byte stream handling: detecting UTF-8 Byte Order Marks (BOM), cascading fallback to CP1252 and Latin-1 without raising unhandled decode exceptions.
  - Defect accounting: parsing malformed CSV and JSON exports, recording every dropped or repaired record with line numbers and defect categories in an audit report.
- Deliverable: write a standalone command-line parser that processes a permitted export with documented defects (or clearly labeled authored corruptions) and emits clean records plus a Defect Accounting Report. See reference code in `interviews/code/parser.py`.

### Week 2: Resilient API Integration and Idempotency

- Core focus: integrating against third-party systems that fail, time out, or rate limit.
- Key skills:
  - HTTP idempotency: designing webhook receivers that compute SHA-256 payload hashes, enforce `Idempotency-Key` headers, detect payload mutations with HTTP 409 Conflict, and cache completed responses.
  - Exponential backoff with full jitter: calculating randomized delays between 0 and min(max_delay, base * 2^attempt) to eliminate thundering herd synchronization.
  - In-memory sliding window rate limiting: tracking rolling request timestamps to defend against boundary bursts across tenant tiers.
- Deliverable: implement an idempotent webhook receiver and resilient API client with automated `pytest` test suites verifying retry behaviors and replay safety. See `interviews/code/webhook_receiver.py` and `interviews/code/resilient_client.py`.

### Week 3: Relational Schemas, Schema Drift, and SQL

- Core focus: navigating and mutating messy enterprise databases.
- Key skills:
  - Navigating foreign-key relationships, recursive employee hierarchies, and composite primary keys in PostgreSQL.
  - Handling schema drift: writing idempotent migration scripts and queries that survive missing columns, type coercions, and null values.
  - Audit logging: implementing database triggers or audit tables that log user ID, timestamp, and field-level before-and-after diffs with write-once integrity.
- Deliverable: author a database schema and migration script for a multi-tenant ticketing platform with role-based access tables, document chunks, and audit logs.

### Week 4: Containerization and Local Operations

- Core focus: packaging reproducible environments that deploy anywhere with one command.
- Key skills:
  - Multi-stage `Dockerfile` construction: pinning base images, minimizing image footprint, running as a non-root user, and establishing healthcheck endpoints.
  - Orchestration with `docker compose`: wiring web API services, databases, and mock external endpoints with environment isolation and persistent volumes.
  - Secrets hygiene: separating environment variables (`.env.example`) from source code and verifying no API credentials exist in git history.
- Deliverable: containerize your Month 1 services with `docker compose up` executing clean health checks on port 8000.

## Month 2: Production AI Systems and Deterministic Governance (Weeks 5 to 8)

Goal: build an evidence-aware application, then add model extraction or hybrid retrieval only when the workflow and evaluation justify them. Keep source-derived inputs separate from authored regression cases.

### Week 5: Document Chunking and Representation Choices

- Core focus: ingesting enterprise unstructured text without destroying semantic boundaries.
- Key skills:
  - Boundary-aware document chunking with overlap and metadata inheritance. The supplied chunker budgets regex word/punctuation units, not a model tokenizer; add and test a provider tokenizer when enforcing model context limits.
  - Dense vector embeddings: projecting text into normalized vector spaces, calculating cosine similarity, and understanding semantic subspace clusters.
  - Multi-modal and layout-aware considerations: extracting structured tables and key-value sections from complex business documents.
- Deliverable: build a document ingestion pipeline that chunks multi-page enterprise policy manuals and indexes them into normalized vector representations. See `interviews/code/chunker.py` for bounded regex-unit splitting. Learned embeddings and layout extraction are additional implementations, not capabilities of that exercise.

### Week 6: Permission-Aware Hybrid Search and RBAC Filtering

- Core focus: enforcing enterprise access control perimeters at query time.
- Key skills:
  - Document-level Access Control Lists (ACLs): binding allowed user roles (`support_tier1`, `compliance`, `admin`) directly to stored chunk metadata.
  - Pre-retrieval role filtering plus authenticated identity: derive effective roles from a verified principal, then test document permissions and tenant scope. Caller-supplied headers alone do not establish authorization.
  - Hybrid retrieval: combining BM25 sparse lexical matching with dense vector cosine similarity to handle both exact enterprise acronyms and conceptual queries.
- Deliverable: test allowed and denied document retrieval with a stated threat model. The reference at `portfolio/reference-project/src/pipeline/ingestion.py` uses feature hashing and token overlap; it has no BM25 or learned embedding model. Its role headers simulate permissions. Authenticated identity, tenant isolation, BM25/RRF, and a representative retrieval evaluation are separate extensions; passing role-header tests does not prove zero leakage.

### Week 7: Structured Extraction and Evidence Gating

- Core focus: converting messy customer text into reliable, validated actions.
- Key skills:
  - Pydantic schema validation: enforcing enum values, mandatory fields, and regex constraints on model outputs.
  - Feedback repair loops: intercepting schema validation errors and feeding the exact error text back to the model in an automated retry turn.
  - Deterministic citation grounding: verifying that cited document quotes appear verbatim in retrieved source text before returning answers.
  - Human-in-the-loop exception queues: routing low-confidence or high-severity tickets to operator review queues.
- Deliverable: inspect `portfolio/reference-project/src/engine/agent.py` and demonstrate missing-evidence review, applicable-document checks, exact quotation checks, and severity routing. It is deterministic and has no model repair loop. If you add a structured model extractor, validate its output, bound retries, record failures, and test it separately on permitted inputs.

### Week 8: Regression Contracts and Independent Evaluation

- Core focus: measuring system quality with reproducible, falsifiable metrics.
- Key skills:
  - Separate authored contract tests from an independently labeled evaluation set. Document record lineage, annotation rules, disagreement, selection, and an untouched holdout; select sample size for the decision and uncertainty rather than copying a fixed count.
  - Run reproducible checks for classification, routing, applicable evidence, and abstention. Interpret precision/recall only against suitable independently established labels. An exact quote can still be irrelevant.
  - Measure end-to-end API latency under specified load and failure conditions. Record token usage and cost only for actual provider calls; local deterministic timings do not establish a production SLA.
- Deliverable: run `portfolio/reference-project/evals/run_evals.py` and retain its report. The existing 25 cases are known regression fixtures with unverified origins, not a real customer holdout. The report gates known routing/document contracts and reports engine-only timings. Add separately justified customer acceptance thresholds and measured API latency for your own system.

## Month 3: System Design, Customer Scenarios, and Interview Execution (Weeks 9 to 12)

Goal: Master enterprise architectural design, customer de-escalation dialogue, take-home assignments, and interview narration.

### Week 9: Enterprise System Design and Multi-Tenant VPC Topology

- Core focus: architecting customer-flavored distributed systems under strict enterprise constraints.
- Key skills:
  - Back-of-the-envelope capacity math: calculating queries per second (QPS), token throughput, GPU memory, vector storage footprints, and network bandwidth.
  - Multi-tenant VPC isolation: designing private VPC endpoints (AWS PrivateLink), customer-managed encryption keys (KMS), and air-gapped egress rules.
  - Palantir-style operational ontologies: modeling relational tables and ERP endpoints into canonical business objects with governed writeback gates.
- Deliverable: author a complete Architecture Decision Record (ADR) and system design blueprint for an enterprise deployment. See `interviews/03-system-design.md`.

### Week 10: Customer Scenarios and De-escalation Role-Plays

- Core focus: developing customer presence, discovery discipline, and composure under fire.
- Key skills:
  - Discovery interviewing: probing the business problem behind the customer ask using the What, Why, How, Who, When framework.
  - Managing executive hype: steering sponsors from vague "AI everywhere" mandates toward high-impact, low-risk initial thin slices.
  - De-escalating production emergencies: managing customer panic when an LLM outputs an incorrect answer, using structured containment, root-cause traces, and regression prevention.
- Deliverable: practice verbatim role-play dialogues for the five core customer scenarios with a study partner. See `interviews/04-customer-scenarios.md`.

### Week 11: A Timed Take-Home Practice

- Core focus: delivering a reviewable small implementation within a stated time budget, with missing production work documented.
- Key skills:
  - Time allocation discipline: spending 20% on discovery and ADRs, 45% on core pipeline and boundary defense, 20% on evaluation harnesses, and 15% on README and runbooks.
  - Authoring operational handovers: writing runbooks that instruct external customer operators how to deploy, monitor, and troubleshoot the system.
  - Scoring against enterprise rubrics: self-evaluating against the guide's authored practice rubric, which is not an authenticated company scoring system.
- Deliverable: execute a timed 72-hour take-home challenge from spec to handover documentation. See `interviews/06-take-homes.md`.

### Week 12: Portfolio Packaging, Demo Video, and Mock Loops

- Core focus: converting engineering artifacts into compelling hire signals.
- Key skills:
  - Recording a three-minute technical walkthrough: demonstrating the problem statement, the permission boundary, the failure-and-recovery path, and the automated evaluation scorecard.
  - Verbal narration discipline: narrating code choices during live coding screens using the STAR-F framework (Situation, Task, Action, Result, Feedback to Product).
  - Mock interview drills: completing two full mock loops covering coding, system design, and customer role-plays with an experienced peer.
- Deliverable: publish your portfolio repository with clean README, architecture diagrams, runbooks, and a recorded video walkthrough.

## Daily execution ritual

One possible study schedule is below. Adjust it to your available time and repeat work until you can demonstrate the exit criteria; the schedule is a recommendation, not measured completion time:

- Morning (60 minutes): core technical implementation (writing Python code, unit tests, or Docker configs).
- Midday (30 minutes): conceptual reading (reading industry papers, AWS architecture blogs, or system design blueprints).
- Evening (60 minutes): evaluation, documentation, or interview role-play narration practice out loud.

## Related documents

- [Beginner to FDE](beginner-to-fde.md) - guidance for candidates without prior engineering experience
- [From Software Engineer](from-software-engineer.md) - the transition path for traditional developers
- [FDE project selection masterclass](../portfolio/04-project-selection-masterclass.md) - the five enterprise archetypes
- [Coding round solutions and playbooks](../interviews/08-coding-solutions.md) - production code implementations
- [FDE interview question bank](../interviews/07-question-bank.md) - authored practice rubrics and response exercises

## Further reading

- [FDE Academy YouTube Channel](https://www.youtube.com/@fdeacademy) - masterclasses and video tutorials
- [FDE Roadmap and Core Tech Stack](https://youtu.be/kBM5UXRbo3U) - background material; this page's schedule is a local recommendation
- [Why FDE is the Most In-Demand AI Role](https://youtu.be/CCt0csEqul0) - career mechanics and interview loop expectations
- [From Software Engineer to FDE](https://youtu.be/vLlIBT0HSSc) - transition guidance for traditional engineers
