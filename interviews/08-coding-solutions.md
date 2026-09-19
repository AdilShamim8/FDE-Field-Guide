# Coding Round Solutions and Narration Playbooks

This file is the companion implementation guide to the [coding and technical preparation guide](02-coding-and-technical.md). It provides production-grade reference solutions to recurring FDE practical technical exercises, the verbatim verbal narration scripts high-scoring candidates use in shared live coding environments, edge case inventories, and full runnable test suites.

All solutions reflect what top-tier Forward Deployed Engineers demonstrate in live assessment loops: defensive input validation, explicit failure boundaries, zero unhandled exceptions, and runnable, tested code over quick hacks.

Runnable test suites for all implementations are located in [`interviews/code/`](code/). You can run the entire test suite locally:

```bash
python -m pytest interviews/code/ -v
```

---

## 1. Parse the Malformed Customer Export

> [!NOTE]
> **Verified Source**: [Nehal Vyas](https://fde.hinehal.com/blogs/fde-interview-questions) | **Dataset ID**: `FDE-TECH-001`  
> **Runnable Implementation**: [`interviews/code/parser.py`](code/parser.py) | **Test Suite**: [`interviews/code/test_parser.py`](code/test_parser.py)

### The Problem Context

A customer exports daily billing data from a legacy on-premise ERP. The export contains mixed character encodings (UTF-8, UTF-8 with BOM, CP1252), missing primary keys, duplicate records, non-standard timestamp strings, and dirty currency figures (e.g., `"$1,240.50"` or `" 450.00 USD "`). The pipeline must ingest the file without crashing, sanitize valid records, and produce an auditable defect ledger.

### What Interviewers Listen For

- **Clarifying error budget upfront**: Asking whether malformed records should halt execution or be logged into an auditable defect ledger.
- **Encoding hygiene**: Checking for byte order marks (BOM `\xef\xbb\xbf`) and trying standard fallback encodings before falling back to lossy decoding.
- **Defect accounting**: Returning a structured `ParseReport` detailing total input rows, valid rows, repaired rows, dropped rows, and line-by-line defect reasons.

### Reference Implementation

Core architecture from [`interviews/code/parser.py`](code/parser.py):

```python
import csv
import io
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

@dataclass
class ParseReport:
    total_raw_records: int = 0
    valid_records: int = 0
    repaired_records: int = 0
    dropped_records: int = 0
    defect_counts: Dict[str, int] = field(default_factory=dict)
    dropped_reasons: List[Dict[str, Any]] = field(default_factory=list)

    def record_defect(self, defect_type: str) -> None:
        self.defect_counts[defect_type] = self.defect_counts.get(defect_type, 0) + 1

def decode_bytes_safely(raw_bytes: bytes) -> Tuple[str, str]:
    if raw_bytes.startswith(b"\xef\xbb\xbf"):
        return raw_bytes.decode("utf-8-sig"), "utf-8-sig"
    encodings = ["utf-8", "cp1252", "latin-1"]
    for enc in encodings:
        try:
            return raw_bytes.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return raw_bytes.decode("latin-1", errors="replace"), "latin-1-lossy"
```

### Verbal Narration Script

**Before typing**:
> "Before writing the parser, I want to clarify our failure policy. In an enterprise ingestion pipeline, dropping customer records silently is unacceptable, but failing the entire batch for one malformed row halts downstream business operations. I will build an extraction pipeline that sanitizes dirty strings and yields valid records while producing an auditable `ParseReport` with exact line numbers and defect categories for every dropped record. Does that match our operational requirements?"

**During coding**:
> "Notice that I inspect byte prefixes for the UTF-8 BOM first before iterating through UTF-8 and CP1252. For monetary figures, I strip currency symbols, commas, and trailing currency codes using regex before parsing to float. If a primary key is missing or duplicated within the batch, we log the defect and quarantine that specific row, allowing the remaining clean records to flow through."

---

## 2. Design an Idempotent Webhook Receiver

> [!NOTE]
> **Verified Source**: [Om Bharatiya](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/15-role-guides/forward-deployed-engineer.md) & [Nehal Vyas](https://fde.hinehal.com/blogs/fde-interview-questions) | **Dataset ID**: `FDE-TECH-002`  
> **Runnable Implementation**: [`interviews/code/webhook_receiver.py`](code/webhook_receiver.py) | **Test Suite**: [`interviews/code/test_webhook_receiver.py`](code/test_webhook_receiver.py)

### The Problem Context

A third-party payment or CRM provider retries webhook events on network timeout. Because distributed networks exhibit at-least-once delivery semantics, identical webhook events arrive multiple times or out of order. Naive execution causes duplicate billing or corrupted database states.

### What Interviewers Listen For

- **Delivery semantics clarity**: Explaining why at-least-once delivery necessitates stateful deduplication.
- **Payload collision verification**: Detecting when a client reuses an idempotency key with different payload contents (returning HTTP 409 Conflict).
- **Concurrency control**: Handling simultaneous in-flight webhook deliveries with a `PENDING` state lock to avoid race conditions.

### Reference Implementation

Core architecture from [`interviews/code/webhook_receiver.py`](code/webhook_receiver.py):

```python
import hashlib
import json
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, Optional, Tuple

class ProcessingState(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

@dataclass
class ExecutionRecord:
    state: ProcessingState
    payload_hash: str
    result: Optional[Any]
    created_at: float
    updated_at: float

class IdempotentWebhookReceiver:
    def __init__(self, ttl_seconds: int = 86400):
        self.ttl_seconds = ttl_seconds
        self._store: Dict[str, ExecutionRecord] = {}

    def _hash_payload(self, payload: Dict[str, Any]) -> str:
        serialized = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
```

### Verbal Narration Script

**Before typing**:
> "Network deliveries are inherently at-least-once, so our receiver must be statefully idempotent. I am structuring our handler around an idempotency key and a three-state machine: `PENDING`, `COMPLETED`, and `FAILED` with SHA-256 payload fingerprinting."

**During coding**:
> "When a request arrives, we check if the idempotency key exists. If it exists but the SHA-256 hash of the payload differs, someone is erroneously reusing a key for a different event, so we reject with HTTP 409 Conflict. If the record is currently `PENDING`, a concurrent delivery is actively executing, so we return 409 to prevent duplicate processing. If it is `COMPLETED`, we return HTTP 200 with the cached output. If the handler fails, we mark it `FAILED` so that future retries can re-attempt."

---

## 3. Exponential Backoff with Full Jitter

> [!NOTE]
> **Verified Source**: [Alexey Grigorev](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md) & [Marc Brooker (AWS)](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)  
> **Runnable Implementation**: [`interviews/code/resilient_client.py`](code/resilient_client.py) | **Test Suite**: [`interviews/code/test_resilient_client.py`](code/test_resilient_client.py)

### The Problem Context

A client calling downstream partner APIs or LLM inference endpoints encounters transient HTTP 429 (Too Many Requests) or HTTP 503 (Service Unavailable). Naive fixed retries cause synchronized retry waves (thundering herd), repeatedly saturating the upstream service.

### What Interviewers Listen For

- **Understanding Full Jitter**: Citing Marc Brooker's empirical proof that uniform random sleep between 0 and exponential ceiling minimizes total completion time and eliminates cluster synchronization.
- **Testability through dependency injection**: Injecting sleep and random functions so unit tests execute in milliseconds without real-world delays.
- **Error classification**: Distinguishing retryable status codes (429, 502, 503, 504) from fatal errors (400 Bad Request, 401 Unauthorized, 403 Forbidden).

### Reference Implementation

Core architecture from [`interviews/code/resilient_client.py`](code/resilient_client.py):

```python
import random
from typing import Any, Callable, Optional, Tuple

class ResilientCaller:
    def __init__(
        self,
        base_delay_sec: float = 0.5,
        max_delay_sec: float = 30.0,
        max_retries: int = 4,
        sleep_func: Optional[Callable[[float], None]] = None,
        random_func: Optional[Callable[[float, float], float]] = None,
    ):
        self.base_delay_sec = base_delay_sec
        self.max_delay_sec = max_delay_sec
        self.max_retries = max_retries
        self.sleep_func = sleep_func or (lambda d: None)
        self.random_func = random_func or random.uniform

    def _calculate_sleep_duration(self, attempt: int) -> float:
        ceiling = min(self.max_delay_sec, self.base_delay_sec * (2 ** attempt))
        return self.random_func(0, ceiling)
```

### Verbal Narration Script

> "Standard exponential backoff spaces out retries, but if hundreds of workers hit a rate limit at the same instant, fixed backoff causes them to retry in lockstep waves. I am implementing Full Jitter, where the sleep duration is drawn uniformly from `[0, min(max_delay, base * 2^attempt)]`. This breaks synchronization. I am also injecting the sleep callable so our unit tests run instantly in CI without sleeping."

---

## 4. Self-Healing Structured Field Extraction

> [!NOTE]
> **Verified Source**: [Om Bharatiya](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/15-role-guides/forward-deployed-engineer.md) & [Dr. Sundeep Teki](https://www.sundeepteki.org/advice/the-definitive-guide-to-forward-deployed-engineer-interviews-in-2026) | **Dataset ID**: `FDE-TECH-003`  
> **Runnable Implementation**: [`interviews/code/structured_extractor.py`](code/structured_extractor.py) | **Test Suite**: [`interviews/code/test_structured_extractor.py`](code/test_structured_extractor.py)

### The Problem Context

An LLM extracts structured incident records from unstructured customer Slack messages and support emails. LLMs occasionally produce malformed JSON, violate schema enums, or omit mandatory fields. The system must capture schema errors and execute a feedback-driven auto-correction loop before failing.

### What Interviewers Listen For

- **Comprehensive schema validation**: Collecting all validation errors across all fields rather than aborting at the first failure.
- **Feedback-driven repair loop**: Formatting exact schema validation errors into a follow-up prompt so the model corrects its specific mistake.
- **Honoring model refusal**: Respecting when the model signals that the input text legitimately lacks required information, rather than hallucinating fields.

### Reference Implementation

Core architecture from [`interviews/code/structured_extractor.py`](code/structured_extractor.py):

```python
import json
from typing import Any, Callable, Dict, List, Optional, Tuple

def extract_with_repair_loop(
    raw_incident_text: str,
    llm_mock_caller: Callable[[str, Optional[List[str]]], str],
    max_repair_attempts: int = 2,
) -> Tuple[Optional[IncidentRecord], List[str]]:
    feedback_errors: Optional[List[str]] = None
    all_trace_errors: List[str] = []

    for attempt in range(max_repair_attempts + 1):
        raw_response = llm_mock_caller(raw_incident_text, feedback_errors)

        if "CANNOT_EXTRACT_INSUFFICIENT_INFORMATION" in raw_response:
            return None, ["Model declined: insufficient information in incident text"]

        try:
            parsed_json = json.loads(raw_response)
        except json.JSONDecodeError as jde:
            feedback_errors = [f"JSONDecodeError: {str(jde)}. You must output valid JSON only."]
            all_trace_errors.extend(feedback_errors)
            continue
```

### Verbal Narration Script

> "A common flaw in AI engineering is expecting 100% schema compliance on the first zero-shot call. When validation fails, discarding the payload is wasteful. Instead, we collect all Pydantic or schema errors, format them into a structured correction prompt, and give the model up to two repair turns. If the source text genuinely lacks required incident data, we preserve explicit refusal semantics to prevent hallucinations."

---

## 5. Multi-Tenant Sliding Window Rate Limiter

> [!NOTE]
> **Verified Source**: [YagyanshB Google FDE Guide](https://github.com/YagyanshB/google-fde-interview-guide) & [Dr. Sundeep Teki](https://www.sundeepteki.org/advice/the-definitive-guide-to-forward-deployed-engineer-interviews-in-2026)  
> **Runnable Implementation**: [`interviews/code/rate_limiter.py`](code/rate_limiter.py) | **Test Suite**: [`interviews/code/test_rate_limiter.py`](code/test_rate_limiter.py)

### The Problem Context

An enterprise integration gateway serves thousands of customer tenants with differing tiers (`free`: 10 req/min, `standard`: 60 req/min, `enterprise`: 300 req/min). Fixed-window counters allow double-limit bursts across window boundaries (e.g., 60 requests at 00:59 and 60 requests at 01:00 = 120 requests in 2 seconds). The gateway requires a sliding window counter algorithm.

### What Interviewers Listen For

- **Defending sliding window vs. fixed window**: Demonstrating why boundary bursts overwhelm downstream services.
- **Accurate `Retry-After` calculation**: Calculating the precise time until the oldest request falls out of the sliding window.
- **Tenant isolation**: Ensuring that noisy free-tier tenants cannot starve enterprise tenant quota.

### Reference Implementation

Core architecture from [`interviews/code/rate_limiter.py`](code/rate_limiter.py):

```python
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

@dataclass
class RateLimitStatus:
    allowed: bool
    limit: int
    remaining: int
    reset_after_sec: float
    retry_after_sec: Optional[float] = None

class SlidingWindowRateLimiter:
    def __init__(self, window_sec: float = 60.0, tier_limits: Optional[Dict[str, int]] = None, time_func=None):
        self.window_sec = window_sec
        self.tier_limits = tier_limits or {"free": 10, "standard": 60, "enterprise": 300}
        self.time_func = time_func or time.time
        self._history: Dict[str, List[Tuple[float, int]]] = {}
```

### Verbal Narration Script

> "Fixed-window counters are vulnerable to boundary bursts: a client can exhaust their quota in the final second of minute one and fire another batch in the first second of minute two. I am implementing a sliding window rate limiter that records timestamped request weights. When a request arrives, we prune entries older than `now - window_sec` and calculate total weight. If over quota, we determine exactly when enough prior requests expire to allow the current request and return that duration in the `Retry-After` header."

---

## 6. Token-Aware Document Chunker with Metadata Lineage

> [!NOTE]
> **Verified Source**: [Dr. Sanjay Kumar PhD](https://skphd.medium.com/top-25-forward-deployed-engineer-fde-interview-questions-and-answers-ad9ac4a6ad7f) & [Alexey Grigorev](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)  
> **Runnable Implementation**: [`interviews/code/chunker.py`](code/chunker.py) | **Test Suite**: [`interviews/code/test_chunker.py`](code/test_chunker.py)

### The Problem Context

In enterprise RAG ingestion pipelines, documents must be partitioned into chunks adhering to model context limits while preserving sentence integrity, sliding overlap, and parent document metadata (document ID, section heading, author, chunk index). Naive character slicing splits words and breaks semantic coherence.

### What Interviewers Listen For

- **Sentence boundary preservation**: Splitting text along sentence boundaries rather than cutting arbitrarily mid-token.
- **Sliding overlap**: Maintaining sentence overlap between chunks so multi-sentence context is preserved during vector similarity search.
- **Metadata lineage**: Injecting document IDs, chunk sequence indices, and total chunk counts into every emitted chunk.

### Reference Implementation

Core architecture from [`interviews/code/chunker.py`](code/chunker.py):

```python
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class TextChunk:
    chunk_id: str
    content: str
    token_count: int
    chunk_index: int
    total_chunks: int
    metadata: Dict[str, Any] = field(default_factory=dict)
```

### Verbal Narration Script

> "Naive character-based chunking truncates words and fractures embedding vectors. I am building a sentence-aware chunker that accumulates complete sentences until approaching the token budget, then seeds the next chunk with the trailing sentences to establish sliding overlap. Every chunk carries parent document metadata and sequential indices so downstream citation verification remains deterministic."

---

## 7. Google FDE "Vibe Coding" 60-Minute Rapid Build Playbook

> [!NOTE]
> **Verified Source**: [YagyanshB Google FDE Guide](https://github.com/YagyanshB/google-fde-interview-guide) & [Nehal Vyas](https://fde.hinehal.com/blogs/fde-interview-questions)  
> **Runnable Implementation**: [`interviews/code/vibe_coding_runner.py`](code/vibe_coding_runner.py) | **Test Suite**: [`interviews/code/test_vibe_coding_runner.py`](code/test_vibe_coding_runner.py)

In Google and top AI lab Forward Deployed Engineer technical interviews, candidates often face an intensive 60-minute practical build round (sometimes referred to as the "Vibe Coding" or practical integration exercise). Rather than abstract algorithmic puzzles, the candidate is given a messy enterprise scenario with customer data, a rate-limited external service, and dirty records, and must deliver a fully functional, defensively coded, and tested integration pipeline before the clock expires.

### Tactical 60-Minute Timebox Schedule

```
+-------------------------------------------------------------------------------+
|                      60-MINUTE RAPID BUILD TIMEBOX                            |
+-------------------+-----------------------------------------------------------+
| 00:00 - 00:10 (10m)| Clarify & Lock Contract (Schema, Failure Policy, Tolerances)|
| 00:10 - 00:25 (15m)| Core Pipeline & Defensive Sanitization (Encoding, Amounts)|
| 00:25 - 00:35 (10m)| Flow Control & Rate-Limiting (Token Bucket / Sliding Window)|
| 00:35 - 00:45 (10m)| Defect Accounting & Error Isolation (Auditable Run Ledger)|
| 00:45 - 00:55 (10m)| Live Verification & Edge Case Battery (Pytest Suite)        |
| 00:55 - 01:00 (05m)| Hand-off Narration, Trade-offs & Production Observability   |
+-------------------+-----------------------------------------------------------+
```

### Core Architecture (`vibe_coding_runner.py`)

The runner demonstrates four enterprise-grade architectural patterns:
1. **Defensive Normalization**: Cleanses dirty currency strings (`"$1,450.50 USD"` -> `1450.50`) and parses non-standard timestamps (`ISO8601`, `YYYY/MM/DD`, `DD-MM-YYYY`).
2. **Client-Side Rate-Limiting**: In-memory Token Bucket algorithm enforcing strict throughput caps (`max_rate_per_sec`) with burst tolerances.
3. **Defect Ledger**: Auditable metrics (`total_ingested`, `processed_count`, `repaired_count`, `rejected_count`, `rate_limited_count`) with structured failure reasons.
4. **Idempotent Output**: Deterministic records ready for downstream data warehouses or vector stores.

### Live Narration Script (Minute-by-Minute)

#### Minute 00–10: Clarify & Lock Contract
> "Before writing code, let me establish our operational invariants. We have messy customer transaction streams. In enterprise environments, three failure modes ruin integrations:
> 1. Silent data drops (where unparseable records disappear without audit logs).
> 2. Gateway saturation (where our pipeline overwhelms the customer's downstream API).
> 3. Pipeline halting (where a single bad row crashes an entire batch).
> 
> I will design `VibeCodingPipeline` with defensive sanitization, token-bucket backpressure, and an auditable `PipelineRunLedger`. If a record has repairable defects (like currency symbols or slash timestamps), we repair and increment `repaired_count`. If it lacks mandatory identity or is fundamentally corrupted, we quarantine it in the ledger and proceed. Does this match your expectations?"

#### Minute 10–25: Core Pipeline & Sanitization
> "I am now implementing `_sanitize_amount` and `_parse_timestamp`. Notice that I use regular expressions to strip non-numeric characters while preserving decimals. For timestamps, I iterate through ISO-8601, slash, and dash formats. If none match, I raise a classified `ValueError` so our ledger can categorize the defect."

#### Minute 25–35: Flow Control & Rate-Limiting
> "To prevent saturating the customer's downstream API, I am embedding a Token Bucket rate-limiter directly into the runner. We track available tokens and refill them proportionally based on elapsed time. If tokens are exhausted, the pipeline returns a `RATE_LIMITED` quarantine status rather than blocking indefinitely or crashing."

#### Minute 35–45: Defect Ledger & Run Accounting
> "Now I am wiring the processing loop. Notice that every execution path yields a structured `ProcessedRecord` or appends to `defects`. At the end of the batch, the ledger provides complete accounting: `total_ingested == processed_count + rejected_count + rate_limited_count`. Nothing is lost."

#### Minute 45–55: Live Verification & Testing
> "Now let us write and run our unit tests. I will verify four scenarios:
> 1. Clean records flow through smoothly.
> 2. Dirty amounts and timestamps are repaired and tracked.
> 3. Missing IDs and unparseable figures are cleanly quarantined without halting.
> 4. Bursts exceeding quota trigger rate-limiting backpressure.
> Let's execute `pytest interviews/code/test_vibe_coding_runner.py`."

#### Minute 55–60: Production Hand-off & Observability
> "In a production deployment, I would replace the in-memory token bucket with a Redis sliding window counter for distributed workers, export the defect counts as Prometheus counters (`fde_pipeline_defects_total{type="..."}`), and route quarantined records to a Dead Letter Queue (DLQ) for customer review."

---

## 8. Live Debugging: Find the Bug in the Failing Trace

> [!NOTE]
> **Verified Source**: [Nehal Vyas](https://fde.hinehal.com/blogs/fde-interview-questions) & [Om Bharatiya](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/15-role-guides/forward-deployed-engineer.md) | **Dataset ID**: `FDE-DEBUG-001`

### The Problem Context

A distributed trace reveals intermittent HTTP 504 Gateway Timeouts between a message queue consumer and an upstream customer authentication service. Failures occur in sharp spikes at minute 00 of every hour.

### Hypothesis Ranking Tree

Senior candidates state a prioritized hypothesis tree before diving into log lines:

1. **Hypothesis 1 (Token Cache Herd)**: An OAuth/JWT token cache with a 60-minute TTL expires simultaneously across all distributed consumer pods at top-of-hour, unleashing a thundering herd of re-authentication calls to the auth service.
2. **Hypothesis 2 (Scheduled Cron CPU Starvation)**: An hourly cron job (such as audit log archiving or database vacuuming) executes on the auth database at minute 00, exhausting CPU or connection pools.
3. **Hypothesis 3 (Upstream Batch Sync)**: An external customer CRM runs an hourly sync, overwhelming the ingress gateway with batch traffic.

### The Discriminating Tests

- **Auth service request volume**: If request count spikes 50x at `:00`, it confirms a thundering herd / token cache expiry. **Fix**: Add random jitter to token cache TTL (`ttl = 3600 + uniform(-300, 300)`).
- **Auth service CPU / DB locks**: If request count is constant but database latency spikes, it confirms a background cron/maintenance lock. **Fix**: Reschedule vacuuming to off-peak hours or throttle worker concurrency.

---

## 9. Security, PII Leak, and Memory Code Review

> [!NOTE]
> **Verified Source**: [YagyanshB Google FDE Guide](https://github.com/YagyanshB/google-fde-interview-guide) & [Nehal Vyas](https://fde.hinehal.com/blogs/fde-interview-questions)

### The Problem Context

You are reviewing an integration pull request from a customer-facing engineer that connects an on-premise document store to an LLM inference endpoint.

### Vulnerability Checklist

- **Secret exposure**: Checking for hardcoded API keys, bearer tokens, or database credentials committed to source code or git history.
- **PII leakage in observability logs**: Inspecting logger statements for raw customer prompts containing SSNs, passwords, or credit card numbers emitted to unencrypted cloud logging buckets.
- **Unbounded memory consumption**: Identifying `f.read()` calls loading multi-gigabyte customer files into memory rather than streaming chunks.
- **SSRF (Server-Side Request Forgery)**: Verifying that user-supplied webhook URLs or document endpoints validate against private IP ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.169.254`).

---

## Related Documents

- [Coding and Technical Rounds](02-coding-and-technical.md) - round structure and evaluation criteria
- [Runnable Test Suites](code/) - complete pytest implementations
- [System Design Rounds](03-system-design.md) - architectural design under enterprise customer constraints
- [Question Bank](07-question-bank.md) - round-by-round interview question directory
- [Market Overview](../job-market/01-market-overview.md) - empirical job market analysis and compensation benchmarks

---

## References & Further Reading

1. **YagyanshB**: [Google Forward Deployed Engineering Interview Prep Guide](https://github.com/YagyanshB/google-fde-interview-guide)
2. **Nehal Vyas**: [Forward Deployed Engineer Interview Questions & Answers](https://fde.hinehal.com/blogs/fde-interview-questions)
3. **Om Bharatiya**: [AI Engineer Interview Questions: Forward Deployed Engineer Guide](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/15-role-guides/forward-deployed-engineer.md)
4. **Dr. Sundeep Teki**: [The Definitive Guide to Forward Deployed Engineer Interviews in 2026](https://www.sundeepteki.org/advice/the-definitive-guide-to-forward-deployed-engineer-interviews-in-2026)
5. **Dr. Sanjay Kumar PhD**: [Top 25 Forward Deployed Engineer (FDE) Interview Questions and Answers](https://skphd.medium.com/top-25-forward-deployed-engineer-fde-interview-questions-and-answers-ad9ac4a6ad7f)
6. **Alexey Grigorev**: [AI Engineering Field Guide: FDE Responsibilities and Skills Analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)
7. **Marc Brooker**: [AWS Architecture Blog: Exponential Backoff And Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
