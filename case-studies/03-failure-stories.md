# Observed failures and regression learning

This document records failures observed in sources and repository code during the 2026-10-09 review. It replaces an unsupported financial-institution postmortem and unmeasured cost multipliers with reproducible findings. None of these findings is represented as an actual customer outage.

## Failure 1: treating different source files as one reconciled dataset

Trigger: the first market refresh required cumulative title matches to equal the union of monthly matches.

Observed failure: source reproduction rejected that assumption. The monthly union contains 237 IDs while the cumulative rule matches 212; titles changed and some IDs are absent from the cumulative source. An initial tool commit was published before this failed validation was noticed.

Correction: retain the 25 scrape-only IDs, label both counts, and validate the discrepancy rather than invent records or force agreement. The correction and successful pinned-source reproduction were committed separately. Each subsequent file change was validated and pushed independently.

Remaining risk: distinct IDs may still represent repostings; source reconciliation is not a deduplication oracle for the underlying hiring opportunities.

## Failure 2: retries without waiting

Trigger: the retry exercise omitted its injected sleep function.

Observed failure: the default callback did nothing, so retrying callers ignored their calculated backoff.

Correction: use `time.sleep` by default and preserve injected clocks for tests. A regression test patches the default clock and confirms the calculated delay is actually applied. Negative retry budgets are rejected.

Remaining risk: a bounded attempt count is not a full end-to-end deadline, circuit breaker, or downstream idempotency contract.

## Failure 3: overlap breaks the advertised chunk budget

Trigger: a long sentence exceeded the chunk limit, or sentence overlap pushed a new chunk over the limit.

Observed failure: sentence-granularity splitting did not enforce the advertised hard bound.

Correction: use advancing regex-token windows with overlap inside the budget and retain sentence ends when they permit progress. Tests reconstruct a 501-word input and verify bounds for zero, partial, and near-full overlap.

Remaining risk: regex tokens are not model tokens; production context budgets require the actual model tokenizer and metadata overhead.

## Failure 4: high-confidence dispatch without evidence

Trigger: fallback confidence was raised to the dispatch threshold, or role filtering removed the evidence.

Observed failure: the previous gate could dispatch an unrelated or evidence-free request.

Correction: preserve raw similarity, route absent verified evidence to review in strict mode, and test the decision boundary. P0 escalation remains separate.

Remaining risk: heuristics are uncalibrated and exact sample quotations do not establish relevance or legal authority. An independently labeled customer holdout remains missing.

## Failure 5: replay semantics omit the request context

Trigger: a caller reused a key with altered content, another account, another simulated role, or concurrent delivery.

Observed failure: the original API replayed a raw key without payload conflict detection or expiry.

Correction: scope local keys, hash the payload, enforce TTL and capacity, and serialize reference state. Tests exercise eight concurrent identical requests and require one classification plus seven cached replays.

Remaining risk: caller-declared accounts and roles are not authenticated identity; a process lock is not distributed state. Queues and feedback still lack tenant authorization and persistence.

## Failure 6: operating instructions invoke absent controls

Trigger: an operator followed the old admin-mode, fallback-switch, or index-rebuild instructions.

Observed failure: the service defines none of those endpoints or commands.

Correction: replace the [runbook](../portfolio/reference-project/docs/SLA_RUNBOOK.md) with available startup, health, query, test, and stop/restart operations. State that restart loses reference data.

Remaining risk: durable restore, production alerts, privacy-safe telemetry, and measured SLOs require implementation and operator-completed drills.

## Related documents

- [Repository audit](../AUDIT.md) - prioritization and evidence scope
- [Reference tests](../portfolio/reference-project/tests/) - executable failure boundaries
- [Expert practicum](../learning-paths/expert-fde-practicum.md) - recovery and handover gates

## Further reading

- [Google SRE objectives](https://sre.google/sre-book/service-level-objectives/) - measurable objectives and operational expectations, checked 2026-10-09
