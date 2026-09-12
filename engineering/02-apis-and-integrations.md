# APIs and Integrations

This is for engineers building the integration layer of a customer deployment: the part of the system that talks to systems you do not own and cannot change. It covers reading API contracts, resilience patterns, enterprise auth, sync designs, and testing when the customer's staging is not available to you. Integration appears in 64.0% of FDE job postings (146 postings scraped February-July 2026, independent job-scrape analysis), second only to building production systems and direct customer work. The customer's systems are fixed; your code adapts.

## Reading the contract

### Working with APIs you do not own

Read the contract properly before writing the happy path. For every API you touch, extract:

- Authentication - scheme, token lifetimes, refresh behavior, and what happens when credentials expire mid-job
- Pagination - cursor or offset, and whether new records appearing mid-scan are included or skipped
- Rate limits - documented limits versus granted limits, per-key or per-IP, burst versus sustained
- Idempotency - whether a retried write is safe, and whether the API supports idempotency keys
- Error taxonomy - which errors are retryable, which are fatal, and which mean "stop and call a human"

Design for the error cases first. The happy path is the same everywhere; the differences between integrations live entirely in the failure paths. Before the first successful call, write down what your code does on timeout, 429, 500, malformed response, and auth expiry. Then assume the API fails on Fridays: transient failure happens at the worst operational moment, so failure behavior must be designed rather than discovered.

## Surviving their limits

### Resilience patterns

- Retries with exponential backoff and jitter - for transient failures: timeouts, connection resets, 5xx, and 429 responses carrying a `Retry-After` header. Cap the total retry time and never retry other 4xx errors; retrying a validation failure only multiplies noise. Jitter stops a thousand failed workers from retrying in lockstep and recreating the outage.
- Timeouts everywhere - set connect and read timeouts separately on every outbound call. A missing timeout is an unbounded hang waiting for a bad day. Pick values from the vendor's stated tail latency, not from optimism.
- Idempotency keys - for any write where money, inventory, or state is at stake. Generate one stable key per logical operation and reuse it on retries so the server can deduplicate. If the API has no key support, deduplicate on your side before writing.
- Circuit breakers - stop calling a dependency that is failing and fail fast while a probe tests recovery. Use when one slow downstream can exhaust your worker pool and take healthy features down with it.
- Bulkheads - isolate connection pools, threads, or queues per dependency so a hung integration consumes only its own resources. Use when one customer system is known to be flaky and must not starve the rest.
- Dead-letter queues - for asynchronous work: messages that fail processing repeatedly go to a queue you can inspect and replay instead of vanishing. Pair every queue with an alert and a written replay procedure, or it becomes a graveyard.

### Rate limits and quotas

Read the documented limits, then confirm the granted limits with the vendor or the customer's account team, because the two numbers frequently differ. Then:

- Throttle client-side - a token-bucket limiter in your client keeps your own traffic under the limit even in bursts; retries are not a substitute for pacing
- Apply backpressure - when the intake rate exceeds the allowed call rate, slow the intake or batch more aggressively rather than hammering the API and shipping 429s to your users
- Negotiate early - if the workload needs more than the granted quota, start the conversation in week 1 with both the vendor and the customer in the loop. Limit negotiation is a normal business conversation, not a hack, but it takes days to weeks, which is exactly why it belongs at the start

## Auth and sync

### Enterprise auth patterns

- API keys - still common for internal and legacy systems. Static, frequently shared, rarely rotated; treat any you receive as a secret with an expiry date in spirit.
- OAuth2 client credentials - the default for modern machine-to-machine access: a token endpoint, short-lived access tokens, scoped roles. Cache tokens; requesting a fresh token per call makes you your own rate-limit problem.
- mTLS - mutual certificate authentication, common in finance and on-premises environments. Certificate issuance and renewal are an operations project; ask who owns renewal before you build around it.
- Service accounts - cloud-native workload identity: IAM roles on AWS, service accounts on GCP, managed identities on Azure. Prefer these to long-lived keys wherever the platform supports them.
- Secrets managers - the customer's secrets manager or vault holds credentials, and your services fetch them at runtime using their workload identity.

The principle underneath all of it: your code reads secrets from configuration or a secret store at runtime and never contains them - not in source, not in git history, not in tickets, not in chat. Give each environment its own credentials so a development mistake cannot write to production. See [security and compliance](05-security-and-compliance.md) for what the customer's review will ask about all of this.

### Sync patterns

- Webhooks versus polling - webhooks give near-real-time updates with less wasted load, but they need an endpoint the vendor can reach, and delivery is best-effort, so you must reconcile missed events anyway. Most teams therefore run webhooks plus a periodic reconciliation poll. When firewall rules make inbound endpoints impossible, polling is the honest design; tune the interval against the rate limit, not against impatience.
- Batch versus streaming - decide on volume, latency requirement, and who operates what. A nightly file drop is simple, debuggable, and usually sufficient when hours of staleness are acceptable. Streaming or change data capture earns its operational cost when minutes matter. Weight the customer's ops maturity too: a streaming platform their team cannot operate becomes your on-call.
- Queue-backed processing - put a queue between ingestion and processing to absorb bursts, isolate slow consumers, and make retries explicit. This is the default shape for anything that consumes customer events at unpredictable rates.

## Boundaries and testing

### Contract safety

- Validate at the boundary - parse every external payload into a strict schema (`pydantic` is the common Python choice) and reject what does not match. Most integration bugs are schema surprises, and a rejection that logs the offending payload is worth an hour of debugging later. See the [pydantic documentation](https://pydantic.dev).
- Pin versions - where the vendor offers API versioning, pin the version you coded against, and pin your dependency versions. Vendor minor upgrades routinely rename or retype fields.
- Track deprecation windows - subscribe to the vendor changelog and put announced sunset dates into the engagement tracker, because nobody else will.
- Build an adapter layer - hide each external API behind your own interface so the rest of the code calls your `get_invoice` function, not vendor client calls. When the customer switches ERP or the vendor ships v2, you rewrite one module. The adapter is also what makes mocks and contract tests possible.

### Testing without their staging

The customer's test environment is not a promise. It may be stale, shared, rate-limited, or down exactly when you need it, and some enterprise vendors offer no sandbox at all. What works instead:

- Sandbox tenants - most SaaS vendors provide them; request access in week 1, not the day you need it
- Contract tests - assert that live vendor responses still match the schema you coded against, and run them on a schedule, so you learn about upstream changes from a test failure rather than from production
- Recorded mocks - capture real responses and replay them in unit tests; keep the recordings in the repository so a failure stays reproducible months later
- Feature flags per dependency - a flag that disables each integration at runtime, degrading the feature instead of the system, with no deploy required

## Pre-launch integration checklist

- [ ] Every outbound call has explicit connect and read timeouts
- [ ] Retries use exponential backoff with jitter and a total retry cap
- [ ] All writes are idempotent, through API keys or local deduplication
- [ ] Client-side rate limiting matches the granted quota, not the documented one
- [ ] Every external payload is validated against a schema at the boundary
- [ ] Secrets load from a secret store; nothing in code, logs, or tickets
- [ ] Environments use separate credentials with minimal production scope
- [ ] Each dependency's failures alert, with a runbook entry
- [ ] Contract tests run on a schedule against live vendor APIs
- [ ] A feature flag can disable each dependency without a deploy

## Related documents

- [Data pipelines](03-data-pipelines.md) - API pulls are one of the four ingestion patterns, with the same schema and rate-limit concerns
- [Security and compliance](05-security-and-compliance.md) - credentials handling and the customer review questions your integrations must answer
- [Debugging customer systems](../troubleshooting/02-debugging-customer-systems.md) - debugging when logs and context live on both sides of a trust boundary
- [Production readiness checklist](../deployment/03-production-readiness-checklist.md) - where integration hardening sits in the go/no-go review
- [Architecture for customer systems](../system-design/01-architecture-for-customer-systems.md) - designing a system around dependencies you do not control

## Further reading

- [pydantic documentation](https://pydantic.dev) - boundary validation models referenced throughout
- [Independent FDE job-scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md) - source of the 64.0% integration figure
