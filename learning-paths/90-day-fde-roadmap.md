# The 90-Day FDE Transition Roadmap

This roadmap provides an intensive, week-by-week transition curriculum for engineers targeting forward deployed engineering roles at AI labs, enterprise platforms, and growth startups. It synthesizes core training frameworks from FDE Academy (2026), practitioner field reports, and enterprise hiring rubrics.

The roadmap assumes you already write basic code in at least one language. It is engineered to bridge the three gaps that eliminate traditional software engineers from FDE loops: defensive data handling outside idealized environments, deterministic evaluation of probabilistic systems, and customer-facing discovery and de-escalation under pressure.

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
- Deliverable: write a standalone command-line parser that processes a corrupted 10,000-row enterprise export and emits clean records plus a Defect Accounting Report. See reference code in `interviews/code/parser.py`.

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

Goal: Build a flagship, permission-aware AI system with self-healing structured extraction, hybrid retrieval, and automated golden evaluations.

### Week 5: Document Chunking and Dense Semantic Embeddings

- Core focus: ingesting enterprise unstructured text without destroying semantic boundaries.
- Key skills:
  - Token-aware document chunking: splitting text on sentence and paragraph punctuation boundaries with configurable sliding overlap and metadata inheritance.
  - Dense vector embeddings: projecting text into normalized vector spaces, calculating cosine similarity, and understanding semantic subspace clusters.
  - Multi-modal and layout-aware considerations: extracting structured tables and key-value sections from complex business documents.
- Deliverable: build a document ingestion pipeline that chunks multi-page enterprise policy manuals and indexes them into normalized vector representations. See `interviews/code/chunker.py`.

### Week 6: Permission-Aware Hybrid Search and RBAC Filtering

- Core focus: enforcing enterprise access control perimeters at query time.
- Key skills:
  - Document-level Access Control Lists (ACLs): binding allowed user roles (`support_tier1`, `compliance`, `admin`) directly to stored chunk metadata.
  - Pre-retrieval security filtering: filtering vector searches so users never receive search results or citations for unauthorized documents.
  - Hybrid retrieval: combining BM25 sparse lexical matching with dense vector cosine similarity to handle both exact enterprise acronyms and conceptual queries.
- Deliverable: implement a search index that takes user role headers and proves zero data leakage when querying identical prompts across different permission tiers. See `portfolio/reference-project/src/pipeline/ingestion.py`.

### Week 7: Self-Healing Structured Extraction and Gating

- Core focus: converting messy customer text into reliable, validated actions.
- Key skills:
  - Pydantic schema validation: enforcing enum values, mandatory fields, and regex constraints on model outputs.
  - Feedback repair loops: intercepting schema validation errors and feeding the exact error text back to the model in an automated retry turn.
  - Deterministic citation grounding: verifying that cited document quotes appear verbatim in retrieved source text before returning answers.
  - Human-in-the-loop exception queues: routing low-confidence or high-severity tickets to operator review queues.
- Deliverable: build an end-to-end triage agent that validates structured JSON outputs, executes automated repair loops, and routes exceptions. See `portfolio/reference-project/src/engine/agent.py`.

### Week 8: The Golden Evaluation Harness

- Core focus: measuring system quality with reproducible, falsifiable metrics.
- Key skills:
  - Curating a 25-case golden dataset: balancing clean requests, noisy inputs, rate-limit edge cases, out-of-domain prompts, and permission test cases.
  - Constructing an automated evaluation harness: executing the golden suite offline and computing accuracy, precision, recall, and citation validity percentages.
  - Latency and cost accounting: measuring p50, p90, p95, and p99 latency distributions and token costs.
- Deliverable: create `run_evals.py` that runs against your project, prints an executive scorecard, and asserts pass/fail against strict SLA thresholds. See `portfolio/reference-project/evals/run_evals.py`.

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

### Week 11: 72-Hour Take-Home Execution and Rubric Mastery

- Core focus: executing take-home assignments to full production standard within tight deadlines.
- Key skills:
  - Time allocation discipline: spending 20% on discovery and ADRs, 45% on core pipeline and boundary defense, 20% on evaluation harnesses, and 15% on README and runbooks.
  - Authoring operational handovers: writing runbooks that instruct external customer operators how to deploy, monitor, and troubleshoot the system.
  - Scoring against enterprise rubrics: self-evaluating your submission against the 100-point enterprise rubric.
- Deliverable: execute a timed 72-hour take-home challenge from spec to handover documentation. See `interviews/06-take-homes.md`.

### Week 12: Portfolio Packaging, Demo Video, and Mock Loops

- Core focus: converting engineering artifacts into compelling hire signals.
- Key skills:
  - Recording a three-minute technical walkthrough: demonstrating the problem statement, the permission boundary, the failure-and-recovery path, and the automated evaluation scorecard.
  - Verbal narration discipline: narrating code choices during live coding screens using the STAR-F framework (Situation, Task, Action, Result, Feedback to Product).
  - Mock interview drills: completing two full mock loops covering coding, system design, and customer role-plays with an experienced peer.
- Deliverable: publish your portfolio repository with clean README, architecture diagrams, runbooks, and a recorded video walkthrough.

## Daily execution ritual

To complete this roadmap alongside existing work commitments, follow this daily structure:

- Morning (60 minutes): core technical implementation (writing Python code, unit tests, or Docker configs).
- Midday (30 minutes): conceptual reading (reading industry papers, AWS architecture blogs, or system design blueprints).
- Evening (60 minutes): evaluation, documentation, or interview role-play narration practice out loud.

## Related documents

- [Beginner to FDE](beginner-to-fde.md) - guidance for candidates without prior engineering experience
- [From Software Engineer](from-software-engineer.md) - the transition path for traditional developers
- [FDE project selection masterclass](../portfolio/04-project-selection-masterclass.md) - the five enterprise archetypes
- [Coding round solutions and playbooks](../interviews/08-coding-solutions.md) - production code implementations
- [FDE interview question bank](../interviews/07-question-bank.md) - scoring rubrics and senior response playbooks

## Further reading

- [FDE Academy YouTube Channel](https://www.youtube.com/@fdeacademy) - masterclasses and video tutorials
- [FDE Roadmap and Core Tech Stack](https://youtu.be/kBM5UXRbo3U) - video breakdown of the 90-day transition curriculum
- [Why FDE is the Most In-Demand AI Role](https://youtu.be/CCt0csEqul0) - career mechanics and interview loop expectations
- [From Software Engineer to FDE](https://youtu.be/vLlIBT0HSSc) - transition guidance for traditional engineers
