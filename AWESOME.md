# Awesome FDE Resources

A curated, verified collection of the best resources for becoming and succeeding as a Forward Deployed AI Engineer. Everything here is cited to a primary source. Nothing is synthetic or fabricated.

Last verified: September 2026.

---

## How to use this file

Read this file once top to bottom. Then return to the section that matches your biggest gap. One section per week, applied to something real, is worth more than collecting the entire list at once.

The ordering within each section is priority order: start at the top, go as deep as your gap demands.

---

## 1. Role Understanding — What an FDE Actually Is

Start here if you are still unclear on what the role is and whether it is right for you.

### Videos (watch in this order)

- [Forward Deployed Engineering 101 — Kevin Bai (Anthropic)](https://www.youtube.com/watch?v=KwhgfwOSToQ) — the single best 30-minute primer. Kevin is a founding FDE at Anthropic, ex-Palantir and ex-Rippling. Covers the FDE Flywheel, the Auditing-Evals-Deployment loop, and why model intelligence is commoditized while deployment is the moat
- [This Is How Forward Deployed Engineering Is Actually Done — AI LABS](https://www.youtube.com/watch?v=AD-EmZ3v6-g) — the operational 5-step method: AS-IS auditing, strategic automation triage (AI vs code vs human), failure-oriented building, ground-truth evals, and ROI quantification
- [Forward Deployed Engineer: The Hottest AI Job of 2026 — Aishwarya Srinivasan](https://www.youtube.com/watch?v=w-Z4QYK1QL4) — market positioning and the dual skill stack
- [What is Forward Deployed Engineer (FDE) Role? — Piyush Garg](https://www.youtube.com/watch?v=7JlEs6zyB_U) — boundary between FDE, Solutions Architect, and Core SWE
- [FDE: The $1M/Year AI Job Explained — FDE Academy](https://youtu.be/zXysLUTLjw4) — Palantir origins, audit-to-deployment blueprint, client discovery

### This guide

- [What is an FDE?](role/01-what-is-an-fde.md) — definition, history, and 2026 market context
- [Responsibilities](role/02-responsibilities.md) — what FDEs do day-to-day, including the 12 Core Principles from the Codebasics FDE Roadmap 2026
- [FDE vs Other Roles](role/03-fde-vs-other-roles.md) — how FDE differs from SWE, Solutions Engineer, AI Engineer, and Consultant
- [The FDE Loop](role/05-the-fde-loop.md) — the Kevin Bai FDE Flywheel and the canonical 6-phase operational loop

### Market data

- [Market Overview](job-market/01-market-overview.md) — 146 deduplicated 2026 postings, 1,000%+ YoY growth, median $188,000
- [Compensation](job-market/02-compensation.md) — sourced base, bonus, and equity bands across Early Startups, Growth Tech, and Tier-1 AI Labs

---

## 2. Learning Roadmaps — How to Get There

Choose the roadmap that fits your timeline and background.

### Primary roadmaps

- [24-Week Enterprise FDE Roadmap](learning-paths/24-week-enterprise-fde-roadmap.md) — the complete curriculum sourced from Codebasics FDE Roadmap 2026. Phase 1 (Weeks 1–16): Python and FastAPI, RAG, Agentic AI and MCP, ERP integration, DevOps, LLMOps, System Design. Phase 2 (Weeks 17–24): Problem Discovery, BRD, TDD, Stakeholder Management, UAT, Change Management. Use this if you are starting from scratch or want the full enterprise context
- [90-Day FDE Transition Roadmap](learning-paths/90-day-fde-roadmap.md) — accelerated 12-week curriculum synthesizing FDE Academy masterclasses. Use this if you already have production engineering experience
- [Forward Deployed Engineer (FDE) Roadmap — codebasics](https://www.youtube.com/watch?v=uE4HTkDtp48) — the video walkthrough of the 24-week curriculum by Dhaval Patel and Hemanand Vadivel

### Background-specific paths

- [From Software Engineer](learning-paths/from-software-engineer.md)
- [From AI / ML Engineer](learning-paths/from-ai-ml-engineer.md)
- [From Data Engineer](learning-paths/from-data-engineer.md)
- [From Solutions Engineer](learning-paths/from-solutions-engineer.md)
- [From Consultant](learning-paths/from-consultant.md)
- [Beginner to FDE](learning-paths/beginner-to-fde.md)

---

## 3. Technical Skills — What to Build

### Core documentation

- [Core Technical Skills](skills/01-core-technical-skills.md) — the baseline stack: Python 3.12+, FastAPI, Docker, SQL, LLM APIs

### AI and LLM engineering

- [LLM Application Patterns](ai/01-llm-application-patterns.md) — Structured Extraction, Constrained Decoding, Classification, Hybrid RAG, Summarization, Dialogue State, and Strategic Automation Triage
- [Agents and Tools](ai/02-agents-and-tools.md) — ReAct state machines, MCP, supervised multi-agent pipelines, persistent memory layers
- [Evaluation and Testing](ai/03-evaluation-and-testing.md) — golden evaluation harnesses, LLM-as-judge, Cohen's Kappa
- [Monitoring and Reliability](ai/04-monitoring-and-reliability.md) — OpenTelemetry GenAI, token cost telemetry, drift detection
- [Building Agentic RAG in Production — FDE Academy](https://youtu.be/Ycl5aiYRcmU) — end-to-end technical: data ingestion to cloud deployment
- [Enterprise AI Deployment and Real Pipelines — FDE Academy](https://youtu.be/FSZhPDzESPU) — bridging prototype code to production infrastructure

### Engineering patterns

- [APIs and Integrations](engineering/02-apis-and-integrations.md) — idempotency, exponential backoff, rate limiting, SAP S/4HANA OData and BAPI integration
- [Data Pipelines](engineering/03-data-pipelines.md) — messy enterprise data ingestion, schema drift, CDC pipelines, SAP integration patterns
- [Cloud and Infrastructure](engineering/04-cloud-and-infrastructure.md) — in-VPC zero-egress deployment, AWS PrivateLink, Terraform
- [Security and Compliance](engineering/05-security-and-compliance.md) — OWASP LLM Top 10, RBAC, PII vaults, InfoSec review navigation

### System design

- [Architecture for Customer Systems](system-design/01-architecture-for-customer-systems.md) — designing under customer network, storage, and compute constraints
- [Reference Architectures](system-design/02-reference-architectures.md) — RAG Knowledge Assistant, Real-Time Intake, Edge-to-Cloud, Batch ETL blueprints
- [Trade-offs and Decision Records](system-design/03-trade-offs-and-decision-records.md) — authoring ADRs that withstand customer audit
- [Systems Design and Technical Skills for FDEs — FDE Academy](https://youtu.be/9CmIPfIYPws) — customer-flavored distributed architecture and Python fluency

### Runnable code (all tests passing)

- [interviews/code/](interviews/code/) — 7 runnable Python implementations: `parser.py`, `resilient_client.py`, `rate_limiter.py`, `chunker.py`, `structured_extractor.py`, `vibe_coding_runner.py`, `webhook_receiver.py`
- [portfolio/reference-project/](portfolio/reference-project/README.md) — full production ETISE FastAPI app with hybrid search, RBAC, Docker, and 25-case golden eval suite

---

## 4. Books (read by gap, not cover to cover)

These are from the [reading list](resources/02-reading.md). The gap column tells you which to reach for first.

| Book | Author(s) | Your Gap |
| :--- | :--- | :--- |
| Designing Data-Intensive Applications | Martin Kleppmann | Data systems vocabulary; maps to any customer estate |
| Designing Machine Learning Systems | Chip Huyen | Evaluation-driven platform thinking; still the best for GenAI |
| Site Reliability Engineering | Google (free at [sre.google](https://sre.google)) | SLOs, error budgets, on-call design; the model you leave behind |
| Accelerate | Forsgren, Humble, Kim | CI/CD evidence ammunition for customer conversations |
| Continuous Delivery | Humble, Farley | Making deployments boring in the good sense |
| The Trusted Advisor | Maister, Green, Galford | Trust formation; why admitting what broke earns the account |
| Never Split the Difference | Chris Voss | Scoping conversations, timeline pushback, saying no gracefully |
| Team of Teams | Stanley McChrystal | Why the embedded-engineer model works when committees stall |
| The Mythical Man-Month | Fred Brooks | Read before you promise a date; still correct after 50 years |

---

## 5. Customer and Delivery Skills

### This guide

- [The Engagement Lifecycle](customer/01-engagement-lifecycle.md) — 5 phases from pre-kickoff to SRE handover, with ADKAR change management
- [Requirements to Spec](customer/02-requirements-to-spec.md) — BRD to TDD to SDD specification chain, Spec Clarity Test, UAT matrix
- [Working in Customer Environments](customer/03-working-in-customer-environments.md) — locked-down laptops, air-gapped VPCs, slow ticketing systems
- [Managing Expectations](customer/04-managing-expectations.md) — scope creep, delivering bad news, boundary conditions
- [Discovery and Requirements](skills/02-discovery-and-requirements.md) — conducting technical discovery, extracting pain, writing SOWs
- [Stakeholder Management](skills/04-stakeholder-management.md) — navigating customer politics and de-escalating conflicts
- [Ambiguity and Prioritization](skills/05-ambiguity-and-prioritization.md) — triaging competing requests under time and security constraints

---

## 6. Real Enterprise Case Study

The single best learning resource in this entire repository for understanding what FDE work looks like end to end.

- [Vaayu Pumps Field Service AI — Case Study](case-studies/05-enterprise-manufacturing-vaayu-pumps.md) — synthesized from 83 pages of real enterprise BRD v1.1, TDD v1.0, and SDD v1.0 (Codebasics FDE Roadmap 2026, September 2026). Covers: 4-agent supervised pipeline architecture, SAP S/4HANA OData and BAPI integration, P1–P4 severity decision matrix, skill-based technician routing algorithm, persistent memory layer, bottom-up model routing, DPDP Act data residency, and measured SLA impact

The three source documents (83 pages total) are stored locally in `forward-deployed-engineer-fde-roadmap/` (not pushed to GitHub):

- `01_BRD_VaayuPumps_FieldServiceAI_v1.1.pdf` — 25 pages, business requirements
- `02_TDD_VaayuPumps_FieldServiceAI_v1.0.pdf` — 25 pages, technical design
- `03_SDD_VaayuPumps_FieldServiceAI_v1.0.pdf` — 33 pages, solution design

---

## 7. Interview Preparation

### Process and strategy

- [The Interview Process](interviews/01-interview-process.md) — 7-stage pipeline at Palantir, OpenAI, Anthropic, Scale AI
- [Coding and Technical Rounds](interviews/02-coding-and-technical.md) — what rounds actually test: systems, concurrency, dirty data
- [System Design Rounds](interviews/03-system-design.md) — customer-flavored system design with capacity, network, and failover
- [Customer Scenario Rounds](interviews/04-customer-scenarios.md) — verbatim role-play transcripts, adversarial pushback, 3-tier rubrics
- [Behavioral Rounds](interviews/05-behavioral.md) — ownership stories, stakeholder negotiation, failure under pressure
- [Take-Home Assignments](interviews/06-take-homes.md) — 72-hour enterprise challenge, 100-point rubric, ADR templates
- [Question Bank](interviews/07-question-bank.md) — 17 verified real-world questions with practitioner response playbooks
- [Systems Coding Solutions](interviews/08-coding-solutions.md) — runnable Python implementations with verbal narration scripts
- [Palantir and AI FDE Interview Breakdown — FDE Academy](https://youtu.be/CCt0csEqul0) — live coding, system design, and customer role-play rounds decoded

### Datasets (verified)

- [interviews/dataset/](interviews/dataset/README.md) — 17 audited interview questions, 10-pass verification, JSON schema
- [job-market/dataset/](job-market/dataset/README.md) — 146 deduplicated 2026 enterprise postings with validator

---

## 8. Portfolio

- [What to Build](portfolio/01-what-to-build.md) — 6 principles separating toy tutorials from enterprise artifacts
- [Project Ideas](portfolio/02-project-ideas.md) — 12 customer-grade project specs: fintech, healthcare, infrastructure
- [Presenting Projects](portfolio/03-presenting-projects.md) — architectural READMEs, Loom demos, executive case studies
- [Project Selection Masterclass](portfolio/04-project-selection-masterclass.md) — 5 enterprise archetypes, verified datasets, anti-patterns
- [Reference Project: ETISE](portfolio/reference-project/README.md) — the complete production reference app
- [AI for Forward-Deployed Engineers Masterclass — FDE Academy](https://youtu.be/Fruw822BMBc) — five enterprise portfolio archetypes, why basic AI projects fail

---

## 9. Ongoing Sources (check quarterly)

- [Chip Huyen's blog](https://huyenchip.com) — long-form pieces on GenAI platforms and evaluation practice
- [The Pragmatic Engineer](https://newsletter.pragmaticengineer.com) — best-sourced engineering-industry newsletter; where hiring-market shifts appear with named sources
- [FDE Academy YouTube](https://www.youtube.com/@fdeacademy) — masterclasses, project breakdowns, practitioner video discussions
- [provider documentation](https://docs.anthropic.com) and [platform.openai.com/docs](https://platform.openai.com/docs) — changelogs and model cards move monthly; read these before any architecture conversation
- [LangChain State of Agent Engineering](https://langchain.com) — 2026 survey of how agents are actually deployed in production
- [The New Stack — May 2026 FDE analysis](https://thenewstack.io/forward-deployed-engineers-ai) — why labs hire FDE teams
- [Fortune — September 2026 Lightcast analysis](https://fortune.com/2026/09/03/forward-deployed-engineers-fast-growing-six-figure-silicon-valley-job-integrate-ai-with-customers-tech-careers-palantir) — market sizing and salary data
- [SAP Business Accelerator Hub](https://api.sap.com) — free public sandbox for OData API practice; no SAP installation required

### Practitioner communities

- [fde.academy](https://fde.academy) — interview framing and by-level compensation analyses
- [joinplank.com](https://joinplank.com) — market tracker: 982 postings across 462 companies in 2026
- [fdepulse.com](https://fdepulse.com) — practitioner career write-ups and role mechanics
- [r/mlops](https://www.reddit.com/r/mlops) — most technical FDE-adjacent discussion: monitoring, evaluation, drift

---

## 10. Verified Practitioners to Follow

These are directly cited in the Codebasics FDE Roadmap 2026 and the five verified YouTube masterclasses. Real people, real roles, verified URLs.

- Kevin Bai — founding FDE at Anthropic, ex-Palantir and Rippling. Source of the FDE Flywheel
- Dhaval Patel — co-founder Codebasics and AtliQ Technologies, [codebasics.io](https://codebasics.io)
- Hemanand Vadivel — co-creator Codebasics FDE Roadmap 2026
- Pankaj Jaiswal — FDE in SAP-heavy manufacturing. Source of the Bonus SAP section, [linkedin.com/in/pankaj29](https://www.linkedin.com/in/pankaj29/)
- Rushi Gandhi — FDE practitioner, [linkedin.com/in/rushi0508](https://www.linkedin.com/in/rushi0508/)
- Pranav Modh — FDE practitioner, [linkedin.com/in/modhpranav](https://www.linkedin.com/in/modhpranav/)
- Daksh Trehan — FDE practitioner, [linkedin.com/in/dakshtrehan](https://www.linkedin.com/in/dakshtrehan/)
- Colin Jarvis — OpenAI (listed in Codebasics roadmap as follow)
- Andrej Karpathy — listed in Codebasics roadmap as follow for AI foundations

---

## 11. Job-Readiness Self-Audit

Before applying to any Tier-1 FDE posting (Anthropic, OpenAI, Palantir, Databricks, Scale AI), verify you can honestly say yes to all five:

1. Production microservice — you have deployed an async FastAPI service with Pydantic v2 validation, distributed rate limiting, and idempotent request handling. It is on GitHub with a Dockerfile and passing tests.

2. Quantitative evaluation harness — you have a CLI runner that executes 25 or more golden test cases and reports precision, recall, latency, and citation grounding. It exits 0 on pass and 1 on fail.

3. Customer architectural governance — you have written a complete Architecture Decision Record (ADR) justifying trade-offs (in-VPC Bedrock vs local vLLM) and a cutover rollback runbook.

4. Messy real-world data parsing — you have written defensive parsers that process corrupted real-world enterprise exports (CFPB or SEC EDGAR format) without unhandled exceptions or data loss.

5. Rehearsed ownership stories — you have drafted and verbally rehearsed 6 core ownership stories (outages, stakeholder conflict, impossible deadlines) in STAR format. You can deliver any of them in 90 seconds without notes.

If you can say yes to all five, apply. If not, the [24-Week Enterprise FDE Roadmap](learning-paths/24-week-enterprise-fde-roadmap.md) maps directly to each gap.

---

## Related documents

- [Reading List](resources/02-reading.md) — books, papers, and sources with detailed context
- [Tools](resources/01-tools.md) — the development, deployment, and observability toolbox
- [Communities and People](resources/03-communities-and-people.md) — where practitioners talk and verified people to follow
- [Learning Paths](learning-paths/README.md) — background-specific transition blueprints
