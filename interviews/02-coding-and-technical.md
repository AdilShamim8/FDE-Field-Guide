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

## The Google FDE "Vibe Coding" & Rapid Build Round

The signature practical round in modern FDE loops—standardized at Google, Palantir, and frontier labs—is the **60-Minute "Vibe Coding" / Rapid Live Build** ([YagyanshB Google FDE Guide](https://github.com/YagyanshB/google-fde-interview-guide), [Om Bharatiya](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/15-role-guides/forward-deployed-engineer.md)).

Unlike algorithmic whiteboarding, the candidate is provided an API key and a messy enterprise dataset (corrupted CSV/JSON with mixed encodings, null values, and dirty types). The goal is building a working, resilient integration under clock pressure.

### The 60-Minute Tactical Timebox

- **Minutes 0 to 10 (Inspection & Alignment)**: Inspect the raw payload schema immediately. Print sample anomalies (null keys, mixed timestamp formats, currency strings with commas). State assumptions aloud: "I notice 8% of records lack customer IDs; I will record them in a defect ledger rather than crashing the batch." Agree with the interviewer on the single core happy path.
- **Minutes 10 to 35 (Core Engine & Integration)**: Build the data transformation and ingestion pipeline. Write clean, testable procedural functions with type hints rather than over-engineered abstract class hierarchies. Connect to the LLM or target API seam.
- **Minutes 35 to 50 (Hardening & Edge Cases)**: Add validation checks, defensive fallbacks, and boundary error handling. Run 3-4 unit test assertions on edge cases (e.g. empty strings, token limit overflows, 429 backpressure).
- **Minutes 50 to 60 (Run & Production Tradeoff Narration)**: Execute the script live on sample data. Narrate remaining production debt cleanly: "In production, I would replace this in-memory dictionary with a distributed Redis sliding window, add OpenTelemetry distributed spans, and deploy an item-level dead letter queue."

---

## Verified Practical Problem Set

All problems reflect verified technical patterns from enterprise interview loops ([Om Bharatiya](https://github.com/ombharatiya/AI-Engineer-Interview-Questions), [Nehal Vyas](https://fde.hinehal.com/blogs/fde-interview-questions), [YagyanshB](https://github.com/YagyanshB/google-fde-interview-guide)). Production-grade runnable implementations and pytest suites are provided in [interviews/code/](code/):

### 1. Parse the malformed customer export (`code/parser.py`)
- **Verified Source**: [YagyanshB Google FDE Guide](https://github.com/YagyanshB/google-fde-interview-guide)
- **Problem**: Given a CSV export from a legacy ERP with mixed character encodings (UTF-8, UTF-8-BOM, CP1252), missing IDs, and dirty currency strings, produce a summary of defect counts by type and return repaired records.
- **Tests**: [test_parser.py](code/test_parser.py) (`pytest interviews/code/test_parser.py`)

### 2. Design an idempotent webhook receiver (`code/webhook_receiver.py`)
- **Verified Source**: [Nehal Vyas](https://fde.hinehal.com/blogs/fde-interview-questions)
- **Problem**: A customer webhook delivery service retries at-least-once deliveries; design an idempotent receiver with payload hash deduplication, sliding TTL cache, and partial failure isolation.
- **Tests**: [test_webhook_receiver.py](code/test_webhook_receiver.py)

### 3. Implement exponential backoff with full jitter (`code/resilient_client.py`)
- **Verified Source**: [Alexey Grigorev](https://github.com/alexeygrigorev/ai-engineering-field-guide)
- **Problem**: A client calling an upstream LLM API encounters 429 Too Many Requests; implement an adaptive retry decorator respecting `Retry-After` headers and randomized full jitter backoff.
- **Tests**: [test_resilient_client.py](code/test_resilient_client.py)

### 4. Extract structured fields with validation and error-feedback retry (`code/structured_extractor.py`)
- **Verified Source**: [Om Bharatiya](https://github.com/ombharatiya/AI-Engineer-Interview-Questions)
- **Problem**: Free-text customer incident logs must become typed Pydantic records; when the LLM returns missing or invalid fields, capture the schema exception and feed it back in a one-turn auto-correction retry.
- **Tests**: [test_structured_extractor.py](code/test_structured_extractor.py)

### 5. Multi-tenant sliding window rate limiter (`code/rate_limiter.py`)
- **Verified Source**: [YagyanshB Google FDE Guide](https://github.com/YagyanshB/google-fde-interview-guide)
- **Problem**: Protect downstream model provider quotas with a sliding-window rate limiter enforcing tiered per-tenant requests and token burst caps.
- **Tests**: [test_rate_limiter.py](code/test_rate_limiter.py)

### 6. Token-aware document chunker with sliding overlap (`code/chunker.py`)
- **Verified Source**: [Dr. Sanjay Kumar PhD](https://skphd.medium.com/top-25-forward-deployed-engineer-fde-interview-questions-and-answers-ad9ac4a6ad7f)
- **Problem**: Ingest enterprise contract documents into token-budgeted chunks with sliding window overlap and structural heading metadata preservation.
- **Tests**: [test_chunker.py](code/test_chunker.py)

### 7. Google FDE Vibe Coding Integration Runner (`code/vibe_coding_runner.py`)
- **Verified Source**: [YagyanshB Google FDE Guide](https://github.com/YagyanshB/google-fde-interview-guide)
- **Problem**: Ingest, normalize, rate-limit, and validate dirty enterprise payloads under 60-minute timebox constraints, generating structured run ledgers and defect metrics.
- **Tests**: [test_vibe_coding_runner.py](code/test_vibe_coding_runner.py)

---

## Preparation Checklist

Work through this list before scheduling the loop; each item is a concrete rehearsal:

- [ ] I can parse and validate messy CSV and JSON input in under 20 minutes from memory
- [ ] I can write an idempotent handler and explain the delivery semantics it assumes
- [ ] I can implement retry with exponential backoff and full jitter without looking it up
- [ ] I can call an LLM API with a structured output schema and validate the result
- [ ] I can write a five-case eval for an extraction or classification task
- [ ] I can read a trace or log excerpt and state a top-three hypothesis list
- [ ] I can review an integration snippet and find the secrets, PII, and error-handling defects
- [ ] I narrate constraints and assumptions before coding in practice sessions, not just in interviews
- [ ] I have completed at least one timed 60-minute mock run of `vibe_coding_runner.py`

---

## Related Documents

- [Coding round solutions and narration playbooks](08-coding-solutions.md) - verbatim verbal scripts and architectures
- [Runnable test suite](code/) - complete pytest implementations
- [Question bank](07-question-bank.md) - round-by-round interview question directory
- [The interview process](01-interview-process.md) - stage breakdown and hiring pipelines

---

## References & Further Reading

1. **YagyanshB**: [Google Forward Deployed Engineering Interview Prep Guide](https://github.com/YagyanshB/google-fde-interview-guide)
2. **Om Bharatiya**: [AI Engineer Interview Questions: Forward Deployed Engineer Guide](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/15-role-guides/forward-deployed-engineer.md)
3. **Nehal Vyas**: [Forward Deployed Engineer Interview Questions & Answers](https://fde.hinehal.com/blogs/fde-interview-questions)
4. **Dr. Sanjay Kumar PhD**: [Top 25 Forward Deployed Engineer (FDE) Interview Questions and Answers](https://skphd.medium.com/top-25-forward-deployed-engineer-fde-interview-questions-and-answers-ad9ac4a6ad7f)
5. **Alexey Grigorev**: [AI Engineering Field Guide: FDE Responsibilities and Skills Analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)
