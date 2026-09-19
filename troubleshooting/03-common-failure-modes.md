# Common Enterprise Failure Modes and Field Troubleshooting

This guide is an operational field catalog of the recurring failure modes that strike enterprise customer deployments, forward deployed engineering integrations, and on-call rotations. In customer environments, failures rarely present as clean stack traces; they manifest as silent data drops, intermittent latency spikes, quota exhaustion, and subtle model hallucinations.

For each failure mode, this catalog documents:
- **The Tell**: How the failure manifests in telemetry and user symptoms.
- **The Root Cause**: The underlying architectural mechanism.
- **The Immediate Containment**: How to stop customer bleeding within 15 minutes.
- **The Permanent Remediation (Prevention)**: The architectural invariant to eliminate the failure class permanently.
- **Runnable Implementation**: Direct cross-reference to production patterns in [`interviews/code/`](../interviews/code/).

---

## 1. Data and Pipeline Failures

---

### Failure 1.1: Silent UTF-8 BOM & Non-Standard Currency Corruption
- **The Tell**: Daily batch ingestion drops 3% of records without a fatal crash, or financial totals in downstream data warehouses disagree with the source ERP export.
- **The Root Cause**: Upstream legacy systems (e.g. SAP, on-premise Windows servers, or Excel exports) prepend a Byte Order Mark (`\xef\xbb\xbf`) to CSV exports and format monetary figures using European comma decimals (`€1.450,50`) or trailing currency codes (`"450.00 USD"`). Standard parsers silently truncate or choke on numeric conversions.
- **The Immediate Containment**: Deploy a hotfix parser that inspects byte prefixes for `\xef\xbb\xbf`, decodes with `utf-8-sig` fallback, and strips non-numeric characters using regex before float conversion.
- **The Permanent Remediation**: Implement an auditable `ParseReport` and defect ledger. Zero unhandled exceptions; every dropped or repaired row is recorded with exact line numbers and reasons.
- **Runnable Reference**: See [`interviews/code/parser.py`](../interviews/code/parser.py) and [`interviews/code/vibe_coding_runner.py`](../interviews/code/vibe_coding_runner.py).

---

### Failure 1.2: Upstream Schema Drift & Silent Field Dropping
- **The Tell**: Critical downstream models begin producing degraded outputs, or extraction confidence scores drop to zero overnight with zero deployments on your side.
- **The Root Cause**: A customer data engineering team renamed a column in their export (e.g. `customer_id` became `client_account_number`) or altered data types from integer to string without notifying integration partners.
- **The Immediate Containment**: Enable strict ingress schema validation that rejects modified batches into a dead-letter quarantine and alerts on-call operators, preventing corrupted data from entering vector stores or databases.
- **The Permanent Remediation**: Implement automated schema contract assertions on every scheduled batch run and establish row-count and null-percentage delta alarms in Datadog or CloudWatch.
- **Runnable Reference**: See [`interviews/code/structured_extractor.py`](../interviews/code/structured_extractor.py).

---

### Failure 1.3: Duplicate Ingestion & Non-Idempotent Replays
- **The Tell**: Total customer records jump 2x overnight; enterprise search assistants return identical duplicate documents with different chunk IDs.
- **The Root Cause**: A network timeout caused an ingestion cron job or webhook worker to retry a batch without an idempotency key or content hash deduplication.
- **The Immediate Containment**: Pause the ingestion pipeline. Run a deduplication query partitioning by `(customer_tenant_id, document_sha256_hash)` to delete duplicate records while keeping the earliest timestamped entry.
- **The Permanent Remediation**: Enforce SHA-256 payload fingerprinting and idempotency keys at the API gateway layer, caching execution records with a 24-hour TTL in Redis.
- **Runnable Reference**: See [`interviews/code/webhook_receiver.py`](../interviews/code/webhook_receiver.py).

---

### Failure 1.4: Stale Vector Index & Grounding Drift
- **The Tell**: The AI assistant quotes retired policies, superseded pricing tiers, or departed executives, despite documents having been updated in SharePoint or Confluence.
- **The Root Cause**: The vector database ingestion job stalled, silent permissions changes blocked the service account from crawling new folders, or embedding recalculation was skipped due to API cost limits.
- **The Immediate Containment**: Pin user sessions to strict dual-citation fallback mode. If a response relies on chunks older than the configured freshness window, route to a human specialist.
- **The Permanent Remediation**: Deploy an automated background freshness canary that runs hourly synthetic queries with known ground-truth dates, alerting when max source timestamp lag exceeds 24 hours.

---

## 2. Integration, Network, and Quota Failures

---

### Failure 2.1: Token Cache Expiry Thundering Herd (Top-of-Hour 504s)
- **The Tell**: Customer authentication endpoints experience sharp 50x request volume spikes and HTTP 504 Gateway Timeouts at minute `:00` of every hour, while remaining quiet at minute `:30`.
- **The Root Cause**: Hundreds of distributed worker pods cache OAuth / JWT bearer tokens with a fixed 3,600-second (60-minute) TTL without jitter. All tokens expire simultaneously at top-of-hour, unleashing a synchronized wave of re-authentication requests.
- **The Immediate Containment**: Increase the auth service instance count and connection pool limits temporarily to absorb the wave.
- **The Permanent Remediation**: Inject randomized uniform jitter into token cache lifetimes:  
  $$\text{TTL}_{\text{effective}} = \text{TTL}_{\text{base}} - \text{uniform}(300, 600) \text{ seconds}$$  
  This spreads token renewals uniformly across a 10-minute window, eliminating peak synchronization.
- **Runnable Reference**: See [`interviews/code/resilient_client.py`](../interviews/code/resilient_client.py).

---

### Failure 2.2: HTTP 429 Rate-Limit Thundering Herd Waves
- **The Tell**: Client calls to an upstream LLM API encounter HTTP 429 (Too Many Requests), followed by repeated waves of 429s every 10 seconds.
- **The Root Cause**: Distributed worker threads execute naive fixed-interval retry loops or standard exponential backoff without randomized jitter, causing retrying clients to hit the rate-limited gateway in lockstep waves.
- **The Immediate Containment**: Throttle client worker concurrency and configure client-side token-bucket rate limiters to cap outbound request rates below the upstream quota.
- **The Permanent Remediation**: Implement **Full Jitter Exponential Backoff** (Marc Brooker, AWS Architecture):  
  $$\text{Sleep} = \text{uniform}(0, \min(\text{MaxDelay}, \text{BaseDelay} \times 2^{\text{attempt}}))$$  
  Respect upstream `Retry-After` headers deterministically.
- **Runnable Reference**: See [`interviews/code/resilient_client.py`](../interviews/code/resilient_client.py) and [`interviews/code/rate_limiter.py`](../interviews/code/rate_limiter.py).

---

### Failure 2.3: Socket Timeouts & TCP Half-Close Application Hangs
- **The Tell**: Microservice worker threads hang indefinitely, exhausting thread pools and causing cascading outages without throwing an error.
- **The Root Cause**: Python `requests` or `urllib` calls executed without explicit timeout parameters (`requests.get(url)` defaults to `timeout=None`). When an upstream customer firewall or NAT gateway silently drops idle connections without sending TCP FIN/RST packets, the client socket waits indefinitely.
- **The Immediate Containment**: Restart hung worker pods.
- **The Permanent Remediation**: Enforce mandatory connection and read timeouts on every outbound HTTP client session:  
  `timeout=(3.05, 10.0)` (3.05s connect timeout, 10s read timeout) and enable TCP keep-alive probes at the OS layer.

---

### Failure 2.4: Pagination Cursor Truncation
- **The Tell**: Backfill jobs report successful completion, but downstream datasets contain only 50% of the expected historical records.
- **The Root Cause**: The integration code assumed a fixed page size limit or treated an opaque cursor string as a numeric offset, terminating pagination when an empty page was encountered instead of checking the `has_more` response flag.
- **The Immediate Containment**: Check source API documentation; query maximum primary key IDs to identify the exact truncation boundary.
- **The Permanent Remediation**: Write comprehensive boundary unit tests that mock multi-page API responses, validating that the pagination loop walks all pages until `has_more == False`.

---

## 3. Applied AI and Model Runtime Failures

---

### Failure 3.1: Context Window Truncation & "Lost in the Middle"
- **The Tell**: The RAG assistant accurately answers questions based on the first or last retrieved document chunk, but repeatedly misses critical policy clauses placed in the middle chunks.
- **The Root Cause**: LLM attention mechanisms exhibit positional bias ("Lost in the Middle" phenomenon), degrading recall for facts embedded in the center of multi-thousand-token context windows.
- **The Immediate Containment**: Reduce retrieved chunk count from $K=10$ to $K=4$, and apply a cross-encoder reranker (e.g. Cohere Rerank or BGE-Reranker) to place the highest-confidence chunk at position 1.
- **The Permanent Remediation**: Implement sentence-aware chunking with sliding overlap and document metadata lineage, ensuring chunks contain self-contained semantic assertions.
- **Runnable Reference**: See [`interviews/code/chunker.py`](../interviews/code/chunker.py).

---

### Failure 3.2: Format Regressions Post-Prompt Modification
- **The Tell**: An engineer modifies a system prompt to fix one customer edge case; hours later, structured output parsers experience a 15% spike in `JSONDecodeError` exceptions.
- **The Root Cause**: Ad-hoc prompt changes made under pressure introduce unmeasured regressions across other query distributions, causing the model to emit markdown wrappers (````json ... ````) or omit mandatory boolean fields.
- **The Immediate Containment**: Roll back the prompt modification immediately.
- **The Permanent Remediation**: Enforce a strict golden evaluation harness. No prompt edit is pushed to production without passing automated regression testing across at least 25 golden edge cases.
- **Runnable Reference**: See [`interviews/code/structured_extractor.py`](../interviews/code/structured_extractor.py) and [`portfolio/reference-project/evals/run_evals.py`](../portfolio/reference-project/evals/run_evals.py).

---

## 4. Production Diagnostic Command Cheat Sheet

When triaging production incidents inside customer networks with limited observability, execute these diagnostic commands:

### Network & Ingress Inspection
```bash
# Detailed HTTP connection timing breakdown (DNS, connect, TLS handshake, TTFB, total)
curl -w "DNS: %{time_namelookup}s | Connect: %{time_connect}s | TLS: %{time_appconnect}s | TTFB: %{time_starttransfer}s | Total: %{time_total}s\n" \
  -so /dev/null https://api.customer-estate.internal/v1/health

# Verify TLS certificate chain and expiry date on private endpoints
openssl s_client -connect api.customer-estate.internal:443 -servername api.customer-estate.internal < /dev/null 2>/dev/null | openssl x509 -noout -dates -subject

# Capture live TCP RST packets on eth0 to diagnose dropped connections
tcpdump -i eth0 'tcp[tcpflags] & (tcp-rst) != 0' -nn -c 20
```

### PostgreSQL Lock & Vector Index Inspection
```sql
-- Identify long-running queries holding locks on active customer tables
SELECT pid, now() - pg_stat_activity.query_start AS duration, query, state
FROM pg_stat_activity
WHERE state != 'idle' AND (now() - pg_stat_activity.query_start) > interval '5 seconds'
ORDER BY duration DESC;

-- Inspect pgvector index build progress
SELECT phase, round(blocks_done * 100.0 / nullif(blocks_total, 0), 2) AS pct_done, tuples_done
FROM pg_stat_progress_create_index;
```

### Structured Log Triage with `jq`
```bash
# Filter structured JSON logs for HTTP 5xx errors and extract correlation IDs
cat /var/log/fde-service.log | jq -r 'select(.status >= 500) | {timestamp, trace_id, error_code, customer_tenant_id, path}'

# Calculate error distribution by category over the last 1,000 log lines
tail -n 1000 /var/log/fde-service.log | jq -r '.defect_type // empty' | sort | uniq -c | sort -nr
```

---

## 5. Enterprise Blameless Post-Mortem Template

Every high-severity incident must produce an auditable post-mortem document within 24 hours. Use this standard template:

```markdown
# P0 Post-Mortem: Intermittent Ingestion Timeouts During Overnight Sync

## 1. Executive Summary
- **Incident Date**: 2026-04-12
- **Severity**: P0 (Production Customer Impact)
- **Duration**: 42 minutes (02:30 UTC to 03:12 UTC)
- **Customer Blast Radius**: 40 regional distribution centers; 14,200 invoices delayed by 45 minutes. Zero permanent data loss.

## 2. Root Cause Analysis (Five Whys)
1. **Why did the batch fail?** Downstream invoice workers hung and timed out after 30 seconds.
2. **Why did workers hang?** Outbound calls to the customer's legacy ERP authentication gateway returned HTTP 504 Gateway Timeouts.
3. **Why did the auth gateway time out?** The gateway experienced a 60x traffic spike at 02:30 UTC, exhausting thread pools.
4. **Why was there a 60x spike?** 200 distributed worker pods were scheduled to start simultaneously at 02:30 UTC, and all requested new OAuth tokens without jitter.
5. **Why was there no jitter?** The authentication client used fixed-delay retries without randomized exponential backoff.

## 3. Chronological Incident Timeline
- **02:30 UTC**: Scheduled cron triggers nightly batch of 14,200 invoices.
- **02:32 UTC**: First HTTP 504 alerts fire in Datadog (`auth_service_errors > 5%`).
- **02:40 UTC**: On-call FDE receives escalation page; confirms worker pool thread exhaustion.
- **02:48 UTC**: FDE applies immediate containment: throttles worker concurrency from 200 to 20 threads.
- **02:55 UTC**: Auth gateway recovers; invoices begin flowing at reduced rate.
- **03:05 UTC**: FDE deploys hotfix enabling client-side Full Jitter retry logic.
- **03:12 UTC**: Entire batch completes ingestion with 99.9% accuracy; incident resolved.

## 4. Permanent Remediation Actions (STAR+P Prevention)
- [x] **Client-Side Full Jitter**: Merged `ResilientCaller` with randomized full jitter to upstream auth client (`PR #142`).
- [x] **Token Cache Jitter**: Injected random $\pm 300\text{s}$ jitter to token cache expiration to prevent synchronized expiry.
- [x] **Ingress Automated Contract Tests**: Added automated schema assertion and row-count alert at ingress gateway.
- [x] **Runbook Update**: Authored operator runbook detailing step-by-step concurrency throttling during auth outages.
```

---

## Related Documents

- [Debugging Methodology](01-debugging-methodology.md) - the 7-step incident response process
- [Debugging in Customer Systems](02-debugging-customer-systems.md) - navigating opaque enterprise security perimeters
- [Coding Round Solutions](../interviews/08-coding-solutions.md) - runnable implementations of resilient clients and parsers
- [Customer Scenario Rounds](../interviews/04-customer-scenarios.md) - adversarial incident de-escalation playbooks

---

## References & Further Reading

1. **Marc Brooker**: [AWS Architecture Blog: Exponential Backoff And Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
2. **Nehal Vyas**: [Forward Deployed Engineer Interview Questions & Answers](https://fde.hinehal.com/blogs/fde-interview-questions)
3. **Dr. Sanjay Kumar PhD**: [Top 25 Forward Deployed Engineer (FDE) Interview Questions and Answers](https://skphd.medium.com/top-25-forward-deployed-engineer-fde-interview-questions-and-answers-ad9ac4a6ad7f)
4. **Om Bharatiya**: [AI Engineer Interview Questions: Forward Deployed Engineer Guide](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/15-role-guides/forward-deployed-engineer.md)
5. **Alexey Grigorev**: [AI Engineering Field Guide: FDE Responsibilities and Skills Analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)
