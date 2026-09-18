# Take-Home Assignments

This file is for candidates who have been given, or expect, a take-home in an FDE loop: a small working system built inside a stated timebox. You get the common formats, what evaluators actually score, the submission structure that reads well, a time budget, and the failure modes that cost otherwise strong submissions.

## Why loops use take-homes

Some FDE loops replace or augment a live round with a take-home: build a small working system against a brief inside a stated timebox. The pattern is most common in startup FDE loops, where schedules are thin and the artifact carries more signal than another conversation; timeboxes commonly run 3-8 hours (pattern). The interpretation: a take-home scores the artifact habit. FDEs ship systems plus documents, and a take-home is exactly that, compressed.

Before you start, pin down the rules in one email: the exact timebox, whether it is a hard ceiling, which external tools and model providers are acceptable, and whether clarifying questions are welcome. Asking one good question about the brief is scored positively in most loops; asking none and guessing silently is the more common failure (interpretation).

## Typical formats

Practitioner reports converge on four formats (pattern):

- Build a small API that does X - against a provided dataset, with stated behaviors and edge cases left implicit
- Prototype from a brief - sample data plus a one-page brief; deliver a working prototype and a `README`
- Review and incident write-up - review a flawed integration or an incident transcript and produce a summary with remediations
- Extend this repo - add feature Y to an existing codebase without breaking its behavior

The first two dominate. The review format rewards the same skills as the debugging round, delivered in writing.

## What evaluators look for

Our interpretation, grounded in what FDEs actually produce on the job:

- `README` quality - the take-home `README` is a spec: what you built, what you decided, and what you did not
- Error handling at boundaries - parsing, timeouts, retries, and validation wherever your code meets the world
- Tests that guard behavior - a handful of tests on the edges beats a suite over trivia
- Honest limitations - what breaks under load, what you would fix with more time; pretending otherwise reads as inexperience
- Production thinking - configuration outside code, no secrets committed, logs that would help a stranger debug
- Scoped ambition - a complete, working slice beats a sprawling half-system; evaluators run code, and code that does not run scores zero

The last line is the regret we most often see: candidates trade the working slice for one more feature and submit something that does not start.

## The submission structure that scores

We recommend this structure; it mirrors what a real engagement artifact looks like.

### The `README`

Five sections, in this order:

1. Problem restatement - the brief in your words, including the assumptions you added to make it decidable
2. Decisions and trade-offs - the three to five choices that mattered, each with the alternative you rejected
3. How to run - commands that work on a fresh clone, with pinned dependencies
4. What is tested - the behaviors guarded by tests and, honestly, the ones not
5. What you would do next - with more time; this is where scoped ambition shows maturity

### The code

Typed where the language allows, validated at boundaries, and tested at boundaries: the parser, the external call, and the retry path. Internal elegance matters less than whether a stranger can change one input and predict the behavior.

### The demo

A `curl` script or a small fixture run that exercises the happy path and one failure case. If evaluators cannot see it work in two minutes, the work did not happen.

## When the take-home includes a model

Briefs increasingly include an LLM component (pattern). The same scoring logic applies with two additions:

- Ship the eval with the code - five to ten fixed input cases with expected properties, runnable with a single command, so the evaluator can reproduce your quality claim instead of trusting it
- Control cost and determinism - a mocked provider for tests, real calls behind a flag, cached responses for the demo, and a note in the `README` about what a month of production traffic would cost at the observed usage

A submission that measures its own model behavior reads as production thinking; one that screenshots a lucky completion reads as a demo.

## Time budgeting

We recommend the 4-hour shape for a 4-hour timebox, scaled proportionally for others:

1. 30 minutes - read the brief twice and write your assumptions down before touching code
2. 60 minutes - design the slice and skeleton it: module boundaries, the schema, the failure behavior
3. 90 minutes - build the core until it runs end to end on the happy path
4. 60 minutes - harden and test: validation, retries, the failure path, boundary tests
5. 30 minutes - write the `README` and record the demo script

When time runs out, cut features first, then hardening, and never the `README` - a modest system with a real `README` beats a richer system with a stub. Stop before the deadline and record what you cut: a submission that says what it is missing reads as controlled, not incomplete.

## Common failure modes

- Overengineering - queues, microservices, and abstraction layers for a task that asked for a function; the brief is the scope
- No tests - the most common deduction and the cheapest to fix
- `README` as an afterthought - decisions unrecorded, run commands that fail on a fresh clone
- Demo data that hides the edge cases - curated fixtures make evaluators suspect the happy path is the only path
- Silent scope assumptions - deciding the brief's ambiguities in your head instead of on paper; undocumented assumptions are indistinguishable from missed ones

## Before you submit

- [ ] A fresh clone runs the demo with two commands or fewer
- [ ] No secrets, API keys, or customer-identifying data in the repo or its history
- [ ] The `README` states assumptions, decisions, and what you would do next
- [ ] Boundary behavior is tested: bad input, empty input, and a failed external call
- [ ] The failure path is visible in the demo, not just the happy path
- [ ] Dependencies are pinned and the install steps match what you actually ran
- [ ] The timebox was respected, and overruns are either absent or disclosed
- [ ] You re-read the brief once more and checked nothing was silently dropped

## Fictional enterprise take-home specification

Below is the representative brief used across elite AI and data platform hiring loops (48 to 72 hour window).

### The customer prompt

"We are a logistics enterprise receiving 15,000 shipment exception emails and customs queries per day across five regional ports. Right now, support agents spend four minutes per ticket manually reading PDFs, extracting invoice numbers, classifying issue urgency, and querying our database. 

Deliver a working prototype service that:
1. Ingests raw ticket payloads and attached markdown documents
2. Extracts shipment ID, carrier, defect category, and urgency score with schema validation
3. Provides an automated answer grounded in our customs handbook, with exact document citations
4. Routes low-confidence or high-severity cases to an exception review queue
5. Ships with an automated test suite, an evaluation script demonstrating extraction accuracy, and client-facing architecture documentation."

## The 100-point hiring committee rubric

Hiring committees score take-homes across five distinct pillars:

### 1. Code architecture and hygiene (25 points)
- Clean separation of concerns (API layer, ingestion pipeline, model engine, validation layer)
- Strong typing with type annotations and Pydantic schemas
- Zero committed credentials or environment leaks
- Pinned dependency management (`requirements.txt` or `pyproject.toml`)

### 2. Resilience and boundary handling (25 points)
- Defensive parsing on corrupted inputs and encoding anomalies
- Client-side timeouts, retry loops with full jitter, and circuit breaker patterns
- Explicit refusal when source context lacks sufficient information
- Idempotency guarantees on repeated ingestion

### 3. Evaluation rigor and measurement (20 points)
- Runnable evaluation harness included in the repository
- Golden dataset testing at least 15 to 25 edge cases (clean, noisy, adversarial, out-of-domain)
- Metric accounting: per-field precision, recall, citation accuracy, and schema failure rate
- Transparent disclosure of model limitations and failure cases

### 4. Client deliverable and documentation (20 points)
- Clear problem restatement with explicit assumption inventory
- Architecture Decision Record (ADR) justifying technology trade-offs
- One-page Executive Handover Memo written for business stakeholders
- Working quickstart instructions that execute cleanly on a fresh machine

### 5. Production readiness and containerization (10 points)
- Clean `Dockerfile` and `docker-compose.yml` configuration
- Structured JSON logging with request tracing IDs
- Health check and metrics endpoint (`/health`, `/metrics`)

## Architecture Decision Record (ADR) template

Include an ADR in your submission (`docs/ADR-001.md`). Evaluators use this to judge senior engineering reasoning:

```markdown
# ADR 001: Hybrid Search and In-Memory Vector Storage for Triage Prototype

## Status
Accepted

## Context
The customer needs sub-second response times across 15,000 daily tickets with strict adherence to port customs handbooks. Budget and engagement constraints require a lightweight footprint that can run on an existing on-premise Kubernetes node without provisioning managed external vector cloud services.

## Decision
We selected an in-process SQLite database paired with sqlite-vec and BM25 sparse keyword search, orchestrating extraction via Pydantic schema validation.

## Consequences
Positive:
- Zero external cloud database dependencies; runs locally in a single Docker container.
- Sub-50ms hybrid retrieval latency on queries under 50,000 document chunks.
- Deterministic schema validation guarantees zero unvalidated payloads reach the database.

Negative:
- Horizontal scaling across multiple worker pods requires transitioning from SQLite to PostgreSQL with pgvector.
- Memory usage scales linearly with chunk count, requiring an index sharding strategy if the corpus exceeds 250,000 documents.
```

## Executive Handover Memo template

Include a one-page business summary in your `README` or `docs/HANDOVER.md`:

```markdown
# Executive Handover: Automated Port Exception Triage Pipeline

## Engagement summary
Over this initial milestone, we engineered an automated ingestion and document grounding service for port customs tickets. The system replaces manual triaging by automatically extracting invoice data, querying regulatory handbooks, and generating citation-grounded response drafts.

## Measured performance baseline
Across our 25-case golden verification suite:
- Field extraction precision: 96.2% on standard customs declarations
- Automated routing accuracy: 91.4% across five defect classifications
- Hallucination rate: 0.0% (system cleanly refuses and routes to human operator when citations cannot be verified)
- Average end-to-end latency: 840ms per ticket

## Recommended next steps
1. Deploy in shadow mode for two weeks alongside the Rotterdam port operations team to capture edge-case drift.
2. Integrate OAuth 2.0 service account credentials with the customer's active SAP shipment ledger.
3. Review human operator override logs weekly to update the golden evaluation suite.
```

## Related documents

- [Coding and technical rounds](02-coding-and-technical.md) - the same skills scored live
- [What to build](../portfolio/01-what-to-build.md) - the portfolio principles that make take-homes easy
- [Requirements to spec](../customer/02-requirements-to-spec.md) - the `README`-as-spec habit in full
- [Production readiness checklist](../deployment/03-production-readiness-checklist.md) - the production thinking evaluators look for
- [Evaluation and testing](../ai/03-evaluation-and-testing.md) - when the take-home includes a model component
- [The interview process](01-interview-process.md) - where the take-home sits in the loop

## Further reading

- [pydantic](https://pydantic.dev) - the validation library most Python take-home evaluators expect at the boundaries
