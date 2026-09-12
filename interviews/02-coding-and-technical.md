# Coding and Technical Rounds

This file is for candidates who can already code and need to know what the FDE coding round actually rewards. You get the skills being scored, the four common formats, what good looks like in a live exercise, a fictional practice problem set, and a preparation checklist.

## What the round actually tests

The round scores practical fluency over algorithmic puzzles. The recurring tasks are the job's daily shape: parsing messy input, designing a small API, transforming data between formats, and debugging a snippet that almost works. This is an industry pattern drawn from practitioner guides and reports rather than a published rubric, and it matches what postings demand: Python appears in 91.0% of 146 scraped FDE postings and RAG in 52.0% ([the scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md), February-July 2026).

Expect AI-adjacent tasks in 2025-2026 loops (pattern, not law): parsing and validating structured output from an LLM, writing chunking logic for documents, and implementing retry logic around a rate-limited call. The Anthropic posting's requirement of production LLM experience ([greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/5302966008), 2026) is the clearest published signal of this drift.

What interviewers listen for underneath the code is narration quality: whether your questions reveal constraint-finding instincts, whether your trade-offs are stated rather than silent, and whether your first instinct on breakage is a hypothesis instead of a hack. This is our interpretation of why the round feels more like pairing than examination.

## Typical formats

Four formats cover most rounds (pattern):

- Live coding - 45-60 minutes in a shared editor; a practical problem, not an algorithm drill
- Practical exercise - a small repository to extend or fix, before or during the session
- Debugging a failing service - a broken snippet, trace, or log set, and the question of what is wrong
- Code review - an integration snippet with planted defects, and your read on it

Ask the recruiter which format to expect; most will say. Knowing it is a debugging exercise rather than greenfield coding changes what you rehearse.

## What good looks like

We recommend this sequence for any live exercise:

1. Narrate constraints before coding - say what you assume about input size, failure rates, and who calls this
2. Clarify inputs, outputs, and error behavior - one round of questions, then commit; what happens on empty input is worth more than a clever parse
3. Write the happy path fast, then harden - timeouts, retries, and validation after the core works, not instead of it
4. Test as you go - run what you wrote; an unexecuted function is a rumor
5. Think out loud without performing - state the trade-off, pick one, and move; interviewers score judgment, not monologue

The difference between passing and scoring well is usually hardening: candidates who stop at the happy path pass, and candidates who add the timeout, the validation, and the test score.

One more habit worth naming: spend the first five minutes reading before writing. Candidates who type immediately and refactor later lose more time than they gain, and the refactor rarely happens under a clock.

## A practice problem set

All problems are fictional but representative. We recommend solving each in 30-45 minutes with a timer and a running commentary.

### Parse the malformed export

Given a CSV export from a fictional customer system with missing columns, mixed encodings, and duplicate rows, produce a summary of defect counts by type. Tests input handling, defensive parsing, and whether you state assumptions instead of silently skipping rows. Strong answers report what they dropped and why.

### Design an idempotent webhook receiver

A vendor retries webhook deliveries; your receiver must deduplicate without losing events. Tests delivery semantics, idempotency keys, deduplication windows, and ordering. Strong answers name the at-least-once assumption out loud.

### Find the bug in the failing trace

You get a trace showing intermittent timeouts between a queue consumer and an external API. Tests hypothesis discipline: narrowing by evidence, forming the cheapest discriminating test, and resisting the shotgun fix. The method is in [debugging methodology](../troubleshooting/01-debugging-methodology.md).

### Extract structured fields from messy text

Free-text incident reports must become typed records, with a validation step and a retry when fields are missing. Tests structured-output handling, schema validation, and a retry loop that feeds the validation error back. Strong answers include a small eval over five fixed cases.

### Implement exponential backoff with jitter

A client for a rate-limited API needs retries that do not synchronize into a thundering herd. Tests resilience primitives, whether you can explain why jitter exists, and testability: a fake clock beats a bare `time.sleep`.

### Review the snippet that leaks credentials

A working integration snippet logs full request bodies including an authorization header, and stores an API key in source. Tests review instincts: secrets handling, log hygiene, and how you deliver findings without grandstanding.

## The AI-flavored round

When the exercise touches an LLM, the scoring follows the same logic with different nouns. Expect some combination of calling a model API with structured outputs, handling rate limits and partial failure, and writing a small eval that checks output quality on fixed cases.

Two calibrations from practitioner reports (pattern):

- Pure-prompt answers score low - a paragraph of prompt engineering with no validation, retries, or evaluation is the easy half of the job, and interviewers know it
- Testable code scores high - a schema check, a retry that feeds the error back, and five golden test cases turn the same prompt into a deployable system

The practical implication: when the exercise says "use an LLM here", budget most of your time for everything around the call. The call itself is one line; the contract around it is the work.

If you can build the extraction problem above and explain when you would escalate from prompt fixes to pipeline changes, you are prepared for this round. The underlying patterns are cataloged in [LLM application patterns](../ai/01-llm-application-patterns.md) and the eval habit in [evaluation and testing](../ai/03-evaluation-and-testing.md).

## Preparation checklist

Work through this list before scheduling the loop; each item is a concrete rehearsal, not a reading task:

- [ ] I can parse and validate messy CSV and JSON input in under 20 minutes from memory
- [ ] I can write an idempotent handler and explain the delivery semantics it assumes
- [ ] I can implement retry with exponential backoff and jitter without looking it up
- [ ] I can call an LLM API with a structured output schema and validate the result
- [ ] I can write a five-case eval for an extraction or classification task
- [ ] I can read a trace or log excerpt and state a top-three hypothesis list
- [ ] I can review an integration snippet and find the secrets, PII, and error-handling defects
- [ ] I narrate constraints and assumptions before coding in practice sessions, not just in interviews
- [ ] I have completed at least one timed mock with a peer watching

## Related documents

- [The interview process](01-interview-process.md) - where this round sits in the loop
- [Take-home assignments](06-take-homes.md) - the same skills tested asynchronously, with a timebox
- [LLM application patterns](../ai/01-llm-application-patterns.md) - the patterns behind the AI-flavored tasks
- [Evaluation and testing](../ai/03-evaluation-and-testing.md) - the eval habit this round rewards
- [APIs and integrations](../engineering/02-apis-and-integrations.md) - boundary handling in depth
- [Project ideas](../portfolio/02-project-ideas.md) - specs that double as practice material

## Further reading

- [fde.academy](https://fde.academy) - practitioner guides on technical round expectations
- [Exponent](https://tryexponent.com) - FDE interview guides and community-sourced question patterns
