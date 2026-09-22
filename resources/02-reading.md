# Reading List

If you want the short list of books and ongoing sources that repay the time, organized by what each one teaches, this is it. It is opinionated and short on purpose: nine books and a handful of sources, each with the reason it earns a slot. External links are kept to the ones verified at writing time; books are listed by title and author. This page will not stay current forever, so re-check the ongoing sources yearly and drop whatever stops repaying the time.

## Books

Nine books cover the arc of the job. Read them in the order your gap demands rather than cover to cover; the [learning paths](../learning-paths/README.md) tell you which gap is yours.

### Systems and delivery

- Designing Data-Intensive Applications, Martin Kleppmann - the vocabulary for the data systems you will integrate with; customer estates are usually less elegant than chapter one, and this book is how you map theirs fast. The replication, partitioning, and consistency chapters transfer to almost every engagement.
- Accelerate, Nicole Forsgren, Jez Humble, and Gene Kim - the research evidence that delivery performance is measurable; useful ammunition when you argue for CI/CD inside a customer organization, because it converts a preference into a measurement
- Continuous Delivery, Jez Humble and David Farley - the mechanics of keeping software deployable; the practical antidote to the production cliff, and the reason your deployments become boring in the good sense
- Site Reliability Engineering, Google, free online at [sre.google](https://sre.google) - SLOs, error budgets, and on-call design: the operating model you will be asked to leave behind in customer environments; read the SLO and postmortem chapters first if time is short

### AI engineering

- Designing Machine Learning Systems, Chip Huyen - the platform thinking that predates the LLM wave and still structures good GenAI systems: data, features, evaluation, deployment. Evaluation-driven design, the book's throughline, is exactly what separates deployments that survive from demos that impress
- Provider documentation and cookbooks as first-class reading - the model cards, prompting guides, and changelogs at [docs.anthropic.com](https://docs.anthropic.com) and [platform.openai.com/docs](https://platform.openai.com/docs); capabilities move monthly and the docs are the primary source, ahead of every summary of them. An hour in a changelog before an architecture conversation is the highest-yield reading habit on this page

### Customer work

- The Trusted Advisor, David Maister, Charles Green, and Robert Galford - the trust-formation model behind every engagement; short, and re-readable at each career stage. The trust equation explains why the engineer who admits what broke faster than the one who hides it ends up running the account
- Never Split the Difference, Chris Voss - negotiation tactics that translate directly to scoping conversations, timeline pushback, and saying no without losing the room; the calibrated-question technique alone earns the cover price

### Deployments at scale

- Team of Teams, Stanley McChrystal - shared consciousness and empowered execution: the organizational design that forward deployment assumes and most enterprises lack; it explains why the embedded-engineer model works when committee models stall
- The Mythical Man-Month, Fred Brooks - fifty years old and still correct about why adding people to a late project makes it later; read it before you promise a customer a date, and again before you staff a delayed engagement

## Ongoing sources

A small rotation covers what the job demands: hiring-market context, deployment practice, and the practitioner layer where the title itself is discussed. Each entry below is one of those:

- The AI Engineering Field Guide repository ([github.com/alexeygrigorev/ai-engineering-field-guide](https://github.com/alexeygrigorev/ai-engineering-field-guide)) - the field-guide-shaped reference this repository imitates; its [job-scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md) is the dataset behind this guide's market figures and gets re-run over time
- The Pragmatic Engineer ([newsletter.pragmaticengineer.com](https://newsletter.pragmaticengineer.com)) - the best-sourced engineering-industry newsletter; where hiring-market shifts show up with named sources
- Chip Huyen's blog ([huyenchip.com](https://huyenchip.com)) - long-form pieces on GenAI platforms and evaluation practice; the quality bar for writing about production AI
- The New Stack ([the May 2026 FDE analysis](https://thenewstack.io/forward-deployed-engineers-ai)) - practitioner infrastructure journalism; that piece explains why the labs hire FDE teams, and the outlet covers the deployment beat generally
- Fortune's AI coverage - the [September 2026 Lightcast analysis](https://fortune.com/2026/09/03/forward-deployed-engineers-fast-growing-six-figure-silicon-valley-job-integrate-ai-with-customers-tech-careers-palantir) and the [August 2025 MIT pilot-failure report](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo) are the two primary pieces of market context this guide cites
- LangChain's State of Agent Engineering ([langchain.com](https://langchain.com)) - the 2026 survey of how agents are actually deployed in production; useful for separating agent hype from agent practice
- The practitioner sites, individually, since they do different jobs:
  - [fde.academy](https://fde.academy) - interview framing and the by-level compensation analyses, including the August 2026 Palantir breakdown
  - [joinplank.com](https://joinplank.com) - the market tracker; the place to see who is hiring first FDEs right now
  - [fdepulse.com](https://fdepulse.com) - career-ladder write-ups and role mechanics from practitioners
  - [gaijineer.co](https://gaijineer.co) - interview-process accounts, such as the April 2026 Cohere FDE walkthrough

### Video lectures and masterclasses

- [FDE Academy YouTube Channel](https://www.youtube.com/@fdeacademy) - core channel for forward deployed engineering breakdowns and curriculum
- [AI for Forward-Deployed Engineers Masterclass](https://youtu.be/Fruw822BMBc) - five enterprise portfolio archetypes and why basic AI projects fail
- [FDE: The $1M/Year AI Job Explained](https://youtu.be/zXysLUTLjw4) - Palantir origins, the audit-to-deployment blueprint, and client discovery
- [Building Agentic RAG in Production](https://youtu.be/Ycl5aiYRcmU) - end-to-end technical implementation from data ingestion to cloud deployment
- [Enterprise AI Deployment and Real Pipelines](https://youtu.be/FSZhPDzESPU) - bridging prototype code to production infrastructure
- [Palantir and AI FDE Interview Breakdown](https://youtu.be/CCt0csEqul0) - live coding, system design, and customer role-play rounds decoded
- [FDE Roadmap and Core Tech Stack](https://youtu.be/kBM5UXRbo3U) - 90-day technical transition plan
- [Systems Design and Technical Skills for FDEs](https://youtu.be/9CmIPfIYPws) - customer-flavored distributed architecture and Python fluency
- [From Software Engineer to FDE](https://youtu.be/vLlIBT0HSSc) - transition guidance for traditional engineers

### Five verified FDE practitioner masterclasses (September 2026)

These five videos are verified practitioner sources cited in the Codebasics FDE Roadmap 2026 (September 2026):

- [Forward Deployed Engineering 101 — Kevin Bai (Anthropic)](https://www.youtube.com/watch?v=KwhgfwOSToQ) - founding FDE perspective from Anthropic, ex-Palantir and Rippling; covers the FDE Flywheel (how customer deployments generate platform primitives for core SWE), the canonical FDE loop (Auditing to Evals to Deployment), and the strategic thesis that model intelligence is commoditized while custom deployment is the competitive moat
- [This Is How Forward Deployed Engineering Is Actually Done — AI LABS](https://www.youtube.com/watch?v=AD-EmZ3v6-g) - the pragmatic 5-step operational methodology: (1) Observation and AS-IS auditing, (2) Strategic Automation Triage (AI for messy judgment, code for fixed rules, humans for high-stakes decisions), (3) Failure-oriented building, (4) Rigorous ground-truth evals, (5) Quantifiable business ROI metrics
- [Forward Deployed Engineer: The Hottest AI Job of 2026 — Aishwarya Srinivasan](https://www.youtube.com/watch?v=w-Z4QYK1QL4) - market positioning of the FDE role in 2026, dual skill stack (applied AI engineering plus domain translation), and enterprise adoption dynamics
- [What is Forward Deployed Engineer (FDE) Role? — Piyush Garg](https://www.youtube.com/watch?v=7JlEs6zyB_U) - granular operational boundaries between FDE, Solutions Architect, and Core SWE in rapid enterprise delivery cycles
- [Forward Deployed Engineer (FDE) Roadmap — codebasics (Dhaval Patel and Hemanand Vadivel)](https://www.youtube.com/watch?v=uE4HTkDtp48) - complete 24-week transition syllabus, SAP PM integration mechanics, and the end-to-end Vaayu Pumps project execution

A caveat on practitioner video sources: treat them as direct engineering blueprints and experience reports, cross-referencing all architectural claims against the working code in this guide.

### Enterprise document pack (Vaayu Pumps Field Service AI)

Three enterprise production documents (83 pages total) produced during the Codebasics FDE Roadmap 2026 capstone project, demonstrating the BRD-to-TDD-to-SDD specification chain:

- Business Requirements Document (BRD v1.1, September 2026) — 25 pages covering business problem statements (P-1 to P-4), quantifiable success metrics (triage latency, first-time fix rate), MoSCoW functional requirements, integration requirements, and testable acceptance criteria for Vaayu Pumps and Systems Ltd (INR 840 Cr manufacturing firm, 11,000 pumps, 1,400 customer sites, 42 field technicians, 180 complaints per week)
- Technical Design Document (TDD v1.0, September 2026) — 25 pages covering supervised multi-agent pipeline (Ingestion, Diagnosis, Dispatch, Memory and Routing agents), Pydantic v2 schemas, REST API contracts (`POST /v1/complaints`), severity decision tables, SLA windows, technician ranking algorithm, parts shortfall logic, and Annex B Spec Clarity Test
- Solution Design Document (SDD v1.0, September 2026) — 33 pages covering C4 context diagram, hybrid deployment topology (on-premise depot edge vs cloud VPC), SAP CPI integration, bottom-up model routing (Gemini 2.5 Flash and Claude 3.5 Haiku vs frontier models), DPDP Act data residency, and evaluation and observability telemetry

See [Vaayu Pumps case study](../case-studies/05-enterprise-manufacturing-vaayu-pumps.md) for the synthesized field guide document derived from this document pack.



## How to read for FDE work

Recommendations, from watching what works for practicing engineers:

- Read for transferable patterns, not tools. Kleppmann's replication chapters map onto whatever replication setup the customer happens to run; the pattern survives, the product names do not. When you catch yourself reading for a specific product, switch to that product's own docs instead.
- Keep a decision journal. One page per real decision on a live project: the context, the options, the choice, and what you expect to happen. Review it quarterly; the gap between expectation and outcome is your actual curriculum, and it is also raw material for the ownership stories interviews ask for.
- Read the primary source before the commentary. The Fortune piece before the thread about the Fortune piece; the provider changelog before the blog about the provider. Commentary is faster but inherits every error it is built on.
- One book per quarter, applied to a real project, beats ten skimmed. Pick the one that matches your current gap from [the learning paths](../learning-paths/README.md), and read it with a project open in another window.

## Related documents

- [The FDE toolbox](01-tools.md) - the doing counterpart to this reading list
- [Market overview](../job-market/01-market-overview.md) - the sourced data behind the market claims the sources above discuss
- [Learning paths overview](../learning-paths/README.md) - which gap to read for next
- [Core technical skills](../skills/01-core-technical-skills.md) - mapping reading to the evidence-weighted skill stack

## Further reading

- [Site Reliability Engineering, online](https://sre.google) - the full book, free, referenced above
- [Chip Huyen's blog](https://huyenchip.com) - the ongoing writing recommended above
- [The Pragmatic Engineer](https://newsletter.pragmaticengineer.com) - the ongoing newsletter recommended above
