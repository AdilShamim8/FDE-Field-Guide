# FDE Interview Question Bank

This document is a practice tool for Forward Deployed Engineer (FDE) interview preparation: recurring question patterns by round type, paired with the underlying evaluation signals, verbatim candidate playbooks, red flags, and scoring rubrics.

Every question in this bank is **empirically grounded** and backed by our machine-readable [dataset](dataset/fde_interview_questions.json). The questions and evaluation patterns are synthesized from real interview accounts across frontier labs (Google, OpenAI, Anthropic, Palantir), enterprise platforms (Databricks, Scale AI), and published practitioner guides.

---

## Empirical Provenance Matrix

Following the data-first methodology of [alexeygrigorev/ai-engineering-field-guide](https://github.com/alexeygrigorev/ai-engineering-field-guide), every question pattern is mapped to verified practitioner sources:

| Source Authority | Core Topics & Rounds Contributed | Verified Citation Link |
|---|---|---|
| **Nehal Vyas** | 5-round hiring structure, customer simulations, live debugging, RAG vs. fine-tuning, scale failure modes | [fde.hinehal.com/blogs/fde-interview-questions](https://fde.hinehal.com/blogs/fde-interview-questions) |
| **Om Bharatiya** | Problem decomposition ("decomp"), 48-hour executive demo scoping, ER wait time triage, contract debugging | [github.com/ombharatiya](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/15-role-guides/forward-deployed-engineer.md) |
| **Dr. Sundeep Teki** | "Ambiguity by default" operating rhythm, frontier lab loops (OpenAI, Anthropic, DeepMind), executive alignment | [sundeepteki.org/advice](https://www.sundeepteki.org/advice/the-definitive-guide-to-forward-deployed-engineer-interviews-in-2026) |
| **Dr. Sanjay Kumar, PhD** | Top 25 FDE questions, least-privilege agent tool tiers, air-gapped VPC data residency, drift mitigation | [skphd.medium.com](https://skphd.medium.com/top-25-forward-deployed-engineer-fde-interview-questions-and-answers-ad9ac4a6ad7f) |
| **YagyanshB** | Google Forward Deployed Engineering loop, "Vibe Coding" practical round, dirty data extraction under time limits | [github.com/YagyanshB](https://github.com/YagyanshB/google-fde-interview-guide) |
| **Startup.jobs** | Customer simulation role-plays, cross-functional bridge engineering, production triage protocols | [startup.jobs/interview-questions](https://startup.jobs/interview-questions/forward-deployed-engineer) |
| **Alexey Grigorev** | Empirical scrape analysis of 146 deduplicated FDE positions, production ownership vs. customer facing mix | [github.com/alexeygrigorev](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md) |

---

## The Question Bank by Round Type

### 1. Discovery and Requirements Decomposition

- **A customer signed a contract because their CEO said "we need AI." They cannot articulate a use case. Walk me through your first two weeks.** - *signal: hunting operator pain over executive hype; rapid vertical slicing* `[Source: Om Bharatiya, Sundeep Teki]`
- **An enterprise COO says: "Our emergency room wait times are too long. Can AI fix this?" Decompose the problem.** - *signal: pipeline deconstruction; recognizing when NOT to use AI; HIPAA/EHR constraints* `[Source: Om Bharatiya]`
- **A VP says "make our reporting smarter". What do you do first?** - *signal: reaching for discovery and operator workflows before software solutions* `[Source: Nehal Vyas]`
- **The data owner refuses to give access. Walk me through your next move.** - *signal: escalation discipline, governance respect, and unblocking data as critical path* `[Source: Om Bharatiya, Startup.jobs]`
- **How do you tell a real production use case from an executive vanity demo?** - *signal: workflow-integration instinct; measuring daily operator repetition* `[Source: Sundeep Teki]`
- **What belongs in a one-page problem statement before writing code?** - *signal: artifact discipline, quantitative success metrics, named veto stakeholders* `[Source: Startup.jobs]`
- **Two stakeholders give you conflicting requirements. What do you do?** - *signal: resolving contradictions in the room with data, not silently in the code* `[Source: Startup.jobs, Nehal Vyas]`
- **How do you manage an engagement operating under "ambiguity by default"?** - *signal: establishing two-week clickable software cadences; ADR delta logs* `[Source: Sundeep Teki]`

### 2. Practical Coding and Technical Integration

- **In a 60-minute Google FDE "Vibe Coding" / rapid live build round, you receive dirty CSV/JSON data and an API key. How do you structure your time?** - *signal: scoping down to critical path; dirty data defensive parsing; testable seams* `[Source: YagyanshB Google FDE]`
- **Build an idempotent API endpoint that integrates an LLM to extract structured entities from documents, with streaming responses and error recovery.** - *signal: FastAPI, Pydantic schemas, Redis idempotency keys, SSE streaming, auto-retry loops* `[Source: Nehal Vyas]`
- **You have 48 hours before an executive demo to a Fortune 500 leadership team using their proprietary data. What do you build and what do you deliberately cut?** - *signal: ruthlessness in scoping; curated data ingestion; citation trails; failure scripting* `[Source: Om Bharatiya]`
- **A 429 Too Many Requests hits mid-batch. What happens to the rest of the batch?** - *signal: item-level state tracking, Retry-After header with full jitter backoff, checkpointed resume, dead-letter queues* `[Source: Alexey Grigorev, Om Bharatiya]`
- **Parse this malformed export and report defect counts by type.** - *signal: input handling, defensive null checking, and explicit assumption stating* `[Source: YagyanshB Google FDE]`
- **Design a sliding window rate limiter with tiered tenant quotas.** - *signal: multi-tenant quota isolation and boundary burst defense* `[Source: YagyanshB Google FDE]`
- **Make this customer integration testable without access to their staging environment.** - *signal: seams, mock fixtures, synthetic record generators, and contractual fakes* `[Source: Alexey Grigorev]`

### 3. LLM and Applied AI Engineering

- **When would you fine-tune vs. use RAG vs. use prompt engineering?** - *signal: prompt -> RAG -> fine-tune decision hierarchy; talking customers OUT of fine-tuning for factual knowledge* `[Source: Nehal Vyas]`
- **How do you design AI agent tools with least-privilege permissions and robust human-in-the-loop safeguards?** - *signal: tool risk classification (Tier 1 read, Tier 2 reversible write, Tier 3 destructive write); HITL approval gateways* `[Source: Sanjay Kumar PhD]`
- **The model worked in the demo and fails in production. Why?** - *signal: distribution shift, OCR noise, index staleness, context window pollution, and schema drift* `[Source: Om Bharatiya]`
- **The customer wants zero hallucinations. What do you say?** - *signal: probabilistic system framing, groundness metrics, citation verification, and fallback routing* `[Source: Sundeep Teki]`
- **Latency doubled after you added retrieval. What are your options?** - *signal: semantic caching, asynchronous chunk pre-fetching, model tiering (small rerankers), streaming for perceived latency* `[Source: Nehal Vyas]`
- **Structured outputs come back malformed about 2% of the time. What do you build?** - *signal: JSON schema enforcement via instructor/Pydantic, validation exception feedback retry loop, deterministic parser fallback* `[Source: Om Bharatiya, Sanjay Kumar PhD]`

### 4. Enterprise System Design and Deployment

- **If a customer needs our product deployed into their AWS VPC with SSO (SAML/OIDC) and secure ingestion from Snowflake, how would you architect it at a high level?** - *signal: federated SAML/OIDC SSO, PrivateLink network perimeter, secure key-pair Snowflake authentication, zero public egress* `[Source: Startup.jobs]`
- **Design an enterprise document Q&A assistant for a regulated financial institution with strict data residency, auditability, and air-gapped VPC requirements.** - *signal: AWS PrivateLink / Azure Private Link, customer-managed KMS encryption, on-prem vLLM inference, append-only audit logging* `[Source: Sanjay Kumar PhD]`
- **We are rolling this system out from 1 pilot to 50 enterprise customers. What breaks first and how do you monitor it?** - *signal: model provider rate limits, per-tenant cost explosion, silent schema drift, OpenTelemetry latency and recall metrics* `[Source: Nehal Vyas]`
- **Where does the model run in this design, and why?** - *signal: data residency perimeters, egress costs, latency budgets, and compliance posture* `[Source: Sundeep Teki]`
- **What data leaves the customer boundary in this design?** - *signal: proactive CISO architecture delivery; 3-tier egress classification (PII, vector embeddings, telemetry)* `[Source: Om Bharatiya, Sanjay Kumar PhD]`
- **Who is on call when this breaks at 2 a.m.?** - *signal: phased operational handover (pilot -> shadowing -> customer ownership), runbook verification, SLA escalation contracts* `[Source: Nehal Vyas, Startup.jobs]`

### 5. Live Production Debugging

- **The pilot RAG system is giving wrong answers on customer contracts. You are on-site tomorrow. How do you debug it?** - *signal: bisection methodology (retrieval miss vs. generation hallucination); chunk inspection; adding regression tests to golden suite* `[Source: Om Bharatiya]`
- **The customer's integration suddenly returns empty results in production. What do you check first?** - *signal: structured triage (reproduce -> change check -> auth/quota -> network proxy -> data schema)* `[Source: Nehal Vyas]`
- **Answers are wrong every Monday. Hypotheses?** - *signal: Sunday night scheduled ETL batch sync failure, timezone boundary edge cases, weekend ticket backlog queue starvation* `[Source: Nehal Vyas, Om Bharatiya]`
- **Two services disagree about the same record. Which is right, and how do you find out?** - *signal: authoritative systems of record by business domain, message lineage inspection, diff reconciliation reports, signed ADRs* `[Source: Startup.jobs, Alexey Grigorev]`

### 6. Customer Simulation and Role-Play

- **Interviewer role-plays a furious VP: "Your implementation is two weeks late and my CEO is asking why we hired you." How do you respond?** - *signal: composure under pressure; non-defensive validation; honest root-cause status; concrete date commitments; clear stakeholder asks* `[Source: Nehal Vyas]`
- **The customer insists on an architectural approach you think is wrong and will fail in production. What do you do?** - *signal: uncovering underlying motivation; translating technical risk into dollar/latency terms; running 48-hour side-by-side benchmarks; disagree-and-commit with ADR* `[Source: Nehal Vyas]`
- **"Our CEO saw a demo and wants AI everywhere across 4 divisions by next quarter."** - *signal: scoping under hype; identifying one high-ROI beachhead workflow; protecting client engineering from distraction* `[Source: Sundeep Teki]`
- **"Your system gave a wrong answer to an external client today."** - *signal: disciplined 4-phase incident triage (immediate acknowledgement -> trace bisection -> blast radius containment -> postmortem regression closure)* `[Source: Om Bharatiya, Nehal Vyas]`

### 7. Behavioral and Ownership

- **Walk me through a system you built and deployed to production that failed, and how you owned the outcome.** - *signal: end-to-end operational ownership; blameless postmortem culture; permanent automated prevention* `[Source: Alexey Grigorev, Google FDE]`
- **Describe a time you pushed back on a customer requirement.** - *signal: customer expectation management; courage to say no with data; protecting customer outcome over short-term pleasing* `[Source: Om Bharatiya]`
- **A project you owned from discovery to production handover.** - *signal: full-loop engineering agency; working across customer IT, executive sponsors, and internal product teams* `[Source: Startup.jobs]`

---

## Deep Response Playbooks for High-Signal Probes

The ten questions below represent the most predictive probes in enterprise FDE interview loops. For each, we provide the verified practitioner signal, a verbatim senior FDE response, the red flag response that gets candidates rejected, and the exact evaluation scoring rubric.

---

### 1. "A customer signed a contract because their CEO said 'we need AI.' They cannot articulate a use case. Walk me through your first two weeks."
*Verified Source: [Om Bharatiya (AI-Engineer-Interview-Questions)](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/15-role-guides/forward-deployed-engineer.md)*

#### The signal
Evaluates ambiguity tolerance, operator discovery over executive hype, identifying high-volume language bottlenecks, and scoping a thin vertical slice.

#### Senior FDE response
"Week one is discovery, not building. I ask for three things: access to the operators who feel workflow pain daily, a tour of the systems of record where work actually occurs, and examples of the business artifacts (tickets, contracts, logs, reports). I hunt for workflows that meet four criteria: (a) high-volume, (b) language-heavy, (c) currently performed by expensive domain specialists, and (d) tolerant of human review before action.

I run 30-minute interviews with 5 to 8 frontline operators asking: 'What did you do yesterday, hour by hour?' rather than 'What could AI do for you?' The latter produces science fiction; the former produces viable use cases. Concurrently, data access is usually the critical-path bottleneck, so I file security and data boundary requests on day one.

In week two, I pick one candidate use case and build a thin vertical slice on real customer data by day 10—not a slide deck. The demo is framed explicitly as 'directionally right, not production.' This grounds executive discussions in concrete reality, allowing stakeholders to react to software.

Deliverables at two weeks: one working clickable slice, a ranked backlog of 2-3 follow-on use cases with effort sizing, and an unblocked data access register."

#### The red flag response
"I organize several executive brainstorming sessions with the VP to design an end-to-end autonomous transformation strategy, then start fine-tuning a frontier model on their documentation."

#### Scoring rubric
- **Strong Hire**: Distinguishes operator discovery from executive mandates; targets high-volume language tasks; files data access requests on day one; delivers a working thin slice within 10 days to drive concrete feedback.
- **Hire**: Focuses on gathering user requirements before writing code and attempts to build a quick demo.
- **No Hire**: Accepts the vague mandate at face value; proposes multi-month R&D research projects or blames the customer for not having clear specifications.

---

### 2. "An enterprise COO says: 'Our emergency room wait times are too long. Can AI fix this?' Decompose the problem."
*Verified Source: [Om Bharatiya (AI-Engineer-Interview-Questions)](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/15-role-guides/forward-deployed-engineer.md)*

#### The signal
Tests problem decomposition into functional pipelines, constraint identification (HIPAA, EHR integration, clinician sign-off), knowing when NOT to use AI, and thin wedge selection.

#### Senior FDE response
"I do not answer the question as asked; I decompose it. 'Wait time' is an aggregate metric resulting from a sequential pipeline: arrival -> triage -> bed assignment -> physician evaluation -> diagnostics -> disposition.

First question to the COO: where does your historical data show the bottleneck accumulating? If they lack instrumentation, step one is telemetry and basic data logging, not AI.

Second, I categorize stages by AI suitability:
- Safe, high-leverage language candidates: triage-note summarization for nursing handoffs, drafting discharge instructions (often the hidden blocker holding occupied beds), and extracting structured billing codes from doctor voice memos.
- Classic ML candidates: admission likelihood prediction and hourly staffing demand forecasting. These require clean tabular historical data and clinical calibration.
- Explicitly ruled out: autonomous diagnostic or triage prioritization decisions. Regulatory, clinical liability, and patient safety requirements dictate that anything touching clinical judgment mandates a human clinician in the loop by design.

Third, verify constraints: EHR integration pathways (Epic/Cerner via HL7/FHIR), PHI handling under HIPAA (BAA agreements with model providers or private VPC inference), and clinical safety committee sign-off.

I propose a wedge project: discharge summary drafting. It is measurable (bed turnover velocity), language-native, human-reviewed by design, and improves operational throughput without autonomous medical liability."

#### The red flag response
"We can train a transformer model on historical ER admissions to autonomously diagnose incoming patients at triage and predict discharge times."

#### Scoring rubric
- **Strong Hire**: Deconstructs the holistic metric into pipeline stages; probes for baseline instrumentation; explicitly rejects autonomous clinical decisions; identifies HIPAA/EHR constraints; selects a safe, high-leverage wedge.
- **Hire**: Recognizes that the problem has multiple sub-steps and highlights regulatory or privacy concerns.
- **No Hire**: Promises that an AI chatbot or end-to-end LLM can solve ER wait times; ignores patient safety regulations.

---

### 3. "In a 60-minute Google FDE 'Vibe Coding' / live build round, you receive dirty CSV/JSON data and an API key. How do you structure your time?"
*Verified Source: [YagyanshB (Google FDE Interview Guide)](https://github.com/YagyanshB/google-fde-interview-guide)*

#### The signal
Evaluates rapid prototyping under pressure, scoping down to the critical path, defensive data cleaning, testable seams over boilerplate architecture, and verbalized engineering narration.

#### Senior FDE response
"In rapid live coding rounds, candidates fail when they over-architect or spend 40 minutes setting up boilerplate classes before data flows. I structure the 60 minutes into four strict phases:

- Minutes 0 to 10 (Inspection & Alignment): Inspect the raw schema and print data anomalies (missing values, mixed date formats, malformed nested JSON). I state my assumptions aloud and agree with the interviewer on the single core happy path that constitutes success.
- Minutes 10 to 35 (Core Engine & Integration): Build the data transformation pipeline with defensive parsing fallbacks, followed immediately by the LLM API integration. I use simple, testable functions with type hints rather than deeply nested OOP hierarchies.
- Minutes 35 to 50 (Hardening & Edge Cases): Write 3-4 concrete unit assertions verifying edge cases: null handling, prompt token limits, and handling malformed API responses.
- Minutes 50 to 60 (Run & Articulate): Execute the script end-to-end on live sample data. I narrate remaining technical debt cleanly: 'In a production deployment, I would replace this in-memory list with a Redis queue, add OpenTelemetry tracing, and implement an exponential backoff retry wrapper around the API client.'"

#### The red flag response
"Spends 40 minutes designing abstract base classes, Dockerfiles, and directory structures without executing an API call or handling dirty data."

#### Scoring rubric
- **Strong Hire**: Quickly inspects edge-case data quirks; produces running software that completes the core workflow within time; articulates conscious tradeoffs clearly.
- **Hire**: Produces working code that meets the prompt requirements with minor prompt/data hiccups.
- **No Hire**: Does not produce running code; gets stuck in boilerplate configuration or panics under time constraints.

---

### 4. "You have 48 hours before an executive demo to a Fortune 500 leadership team using their proprietary data. What do you build and what do you deliberately cut?"
*Verified Source: [Om Bharatiya (AI-Engineer-Interview-Questions)](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/15-role-guides/forward-deployed-engineer.md)*

#### The signal
Tests executive demo prioritization, scope ruthlessness, grounding and citation verification, and proactive failure scripting.

#### Senior FDE response
"First hour: lock scope with the account executive or meeting owner. One workflow, five minutes of live demonstration, and one clear business wow-moment (e.g., querying across disparate ERP tables that previously took analysts days).

Build priorities, in order:
1. Ingestion of a curated subset: 50 clean, high-signal documents beat 50,000 messy ones every time.
2. Hardened happy path: script the 5 demo queries and test them 20 times each to verify consistent output.
3. Grounding and citations: ensure every model answer highlights clickable source excerpts. The first executive objection is always 'How do I know this is not hallucinated?'; clickable citations neutralize that objection immediately.
4. Clean, intentional UI: simple, polished tables and typography beat flashy, fragile UI elements.

Deliberate cuts:
- Auth & SSO: use a single hardcoded session.
- Automated evals: hand-verify the demo set instead.
- Broad edge-case coverage: steer the demo presentation away from unvetted edges.
- Scale & concurrency: optimize for 1 presenter, not 1,000 users.
- Write actions: strictly read-only; no automated writes for demos.

Two non-negotiable disciplines: rehearse twice on the exact venue network, and prepare a recovery script: if the model stumbles live, I say 'That illustrates exactly why we build automated citation verifiers and evaluation gates in production.'"

#### The red flag response
"Attempts to ingest the full uncurated multi-gigabyte corpus overnight, implements autonomous write tools without guardrails, or fails to prepare a backup path for model latency/outage."

#### Scoring rubric
- **Strong Hire**: Prioritizes curated data and source citations; ruthlessly cuts non-essential production features (SSO, scale, write tools); rehearses live venue networking; scripts failure recovery.
- **Hire**: Focuses on delivering a working happy-path demo and explains what was left out.
- **No Hire**: Tries to build the entire production system in 48 hours; delivers a broken or ungrounded demo.

---

### 5. "When would you fine-tune vs. use RAG vs. use prompt engineering?"
*Verified Source: [Nehal Vyas (fde.hinehal.com)](https://fde.hinehal.com/blogs/fde-interview-questions)*

#### The signal
Tests architectural pragmatism, understanding the simplest-viable-system principle, and knowing when to talk enterprise customers OUT of expensive fine-tuning.

#### Senior FDE response
"My architectural hierarchy follows the principle of simplest sufficient mechanism: Prompt Engineering -> RAG -> Fine-Tuning.

1. Prompt Engineering with in-context examples is always step one. It requires zero infrastructure, iterates in seconds, and resolves 70% of formatting, tone, and reasoning issues.
2. RAG (Retrieval-Augmented Generation) is required when the model needs access to dynamic, proprietary, or private enterprise knowledge that cannot fit in a prompt or updates frequently (e.g. internal wikis, customer support tickets, catalog inventory). RAG provides source citations and updates immediately when documents change.
3. Fine-tuning is reserved strictly for teaching behavior, specialized syntax, or compressing capability. Valid reasons to fine-tune: enforcing complex structured outputs that prompt engineering fails to stabilize, adhering to niche domain style (e.g., medical pathology summaries), or distilling a 70B frontier model's performance into an 8B open-weight model to cut inference latency and costs.

I explicitly advise enterprise customers against fine-tuning to inject factual knowledge: training data is expensive to curate, knowledge goes stale immediately, and fine-tuning does not eliminate hallucinations or provide verifiable citation links."

#### The red flag response
"Whenever a customer provides their company PDF manuals, we should immediately fine-tune an LLM on those files so it memorizes the business."

#### Scoring rubric
- **Strong Hire**: Enforces prompt -> RAG -> fine-tune progression; articulates why fine-tuning fails for dynamic factual knowledge; considers maintenance and distillation trade-offs.
- **Hire**: Explains the difference between RAG for dynamic context and fine-tuning for style/format.
- **No Hire**: Recommends fine-tuning to update daily facts or claims prompting is insufficient for any serious task.

---

### 6. "How do you design AI agent tools with least-privilege permissions and robust human-in-the-loop safeguards?"
*Verified Source: [Dr. Sanjay Kumar PhD (Medium)](https://skphd.medium.com/top-25-forward-deployed-engineer-fde-interview-questions-and-answers-ad9ac4a6ad7f)*

#### The signal
Evaluates agentic deployment security, tool risk classification (read vs. reversible write vs. destructive write), human-in-the-loop approval workflows, and blast radius defense.

#### Senior FDE response
"In enterprise agent deployments, models must never possess unconstrained API credentials. I enforce least-privilege tool execution across three risk tiers:

- Tier 1 (Read-Only Tools): Searching documentation, querying vector stores, retrieving read-only CRM data. These execute autonomously but are scoped with tenant-isolation filters and token budgets.
- Tier 2 (Reversible Writes): Generating draft emails, creating staged tickets, updating sandbox records. The agent can invoke these tools, but all mutations are marked as 'PENDING_CONFIRMATION' and require explicit schema validation and append-only audit logging.
- Tier 3 (High-Impact / Destructive Writes): Initiating wire transfers, issuing refunds, deleting records, deploying code, modifying user permissions. These strictly require Human-in-the-Loop (HITL) approval.

Architecture: When the agent decides to invoke a Tier 3 tool, it generates an idempotent ActionProposal payload containing proposed parameters, justification, and an expiration timestamp. The system halts the execution branch and sends an approval card to authorized personnel via Slack/Teams or admin portal. Only upon cryptographic human sign-off does the execution engine dispatch the API call."

#### The red flag response
"Gives the agent API keys with full admin rights and relies on a system prompt instruction telling it 'please only perform safe actions'."

#### Scoring rubric
- **Strong Hire**: Classifies tools by risk level; isolates read operations from destructive writes; mandates human approval for high-risk operations; enforces parameter bounds and audit trails.
- **Hire**: Mentions restricting tool access and keeping human review on important actions.
- **No Hire**: Allows agents unconstrained execution capabilities; fails to consider security vulnerabilities of tool use.

---

### 7. "The pilot RAG system is giving wrong answers on the customer's contracts. You are on-site tomorrow. How do you debug it?"
*Verified Source: [Om Bharatiya (AI-Engineer-Interview-Questions)](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/15-role-guides/forward-deployed-engineer.md)*

#### The signal
Tests bisection debugging methodology (retrieval vs. generation), error taxonomies, chunk inspection, and preventing regression via golden eval suites.

#### Senior FDE response
"Before flying on-site, I request 10 concrete failing examples with the exact customer input, the generated incorrect answer, and the verified correct clause. 'It's wrong sometimes' is impossible to debug; 10 concrete traces cluster into root causes.

On-site, I bisect the pipeline into retrieval vs. generation:
For each failure, I inspect the raw retrieved chunks passed into the prompt context.
1. If the correct clause was NOT retrieved: this is a retrieval defect. I investigate: Did OCR fail on scanned tables? Did naive fixed-length chunking split a critical indemnity clause across boundaries? Did vector semantic similarity miss keyword-exact terms (e.g. Section 14.2)? Fix: Increase chunk overlap, implement hybrid search (dense embeddings + BM25 keyword matching), or add a cross-encoder reranker.
2. If the correct clause WAS retrieved: this is a generation/context defect. I investigate: Did large context cause 'lost in the middle' attention degradation? Did contradictory boilerplate confuse the model? Was the system prompt ambiguous on how to interpret silence? Fix: Re-order context by relevance, tighten negative constraints ('refuse to answer if not explicitly stated in context'), and enforce strict citation output schemas.

Finally, I codify all 10 examples into our automated golden evaluation dataset with assertion gates to ensure regressions cannot deploy."

#### The red flag response
"Tinkers with the prompt wording randomly or suggests upgrading to a bigger model without looking at the retrieved text."

#### Scoring rubric
- **Strong Hire**: Systematically bisects retrieval vs generation; diagnoses chunking/embedding vs context attention issues; converts production failures into regression tests.
- **Hire**: Checks both the search results and the model prompt to see where the mistake happened.
- **No Hire**: Tinkers blindly with prompts; blames the model or claims RAG cannot handle contracts.

---

### 8. "Interviewer role-plays a furious VP: 'Your implementation is two weeks late and my CEO is asking why we hired you.' How do you respond?"
*Verified Source: [Nehal Vyas (fde.hinehal.com)](https://fde.hinehal.com/blogs/fde-interview-questions)*

#### The signal
Evaluates composure under fire, non-defensive accountability, separating technical facts from excuses, delivering concrete recovery dates, and establishing collaborative customer action items.

#### Senior FDE response
"I stay calm, listen without interrupting, and refrain from defensiveness.

1. Validate the frustration: 'I completely understand your frustration. If I were reporting to your CEO, I would be asking the exact same question. We take full accountability for getting this live.'
2. State the objective technical facts without jargon: 'The data ingestion pipeline and model integration are functional in staging. However, during end-to-end testing with your billing database, we discovered that 12% of customer invoice records had inconsistent date encodings, which caused extraction validation to halt to protect data integrity.'
3. Provide a concrete recovery plan with committed milestones: 'Here is how we close the gap: we have completed the patch for the invoice parser today. Tomorrow at 2 PM, we re-run staging validation. On Thursday, we run user acceptance testing with your lead analyst, and on Friday at 9 AM, we initiate production rollout.'
4. Ask for what you need: 'To stay on this schedule, we need 30 minutes with your database administrator tomorrow morning to verify the historical date formats.'
5. Follow up in writing: within 30 minutes of the call, I send an executive summary email documenting the timeline, dependencies, and owners."

#### The red flag response
"Gets defensive, argues that the customer's dirty data caused the delay, or makes an unrealistic promise ('I will have it done tomorrow at 8 AM') just to end the uncomfortable conversation."

#### Scoring rubric
- **Strong Hire**: De-escalates tension calmly; validates customer stakes; gives honest technical status with concrete dates; defines clear mutual action items; follows up in writing.
- **Hire**: Maintains composure, explains the reason for the delay, and provides an updated timeline.
- **No Hire**: Argues with the customer; blames customer employees; makes empty promises to escape the conversation.

---

### 9. "The customer insists on an architectural approach you know is technically wrong and will fail in production. What do you do?"
*Verified Source: [Nehal Vyas (fde.hinehal.com)](https://fde.hinehal.com/blogs/fde-interview-questions)*

#### The signal
Tests customer diplomacy, translating technical debt into business impact, running empirical benchmarks, and practicing healthy disagree-and-commit discipline.

#### Senior FDE response
"1. Understand the root motivation: I do not attack their proposal. I ask open-ended questions: 'Help me understand how your team arrived at this architecture—are there legacy system constraints, security policies, or internal tooling requirements driving this?'
2. Translate technical concerns into customer business risks: Customers ignore abstract software design complaints, but they care about dollars, latency, and downtime. Instead of saying 'Your pipeline design isn't scalable', I explain: 'Under this architecture, querying external APIs synchronously on every user turn will introduce 4 to 6 seconds of latency and expose the workflow to third-party outages that will halt your customer service desk.'
3. Offer an empirical proof of concept: I propose a 48-hour side-by-side benchmark: 'Let's build a prototype of both approaches on a sample of 500 records and measure latency, cost per 1,000 queries, and error rates.'
4. Disagree and commit: If after reviewing the data they still insist, I document the decision and its risks in an Architecture Decision Record (ADR) signed by stakeholders, build the requested architecture cleanly, and ensure defensive monitoring and alerting are deployed to detect failures quickly."

#### The red flag response
"Refuses to write the code; calls the customer's architecture stupid; or silently writes the bad code without warning them of risks."

#### Scoring rubric
- **Strong Hire**: Uncovers the root motivation; translates technical debt into dollar and latency impact; proposes objective data benchmarks; documents risk in an ADR while preserving trust.
- **Hire**: Explains why the approach is risky and suggests an alternative.
- **No Hire**: Refuses to cooperate or mocks the customer; silently complies while knowing the system will break.

---

### 10. "Walk me through a system you built and deployed to production that failed, and how you owned the outcome."
*Verified Source: [Alexey Grigorev (AI Engineering Field Guide)](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)*

#### The signal
Evaluates full-lifecycle operational ownership, blameless postmortem discipline, telemetry awareness, and permanent automated prevention.

#### Senior FDE response
"I discuss an enterprise document ingestion pipeline I owned for a legal customer.
- Architecture: Users uploaded multi-hundred-page contract portfolios. The pipeline extracted text, generated embeddings, and populated a vector index.
- The Failure: During an unannounced customer audit, legal associates uploaded 4,000 contracts simultaneously. Our ingestion workers flooded the embedding API, hitting account-level TPM rate limits. The unhandled 429s triggered worker crashes, creating a backlog that delayed search access for 6 hours during active litigation review.
- Immediate Response: I acknowledged the outage within 15 minutes, communicated status updates to customer leads every 30 minutes, deployed a temporary circuit breaker to halt new batch submissions, and manually drained poisoned queue items.
- Root Cause & Permanent Prevention: The system lacked backpressure and item-level retry isolation. Within 48 hours, I published a blameless postmortem. I re-architected the worker queue with token-bucket rate limiting, exponential backoff with full jitter, item-level state machines, and a Dead Letter Queue (DLQ). I committed an automated integration test that simulates 10x burst traffic to ensure the system degrades gracefully under rate limits."

#### The red flag response
"Describes an incident where they blame third-party APIs or infrastructure teams and took no personal ownership, or claims they have never had a production outage."

#### Scoring rubric
- **Strong Hire**: Demonstrates full production ownership; details structured incident triage; communicates transparently with stakeholders; adds regression tests and architectural guardrails.
- **Hire**: Describes a real production failure and how they fixed it.
- **No Hire**: Passes blame to colleagues; claims their code has never failed; exhibits defensiveness.

---

## How to Use This Bank

- **Practice out loud**: Answers that remain in your head have never survived an adversarial room. Rehearse responses verbally into a recorder or with a technical peer.
- **Time-box rigorously**: Limit discovery and coding explanations to 2-3 minutes, and scenario role-plays to 5 minutes. Stopping on time signals executive composure.
- **Run mock role-plays**: Alternate being the stressed customer VP and the FDE. Playing the customer teaches you how transparent communication de-escalates tension.
- **Track your weak points**: Note questions where you reached for excuses or jumped to code before clarifying constraints. Re-run those questions weekly.

---

## Related Documents

- [Dataset Schema & Provenance](dataset/README.md) - dataset structure and verification guidelines
- [Validated Dataset File](dataset/fde_interview_questions.json) - machine-readable JSON questions and rubrics
- [Coding and Technical Rounds](02-coding-and-technical.md) - practical coding challenge breakdowns
- [Coding Round Solutions](08-coding-solutions.md) - runnable implementations for rate limiters, extractors, and chunkers
- [Customer Scenario Rounds](04-customer-scenarios.md) - adversarial discovery transcripts and role-plays
- [System Design Rounds](03-system-design.md) - enterprise VPC blueprints and security perimeters
- [The Interview Process](01-interview-process.md) - round-by-round hiring timelines

---

## References & Further Reading

1. **Nehal Vyas**: [Forward Deployed Engineer Interview Questions & Answers](https://fde.hinehal.com/blogs/fde-interview-questions)
2. **Om Bharatiya**: [AI Engineer Interview Questions: Forward Deployed Engineer Guide](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/15-role-guides/forward-deployed-engineer.md)
3. **Dr. Sundeep Teki**: [The Definitive Guide to Forward Deployed Engineer Interviews in 2026](https://www.sundeepteki.org/advice/the-definitive-guide-to-forward-deployed-engineer-interviews-in-2026)
4. **Dr. Sanjay Kumar, PhD**: [Top 25 Forward Deployed Engineer (FDE) Interview Questions and Answers](https://skphd.medium.com/top-25-forward-deployed-engineer-fde-interview-questions-and-answers-ad9ac4a6ad7f)
5. **YagyanshB**: [Google Forward Deployed Engineering Interview Prep Guide](https://github.com/YagyanshB/google-fde-interview-guide)
6. **Startup.jobs**: [Forward Deployed Engineer Interview Questions & Answers](https://startup.jobs/interview-questions/forward-deployed-engineer)
7. **Alexey Grigorev**: [AI Engineering Field Guide: FDE Data Analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)
