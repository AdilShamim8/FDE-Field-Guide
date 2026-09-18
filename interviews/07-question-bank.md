# FDE Interview Question Bank

This file is a practice tool for FDE interview preparation: recurring question patterns by round type, each with the signal the interviewer is listening for. The questions are practitioner-pattern-based, assembled from guides and reports (fde.academy, Exponent, the gaijineer.co Cohere account, Reddit threads, 2026); the exact wording is fictional but representative, and no company's actual question set is reproduced. This is not a leaked-answers sheet - the value is practicing the signals, not memorizing phrasing.

## How the bank is organized

One subsection per round type. Each question is followed by a dash and the signal behind it. Questions overlap deliberately: the same scenario can open a discovery round or a design round, and interviewers reuse patterns the way the job does. Revisit the bank after each mock interview; the questions you answered clumsily are the ones worth re-running a week later.

## The question bank by round type

### Discovery and requirements

- A VP says "make our reporting smarter". What do you do first? - whether you reach for discovery before solutions
- The data owner refuses to give access. Walk me through your next move - escalation discipline and respect for governance
- The customer asks for a chatbot. What do you ask next? - finding the problem behind the ask
- How do you tell a real use case from a demo-driven one? - workflow-integration instinct
- What would you need to see before calling a pilot successful? - success metrics over enthusiasm
- Who decides whether this ships, and who can veto it? - decision-process probing
- Two stakeholders give you conflicting requirements. What do you do? - resolving contradictions in the room, not in the code
- What belongs in a one-page problem statement? - artifact discipline
- How do you scope a first deployment you can actually deliver? - thin slicing and honest sizing
- What has been tried before here, and how would you find out? - prior-attempts discipline

### Technical and coding

- Parse this malformed export and report defect counts by type - input handling, and whether you state assumptions
- Design an idempotent webhook receiver - delivery semantics and deduplication thinking
- This retry loop hammers a rate-limited API. Fix it - backoff, jitter, and budget awareness
- Extract structured fields from this text, with validation - structured outputs and retry design
- A 429 hits mid-batch. What happens to the rest of the batch? - partial-failure handling
- What timeout would you set here, and why? - reasoning about defaults instead of inheriting them
- Review this snippet that logs full request bodies - secrets and PII in logs
- Make this integration testable without the customer's staging environment - seams, fixtures, and fakes
- Here is a failing trace. Where do you look first? - hypothesis discipline before fixes
- Implement a sliding window rate limiter with tiered tenant quotas - quota isolation and boundary burst defense
- Split an enterprise document into token-aware chunks with sliding overlap and metadata - retrieval preservation

### AI and LLM engineering

- Retrieval quality is poor on the customer's documents. Walk me through debugging it - splitting retrieval from generation before touching prompts
- Design a small eval for this extraction feature - golden-set thinking and honest metrics
- When would you not use an agent here? - simplest-thing discipline
- The customer wants zero hallucinations. What do you say? - probabilistic-system framing and expectation setting
- How do you contain hallucinations when you cannot eliminate them? - grounding, citations, refusal behavior, and routing
- What is your context budget in this design, and what gets cut first? - context engineering
- The model worked in the demo and fails in production. Why? - distribution shift between curated and real data
- Structured outputs come back malformed about 2% of the time. What do you build? - validation plus a retry that feeds the error back
- How would you evaluate a prompt change before shipping it? - regression discipline
- Latency doubled after you added retrieval. What are your options? - budgets, caching, and graceful degradation

### System design and deployment

- Design a document Q&A assistant for an insurance back office with strict data residency - constraint discovery before architecture
- Design ticket triage for a company with two ops engineers - designing for the operator
- Where does the model run in this design, and why? - residency, egress, and cost reasoning
- What is your rollout plan, and what is the rollback? - staged delivery with a reverse gear
- What data leaves the customer boundary in this design? - data boundaries raised unprompted
- Who is on call when this breaks at 2 a.m.? - ownership design
- What would you cut to ship in six weeks? - scoping under a real deadline
- Which parts of this would you buy rather than build? - build-versus-buy judgment
- The model provider has an outage. What does your system do? - graceful degradation
- What does this cost to run per month, and who approves that number? - cost visibility and stakeholder awareness

### Debugging

- The system got slower two weeks after launch. Find it - correlation versus causation, and a structured hunt
- Answers are wrong every Monday. Hypotheses? - scheduled-job staleness and time-patterned failure
- The customer says it "fails sometimes". How do you reproduce it? - handling the unreproducible without flailing
- You cannot access the logs. What do you do? - working through opacity with what you can request
- Your fix passed your tests but broke their workflow. What now? - eval gaps, rollback, and trust repair
- Walk me through a production incident you handled end to end - structure under pressure, from your own history
- Two services disagree about the same record. Which is right, and how do you find out? - boundary contracts and evidence
- How do you keep the customer informed while you debug? - updates on a clock, with facts separated from speculation
- What would you have instrumented on day one to catch this faster? - prevention instincts after the fix

### Customer scenarios

- "Our CEO saw a demo and wants AI everywhere by Q3" - discovery under hype
- "The pilot works but ops will not support it" - stakeholder conflict and ownership design
- "We go live in six weeks and security has reviewed nothing" - sequencing and honesty
- "Everything you showed us is fine, but it is too slow" - expectations and priority discipline
- "Can you just add this one thing?" - scope-creep handling
- "Your system gave a wrong answer to a customer today" - composure and ownership under fire

### Behavioral

- A project you owned end to end - agency
- A requirement you pushed back on - judgment
- Debugging something you did not build - ownership beyond your own code
- When did you under-deliver, and what did you do next? - honesty and recovery
- A time you said no to a customer - expectation management
- A failure you repaired - postmortem habits
- A time you made someone else successful - cooperation and low ego

## Deep response playbooks for high-signal questions

The ten questions below represent the most predictive probes in enterprise FDE interview loops. For each, we provide the underlying signal, a verbatim senior FDE response, the red flag answer that gets candidates rejected, and the evaluation scoring rubric.

### 1. "A VP says 'make our reporting smarter'. What do you do first?"

#### The signal

Tests whether you reach for discovery before solutions. Junior candidates immediately propose vector search or automated LLM summarizers. Senior FDEs treat the request as an ambiguous symptom, identifying who reads the report, what business decisions depend on it, and what currently fails.

#### Senior FDE response

"I do not touch code or model architecture. First, I schedule a 30-minute discovery session with the actual consumers of the reports rather than the VP who sponsored it. I ask three specific questions:

First, what decision does this report trigger today, and what happens if the report arrives three hours late? If nobody makes an operational decision from the report, automating it produces zero business value.

Second, what is broken about the current report: is it the latency of generation, inaccurate source data from legacy databases, or unstructured free text that nobody has time to read?

Third, what does a successful output look like in numbers? If we cannot define a quantifiable metric, such as reducing analyst drafting time from 45 minutes to 5 minutes with zero ungrounded metrics, we do not have a deployment-shaped project.

From that conversation, I write a one-page Problem Statement and Scope Boundary document before proposing any technical architecture."

#### The red flag response

"I would immediately build a LangChain agent with a retrieval pipeline over their SQL database so the VP can chat with their data using natural language."

#### Scoring rubric

- Strong Hire: refuses to propose architecture without talking to report consumers; identifies decision stakes; demands quantifiable acceptance metrics; produces a one-page problem document.
- Hire: asks clarifying questions about data sources and user personas before proposing tools.
- No Hire: immediately proposes model frameworks and vector databases; assumes the VP's prompt is a complete requirement.

### 2. "The customer wants zero hallucinations. What do you say?"

#### The signal

Tests probabilistic framing, customer expectation management, and refusal to make false promises under executive pressure.

#### Senior FDE response

"I address this directly in the room without defensive jargon. I tell them:

'Zero hallucinations does not exist in probabilistic language models, just as zero errors does not exist in human analytical teams. If a vendor promises you zero hallucinations, they are either misinformed or misleading you.

What we can guarantee, and what we build toward in production, is zero ungrounded claims and strict refusal behavior. We achieve this through four architectural controls:

First, strict citation grounding: the model is prohibited from generating a factual assertion unless it points to an exact document ID and quoted passage retrieved from your authorized knowledge base.

Second, deterministic quote verification: an automated post-generation guardrail verifies that every cited passage exists verbatim in the source text. If a quote is invented, the response is discarded.

Third, explicit refusal boundaries: when retrieved document similarity drops below our confidence threshold of 0.85, the model is instructed to output an honest 'I do not have sufficient information in the provided records to answer this question' rather than guessing.

Fourth, a human-in-the-loop exception queue: high-stakes claims or low-confidence tickets are routed to human operators with one-click review.

Our evaluation metric is not zero hallucination; our metric is a 100% citation grounding rate on our golden evaluation suite.'"

#### The red flag response

"I will set model temperature to 0.0 and tell the model in the system prompt 'Do not hallucinate under any circumstances'."

#### Scoring rubric

- Strong Hire: clearly reframes the problem from eliminating hallucinations to containing errors via deterministic citation checks, confidence thresholding, and refusal boundaries.
- Hire: explains that LLMs are probabilistic and discusses RAG and citation checks.
- No Hire: claims temperature 0.0 or prompt engineering prevents hallucinations; promises perfection to please the customer.

### 3. "Retrieval quality is poor on the customer's documents. Walk me through debugging it."

#### The signal

Tests disciplined hypothesis ranking and isolating retrieval from generation before editing prompts.

#### Senior FDE response

"I split the system into two isolated evaluation boundaries: retrieval quality versus generation quality. You cannot fix bad retrieval with prompt engineering.

Step one: evaluate retrieval independently. I take 50 representative customer queries from our golden evaluation set and measure Mean Reciprocal Rank (MRR) and Recall@K directly against ground-truth document chunks. If the correct chunk is not in the top 5 retrieved items, generation never had a chance.

Step two: inspect document chunking and ingestion. Most enterprise retrieval failures stem from dirty chunking: fixed 500-character slices that cut tables in half or sever headings from paragraph bodies. I verify whether semantic boundaries or layout-aware parsers preserve table rows and section headers.

Step three: analyze keyword versus semantic vocabulary mismatch. Enterprise documents are packed with internal acronyms, part numbers, and error codes that dense vector embeddings miss. If queries fail on exact terms, I introduce hybrid search: BM25 sparse lexical matching combined with dense vector cosine similarity via Reciprocal Rank Fusion (RRF).

Step four: examine metadata filtering and security boundaries. If retrieval returns irrelevant documents, we evaluate whether pre-retrieval filters (e.g. document type, department, date range) are properly applied.

Only after Recall@5 exceeds 90% do I evaluate generation prompts and synthesis."

#### The red flag response

"I would switch from text-embedding-ada-002 to a bigger embedding model, increase chunk size, and add few-shot examples to the generation prompt."

#### Scoring rubric

- Strong Hire: decouples retrieval evaluation from generation; measures MRR and Recall@K; identifies tabular and acronym chunking failures; implements hybrid BM25 and dense retrieval; validates pre-retrieval filters.
- Hire: looks at chunk size and embedding quality before touching generation.
- No Hire: tweaks generation prompts; changes models blindly without offline metrics.

### 4. "The model worked in the demo and fails in production. Why?"

#### The signal

Tests understanding of distribution shift, production data messiness, and the gap between curated staging data and live inputs.

#### Senior FDE response

"This is the classic prototype-to-production gap. In my experience, demo success followed by production degradation is caused by five structural differences:

First, distribution shift in inputs: demo data is usually clean, single-intent, grammatical text curated by an engineer. Live production inputs contain slang, OCR noise, truncated mobile speech-to-text, multiple conflicting questions in one message, and malformed encoding.

Second, document versioning and index staleness: the demo vector store was indexed once from a clean snapshot. In production, documents are amended, superseded, or deleted daily. If ingestion pipelines do not handle incremental updates, the model retrieves outdated policy manuals.

Third, context window pollution: production users paste multi-page email threads or log dumps that push relevant system instructions and citations out of attention focus.

Fourth, unhandled edge cases in schemas: production responses occasionally return unexpected JSON formatting, missing required keys, or invalid enum strings that crash downstream consumers.

To fix this, I do not tweak prompts blindly. I capture the 50 most recent failing production traces, label the failure mode into an error taxonomy (retrieval miss, schema violation, out-of-domain query), add them to our golden test suite, and add automated regression gates."

#### The red flag response

"The model provider probably updated their API model weights behind the scenes, or production users are prompting it incorrectly."

#### Scoring rubric

- Strong Hire: identifies distribution shift, dirty encodings, stale index updates, and context pollution; captures failing production traces into an error taxonomy; updates the golden evaluation suite.
- Hire: recognizes that live users submit messier inputs than engineers in demos.
- No Hire: blames the model provider or blames the customer's end users.

### 5. "A 429 hits mid-batch. What happens to the rest of the batch?"

#### The signal

Tests partial failure handling, idempotency, checkpointing, and backpressure in batch engineering.

#### Senior FDE response

"In enterprise batch ingestion, encountering an HTTP 429 Too Many Requests mid-batch must never result in either aborting the entire job or blindly retrying the whole batch from item one.

Here is the production architecture:

First, item-level state tracking: each record in the batch exists in an explicit state machine (PENDING, IN_FLIGHT, COMPLETED, FAILED_RETRYABLE, FAILED_TERMINAL). As items succeed, their outputs are committed idempotently to the database.

Second, adaptive backpressure: the moment a 429 is received on an item, the batch runner pauses all concurrent worker threads. It inspects the HTTP Retry-After header. If present, it sleeps for that duration; if absent, it applies exponential backoff with full jitter (e.g. random sleep between 0 and min(max_backoff, base * 2^attempt)).

Third, checkpointed resume: items that were already COMPLETED before the 429 are never re-sent, avoiding duplicate cost and downstream quota waste. The remaining PENDING and FAILED_RETRYABLE items resume in throttled chunks once the cooldown expires.

Fourth, dead letter queue (DLQ): if an individual item fails after maximum retries (e.g. 5 attempts), it is written to an exception ledger with line number and trace ID, allowing the remaining batch to complete."

#### The red flag response

"I wrap the batch loop in a try-catch block. If it catches a 429, I sleep for 5 seconds and rerun the loop."

#### Scoring rubric

- Strong Hire: designs item-level state machines, respects Retry-After with full jitter backoff, ensures completed items are not re-executed, and routes exhausted items to a dead letter queue.
- Hire: pauses execution and retries without re-running completed records.
- No Hire: aborts the whole batch or re-runs the entire batch from record zero.

### 6. "Two services disagree about the same record. Which is right, and how do you find out?"

#### The signal

Tests boundary contracts, authoritative systems of record, and reconciliation discipline.

#### Senior FDE response

"When two enterprise services disagree on a record state (e.g. CRM says an account is Active but the Billing ERP says Delinquent), you cannot write heuristic tie-breaking logic in code until you establish the authoritative system of record.

My procedure:

First, consult the data governance contract: every business object has an authoritative owner. Billing owns invoices, payment statuses, and balance ledgers. CRM owns contact details and pipeline stages. If they disagree on payment status, Billing is authoritative by default.

Second, check event timestamps and update lineage: examine the database audit timestamps and message queue event logs. Did the CRM receive a manual edit at 10:00 AM while the Billing webhook failed to deliver at 10:05 AM? Look for failed webhook deliveries or unhandled schema migrations.

Third, generate a reconciliation anomaly report: write a scheduled job that queries both systems, computes diffs, and flags discrepancies into an exceptions table rather than letting one service silently overwrite the other.

Fourth, document the tie-breaking rule in an Architecture Decision Record (ADR): have both department heads sign off on which system wins under conflict before automating the sync."

#### The red flag response

"I would write a script that takes the newest timestamp or takes whichever record has fewer null fields."

#### Scoring rubric

- Strong Hire: identifies authoritative systems of record by business domain, checks message delivery lineage, generates exception reconciliation reports, and formalizes resolution in an ADR.
- Hire: investigates timestamps and talks to stakeholders to find out which database is trusted.
- No Hire: writes code to pick the newest timestamp or averages the fields without consulting business owners.

### 7. "Who is on call when this breaks at 2 a.m.?"

#### The signal

Tests handover discipline, operational ownership, and refusing to build orphaned systems that rely on vendor engineers permanently.

#### Senior FDE response

"The answer to who is on call must be agreed upon in writing in the Statement of Work (SOW) before we deploy to production, not discovered during an outage at 2 a.m.

In a healthy FDE engagement, operational responsibility transitions across three phases:

During pilot and initial deployment (Weeks 1 to 4): the forward deployed engineering team is primary on-call during business hours, with a named internal customer lead shadowing every incident and alert.

During handover transition (Weeks 5 to 6): the customer's operations or platform team takes over primary on-call, with the FDE team acting as secondary escalation. Handover exit criteria require that the customer's on-call engineers successfully resolve two simulated drill incidents using our operations runbook without our intervention.

Post-handover: the customer's internal tier-1 and tier-2 operations teams own 24/7 on-call. If a defect in our platform code occurs, it is escalated via established enterprise support SLAs with clear ticket severity definitions (P0 response within 15 minutes, P1 within 1 hour).

An FDE system without a named customer operational owner is not a production deployment; it is a liability waiting to be shut down."

#### The red flag response

"I will put my phone number on the alert dashboard and answer it whenever it rings."

#### Scoring rubric

- Strong Hire: structures phased ownership transition, mandates shadowing and drill verification, establishes runbook requirements, and enforces SLA escalation contracts.
- Hire: emphasizes creating runbooks and training the customer's engineers before departure.
- No Hire: offers to be on call indefinitely; ignores operational handover.

### 8. "What data leaves the customer boundary in this design?"

#### The signal

Tests security perimeters, compliance boundaries, egress awareness, and unprompted data privacy discipline.

#### Senior FDE response

"In an enterprise deployment, my default assumption is that zero customer data leaves their network perimeter until explicit security authorization is granted.

I classify data into three egress tiers:

Tier 1: High-risk customer data (PII, PHI, financial records, authentication secrets). This data must never leave the customer's VPC or on-premise boundary. If cloud LLMs are used, we deploy private VPC endpoints (e.g. AWS PrivateLink or Azure Private Link) so traffic traverses private cloud backbones without crossing the public internet. If policy mandates zero third-party egress, we host open-weight models locally on customer-managed GPU instances.

Tier 2: Vector embeddings and indices. These reside in a self-hosted or dedicated single-tenant vector database inside the customer's VPC, encrypted at rest with customer-managed KMS keys.

Tier 3: Observability telemetry. Only sanitized error codes, trace latency percentiles, and token consumption counts egress to monitoring platforms. Customer prompt bodies and document contents are strictly redacted at the logging adapter layer.

I provide the customer's Chief Information Security Officer (CISO) with an egress architecture diagram detailing network ports, protocols, and data flows before commencing integration."

#### The red flag response

"Only the prompt text and document chunks leave the network to call the model API over HTTPS, which is encrypted in transit so it is safe."

#### Scoring rubric

- Strong Hire: details private VPC endpoints, PII redaction at logging adapters, local inference alternatives, customer-managed KMS encryption, and proactive CISO architecture delivery.
- Hire: explains encryption in transit and rest, and asks what compliance rules apply.
- No Hire: assumes HTTPS over public internet is sufficient for enterprise compliance.

### 9. "Answers are wrong every Monday. Hypotheses?"

#### The signal

Tests time-patterned debugging, scheduled job failure awareness, and systematic hypothesis generation over guessing.

#### Senior FDE response

"Recurring Monday failures indicate a time-dependent batch or synchronization failure over the weekend rather than an inherent model defect.

My hypothesis tree, ranked by likelihood:

Hypothesis 1: Weekend batch synchronization failure. A scheduled ETL job or vector re-indexing pipeline runs on Sunday night at midnight. If upstream databases perform maintenance or network reboots, the ingestion job fails silently, leaving the vector index out of sync with Monday's operational state.

Hypothesis 2: Time-window and timezone edge cases. Date parsing logic in queries (e.g. 'show me issues from this week') resets on Sunday/Monday midnight boundaries. If the parser mishandles UTC versus local office timezones, Monday queries search an empty weekly bucket.

Hypothesis 3: Weekend document backlog overload. Customer ticketing queues accumulate unread backlogs over Saturday and Sunday. When the Monday morning spike hits, the system encounters rate limits or worker queue starvation, triggering fallback paths that generate lower-quality answers.

To verify, I inspect Sunday night ETL scheduler logs and compare Monday query latency and rate limit metrics against mid-week averages."

#### The red flag response

"Maybe Monday questions are just harder, or users are grumpy on Mondays."

#### Scoring rubric

- Strong Hire: identifies Sunday ETL batch failures, timezone and weekly window boundary logic, and weekend queue volume spikes; tests scheduler logs first.
- Hire: looks at weekend automated jobs and cache expiration.
- No Hire: makes jokes or guesses that the model is tired.

### 10. "Your system gave a wrong answer to a customer today."

#### The signal

Tests composure under pressure, incident triage discipline, accountability, and preventing regression.

#### Senior FDE response

"When an executive or customer escalates a production hallucination or wrong answer, my response follows four strict phases:

Phase 1: Immediate acknowledgement and fact collection (within 15 minutes). I acknowledge the issue without defensiveness: 'Thank you for flagging this. We are treating this with high urgency.' I request the exact ticket ID, user input, output timestamp, and what the correct answer should have been.

Phase 2: Trace inspection and blast radius containment (within 1 hour). I pull the distributed trace using the request correlation ID. I examine the retrieved chunks: did retrieval fail to return the correct policy document, or did the model misinterpret the retrieved text? If a critical compliance or safety violation occurred, I immediately activate the policy kill-switch to route that specific intent category to human operators.

Phase 3: Root cause analysis and remediation (within 24 hours). I determine the technical fix: updating chunking metadata, adding an explicit negative example to our golden test suite, or tightening the citation verification threshold.

Phase 4: Postmortem and regression test closure (within 48 hours). I publish a blameless postmortem to the customer stakeholders detailing what happened, why our existing evaluation missed it, and the automated regression test added to our golden suite to ensure this failure mode can never deploy again."

#### The red flag response

"I apologize profusely, tell them AI is not 100% accurate, and tell them to add more detail to their prompt next time."

#### Scoring rubric

- Strong Hire: follows disciplined four-phase incident response, pulls correlation ID traces, isolates retrieval vs generation, activates blast radius containment, and commits regression test to golden suite.
- Hire: investigates the logs and explains the cause to the customer calmly.
- No Hire: gets defensive; blames the model or user; promises it will never happen again without changing any code or tests.



## How to use this bank

We recommend four practices:

- Practice out loud - answers that live in your head have never survived a room; say them to a person or a recorder
- Time-box answers - two minutes for most questions, five for scenarios; the discipline of stopping is part of the signal
- Alternate asking and answering with a peer - playing the interviewer teaches the signals faster than answering does
- Track your dodges - the questions you route away from are your preparation list; live loops find them anyway

## Related documents

- [Customer scenario rounds](04-customer-scenarios.md) - the full scenarios behind the role-play openers
- [Behavioral rounds](05-behavioral.md) - the story inventory behind the trait questions
- [Coding and technical rounds](02-coding-and-technical.md) - practice problems for the technical patterns
- [System design rounds](03-system-design.md) - the framework behind the design prompts
- [Discovery and requirements](../skills/02-discovery-and-requirements.md) - the full discovery question bank
- [The interview process](01-interview-process.md) - how the rounds fit together

## Further reading

- [fde.academy](https://fde.academy) - practitioner guides on what FDE interviews test
- [Exponent](https://tryexponent.com) - documented FDE loops and community question patterns
