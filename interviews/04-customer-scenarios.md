# Customer Scenario Rounds

This file is for candidates preparing the round that most distinguishes FDE loops: a role-play where the interviewer plays the customer and you run the engagement conversation. You get the round's formats, the signals interviewers score, a discovery playbook, three fully worked practice scenarios with hidden goals and failure responses, and a practice method.

## Why this round exists

FDE loops test the conversation, not just the code. Two published anchors:

- Exponent's interview guides describe the ElevenLabs FDE loop as "a compressed loop that runs from coding to conversation, testing technical range and customer instinct" ([tryexponent.com](https://tryexponent.com), July 2026, observed evidence) - the conversation half is this round
- Anthropic's FDE posting lists strong communication for discovery among its fit criteria ([greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/5302966008), 2026, observed evidence) - this round tests it under pressure

This suggests the round exists because the job does: the FDE loop opens with problem and discovery stages ([the FDE loop](../role/05-the-fde-loop.md)), so the interview opens there too.

## The five formats

Practitioner reports converge on five role-play shapes (pattern):

- Discovery role-play - the interviewer is a vague sponsor ("we want AI in our reporting") and expects you to find the real problem
- Angry-stakeholder role-play - something broke or disappointed, the room starts upset, and you stabilize it
- Demo-and-pushback - you present a design or demo, then defend cost, accuracy, and risk against challenge
- Prioritization trap - everything is urgent, resources are fixed, and the test is what you cut and how you say it
- Scope-creep probe - mid-engagement requests keep arriving, and the test is whether you absorb, deflect, or renegotiate

Most loops run one of these for 45-60 minutes; the discovery role-play is the most common opener (pattern).

## What interviewers score

This rubric is our interpretation, consistent across practitioner accounts:

- Questions before answers - did the first third of the conversation contain questions rather than a pitch
- Who-owns-what probing - did you find who decides, who operates, and who can veto
- Expectation setting - did you leave promises the customer could hold you to, and avoid ones they could not
- Composure under pushback - did the challenge make you sharper or defensive
- Concrete next steps - did the conversation end with a dated action rather than a vibe
- Honesty about unknowns - did you say what you do not know yet and how you will find out
- Protecting the customer's time - did you drive to decisions, or fill air

Expect the interviewer to interrupt, redirect, and occasionally disagree badly on purpose. The interruptions are the test: each one checks whether you absorb new information without losing the thread of the conversation. We recommend treating every interruption as data about the customer rather than as an obstacle to your plan.

## The discovery role-play playbook

We recommend this arc inside any discovery scenario. It is the compressed version of the full framework in [discovery and requirements](../skills/02-discovery-and-requirements.md).

1. Open with context, not a pitch - "before I propose anything, I want to understand how this works today"
2. Run the funnel - situation (walk me through the last time this happened), pain (what does it cost you), success metric (what number tells you this worked), constraints (systems, compliance, deadline), decision process (who decides and who can veto)
3. Capture and replay - read back what you heard in two sentences and ask what you got wrong; the correction is where the truth lives
4. Close with a summary and a next step - a one-line problem statement, a proposed next meeting with an agenda, and a date

Practice the funnel until it survives interruption, because in the round it will be interrupted.

## Practice scenarios

All three are fictional. Each lists the setup, the interviewer's hidden goals, a strong response outline, and the common failure responses. Practice aloud with a peer playing the interviewer; keep the hidden goals hidden from the candidate.

### Scenario 1: "Our CEO saw a demo at a conference and wants AI everywhere by Q3"

- Setup - you are three weeks into a new engagement. The VP of engineering relays that the CEO returned from a conference demo and wants AI "everywhere" by end of Q3. The VP is half-embarrassed, half-serious, and watching how you handle it.
- Hidden goals - can you find a real use case under the hype without deflating the sponsor; will you commit to a delivery date before discovery; do you push back while preserving the CEO's momentum
- A strong response outline - treat the enthusiasm as fuel and convert it to structure. Congratulate the ambition, then propose a two-week discovery sprint across the three noisiest workflows, with explicit selection criteria: a measurable baseline, reachable data, and contained blast radius. Offer one candidate workflow to make it concrete. Set the expectation that Q3 delivers a ranked shortlist and one pilot, not "everywhere". End with a dated next step: the discovery schedule.
- Common failure responses - pitching before asking anything; promising the Q3 timeline to be agreeable; lecturing the room about AI hype and killing the sponsor's energy; accepting "everywhere" as a requirement and designing for it

#### Verbatim dialogue transcript

Interviewer (VP of Engineering): "Our CEO was in San Francisco last week, saw a keynote demo, and pinged our executive staff at midnight. He wants AI deployed across all our internal operations by the end of Q3. We have nine weeks. What is your rollout timeline?"

Weak candidate response: "Nine weeks is completely unrealistic for enterprise AI. LLMs hallucinate, and you have no data governance. We need at least six months to set up a vector database and clean your data lakes."

Why it fails: Lectures the customer, dismisses executive excitement, and stalls without offering a constructive path forward.

Expert FDE response: "Executive momentum like this is rare, and we should use it to unlock the data access and engineering resources we need. But attempting to deploy across all operations simultaneously in nine weeks guarantees we ship something fragile that damages internal trust. 

Here is what we can commit to: over the next ten days, we conduct a rapid discovery sprint across the three highest-friction workflows in operations. We evaluate each on three filters: first, do we have accessible, high-quality data today; second, is there an existing manual baseline metric we can measure against; and third, can we contain the blast radius with human review? 

By next Friday, we will present the CEO with a ranked scorecard and a production architecture for the single highest-return workflow. We deploy that one system in Q3 with measurable ROI, and use its success to fund the broader rollout in Q4. Would you be open to introducing us to your two top operations leads on Monday morning to begin that discovery sprint?"

Why it succeeds: Validates the ambition, channels executive urgency into disciplined focus, defines clear selection criteria, and commits to a dated next action.

### Scenario 2: "Your pilot's outputs are fine, but the ops team will not support it"

- Setup - the pilot works and the business sponsor calls the outputs fine. Then the ops team lead says flatly: "my team will not support this. It fails silently and we find out from users."
- Hidden goals - do you treat ops as a blocker or as a design constraint; can you fix the ownership and failure-mode design rather than the mood; will you throw the sponsor or ops under the bus
- A strong response outline - take the objection as requirements. Ask what "fails silently" looked like, twice, with specifics. Commit to the fixes that address it: structured logging with alerts on symptoms, a kill switch, a runbook, and a named on-call arrangement with a response window. Offer a weekly ops review for the pilot's duration. Then reset expectations with the sponsor separately: go-live moves until the ownership design exists, and that is what makes the system dependable. End with a joint session to sign off the runbook.
- Common failure responses - escalating to the sponsor to overrule ops; promising to fix everything without asking what specifically failed; defending the pilot's accuracy when accuracy was never the objection; agreeing with everything and leaving with no artifact

#### Verbatim dialogue transcript

Interviewer (Ops Team Lead): "I do not care that the VP liked your demo. My on-call team will not take pager duty for this service. When your model or your upstream API hiccups, it does not throw clean errors; it just hangs or returns empty JSON, and we only find out when angry customer service agents start pinging us on Slack. We are not supporting this."

Weak candidate response: "We can adjust the prompt to make it more reliable, and our model provider has a 99.9% SLA. The VP already signed off on the pilot launch next Tuesday."

Why it fails: Relies on executive authority to override operators, misses the architectural root of the complaint (lack of observability and dead-letter handling), and cites third-party SLAs that do not prevent application-level hangs.

Expert FDE response: "You are completely right to refuse pager duty for a black box. If an on-call engineer cannot diagnose a failure within five minutes from a dashboard, the system is not production-ready. 

Let us pause the Tuesday rollout right now. I want to walk through the exact failure you experienced. What was the last incident where the service hung silently? 

Here is what we will build before asking you to touch this service: first, an explicit client-side timeout of 2.5 seconds on every upstream call with an automated circuit breaker. Second, structured JSON logging with correlation IDs on every request, so any empty response immediately emits a high-priority alert to your Datadog or CloudWatch cluster. Third, an emergency feature flag kill-switch that instantly routes traffic back to your legacy rule engine without needing a code deployment. Finally, our team will stay on primary on-call rotation for the first 30 days of production. 

Can we sit together for 45 minutes on Thursday to review the telemetry dashboard and sign off on the rollback runbook before we schedule any customer-facing launch?"

Why it succeeds: Takes total ownership, validates the operator's operational burden, pauses launch until reliability tooling is built, offers shared on-call skin in the game, and establishes a concrete runbook review.

### Scenario 3: "We go live before the audit in six weeks, and security has not reviewed anything"

- Setup - a compliance audit lands in six weeks. The sponsor wants the system live before it. Security review has not started, and the data includes customer PII.
- Hidden goals - will you sequence honestly under deadline pressure; can you say no to a plan while saying yes to a revised one; do you treat security review as an obstacle or as a dependency to manage
- A strong response outline - name the dependency out loud and sequence around it. Start the security review this week with a minimal review pack: data flows, model and vendor retention terms, secrets handling, audit logging. Propose a phased scope: a read-only, no-PII slice live in three weeks, the PII-touching slice after security sign-off, and pre-agreed rollback for both. Give the sponsor the audit-relevant win, the no-PII slice plus documentation, rather than the full ask. End with the review pack as the dated next step.
- Common failure responses - promising the date and hoping security moves fast; going around security as "an engineering decision"; scoping to everything and delivering nothing by the audit; refusing the deadline without offering a revised plan

#### Verbatim dialogue transcript

Interviewer (Business Sponsor): "The annual SOC 2 and customer trust audit begins in six weeks. If this automated document verification pipeline is not running in production by then, we lose our efficiency rating and our executive bonus pool takes a hit. The CISO says security review takes four to six weeks alone. Can we just push to production on our private subnets and get security sign-off retroactively?"

Weak candidate response: "Sure, as long as it is on a private subnet and we use environment variables for the API keys, we can go live and do the security paperwork after the audit passes."

Why it fails: Disregards security governance, exposes the company to audit failure and regulatory penalties, and destroys professional credibility.

Expert FDE response: "Deploying unvetted PII pipelines into production before an audit is the quickest way to fail that audit and trigger a regulatory freeze. If the auditors inspect our change logs and see an unapproved production deployment touching customer data, the consequences for the business will far outweigh the efficiency score. 

However, we can still give you an audit-ready production win in six weeks. We split the deployment into two distinct phases. Phase 1 scopes the pipeline strictly to internal public documentation and sanitized, non-PII test sets. We can package a security review packet by this Wednesday that contains our threat model, data flow diagram, encryption-at-rest proofs, and zero-data-retention agreements from the model vendor. 

Because Phase 1 touches zero customer PII, we can request an expedited two-week security review for that slice. That gets Phase 1 live in production four weeks before the audit, proving automated pipeline capability to the auditors with full governance approval. Phase 2 with live PII customer data will follow its standard review queue without risking the audit. 

Let us draft that security packet today so we can put it on the CISO's desk tomorrow morning."

Why it succeeds: Protects the organization from security breaches and compliance violations while structuring an honest, phased path to satisfy the business objective.

### Scenario 4: "Can you just add this one little feature before next week's sign-off?"

- Setup - you are 80% through an engagement. The business sponsor loves the progress and asks for a "small" change: also integrating live audio transcripts from call center feeds into the existing text classification pipeline before next Tuesday's sign-off.
- Hidden goals - can you hold scope boundaries without offending the client; do you expose the hidden technical iceberg; do you trade off scope constructively

#### Verbatim dialogue transcript

Interviewer (Product Director): "The ticket categorization demo looks incredible. Since you already have the pipeline running, can we also plug in the audio recordings from our Twilio call center before next Tuesday's steering committee? It is just passing the audio through Whisper, right? Should only take an afternoon."

Expert FDE response: "It is exciting that the text pipeline is performing well enough that you want to expand it to voice. From the outside, passing audio to a speech model looks like an afternoon task, but in production, audio introduces three hidden systems: diarization to separate the customer from the agent, handling audio packet loss and compression artifacts, and managing latency spikes from multi-megabyte audio payloads. 

If we rush that into the pipeline before next Tuesday, we introduce unvetted failure modes that could cause the steering committee demo to fail. 

Our priority for Tuesday is securing formal sign-off on the text classification pipeline, which is currently on track with an 88% precision score. What we will do is include an architectural slide in Tuesday's presentation showing the exact roadmap and data flow for audio ingestion as Phase 2. Let us lock in the win on the text system first, and then kick off the audio spike the following week."

### Scenario 5: "Your system returned a hallucinated policy clause to a Tier-1 customer"

- Setup - an urgent morning escalation. A Tier-1 enterprise account received an answer from the document assistant that quoted a non-existent insurance discount. The client is furious and threatening to pull their contract.
- Hidden goals - incident composure; triage discipline; separating root cause from blame; preventing panic prompt-hacking; establishing regression defense

#### Verbatim dialogue transcript

Interviewer (VP of Customer Success): "We have a catastrophic incident. Your system quoted a 20% loyalty discount to our largest enterprise client that does not exist in any policy document. The client thinks we are incompetent and our CEO is on the phone. What did you break, and why did the prompt let this happen?"

Expert FDE response: "I hear the urgency, and we are treating this as a P0 severity incident. Let us stabilize the immediate customer impact first before we analyze the root cause. 

First: have we pinned the tenant session? I am immediately enabling our strict fallback mode for this client's workspace, which forces every answer to require two independent verbatim document citations or refuse with a transfer to a human specialist. 

Second: do not modify any prompts right now. Prompt changes made under panic introduce regressions across other document types. I have pulled the exact request ID and trace from our logs. We need to determine if this was a retrieval failure—meaning the search engine retrieved an outdated or irrelevant promotional memo—or a generator grounding failure, where the model fabricated the clause despite the retrieved text. 

Once we inspect the retrieved chunks in the trace, we will write a dedicated regression test case for this specific policy query and add it to our automated golden test suite. Within two hours, I will deliver an incident summary document for the CEO explaining the failure mechanism, the immediate containment switch enabled, and the deterministic citation validator we are putting in place to ensure this cannot recur."

## How to practice

We recommend three practices, in order of return:

- Peer role-plays - run each scenario twice, once as candidate and once as interviewer; playing the interviewer teaches the hidden goals faster than any write-up
- Record yourself - the gap between how you think you sound and how you sound is widest under pushback
- The five-question self-review rubric - score every practice round:

1. Were my first three exchanges questions rather than answers or a pitch?
2. Did I get the success metric and the decision process before proposing anything?
3. Did I replay what I heard and invite correction?
4. Did I leave at least one expectation the customer could hold me to?
5. Did the conversation end with a concrete, dated next step?

## Related documents

- [Discovery and requirements](../skills/02-discovery-and-requirements.md) - the full discovery framework this playbook compresses
- [Managing expectations](../customer/04-managing-expectations.md) - saying no and delivering bad news, the scenario 3 skill set
- [Stakeholder management](../skills/04-stakeholder-management.md) - who decides, who vetoes, who operates
- [Debugging customer systems](../troubleshooting/02-debugging-customer-systems.md) - the shared on-call reality behind scenario 2
- [System design rounds](03-system-design.md) - the design conversation that pairs with this one
- [Coding round solutions](08-coding-solutions.md) - code solutions for technical scenarios
- [The interview process](01-interview-process.md) - where this round sits in the loop

## Further reading

- [Exponent](https://tryexponent.com) - FDE interview guides with role-play descriptions
- Never Split the Difference (Chris Voss) - negotiation moves that translate directly to pushback handling

