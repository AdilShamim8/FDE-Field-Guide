# Operations Runbook and SLA Disaster Recovery

This runbook outlines operational procedures, telemetry alerts, troubleshooting workflows, and emergency disaster recovery protocols for the Enterprise Ticket Intelligence and Grounded Synthesis Engine (ETISE).

## System SLOs and SLA thresholds

- Availability: 99.9% uptime for the REST ingestion API (`GET /health`, `POST /api/v1/tickets/process`).
- Latency: p95 latency under 1,200ms; p99 latency under 2,000ms.
- Accuracy floor: 88% precision on ticket classification; 100% citation grounding (zero ungrounded claims in customer drafts).
- Review queue lag: tickets routed to the exception queue must not wait more than 30 minutes for operator review during business hours.

## Telemetry and alerting rules

All alerts page the primary on-call engineer via PagerDuty or enterprise incident management.

### Alert 1: High 5xx Error Rate (P0 Severity)

- Trigger condition: HTTP 5xx responses exceed 1.0% of total requests over a rolling 5-minute window.
- Probable cause: Upstream model API outage, Redis connection pool exhaustion, or database lock contention.
- Triage steps:
  1. Check endpoint health via `curl -f http://localhost:8000/health`.
  2. Inspect container logs for connection timeouts or authentication errors.
  3. If upstream provider is down, activate the automated fallback kill-switch (`SYSTEM_MODE=FALLBACK_BYPASS`).

### Alert 2: Model Grounding Canary Failure (P1 Severity)

- Trigger condition: Synthetic golden evaluation canary fails citation validation on 2 consecutive 5-minute runs.
- Probable cause: Upstream model prompt drift, knowledge base index corruption, or context truncation.
- Triage steps:
  1. Inspect the canary trace to compare the generated quotation against the indexed source chunk.
  2. If retrieval index is corrupted, trigger an index rebuild: `python -m src.pipeline.ingestion --rebuild`.
  3. Force strict refusal mode (`STRICT_GROUNDING_REFUSAL=TRUE`) to prevent ungrounded outputs from reaching operators.

### Alert 3: Exception Queue Depth Spike (P2 Severity)

- Trigger condition: Number of pending tickets in the human exception queue exceeds 150 items.
- Probable cause: Sudden burst of ambiguous tickets, low model confidence scores, or supervisor staffing shortage.
- Triage steps:
  1. Inspect the distribution of low-confidence scores across incoming tickets.
  2. Notify support team shift leads to allocate temporary secondary reviewers.

## Emergency rollback and kill-switch procedures

If the automated triage service causes workflow disruption, execute the appropriate containment protocol below:

### Level 1: Switch to shadow mode (soft bypass)

The service continues ingesting tickets and logging predictions for observability, but stops publishing automated suggestions to the operator UI.

Command:

`curl -X POST http://localhost:8000/api/v1/admin/mode -H "Authorization: Bearer $ADMIN_TOKEN" -d '{"mode": "SHADOW"}'`

Result: All tickets pass directly through to standard human queues without suggestions. Zero user impact.

### Level 2: Complete service bypass (hard kill-switch)

Traffic is routed completely around the ETISE service at the reverse proxy or API gateway level.

Command:

Update NGINX or AWS ALB target group to route traffic directly to the legacy Zendesk or ServiceNow webhook endpoint.

## Incident postmortem checklist

Following any P0 or P1 incident, the on-call FDE must complete the postmortem process within 48 hours:

- [ ] Capture the immutable trace ID and full request payload for the failing transaction
- [ ] Add the failure scenario to the regression test suite (`tests/`)
- [ ] Add the query and expected output to the golden dataset (`evals/golden_dataset.json`)
- [ ] Deliver a written one-page incident report to customer operations leadership

## Related documents

- [Project README](../README.md) - system overview and quickstart
- [Architecture and threat model](ARCHITECTURE.md) - system components and boundaries
- [Statement of work](SOW.md) - engagement SLAs and milestone commitments
- [Debugging customer systems](../../troubleshooting/02-debugging-customer-systems.md) - field guide to troubleshooting in client estates

## Further reading

- [Google SRE Book: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/) - principles of error budgets and alert design
- [The Datadog Guide to Monitoring LLM Systems](https://www.datadoghq.com/) - production observability for probabilistic systems
