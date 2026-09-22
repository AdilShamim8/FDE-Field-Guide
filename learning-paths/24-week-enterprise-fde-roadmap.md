# 24-Week Enterprise Forward Deployed AI Engineer Roadmap

This roadmap provides the complete week-by-week enterprise transition curriculum for aspiring Forward Deployed AI Engineers. It is sourced directly from the Codebasics FDE Roadmap 2026 (Dhaval Patel and Hemanand Vadivel, AtliQ Technologies), built from practitioner interviews with Pankaj Jaiswal, Rushi Gandhi, Pranav Modh, and Daksh Trehan, and validated against 146 deduplicated 2026 FDE job postings.

FDE = AI engineer + a slice of AI PM. Phase 1 builds core AI engineering skills. Phase 2 builds product management and soft skills required to succeed on the client floor.

Prerequisites: minimum one year of programming experience in any language, SQL fundamentals (SELECT, JOIN, GROUP BY), Git and GitHub (clone, commit, push, branching), how HTTP requests and JSON APIs work, and the debugging habit of reading error messages and searching documentation.

## Phase 1: Technical Skills (Weeks 1 to 16)

Build and ship enterprise AI: Python, RAG, agents, ERP data, DevOps, LLMOps, and system design.

### Weeks 1 and 2: Python for Enterprise AI

Python is named in 133 of 146 scraped FDE postings (91.0%) (observed evidence, Codebasics job analysis, September 2026). Start with the basics and go deep into how Python is used for enterprise AI.

Topics:

- Python basics: loops, data types, variables, conditionals
- `fastapi`: route definitions, request and response models with Pydantic, background tasks, middleware
- `pydantic` v2 for data validation: schema definition, custom validators, nested models
- Error handling patterns: `HTTPException`, custom exception handlers, structured error responses
- Environment management: `.env` files, secrets management, never hardcoding API keys
- Calling LLMs from Python using GroqCloud or similar providers

Assignments:

- [ ] Build a FastAPI service for a work-order tracker with 4 endpoints (create, list all, update status, get by ID) using Pydantic models for request and response validation and proper error handling
- [ ] Add a `/summarize` endpoint that calls an LLM (GroqCloud free tier) to summarize a work order description, with API key loaded from `.env`
- [ ] Push the project to GitHub with a README explaining how to run it

### Week 3: Vibe Coding

An FDE who codes with AI is 3x faster. An FDE who blindly trusts AI code fails in production. MakeMyTrip CTO Sambit Sarangi stated that what they check in interviews is how well candidates review AI-generated code (Codebasics FDE Roadmap 2026, September 2026).

Topics:

- You are responsible for the code you ship, not the AI. Build a strong testing layer
- Tools: Claude Code, Cursor, GitHub Copilot, Antigravity — pick one, go deep
- Claude Skills, `CLAUDE.md`, and context management
- Spec-first workflow: SDD to implementation plan to execute step by step
- Validating AI-generated code: read every diff, catch hallucinated APIs, weak error handling, hardcoded secrets — this is now an FDE interview skill

Assignments:

- [ ] Extend your Week 1 and 2 work-order tracker using Claude Code or Cursor: first write a `CLAUDE.md` with 5 project conventions, then add 2 new features through AI — technician assignment and a priority field with validation
- [ ] Code review drill: ask AI to generate around 100 lines of code for a new feature, then find and fix at least 3 issues (hallucinated API, missed edge case, weak error handling) without AI help

### Weeks 4 and 5: LLM Fundamentals and RAG

30 to 40% of projects at AtliQ Technologies require some type of RAG (Retrieval Augmented Generation), consistent with industry-wide patterns (Codebasics FDE Roadmap 2026).

Topics:

- Understanding the AI landscape: ML, DL, Gen AI, Agentic AI
- Transformer architecture and how LLMs work
- LLM core concepts: temperature, top-p, top-k, context window, autoregressive generation
- RAG and chunking strategies: vector RAG and vectorless RAG
- Ingestion pipeline: PDFs, Word SOPs, Excel exports to chunking (fixed, recursive, semantic) to embeddings
- Vector databases: at minimum one (ChromaDB, Qdrant, PineCone, PgVector)
- Retrieval quality: semantic vs keyword (BM25) vs hybrid search, re-ranking
- Hallucination guardrails: grounding, citations, explicit refusal behavior
- Cost and latency: experiment with different models, open-source and commercial, and pick the most cost-effective option that meets latency requirements

Assignments:

- [ ] Build a RAG system over 10 real PDFs (equipment manuals, HR policies, or vendor contracts): ingest, chunk, embed, and answer questions with citations to the source page
- [ ] Write a Kaggle notebook or GitHub repository for your RAG project and share on LinkedIn

### Weeks 6, 7, and 8: Agentic AI, Multi-Agent Systems, MCP

The world is focused on Agentic AI. As an FDE, you will build agentic automations while working at client sites.

Topics:

- What exactly is an agent: the ReAct loop (Reason, Act, Observe)
- Tool calling: defining tools with clear schemas and boundaries, structured JSON output
- Building agents using LangChain
- Multi-agent systems using LangGraph: state, nodes, conditional edges, memory persistence
- Multimodal agents
- Human-in-the-loop: interrupt and route to a person when confidence is low or the action is irreversible
- MCP (Model Context Protocol): the standard way to expose enterprise tools to agents
- Guardrails and evals: limiting what an agent can do and testing it before a client does

Assignments:

- [ ] Build a work-order triage agent on top of your Week 1 tracker: reads an incoming complaint, uses your RAG system to check the equipment manual, decides priority, and creates the work order via your API through tool calls
- [ ] Add a human-in-the-loop interrupt: if the agent confidence is below 85% or priority is P1, route to a "needs review" state instead of auto-creating
- [ ] Record a 5-minute demo video explaining the agent decision flow as if presenting to a client IT team, and post it on LinkedIn
- [ ] Build a 3-agent LangGraph system: Agent 1 extracts key fields from RFQ or vendor documents, Agent 2 validates completeness against approved vendor list, Agent 3 drafts a procurement recommendation and posts to a mock approval API

Development philosophy: you are not building a demo. You are building production code that will run inside a client environment with their messy legacy data, their IT security policies, and their end-users who are not technical. Build defensively. Document everything.

### Week 9: ERP and Enterprise Data Integration

You will almost always build AI on top of an ERP — SAP, NetSuite, Dynamics, Tally, or a custom one. Learn ERP literacy and how to pull data out. Go deeper only if your client lives inside SAP (see the Bonus section at the end of this document).

Topics:

- Many FDE job openings have the title "FDE / Integration Engineer". You are required to build an integration layer on top of ERP that can interact with ERP data and make things ready for the AI layer
- ERP landscape: SAP, Oracle NetSuite, MS Dynamics, Tally — what a system of record is, master data vs transactional data
- SAP module map (PM, CS, MM, SD, HR): know what each module owns
- How data gets out: pre-built connectors (Palantir Foundry, Databricks, Airbyte), OData and REST APIs, MCP servers
- SAP OData in practice: consuming S/4HANA APIs (Equipment Master, Work Orders) via the free sandbox, no SAP installation needed
- REST API design for enterprise: authentication (OAuth2, API keys), rate limiting, retry logic, idempotency
- Data quality realities: duplicate masters, cryptic codes needing lookup tables, stale data
- The scarce skill: knowing what to ask the client IT team for — data dictionary, API catalogue, authorizations, sandbox access

Assignments:

- [ ] Call the Equipment Master OData API (`API_EQUIPMENT`) from the SAP Business Accelerator Hub free public sandbox (api.sap.com) and retrieve equipment details including functional location and maintenance plant
- [ ] Build a Python FastAPI endpoint that wraps this call and returns structured JSON (equipment status, last maintenance date, assigned technician), then connect it as a tool to your agent
- [ ] Write a one-page integration spec (source system, API, auth, fields, refresh frequency) as if submitting to a client IT team

### Weeks 10 and 11: DevOps for AI

FDE is responsible for code deployment and continuous delivery. Knowledge of DevOps is essential.

Topics:

- As an FDE, you will be responsible for building the infrastructure behind the AI layer. A disciplined approach and reusable documentation saves everyone time
- Docker: multi-stage builds, container registries (AWS ECR, Azure ACR), optimizing image size for AI apps
- Kubernetes: deployments, services, config maps, secrets, resource limits, liveness and readiness probes
- CI/CD with GitHub Actions: lint to test to build to push to deploy pipeline for AI applications
- API Gateway patterns: rate limiting, authentication (OAuth2 and JWT), CORS, request routing
- Infrastructure as Code: Terraform basics for provisioning cloud resources
- Secrets management: AWS Secrets Manager, Azure Key Vault — never in environment variables
- A/B testing and canary releases for AI model versions
- On-premise Kubernetes: kubeadm, Rancher, air-gapped Docker registries, private LLM hosting (Ollama, vLLM)

Assignments:

- [ ] Containerize your Weeks 4 to 6 multi-agent system with Docker and push to Docker Hub or AWS ECR
- [ ] Write a GitHub Actions workflow that runs tests and deploys on push to main
- [ ] Deploy to a cloud VM or cloud container service (AWS ECS, Azure Container Apps) and share the live URL

### Weeks 12 and 13: LLMOps — Observability, Evaluation, and Security

Deploying your AI system is step one. LLMOps is keeping it observable, evaluated, secure, and within budget once real users depend on it.

Topics:

- LLM trace logging: capturing inputs, outputs, latency, and token usage per request (LangSmith, LangFuse, OpenTelemetry)
- Metrics dashboards with Prometheus and Grafana: requests per minute, P95 latency, error rate, token cost per day
- Evaluation in production: regression test suites, hallucination rate monitoring, comparison against ground truth
- Cost management: token budgets, model routing (lightweight models for simple tasks, premium models only where accuracy demands), alert thresholds
- Security: OWASP Top 10 for LLMs — prompt injection, data leakage, insecure output handling
- RBAC and SSO: permission layers for multi-tenant AI apps, OAuth2, SAML, Azure AD integration patterns
- Scaling and reliability: horizontal pod autoscaling, load testing with Locust, defining SLAs

Assignments:

- [ ] Add LangSmith or LangFuse tracing to your AI agent and capture 50 test traces across different work order types
- [ ] Set up a Grafana dashboard with requests per minute, P95 latency, error rate, and token cost per day
- [ ] Write a security threat model for your AI system: identify 3 prompt injection risks and document mitigations
- [ ] Load test your API with 50 concurrent users using Locust and document the results

### Weeks 14, 15, and 16: System Design for Enterprise AI

Calling an LLM API is easy. Building a system around it that is fast, cheap, reliable, and does not embarrass you in production is AI System Design. FDE interviews open with system design.

Topics:

- As an FDE, you need to understand the client current system design and suggest enhancements for the integration layer you are building such that it does not impact their current usage
- Why AI system design is different: an LLM is non-deterministic, expensive per call, slow, and confidently wrong. Almost every unusual box in an AI architecture exists to defend against one of those four properties
- The model layer: API models vs self-hosted, and model routing. Small model for extraction and classification, frontier model only where synthesis is genuinely required. This is the single largest cost lever you control
- The retrieval layer: ingestion path vs query path, hybrid search (vector plus keyword), reranking, chunking strategy, metadata filtering. When RAG answers are bad, it is retrieval 8 times out of 10
- Orchestration: tool calling, the think-act-observe loop, and reliability maths — 95% per step across 10 steps lands near 60% end to end
- Latency and cost design: time-to-first-token vs total time, streaming, the caching ladder (exact-response cache, then semantic cache, then stable prompt prefix). Cost is a designed property, not an invoice you discover at month end
- The trust layer: input and output guardrails, evals as the unit tests of an AI system, and end-to-end tracing
- Degradation and fallback design: primary model to secondary to graceful manual path, with every tier announced to the user rather than failing silently
- HLD (High-Level Design): components and interactions, technology stack with rationale and trade-offs, deployment topology (cloud vs on-premise, ERP connection), and NFRs
- LLD (Low-Level Design): API endpoint specs with OpenAPI and Swagger, request and response contracts, database schema, and sequence diagrams including the failure sequence
- Architecture Decision Records: the decision, the alternatives rejected, and what it costs you. Tools: draw.io (free), Eraser.io (AI-native diagram-as-code), Mermaid

Assignments:

- [ ] Write the HLD for an AI-powered field service management system: architecture diagram, component list, technology stack with rationale and trade-offs, deployment topology, model routing policy, and one Architecture Decision Record for your model hosting choice
- [ ] Write the LLD for the same system: API endpoint table (at least 8 endpoints with request and response models), database schema (Equipment, WorkOrder, Technician, SLAPolicy), a sequence diagram for work-order creation, and a second sequence diagram for when the ERP write fails
- [ ] Explain your design out loud in 5 minutes as if in an interview — record yourself, review it, and share the architecture diagram on LinkedIn

## Phase 2: Product Management and Soft Skills (Weeks 17 to 24)

Phase 1 taught you to build and ship enterprise AI. Phase 2 teaches you to work on the client floor: find the real problem, document it, manage the people, and land the go-live.

### Weeks 17 and 18: Problem Discovery and User Research

An FDE is like a calm, mature doctor. A patient may come with a headache, but a calm doctor does not give headache medicine immediately. They inquire and test to find the root cause. Similarly an FDE finds the root cause before building.

Topics:

- 5-Whys technique for root cause identification; the Mom Test
- Interviewing and shadowing end users: mapping their manual process step by step
- User research basics: personas, jobs-to-be-done, buyer (CXO) needs vs end-user needs
- Separating the stated request from the real problem — always ask "what does success look like?"
- Pre-discovery checklist: documents to request — SOPs, org charts, current process metrics
- Discovery interview framework: open-ended questions that uncover real pain
- Facilitating discovery workshops: agenda, room rules, capturing outputs
- Quantifying the problem: error rates, manual hours, SLA breaches, cost per error
- Handling scope creep during discovery; NDA, data governance, and onsite access protocols

Assignments:

- [ ] Pick a real process you know (family business, your workplace) and write a discovery interview script with 10 open-ended questions
- [ ] Run the interview with someone who actually does the process — document the AS-IS steps, pain points, and quantify: manual hours, error rate, cost per error
- [ ] Write a one-page problem statement with quantified business impact, and get the interviewee to confirm it is accurate

### Week 19: AS-IS Process Mapping with Swim-Lane Diagrams

Before automating anything, draw how work happens today. The diagram is how you and the client agree on reality.

Topics:

- BPMN (business process model notation) basics: pools, swim-lanes, events, gateways, tasks, connectors
- Drawing AS-IS (current state) process flows that capture manual steps precisely
- Identifying automation candidates: repetitive, rule-based, high-volume, error-prone steps
- Defining the TO-BE (future AI-automated) vision with stakeholders
- Tools: draw.io (free), Miro (free tier), Eraser.io (AI-native diagrams)

Assignments:

- [ ] Draw a complete AS-IS swim-lane diagram for the process discovered in Weeks 17 and 18
- [ ] Highlight in orange the steps you would automate with AI, and note why
- [ ] Share the diagram on LinkedIn with a caption explaining what you learned

### Weeks 20 and 21: Business Requirement Document Mastery

An enterprise client judges your competence by your documentation before they see a single line of code.

Topics:

- BRD structure: Executive Summary, Scope and Out-of-Scope, AS-IS and TO-BE, Functional Requirements, Integration Requirements, Data Requirements, Acceptance Criteria, Risks and Assumptions
- Writing measurable acceptance criteria: not "the system shall be fast" but "work order assignment at or below 5 seconds at P95"
- Managing scope: what goes out-of-scope and why
- BRD versioning and change log management
- Common mistakes: ambiguous requirements, missing exclusions, untestable criteria
- The BRD review rubric used in the Vaayu Pumps project: completeness, specificity, testability, traceability to business outcomes (source: BRD v1.1, September 2026)

Assignments:

- [ ] Write a full BRD for your Week 19 process — minimum 8 sections, including a functional requirements table with 10 or more requirements
- [ ] Get peer feedback: does each requirement have a measurable acceptance criterion?
- [ ] Publish your BRD summary as a LinkedIn carousel post or article

### Week 22: Technical Design Document

The BRD says what and why. The TDD tells a developer or an AI coding agent exactly how the system should behave.

Topics:

- TDD vs BRD: deriving functional flows and data flows from the BRD
- Field-level validation specs: mandatory fields, allowed formats, tolerance thresholds
- Business rule specs: for example, SLA escalation — first warning at 80% of the SLA window, auto-escalation at 100%
- Error scenarios and exception handling requirements
- Integration specs: source systems, APIs, auth, refresh frequency
- The Spec Clarity Test: feed your TDD to an AI coding agent; if it cannot build correctly from your spec, the spec is not clear enough (source: TDD v1.0, September 2026)

Assignments:

- [ ] Derive a TDD from your Week 21 BRD: functional flows, validation rules, exception handling, integration specs
- [ ] Write one business-rule spec (flowchart plus rule table) as if handing it to a developer, then feed it to an AI coding agent and check whether it builds correctly

### Weeks 23 and 24: Stakeholder Management, UAT, and Go-Live

Technical skills get you shortlisted. These skills decide whether you succeed on the client floor.

Stakeholder management topics:

- Stakeholder ecosystem: end-users, process owners, IT gatekeepers, C-suite sponsors — map influence vs interest
- Setting expectations: saying no diplomatically, trading scope for timeline, documenting agreements
- Communication rhythm: meeting agendas, minutes of meeting, weekly status updates, escalation paths
- Presenting to C-suite: the 3-slide format (problem, solution, results)
- Communication in regional languages: following what the client is saying in Hindi or their local language (Principle 1 of the 12 Core Principles of Enterprise FDE)
- Confidence under uncertainty: clarify with authority — "Help me understand this better: are you saying X or Y?" (Principle 4)

UAT topics:

- UAT vs QA testing: what UAT validates that unit tests cannot
- Writing UAT test scripts: scenario, pre-conditions, test steps, expected vs actual result, pass or fail
- UAT entry and exit criteria
- Go-live checklist: data migration verified, rollback plan documented, support contacts listed
- Hypercare period: escalation matrix, incident response playbook

Change management topics:

- Why end-users resist AI systems and how to address it — the ADKAR model (Awareness, Desire, Knowledge, Ability, Reinforcement)
- End-user training: role-based guides, video walkthroughs, FAQ documents
- KPI design: ROI, efficiency gain, error reduction, SLA compliance percentage
- Building KPI dashboards a non-technical client can read and trust
- Documentation handover pack: architecture overview, runbook, contact matrix, known issues

Assignments:

- [ ] Write a 300-word note: "What problem does an FDE solve that a solutions engineer cannot?"
- [ ] Record a 5-minute, 3-slide C-suite presentation of your Phase 1 project and post it on LinkedIn
- [ ] Write a 15-scenario UAT test script covering P1 emergency dispatch, SLA breach escalation, parts unavailability, and technician skill mismatch
- [ ] Write a 3-page IT handover document: architecture overview, runbook, contact matrix, known issues
- [ ] Build a KPI dashboard showing: work orders processed, first-time fix rate, SLA compliance percentage, technician utilisation, MTTR
- [ ] Create a 10-minute end-to-end presentation video of your full 24-week project as if presenting to a client CXO, and upload to LinkedIn

## Bonus: Deep SAP Integration and Field Service Domain

Not required for most FDE roles, but if you target SAP-heavy consultancies or manufacturing and field service clients, this depth is a differentiator. This section is based on inputs from Pankaj Jaiswal, an FDE working in this exact environment (Codebasics FDE Roadmap 2026, September 2026).

### SAP Integration Patterns

- SAP integration options: BAPI (Business API), OData (REST-style), RFC (Remote Function Call), IDocs, SAP CPI (Cloud Platform Integration)
- SAP CPI as middleware: integration flows, message mapping, content-based routing
- SAP Datasphere: read-layer views for AI consumption — equipment performance, technician utilization, SLA compliance history
- Writing BAPI integration catalogues: function name, input and output parameters, error codes (for example, `BAPI_ALM_ORDER_MAINTAIN` for work order updates)

### SAP Domain Knowledge — Manufacturing and Field Service

- SAP PM (Plant Maintenance): equipment master (`IE01`, `IE03`), functional locations (`IL01`), work orders (`IW31`, `IW32`, `IW33`), notifications (`IW51`)
- SAP CS (Customer Service): service orders, service contracts, resource-related billing
- Spare parts management: material reservations (`MB21`), goods issue (`MB1A`), stock overview (`MMBE`)
- SLA management: response time vs resolution time, P1 to P4 priority matrix, penalty clauses
- Field technician scheduling: skill-based routing, geography-based dispatch, availability calendars
- IoT integration basics: how sensor data (vibration, temperature, pressure) triggers predictive maintenance work orders
- Warranty management and Indian manufacturing compliance: BIS certifications, statutory inspection logs, safety audit trails

Assignment:

- [ ] Write a BAPI Integration Catalogue table with 5 BAPIs for field service automation (create work order, read equipment master, confirm work order operation, create service notification, check material availability)

## AI Tools to Accelerate Your Delivery Workflow

An FDE who uses AI tools intelligently produces better deliverables in half the time. These are tools actively used on real enterprise projects (Codebasics FDE Roadmap 2026, September 2026):

| Tool | Best Used For | Pro Tip |
| :--- | :--- | :--- |
| Claude (Anthropic) | Generating BRDs, FRDs, System Design Documents, meeting summaries, email drafts, validation rule tables | Use structured XML prompts with clear section templates. Claude maintains long document context well |
| ChatGPT (OpenAI) | Generating system architecture diagrams, flowcharts, and data flow visuals | Describe components and connection lines clearly for clean architecture diagrams from text |
| Eraser.io | System design diagrams, flow diagrams, and sequence diagrams using AI-assisted DSL | Use direction-right for landscape swimlane layouts. Describe actors, systems, and data flows in plain English |
| Multi-Model Approach | When a model gets a diagram or data flow consistently wrong | Switch models: if Claude keeps making the same structural mistake, try ChatGPT. If ChatGPT hallucinates, try Gemini |
| Screen recording tool | Walkthrough and demo videos for client training, UAT handholding, and stakeholder presentations | A 3-minute recording replaces 10 pages of written user guide for non-technical users |

## Real-World Case Studies

Three reference case studies demonstrate the full 24-week curriculum in practice:

Case Study 01: AI Field Service Management Command Centre — multi-agent system for automated work order triage, skill-based technician dispatch, real-time SLA breach prediction, and spare parts availability check. Tech stack: LangGraph Supervisor, GPT-4o, SAP PM OData, Azure SQL, Datasphere, IoT event stream. Documents produced: BRD, FRD, SDD with agent diagrams, SAP BAPI Integration Catalogue, UAT scripts. See [Vaayu Pumps case study](../case-studies/05-enterprise-manufacturing-vaayu-pumps.md) for the full 83-page document set.

Case Study 02: Predictive Maintenance AI Agent — agentic system that ingests IoT sensor data, detects anomaly patterns, auto-creates SAP PM work orders before equipment failure, and routes to the right technician. Tech stack: LangGraph, Gemini 2.5 Flash, SAP PM BAPI, IoT Hub, FastAPI, LangSmith. Documents produced: SDD with IoT integration spec, BAPI catalogue, anomaly detection rule library, KPI dashboard design.

Case Study 03: Contract Lifecycle Management AI Agent — AI agent that extracts key clauses from service contracts, flags SLA breaches and renewal deadlines, and answers natural language questions about contract terms. Tech stack: Claude Sonnet, CrewAI, pgvector, Python FastAPI, MS Graph API, RAGAS evaluation. Documents produced: prompt library, clause extraction templates, evaluation report, handover runbook.

## Related documents

- [90-Day FDE Transition Roadmap](90-day-fde-roadmap.md) - the accelerated 12-week curriculum for engineers transitioning from adjacent roles
- [Learning Paths Overview](README.md) - background-specific transition blueprints and the readiness self-audit protocol
- [Vaayu Pumps Case Study](../case-studies/05-enterprise-manufacturing-vaayu-pumps.md) - the complete enterprise project referenced in Case Study 01 above
- [Requirements to Spec](../customer/02-requirements-to-spec.md) - the BRD, TDD, and SDD chain with Spec Clarity Test
- [Agents and Tools](../ai/02-agents-and-tools.md) - supervised multi-agent pipeline architecture and persistent memory layers
- [ERP and SAP Integration](../engineering/02-apis-and-integrations.md) - deep SAP S/4HANA OData, BAPI, and CPI integration patterns

## Further reading

- [Codebasics](https://codebasics.io) - primary source for this 24-week curriculum (FDE_Roadmap_2026.pdf, September 2026)
- [SAP Business Accelerator Hub](https://api.sap.com) - free sandbox for OData API practice, no SAP license required
- [LangChain Academy](https://academy.langchain.com) - free courses on LangChain and LangGraph for agentic systems
- [Prosci ADKAR Model](https://www.prosci.com/methodology/adkar) - the change management framework for enterprise AI adoption
- [OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-for-large-language-model-applications/) - security requirements for LLM applications
