# ETISE local operations and recovery runbook

This runbook covers the development service reviewed on 2026-10-09. There is no measured production SLA, paging integration, model provider, database, backup, or durable queue. The commands below describe available behavior; proposed production operations belong in a separately accepted runbook.

## Start and verify

From `/workspace/FDE-Field-Guide/portfolio/reference-project` in the prepared cloud environment:

```bash
../../.venv/bin/python -m uvicorn src.api.server:app --host 127.0.0.1 --port 8000
```

Keep one worker and the execution session alive. Do not expose the unauthenticated reference to untrusted traffic.

In another terminal:

```bash
curl --fail --silent --show-error http://127.0.0.1:8000/health
curl --fail --silent --show-error 'http://127.0.0.1:8000/api/v1/knowledge/search?q=Section%203.1%20critical%20outage'
curl --fail --silent --show-error http://127.0.0.1:8000/metrics
```

Require `status: healthy`, an indexed corpus, and a relevant returned sample-policy result. These requests do not demonstrate production availability or legal source authenticity.

For authored smoke inputs and assertions, run from the repository root:

```bash
.venv/bin/python -m pytest portfolio/reference-project/tests/test_server.py -v
.venv/bin/python portfolio/reference-project/evals/run_evals.py --report /tmp/etise-regression.json
```

The API tests process tickets, exercise local review and resolution, and reject conflicts and invalid inputs. Adversarial test requests are code-contract inputs, not real-world dataset records. The regression report is known-case evidence rather than customer accuracy.

## Diagnose available failure responses

- Startup import error: confirm the working directory and `src.api.server:app` target. Use the project's environment and pinned dependency constraints.
- HTTP 422: inspect the validation response for a blank ID, oversized field, invalid action, or malformed payload. Preserve the original source record separately; do not silently relabel missing data.
- HTTP 400 on role simulation: check the declared role spelling. Only the listed reference roles are accepted; this does not authenticate the caller.
- HTTP 409 on replay: a key was reused with different ticket content within the same declared account/role scope. Correct the upstream key contract instead of blindly retrying altered payloads.
- HTTP 503 from replay-cache capacity: the local cache reached its bounded entry count. Inspect workload and expiry; do not increase limits without evaluating resource use. Queues and other state still lack production retention bounds.
- Human review result: inspect confidence, evidence, and permissions. No retrieved evidence must not be bypassed by claiming a higher confidence score.

## Stop, restart, and state-loss behavior

Stop the foreground service you started with Ctrl-C, inspect its exit, then rerun the startup command. Check health and functional requests again. Do not stop another user's process to free a port.

A restart discards replay records, queued review items, feedback, and counters. There is no restore command. Do not use this service as the authoritative record for customer work. Increasing worker count creates independent state and breaks the single-process replay assumption.

There is no `/api/v1/admin/mode`, `SYSTEM_MODE=FALLBACK_BYPASS`, automatic PagerDuty integration, or `src.pipeline.ingestion --rebuild` command. The previous runbook instructions claiming them are withdrawn.

## Requirements before a real operational handover

A production owner must demonstrate authenticated tenant access, authorized reviews, durable audit and queue storage, resource/retention limits, telemetry privacy, workload-based service indicators, and a restore/replay drill. Define customer-approved objectives and rollback routing in the actual deployment environment. Do not substitute a checklist or local regression timing for these measurements.

## Related documents

- [Project README](../README.md) - setup and boundaries
- [Architecture](ARCHITECTURE.md) - process-local state and threat model
- [Expert practicum](../../../learning-paths/expert-fde-practicum.md) - operational acceptance gates

## Further reading

- [Google SRE objectives](https://sre.google/sre-book/service-level-objectives/) - service measurement principles, checked 2026-10-09
