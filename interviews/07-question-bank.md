# FDE Interview Question Bank

This file is a practice tool for FDE interview preparation: recurring question patterns by round type, each with the signal the interviewer is listening for. The questions are practitioner-pattern-based, assembled from guides and reports (fde.academy, Exponent, the gaijineer.co Cohere account, Reddit threads, 2026); the exact wording is fictional but representative, and no company's actual question set is reproduced. This is not a leaked-answers sheet - the value is practicing the signals, not memorizing phrasing.

## How the bank is organized

One subsection per round type. Each question is followed by a dash and the signal behind it. Questions overlap deliberately: the same scenario can open a discovery round or a design round, and interviewers reuse patterns the way the job does. Revisit the bank after each mock interview; the questions you answered clumsily are the ones worth re-running a week later.

## The question bank

### Discovery and requirements

The full discovery framework behind these is in [discovery and requirements](../skills/02-discovery-and-requirements.md).

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

The full role-play scenarios, with hidden goals and response outlines, are in [customer scenario rounds](04-customer-scenarios.md). The openers, briefly:

- "Our CEO saw a demo and wants AI everywhere by Q3" - discovery under hype
- "The pilot works but ops will not support it" - stakeholder conflict and ownership design
- "We go live in six weeks and security has reviewed nothing" - sequencing and honesty
- "Everything you showed us is fine, but it is too slow" - expectations and priority discipline
- "Can you just add this one thing?" - scope-creep handling
- "Your system gave a wrong answer to a customer today" - composure and ownership under fire

### Behavioral

The story inventory behind these is in [behavioral rounds](05-behavioral.md). The trait questions, briefly:

- A project you owned end to end - agency
- A requirement you pushed back on - judgment
- Debugging something you did not build - ownership beyond your own code
- When did you under-deliver, and what did you do next? - honesty and recovery
- A time you said no to a customer - expectation management
- A failure you repaired - postmortem habits
- A time you made someone else successful - cooperation and low ego

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
