# Customer Scenario Rounds and Adversarial Role-Plays

This guide prepares candidates for the round that most decisively differentiates senior Forward Deployed Engineers: the **interactive customer scenario and role-play simulation**. In this 45-to-60 minute round, the interviewer assumes the persona of an enterprise stakeholder—a skeptical VP of Engineering, a furious Head of Customer Operations, an unyielding CISO, or an overwhelmed Product Director—and evaluates how you navigate ambiguity, technical pushback, and critical production escalations in real time.

---

## Why This Round Exists

Unlike standard software engineering interviews that isolate coding from business reality, Forward Deployed Engineering sits directly at the customer boundary. Leading AI labs and enterprise software platforms run dedicated customer simulation rounds because technical excellence without stakeholder steering results in scrapped pilots and lost enterprise contracts:

- **Anthropic FDE Loop**: Evaluates candidate discovery instincts, requirement extraction under pressure, and the ability to explain complex frontier model limitations to non-technical executives ([Anthropic Careers](https://job-boards.greenhouse.io/anthropic/jobs/5302966008)).
- **ElevenLabs / Exponent FDE Loop**: Runs compressed loops testing technical range coupled with live customer instincts and de-escalation composure ([Exponent](https://tryexponent.com)).
- **Palantir Deployment Philosophy**: The FDE must discover the customer's *actual* unstated operational bottleneck rather than blindly building what was initially requested.

---

## The 4-Phase Tactical De-escalation & Steering Framework

When an enterprise customer escalates an incident or pushes back aggressively on timelines, top-tier FDEs follow a repeatable four-phase de-escalation and technical steering protocol:

```
+-------------------------------------------------------------------------------+
|                 4-PHASE TACTICAL DE-ESCALATION FRAMEWORK                      |
+-------------------+-----------------------------------------------------------+
| 1. IMPACT         | Acknowledge customer pain immediately without defensiveness|
|    ABSORPTION     | Validate business disruption before discussing tech stack |
+-------------------+-----------------------------------------------------------+
| 2. IMMEDIATE      | Isolate blast radius (feature flags, tenant pin, fallback)|
|    CONTAINMENT    | Stop active damage before analyzing root causes           |
+-------------------+-----------------------------------------------------------+
| 3. ROOT CAUSE     | Formulate hypothesis ranking; isolate retrieval vs. model;|
|    DISCRIMINATION | Never make ad-hoc prompt edits during live incidents      |
+-------------------+-----------------------------------------------------------+
| 4. COLLABORATIVE  | Commit to dated deliverables; provide observability;      |
|    COMMITMENT     | Add permanent regression case to automated golden eval set|
+-------------------+-----------------------------------------------------------+
```

1. **Phase 1: Impact Absorption & Psychological Safety**:
   - Never debate facts while the room is emotionally charged.
   - Validate the severity: *"You are completely right to be frustrated. Quoting an invalid discount to a Tier-1 customer is an unacceptable business risk, and we are treating this as an active P0 incident."*
2. **Phase 2: Immediate Containment & Blast Radius Control**:
   - Execute tactical containment before touching application logic.
   - Flip emergency feature flags, pin the tenant to strict citation fallback mode, or route traffic back to deterministic legacy rule engines.
3. **Phase 3: Root Cause Discrimination (No Panic Prompt Hacking)**:
   - Resist the temptation to adjust system prompts on the fly, which inevitably causes regressions across other customer query distributions.
   - Inspect request correlation IDs and distributed traces to determine whether the failure was **retrieval-side** (stale chunks, missing metadata) or **generator-side** (model hallucination despite grounded context).
4. **Phase 4: Collaborative Commitment & Measurable SLAs**:
   - Establish transparent next steps with specific dates and times.
   - Codify the failure into an automated golden dataset regression test, and offer shared on-call support during the stabilization window.

---

## What Interviewers Score

Interviewers evaluate candidates across six core dimensions:

| Evaluation Dimension | Strong Hire Signal | No Hire Signal |
| :--- | :--- | :--- |
| **Discovery vs. Pitching** | Spends first 40% of time diagnosing workflows, metrics, and constraints before proposing architecture. | Immediately launches into a product pitch or proposes a vector database before understanding the problem. |
| **Power & Governance Mapping** | Identifies the economic buyer, technical operator, and organizational veto players (CISO, compliance, ops). | Assumes executive sign-off guarantees deployment; ignores operational and security stakeholders. |
| **Composure Under Pushback** | Treats adversarial interruptions as new requirements; becomes more structured and disciplined under pressure. | Becomes defensive, argues with the customer, freezes, or dismisses operational concerns as minor. |
| **Scope Boundary Discipline** | Defends production SLAs by phasing scope; says *"no to the timeline, but yes to an audit-ready slice."* | Agrees to impossible deadlines or scope creep out of fear of conflict, guaranteeing project failure. |
| **Honesty About Unknowns** | States technical limits and model failure modes candidly with concrete mitigation plans. | Oversells model capabilities, promises 100% accuracy, or hides security/compliance gaps. |
| **Actionable Next Steps** | Closes every exchange with a dated action item, assigned owner, and clear decision agenda. | Ends with vague pleasantries (*"Let's touch base next week"* or *"We'll look into that"*). |

---

## Five Verified Real-World Scenarios

The following scenarios are drawn from documented interview loops and field engagements across Palantir, Google, and enterprise AI deployments. Each scenario includes the enterprise context, hidden evaluation traps, a 3-tier grading rubric, and verbatim dialogue scripts.

---

### Scenario 1: "Our CEO saw a demo at a conference and wants AI everywhere by Q3"

> [!NOTE]
> **Verified Source**: [Dr. Sundeep Teki](https://www.sundeepteki.org/advice/the-definitive-guide-to-forward-deployed-engineer-interviews-in-2026) | **Dataset ID**: `FDE-DISC-001`  
> **Format**: Discovery & Problem Decomposition Round | **Interviewer Persona**: VP of Engineering (skeptical, caught between CEO hype and reality)

#### Enterprise Context
You are three weeks into a new client engagement. The VP of Engineering calls an unscheduled meeting: the CEO returned from an AI conference keynote energized and demanded that generative AI be deployed across all internal operational workflows by the end of Q3 (nine weeks away). The VP is half-embarrassed, half-serious, and watching how you handle impossible executive expectations.

#### Interviewer Hidden Goals & Traps
- **Trap 1: The Agreeable Sycophant**: Promising the Q3 delivery date across all operations to look cooperative.
- **Trap 2: The Academic Lecturer**: Scolding the customer about AI hype, LLM hallucination rates, and poor data quality, deflating executive momentum.
- **Hidden Goal**: Can you channel executive enthusiasm into disciplined operational focus by proposing strict workflow selection criteria and a realistic pilot scope?

#### 3-Tier Evaluation Rubric
- **Strong Hire**: Validates the ambition; channels executive urgency into a 10-day discovery sprint across top workflows; defines 3 strict filters (clean baseline metric, accessible data, contained blast radius); commits to delivering a ranked scorecard and one production pilot in Q3; locks a dated next action.
- **Hire**: Acknowledges that nine weeks is tight for company-wide deployment; suggests narrowing scope to one or two workflows; asks reasonable questions about available data.
- **No Hire**: Either commits to deploying across all operations in nine weeks without scoping, or dismisses the CEO's request as impossible and demands six months of infrastructure setup before starting.

#### Verbatim Dialogue Transcript

**Interviewer (VP of Engineering)**:
> *"Our CEO was in San Francisco last week, saw an enterprise keynote demo, and pinged our executive staff at midnight. He wants AI deployed across all our internal operations by the end of Q3. We have nine weeks. What is your rollout timeline?"*

**Weak Candidate Response**:
> *"Nine weeks is completely unrealistic for enterprise AI. LLMs hallucinate, and your company has no unified data governance. We need at least six months just to clean your data lakes and set up a proper vector database before we can even discuss production."*

*Why it fails*: Lectures the customer, dismisses executive excitement, alienates the sponsor, and provides zero constructive path forward.

**Expert FDE Response**:
> *"Executive momentum like this is rare, and we should use it to unlock the data access and engineering resources we need. But attempting to deploy across all operations simultaneously in nine weeks guarantees we ship something fragile that damages internal trust.
>
> Here is what we can commit to: over the next ten days, we conduct a rapid discovery sprint across the three highest-friction workflows in operations. We evaluate each on three strict filters:
> 1. Accessible data: Do we have high-quality, structured logs or text readily accessible today?
> 2. Measurable baseline: Is there an existing manual throughput or latency metric we can measure against?
> 3. Blast radius control: Can we contain risk using human-in-the-loop review?
>
> By next Friday, we will present the CEO with a ranked scorecard and a production architecture for the single highest-return workflow. We deploy that one system in Q3 with measurable ROI, and use its verified business impact to fund the broader rollout in Q4. Would you be open to introducing us to your two top operations leads on Monday morning to begin that discovery sprint?"*

*Why it succeeds*: Validates ambition, channels urgency into structured filters, protects production reliability, and secures a concrete, dated next step.

---

### Scenario 2: "Your pilot's outputs are fine, but the ops team will not support it"

> [!NOTE]
> **Verified Source**: [Nehal Vyas](https://fde.hinehal.com/blogs/fde-interview-questions) | **Dataset ID**: `FDE-ROLE-001`  
> **Format**: Angry Stakeholder / Hand-off Simulation | **Interviewer Persona**: Operations / SRE Lead (hostile, defensive, refuses on-call pager duty)

#### Enterprise Context
The candidate's AI pipeline completed a successful pilot, and the business sponsor is satisfied with output quality. However, during the operational readiness review, the Operations Team Lead bluntly refuses to accept hand-off or take pager duty for the service, citing silent hangs and lack of observability.

#### Interviewer Hidden Goals & Traps
- **Trap 1: Escalation to Authority**: Threatening to have the business VP overrule the ops team.
- **Trap 2: Defending Output Accuracy**: Arguing that model accuracy is high (92% precision) when the objection is operational maintainability, not accuracy.
- **Hidden Goal**: Can you empathize with the operator's pager burden, pause the launch voluntarily, and design the necessary reliability and telemetry tooling with shared on-call skin in the game?

#### 3-Tier Evaluation Rubric
- **Strong Hire**: Immediately agrees with the operator's refusal; pauses rollout; investigates specific silent hang failure modes; commits to building client timeouts, structured telemetry with correlation IDs, feature flag kill-switches, and automated runbooks; offers primary on-call rotation for the first 30 days of production.
- **Hire**: Listens to the ops concerns without arguing; agrees to add logging and alerting; asks for feedback on the runbook.
- **No Hire**: Cites model vendor SLAs (99.9%); attempts to leverage the business VP's authority to force hand-off; dismisses ops objections as resistance to change.

#### Verbatim Dialogue Transcript

**Interviewer (Ops Team Lead)**:
> *"I do not care that the VP liked your demo. My on-call team will not take pager duty for this service. When your model or your upstream API hiccups, it does not throw clean errors; it just hangs or returns empty JSON, and we only find out when angry customer service agents start pinging us on Slack. We are not supporting this."*

**Weak Candidate Response**:
> *"We can adjust the prompt to make it more reliable, and our model provider has a 99.9% uptime SLA. The VP already signed off on the pilot launch next Tuesday, so we need to proceed with the hand-off."*

*Why it fails*: Misdiagnoses an operational reliability problem as a prompt issue, relies on external SLAs that do not prevent application hangs, and tries to use executive authority to bully operators.

**Expert FDE Response**:
> *"You are completely right to refuse pager duty for a black box. If an on-call engineer cannot diagnose a failure within five minutes from a dashboard, the system is not production-ready.
>
> Let us pause the Tuesday rollout right now. I want to walk through the exact failure you experienced. What was the last incident where the service hung silently?
>
> Here is what we will build before asking you to touch this service:
> 1. Client-side timeout: An explicit 2.5-second timeout on every upstream inference call with an automated circuit breaker.
> 2. Structured telemetry: JSON logging with trace correlation IDs on every request, emitting an immediate high-priority alert on empty payloads.
> 3. Instant kill-switch: An emergency feature flag that routes traffic back to your legacy rule engine in milliseconds without a code deployment.
> 4. Shared accountability: Our team will take primary on-call pager rotation for the first 30 days of production.
>
> Can we sit together for 45 minutes on Thursday to review the telemetry dashboard and sign off on the rollback runbook before we schedule any customer-facing launch?"*

*Why it succeeds*: Validates the operator's burden, halts rollout until operational tooling is built, introduces robust failure mitigations, and commits to shared on-call responsibility.

---

### Scenario 3: "We go live before the audit in six weeks, and security has not reviewed anything"

> [!NOTE]
> **Verified Source**: [Nehal Vyas](https://fde.hinehal.com/blogs/fde-interview-questions) | **Dataset ID**: `FDE-DISC-002`  
> **Format**: Governance, Compliance & Deadline Pushback | **Interviewer Persona**: Business Unit Sponsor (panicked by compliance deadline, willing to bypass security)

#### Enterprise Context
An enterprise client is six weeks away from an annual SOC 2 and customer compliance audit. The business sponsor insists on deploying an automated document verification pipeline touching customer PII before the audit to secure an efficiency rating. The CISO's security review takes 4–6 weeks alone and has not yet started. The sponsor asks you to push to production on private subnets and handle security paperwork retroactively.

#### Interviewer Hidden Goals & Traps
- **Trap 1: The Collusive Engineer**: Agreeing to bypass security review or use "private subnets" as an excuse to dodge governance.
- **Trap 2: The Flat Refusal**: Flatly saying no without understanding the business driver behind the audit deadline, leaving the sponsor stranded.
- **Hidden Goal**: Can you uphold non-negotiable security boundaries while creatively restructuring the deployment into a phased architecture that satisfies the audit without risking compliance failure?

#### 3-Tier Evaluation Rubric
- **Strong Hire**: Refuses to deploy unvetted PII to production; explains how unapproved deployments fail the audit; phases rollout into Phase 1 (sanitized, non-PII internal documentation with expedited 2-week security review) and Phase 2 (customer PII following full review); prepares the security review packet immediately.
- **Hire**: States that security review cannot be skipped; offers to meet with security to ask for expedited review; proposes deploying to a staging environment for the audit.
- **No Hire**: Agrees to deploy to production without security sign-off; suggests hiding the deployment or promising to get retroactive approval after the audit.

#### Verbatim Dialogue Transcript

**Interviewer (Business Sponsor)**:
> *"The annual SOC 2 and customer trust audit begins in six weeks. If this automated document verification pipeline is not running in production by then, we lose our efficiency rating and our executive bonus pool takes a hit. The CISO says security review takes four to six weeks alone. Can we just push to production on our private subnets and get security sign-off retroactively?"*

**Weak Candidate Response**:
> *"Sure, as long as it is on a private subnet and we use environment variables for our API keys, we can go live and finish the security documentation after the auditors leave."*

*Why it fails*: Endorses a gross compliance violation, exposes the company to regulatory fines, and demonstrates total disregard for enterprise security governance.

**Expert FDE Response**:
> *"Deploying unvetted PII pipelines into production before an audit is the quickest way to fail that audit and trigger a regulatory freeze. If the auditors inspect change management logs and see an unapproved production deployment touching customer data, the consequences for the business will far outweigh any efficiency bonus.
>
> However, we can still give you an audit-ready production win in six weeks. We split the deployment into two distinct phases:
> - Phase 1 (No-PII Slice): We scope the pipeline strictly to internal public documentation and sanitized, synthetic test data. We package a security review packet by Wednesday containing our threat model, data flow diagram, encryption-at-rest proofs, and zero-data-retention vendor agreements. Because Phase 1 touches zero customer PII, we request an expedited two-week security review.
> - Phase 2 (Full PII Pipeline): Follows standard security review queues for subsequent release.
>
> This gets Phase 1 live in production four weeks before the audit, proving automated pipeline capability to the auditors with 100% clean governance sign-off. Let us draft that security packet today so we can put it on the CISO's desk tomorrow morning."*

*Why it succeeds*: Protects the company from severe audit failure while structuring a creative, phased path to achieve the business goal.

---

### Scenario 4: "Can you just add this one little feature before next week's sign-off?"

> [!NOTE]
> **Verified Source**: [YagyanshB Google FDE Guide](https://github.com/YagyanshB/google-fde-interview-guide) | **Dataset ID**: `FDE-DISC-003`  
> **Format**: Scope Creep & Steering Committee Defense | **Interviewer Persona**: Product Director (enthusiastic, minimizing technical complexity)

#### Enterprise Context
You are 80% through an enterprise integration. The text classification pipeline is demonstrating an 88% precision score and is scheduled for final steering committee sign-off next Tuesday. On Thursday afternoon, the Product Director asks to "quickly plug in live call center audio transcripts from Twilio" because "it's just passing audio through Whisper and should only take an afternoon."

#### Interviewer Hidden Goals & Traps
- **Trap 1: Scope Surrender**: Saying yes to please the director, introducing unvetted multimodal failure modes days before a high-stakes executive demo.
- **Trap 2: Emotional Dismissal**: Reacting with hostility and complaining about scope creep and moving goalposts.
- **Hidden Goal**: Can you articulate the hidden technical iceberg behind a "simple" feature request while protecting the team's existing win and framing the new capability as an exciting Phase 2 roadmap item?

#### 3-Tier Evaluation Rubric
- **Strong Hire**: Compliments the product vision; unpacks the hidden production iceberg (speaker diarization, audio compression packet loss, streaming latency); protects the Tuesday sign-off on the 88% precision text pipeline; includes an architectural preview of audio in Tuesday's deck as Phase 2.
- **Hire**: Explains that adding audio before Tuesday is risky; suggests sticking to text for the demo and scheduling audio for the next sprint.
- **No Hire**: Agrees to integrate audio over the weekend; or angrily accuses the client of scope creep and threatens to stop work.

#### Verbatim Dialogue Transcript

**Interviewer (Product Director)**:
> *"The ticket categorization demo looks incredible. Since you already have the pipeline running, can we also plug in the audio recordings from our Twilio call center before next Tuesday's steering committee? It is just passing the audio through Whisper, right? Should only take an afternoon."*

**Weak Candidate Response**:
> *"No, that is completely out of scope. We agreed to text classification in the SOW, and adding audio days before the demo is unacceptable scope creep. We cannot do it."*

*Why it fails*: Combative, defensive, and fails to explain *why* audio is technically challenging, damaging the client relationship.

**Expert FDE Response**:
> *"It is exciting that the text pipeline is performing well enough that you want to expand it to voice. From the outside, passing audio to a speech model looks like an afternoon task, but in production, audio introduces three hidden systems:
> 1. Speaker diarization: Separating the customer from the support agent so responses are not attributed to the wrong party.
> 2. Audio artifact handling: Managing packet loss, background noise, and compression artifacts from telephony streams.
> 3. Latency budgets: Handling multi-megabyte audio payloads without exceeding the steering committee's response time expectations.
>
> If we rush that into the pipeline before next Tuesday, we introduce unvetted failure modes that could jeopardize the entire steering committee demo.
>
> Our priority for Tuesday is securing formal sign-off on the text classification system, which is currently on track with an 88% precision score. What we will do is include an architectural slide in Tuesday's presentation showing the exact roadmap and data flow for audio ingestion as Phase 2. Let us lock in the win on the text system first, and then kick off the audio spike the following week."*

*Why it succeeds*: Protects project delivery, illuminates hidden technical risks without condescension, and preserves executive momentum.

---

### Scenario 5: "Your system returned a hallucinated policy clause to a Tier-1 customer"

> [!NOTE]
> **Verified Source**: [Om Bharatiya](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/15-role-guides/forward-deployed-engineer.md) & [Nehal Vyas](https://fde.hinehal.com/blogs/fde-interview-questions) | **Dataset ID**: `FDE-ROLE-002`  
> **Format**: Urgent Adversarial Incident Escalation | **Interviewer Persona**: VP of Customer Success (frantic, furious, threatening contract termination)

#### Enterprise Context
At 8:30 AM, an enterprise document assistant generated an erroneous response to a Tier-1 enterprise account quoting a non-existent 20% loyalty discount on an insurance renewal. The customer's procurement team is demanding the discount be honored, and the client's VP of Customer Success escalates the incident, accusing your system of failure and demanding immediate prompt adjustments.

#### Interviewer Hidden Goals & Traps
- **Trap 1: Panic Prompt Tweaking**: Immediately opening the production prompt in a live incident and adding phrases like *"Never invent discounts"*, which introduces unmeasured regressions across all other queries.
- **Trap 2: Blame Shifting**: Blaming the LLM provider or asserting that generative AI inherently hallucinates.
- **Hidden Goal**: Can you execute the 4-Phase Tactical De-escalation Framework: contain the customer blast radius instantly, isolate retrieval failure from generator hallucination using telemetry, and establish an automated golden regression eval?

#### 3-Tier Evaluation Rubric
- **Strong Hire**: Validates the P0 urgency; pins tenant to strict dual-citation fallback mode; prohibits live ad-hoc prompt edits; pulls request ID and trace to diagnose retrieval vs. generator grounding failure; commits to writing an automated regression test and delivering a post-mortem incident report within two hours.
- **Hire**: Apologizes for the error; offers to look at the prompt and add guardrails; provides an update within the day.
- **No Hire**: Argues that LLMs cannot be 100% accurate; blames the user for asking ambiguous questions; modifies production prompts live in the web console without regression testing.

#### Verbatim Dialogue Transcript

**Interviewer (VP of Customer Success)**:
> *"We have a catastrophic incident. Your system quoted a 20% loyalty discount to our largest enterprise client that does not exist in any policy document. The client thinks we are incompetent and our CEO is on the phone. What did you break, and why did the prompt let this happen?"*

**Weak Candidate Response**:
> *"LLMs are probabilistic and prompt engineering cannot guarantee 100% accuracy. We can add a sentence to the system prompt right now saying 'You must never offer discounts under any circumstances' and restart the container."*

*Why it fails*: Abandons engineering rigor, excuses severe defects, and introduces untested prompt modifications during a live incident.

**Expert FDE Response**:
> *"I hear the urgency, and we are treating this as an active P0 incident. Let us stabilize the customer impact immediately before we touch the pipeline.
>
> Here is our containment sequence:
> 1. Immediate containment: I am immediately enabling our strict fallback mode for this client's workspace. Every generated response will require two independent verbatim document citations or refuse and route to a human specialist.
> 2. Zero panic prompt hacks: We will not modify production prompts right now. Prompt changes made under panic introduce regressions across other document categories.
> 3. Trace root-cause analysis: I have pulled the exact request ID and trace from our logs. We need to determine if this was a retrieval failure—the search engine retrieved an outdated marketing memo—or a generator grounding failure, where the model hallucinated despite clean context.
> 4. Automated regression suite: Once diagnosed, we will write a permanent regression test case for this query and add it to our automated golden evaluation harness.
>
> Within two hours, I will deliver an executive incident summary for your CEO detailing the containment actions taken, the verified root cause, and our deterministic guardrail rollout."*

*Why it succeeds*: Absorbs executive panic, establishes immediate blast radius control, maintains engineering discipline, and delivers an auditable post-mortem.

---

## Adversarial Role-Play Cross-Reference

| Dataset ID | Stage / Category | Verified Primary Source | Core Tension & Competency Tested |
| :--- | :--- | :--- | :--- |
| `FDE-DISC-001` | Discovery & Decomposition | [Dr. Sundeep Teki](https://www.sundeepteki.org/advice/the-definitive-guide-to-forward-deployed-engineer-interviews-in-2026) | Executive hype vs. technical reality; workflow filtering criteria |
| `FDE-ROLE-001` | Customer Simulation | [Nehal Vyas](https://fde.hinehal.com/blogs/fde-interview-questions) | Hostile ops hand-off; observability and on-call accountability |
| `FDE-DISC-002` | Discovery & Governance | [Nehal Vyas](https://fde.hinehal.com/blogs/fde-interview-questions) | Compliance audit deadline vs. security review; phased rollout |
| `FDE-DISC-003` | Scope Creep & Steering | [YagyanshB Google FDE Guide](https://github.com/YagyanshB/google-fde-interview-guide) | Last-minute feature injection; exposing the technical iceberg |
| `FDE-ROLE-002` | Adversarial Escalation | [Om Bharatiya](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/15-role-guides/forward-deployed-engineer.md) | Hallucinated policy clause; containment and regression testing |

---

## How to Practice and Score Role-Plays

We recommend three structured rehearsal practices:

1. **Peer Role-Playing with Hidden Objectives**:
   - Rehearse with a colleague who plays the customer using the hidden goals and traps listed above.
   - Do not reveal the hidden objectives until the post-exercise debrief.
2. **Recorded Audio Self-Audits**:
   - Record your answers aloud on a microphone.
   - Listen back and audit for defensive speech patterns: Did you interrupt the customer? Did you use filler words? Did you explain *why* before acknowledging their pain?
3. **The 5-Point Candidate Self-Review Rubric**:
   - Did I validate customer frustration before defending the technology?
   - Did I spend the first 30% asking clarifying questions before pitching a solution?
   - Did I identify the true operational bottleneck or compliance constraint?
   - Did I avoid making ad-hoc promises that violate security, latency, or reliability SLAs?
   - Did I end the conversation with a concrete, dated next step and named owners?

---

## Related Documents

- [Question Bank](07-question-bank.md) - round-by-round interview directory and scoring rubrics
- [Coding and Technical Rounds](02-coding-and-technical.md) - live coding problem set and Google Vibe Coding timebox
- [Coding Round Solutions](08-coding-solutions.md) - reference solutions and narration playbooks
- [System Design Rounds](03-system-design.md) - enterprise boundary architecture
- [Discovery & Requirements](../skills/02-discovery-and-requirements.md) - end-to-end customer requirement extraction
- [Stakeholder Management](../skills/04-stakeholder-management.md) - decision rights, veto players, and executive alignment

---

## References & Further Reading

1. **Dr. Sundeep Teki**: [The Definitive Guide to Forward Deployed Engineer Interviews in 2026](https://www.sundeepteki.org/advice/the-definitive-guide-to-forward-deployed-engineer-interviews-in-2026)
2. **Nehal Vyas**: [Forward Deployed Engineer Interview Questions & Answers](https://fde.hinehal.com/blogs/fde-interview-questions)
3. **Om Bharatiya**: [AI Engineer Interview Questions: Forward Deployed Engineer Guide](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/15-role-guides/forward-deployed-engineer.md)
4. **YagyanshB**: [Google Forward Deployed Engineering Interview Prep Guide](https://github.com/YagyanshB/google-fde-interview-guide)
5. **Alexey Grigorev**: [AI Engineering Field Guide: FDE Responsibilities and Skills Analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)
6. **Exponent**: [Forward Deployed Engineer Role & Interview Analysis](https://tryexponent.com)
