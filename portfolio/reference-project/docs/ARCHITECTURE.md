# ETISE architecture and threat boundaries

This architecture describes the code present on 2026-10-09. It is a local deterministic reference with process-local state. Proposed production controls are requirements, not implemented guarantees.

## Request path

FastAPI validates a ticket, parses simulated roles, expires cached entries, and checks the account/key/role replay scope under an in-process lock. A conflicting payload returns 409; a full replay cache returns 503. The engine classifies with keyword rules and feature-hash similarity, retrieves sample policies, checks exact quotations, and returns a routing decision.

Missing evidence or low heuristic confidence routes to human review. P0 incidents escalate. The response is a local draft; no downstream dispatch or business mutation occurs. Queued review items, feedback, metrics, and cached results are lost on restart.

## Implemented controls and limits

| Boundary | Present behavior | Remaining production requirement |
|---|---|---|
| Input | Pydantic field limits and action enums | Ingress byte, concurrency, queue, retention, and resource budgets |
| Replay | Payload digest, scoped key, monotonic TTL, bounded cache | Durable uniqueness and transactional downstream effects |
| Concurrent requests | Process-local serialized state | Shared storage and concurrency across workers and hosts |
| Retrieval | Simulated role intersection | Authenticated principal, object-level policy, revocation |
| Grounding | Exact quote and cited-section membership | Approved source version, relevance, legal authority |
| Review | In-memory queue and feedback records | Authorized operator, tenant scoping, durable append-only audit |
| Monitoring | Health and counters | Structured telemetry, privacy filtering, alerts, SLO measurements |

## Identity and data boundaries

The API accepts account IDs and role headers from callers. These are not verified identity claims. An omitted role header defaults to `support_tier1`, but a caller can declare `admin`; queue and resolution endpoints lack tenant authorization. The sample API secret setting does not authenticate requests.

The process-local replay scope prevents one declared account or role context from accidentally receiving another cached result. It does not prove tenant isolation, authenticate an account, or stop unauthorized queue access. Run locally and do not expose this service to untrusted traffic.

## Source and model boundaries

The corpus consists of authored Apex examples, not authenticated regulatory or provider policies. The classifier does not call an LLM or repair model output. Its feature-hash scores and fixed confidence constants are not calibrated probabilities.

Exact quotation membership prevents accepting text absent from the cited sample section. It does not ensure that the quote answers the question or that a claim is legally correct. Approved document versions and relevance evaluation are prerequisites for a real customer deployment.

## Failure handling and recovery

The single process lock simplifies concurrent reference behavior while limiting throughput. Expiry permits a key to execute again; replay state is not durable. A restart clears all local state. No Redis, database, outbox, model-provider fallback, automatic index rebuild, or backup restore exists.

Production review must demonstrate authenticated tenant boundaries, durable state recovery, resource bounds, independent quality validation, and an operator-owned rollback path before accepting live traffic.

## Related documents

- [Project README](../README.md) - setup and behavior
- [Operating runbook](SLA_RUNBOOK.md) - available commands and recovery limits
- [Expert practicum](../../../learning-paths/expert-fde-practicum.md) - required evidence gates

## Further reading

- [OWASP 2026 source](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/tree/9253e38ade58e959b531c0c5c9a4842272c9cd0e/2026/final) - risk guidance, checked 2026-10-09
