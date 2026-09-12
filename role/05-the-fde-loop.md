# The FDE Loop

Every FDE engagement, however messy, runs the same loop. This is the mental model behind every other document in this guide, and the most honest answer to "what does an FDE do all day": you move a customer around this loop, then find the next problem and go again.

If you read only one file in this guide, read this one. Each stage below names the artifact that proves it happened, the way it classically fails, and the section that covers it in depth.

## The loop in one view

The stages, in order:

1. Problem
2. Discovery
3. Requirements
4. Architecture
5. Prototype
6. Integration
7. Deployment
8. Evaluation
9. Iteration
10. Production
11. Customer impact

Then back to new problems. OpenAI's FDE postings compress the same sequence into one job-description line: lead "technical discovery, architecture, implementation, evaluation, productionization, and handoff" (observed evidence, [OpenAI careers](https://openai.com/careers), 2026).

## The stages

Each stage has four parts: the goal, the key artifact, the FDE's job, and the classic failure. The artifact matters more than it looks: engagements drift when stages produce conversations instead of documents.

### 1. Problem

- Goal - turn a vague customer ask into a problem statement the customer recognizes as their own
- Key artifact - a one-page problem statement naming the business metric the system should move
- The FDE's job - interview stakeholders until the real problem, not the requested feature, is on paper
- Classic failure - building what was asked for instead of what was meant, and finding out at evaluation

### 2. Discovery

- Goal - map the workflows, data, systems, and people the problem actually touches
- Key artifact - discovery notes: workflow maps, system inventory, data sources, constraints, and the politics
- The FDE's job - sit with the people who do the work and watch the real process, not the documented one
- Classic failure - discovering in week six that the real workflow runs in a spreadsheet nobody mentioned

### 3. Requirements

- Goal - convert discovery into requirements specific enough to build and test against
- Key artifact - a requirements document the customer signs, with explicit non-goals
- The FDE's job - force trade-offs into the open and pin down what is out of scope before anything is built
- Classic failure - requirements written as aspirations ("the assistant should be intelligent") that no evaluation can falsify

### 4. Architecture

- Goal - choose a design that fits the customer's constraints, not the habits from your last engagement
- Key artifact - architecture decision records plus a deployment sketch covering regions, environments, and data boundaries
- The FDE's job - make trade-offs legible to both sides: latency against cost, build against buy, SaaS against VPC-embedded
- Classic failure - importing the previous engagement's architecture into a customer whose compliance rules forbid half of it

### 5. Prototype

- Goal - answer the riskiest question first with the cheapest thing that can answer it
- Key artifact - a proof of concept scoped to a decision, with success criteria agreed before the build starts
- The FDE's job - timebox it and make it produce a decision, not a demo
- Classic failure - a demo that works on ten hand-picked rows and collapses on the customer's real data

### 6. Integration

- Goal - connect the prototype to the customer's real systems, data, and identities
- Key artifact - an integration contract: APIs, schemas, auth flows, rate limits, and error handling, written down
- The FDE's job - work against systems you do not own and cannot reset, through the customer's change process
- Classic failure - treating the customer's shared staging environment like your own

### 7. Deployment

- Goal - get the system running in the environment where it will actually live
- Key artifact - a deployment runbook: environments, promotion path, rollback, secrets, and monitoring hooks
- The FDE's job - run go-live like a drill rather than a leap, against a production readiness checklist
- Classic failure - going live on a Friday, with no rollback plan, during the customer's busiest week

### 8. Evaluation

- Goal - define what good means and measure it continuously
- Key artifact - an evaluation report: golden datasets, scoring rubric, baseline against current, and tracked regressions
- The FDE's job - make quality a number both you and the customer trust, before and after every change
- Classic failure - nobody defined good, so every quality debate is unfalsifiable and lasts forever

### 9. Iteration

- Goal - close the measured gap between current behavior and the requirements
- Key artifact - a prioritized defect and improvement list tied to evaluation results
- The FDE's job - debug in an environment you did not build, fix, re-evaluate, and repeat without regressing what already worked
- Classic failure - shipping changes without re-running the evaluation suite, and quietly breaking last month's fix

### 10. Production

- Goal - cross the cliff from working pilot to a system the customer's business depends on
- Key artifact - a production readiness sign-off covering reliability, security review, monitoring, on-call, and ownership
- The FDE's job - drive the go/no-go honestly, including the option of no
- Classic failure - declaring victory at the demo and letting the pilot rot instead of either dying or growing

### 11. Customer impact

- Goal - prove the system moved the business metric named back in the problem stage
- Key artifact - a handover document plus an impact report: metric before and after, owners, and the next problems
- The FDE's job - hand over cleanly and carry the lessons back into your own product team
- Classic failure - handover to nobody, so the system works, decays slowly, and poisons the customer's appetite for round two

The loop feeds itself: a delivered system exposes the next problem, and trust from round one is what gets you round two. Most mature FDE engagements are sequels.

## The loop is not linear

The stage order is real, but not a waterfall. Three recursions are normal:

- Evaluation loops back to requirements - when the evaluation suite reveals that the requirement itself was wrong or unmeasurable, rewrite it before iterating on the system
- Iteration reopens architecture - when fixes start needing design changes rather than parameter changes, stop and re-decide
- Deployment findings reopen integration - the go-live drill regularly exposes auth, data, and environment assumptions that discovery missed

Teams that pretend the loop is linear are easy to spot: their requirements documents are frozen while their systems quietly stop matching them. We recommend treating the stage list as a map of what must be true at handover, not a calendar.

## Where loops die

Most failed engagements die at one of two stages, and neither death is dramatic.

### The evaluation gap

The loop dies at evaluation when nobody defined what good means. Without a trusted evaluation, iteration is opinion, the customer cannot tell progress from motion, and every stakeholder meeting re-litigates quality from scratch. The fix is unglamorous: agree on golden datasets and a scoring rubric during requirements, before the prototype exists. [Evaluation and testing](../ai/03-evaluation-and-testing.md) covers how.

### The production cliff

The loop dies at production when a working pilot never becomes a system the business depends on. The scale of this is measured, not anecdotal: an MIT NANDA report, The GenAI Divide: State of AI in Business 2025, found that approximately 95% of enterprise GenAI pilots deliver no measurable P&L impact (Fortune, August 2025, observed evidence). The same research found the survivors correlate with workflow integration, domain specificity, and buying external tools - in loop terms, teams that took integration, requirements, and production seriously.

The production cliff is the single most important fact in this guide. It is why the role exists, why employers pay for engineers who stay past the demo, and why [prototype to production](../deployment/01-prototype-to-production.md) gets its own section.

## The loop maps to this guide

Every stage has a section that goes deep:

- Problem - [the engagement lifecycle](../customer/01-engagement-lifecycle.md) opens with problem framing and kickoff
- Discovery - [discovery and requirements](../skills/02-discovery-and-requirements.md) has the interview frameworks and question banks
- Requirements - [requirements to spec](../customer/02-requirements-to-spec.md) turns conversations into documents both sides accept
- Architecture - [architecture for customer systems](../system-design/01-architecture-for-customer-systems.md) and [decision records](../system-design/03-trade-offs-and-decision-records.md)
- Prototype - [prototyping and PoCs](../engineering/01-prototyping-and-pocs.md) runs proofs of concept that produce decisions
- Integration - [APIs and integrations](../engineering/02-apis-and-integrations.md) and [data pipelines](../engineering/03-data-pipelines.md) cover the systems and the data
- Deployment - [deployment patterns](../deployment/02-deployment-patterns.md) covers VPC-embedded, SaaS-adjacent, and hybrid shapes
- Evaluation - [evaluation and testing](../ai/03-evaluation-and-testing.md) covers golden sets, judges, and regression
- Iteration - [debugging methodology](../troubleshooting/01-debugging-methodology.md) and [debugging customer systems](../troubleshooting/02-debugging-customer-systems.md)
- Production - [prototype to production](../deployment/01-prototype-to-production.md) and the [production readiness checklist](../deployment/03-production-readiness-checklist.md)
- Customer impact - [monitoring and reliability](../ai/04-monitoring-and-reliability.md) keeps the system healthy after handover

## Why interviews and portfolios mirror the loop

Interviewers structure FDE loops around this sequence because it is the job. Exponent's interview guides describe the ElevenLabs loop as "a compressed loop that runs from coding to conversation, testing technical range and customer instinct" (tryexponent.com, 2026), and a practitioner account of Cohere's FDE process (gaijineer.co, April 2026) expects candidates to talk through system context, scale assumptions, reliability decisions, and "what broke and how you fixed it". Customer scenario rounds are the loop compressed into forty-five minutes; see [customer scenario interviews](../interviews/04-customer-scenarios.md).

The same logic applies to portfolio projects. A project that walks the loop end to end - a problem statement, a real integration with messy data, an evaluation with a rubric, a deployment someone else could run - beats a polished tutorial, because it proves you can run the loop, not just the coding stage. [What to build](../portfolio/01-what-to-build.md) turns this into project principles.

We recommend rehearsing the loop before interviews: pick a system you have shipped and be ready to name the artifact and the failure at each stage. It is the shortest credible story an FDE candidate can own.

## Related documents

- [Prototype to production](../deployment/01-prototype-to-production.md) - the production stage and the cliff, in depth
- [Evaluation and testing](../ai/03-evaluation-and-testing.md) - the stage where most loops silently die
- [Customer scenario interviews](../interviews/04-customer-scenarios.md) - the loop compressed into interview rounds
- [What to build](../portfolio/01-what-to-build.md) - portfolio projects that walk the loop end to end
- [The engagement lifecycle](../customer/01-engagement-lifecycle.md) - the customer-facing phases from kickoff to handover
- [Responsibilities](02-responsibilities.md) - the posting evidence that produced this model

## Further reading

- [Fortune: MIT report on GenAI pilots](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo) - the production cliff, measured (August 2025)
- [The New Stack: why AI labs hire FDE teams](https://thenewstack.io/forward-deployed-engineers-ai) - integrate, launch, improve: the loop as hiring rationale (May 2026)
