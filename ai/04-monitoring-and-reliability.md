# Monitoring and Reliability for LLM Systems

For engineers operating LLM systems in customer environments after launch. These systems
fail differently from the software you are used to: probabilistically. The service
reports healthy while producing wrong answers, so monitoring has to catch two failure
classes at once - the infrastructure failures every system has, and the quality drift
only LLM systems have. Employers price this skill: evaluation, testing, and monitoring
appear in 49.0% of FDE postings (146 postings scraped February-July 2026,
[independent job-scrape analysis](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md)).

## Tracing

The trace is the unit of debugging. Record every model call as a structured entry:

- Inputs and outputs - prompts, retrieved chunks, tool calls and results, generated text.
  Log metadata by default and capture content only behind the exceptions the customer's
  security review approved (see
  [security and compliance](../engineering/05-security-and-compliance.md))
- Identifiers - request ID, session ID, feature flag state, customer or tenant ID
- Cost and latency - tokens in and out, per-call cost, duration, and the model and
  prompt versions that served the call

OpenTelemetry provides the conventions: spans for retrieval, model call, and tool call,
parented under the request ([OpenTelemetry](https://opentelemetry.io)). Most teams export
traces into the observability stack already running at the customer rather than
introducing a new one (industry pattern). Agree on retention up front: traces holding
prompt content are sensitive data, so they may need shorter retention, restricted
access, or sampling that keeps full content for failures only.

For agents, traces are not optional: a
multi-step run is undebuggable without them, and the trace is the difference between
"the answer was wrong" and "step three misread the tool result"
([agents and tools](02-agents-and-tools.md),
[debugging methodology](../troubleshooting/01-debugging-methodology.md)).

## Dashboards and alerting

Chart the metrics that answer "is the system working for its users":

- Reliability - error rate, latency percentiles (p50/p95/p99), dependency availability
- Cost and load - tokens and cost per request and per day, volume per feature
- Tool health - tool call failure rates and durations, queue depths for async flows
- Provider health - upstream 429 and 5xx rates, quota consumption, and rejected-request
  counts, so a provider-side problem is visible before your users report it
- Quality proxies - the LLM-specific signals: refusal rates, empty outputs, schema
  validation failures, context-overflow rejections, judge scores on a sampled slice, and
  user feedback rates

`prometheus` for metrics and `grafana` for dashboards are the common stack in customer
environments ([prometheus.io](https://prometheus.io), [grafana.com](https://grafana.com)).

Alert on user-visible symptoms, not internal noise - the SRE practice of paging on
symptoms rather than causes
([Google SRE](https://sre.google)). A page for "p95 over budget for ten minutes" or
"refusal rate tripled hour over hour"; a ticket, not a page, for a single failed call.
Every alert links to a runbook, because in a customer environment the responder may be
their engineer, who knows neither your system nor your vocabulary.

## Quality drift

Drift is the normal state of an LLM system, not the exception. The sources:

- Provider model updates - the served model changes under you
- Corpus staleness - indexed documents age away from reality, resurfacing as confident
  wrong answers (the freshness problem from
  [data pipelines](../engineering/03-data-pipelines.md))
- Input mix changes - seasonal traffic, a new region, a new product line: the
  distribution your evaluation set described no longer matches production
- Upstream schema changes - a renamed field or new format flowing through quietly

Defenses, in the order we recommend building them:

1. Scheduled evaluation runs - replay the golden set against production-like conditions
   on a schedule (weekly is common); a score drop is the drift alarm
2. Distribution monitoring - chart input distributions (lengths, languages, categories)
   and output distributions (refusals, empty outputs), and alarm on sudden shifts
3. Upgrade discipline - treat a provider model upgrade like a dependency upgrade: run
   the evaluation set before accepting, roll back on regression
   ([evaluation and testing](03-evaluation-and-testing.md))

A typical shape: scores hold for a quarter, then answer quality dips on one customer
segment. Nothing in the error rate moved; the distribution did - a new product line
doubled the share of short, jargon-heavy tickets, and the prompt written for last
quarter's mix underperforms on them. The evaluation set alone would not have caught it,
because the set describes the old mix; the distribution monitor did. Both defenses exist
for exactly this case.

## Reliability patterns

- Fallbacks - a secondary model or a degraded-mode response when the primary fails or
  times out; the fallback's quality bar and cost are design decisions, not accidents
- Timeouts and budgets per stage - per-call timeouts, token budgets, and a per-request
  cost cap, so a runaway loop is bounded in dollars, not just in seconds
- Graceful degradation - a rule-based path when the model path fails: keyword routing
  instead of the classifier, cached answers instead of generation, a human queue instead
  of automation
- Kill switches per feature - a flag that turns off each model-backed feature without a
  deploy; tested before launch, not written during the incident
- Caching - exact-match caching for identical inputs and semantic caching for
  near-identical ones; both trade staleness and wrongness for cost. Cache only where
  correctness tolerates it, and evaluate a semantic cache like a model change, because a
  near-miss hit is a confident wrong answer

## Feedback loops

Monitoring tells you something drifted; feedback tells you what. Collect both kinds:

- Explicit - thumbs up and down, report buttons, correction forms. Low volume, high
  signal, biased toward strong feelings
- Implicit - edits to drafted text, abandonment mid-conversation, retry storms, override
  rates on suggestions. High volume and noisy, but the volume is the point: a rising
  retry rate is a quality incident in progress

Route failed and flagged cases into the evaluation set on a schedule, so the golden set
grows from production and stays honest
([evaluation and testing](03-evaluation-and-testing.md)). And settle ownership before
handover: who triages the feedback queue, who owns the evaluation set, who gets paged.
The handover artifacts in
[the engagement lifecycle](../customer/01-engagement-lifecycle.md) cover the runbook and
the tests, but the named owner has to exist in the customer's org chart, not just in the
runbook.

## Monitoring readiness checklist

- [ ] Every model call is traced with request ID, inputs, outputs, latency, cost, and versions
- [ ] A customer complaint can be traced end to end from request ID or session ID
- [ ] Dashboards show error rate, latency percentiles, token usage, and cost per day
- [ ] Quality proxies are charted: refusals, empty outputs, validation failures, sampled judge scores
- [ ] Alerts fire on user-visible symptoms, each with a linked runbook
- [ ] The golden evaluation set runs on a schedule against production-like conditions
- [ ] A provider model upgrade triggers a mandatory evaluation run before acceptance
- [ ] Each model-backed feature has a kill switch, tested before launch
- [ ] Fallback paths are exercised before launch, including the degraded-mode response
- [ ] Feedback events flow into a triage queue with a named owner after handover

This checklist aligns with the go/no-go gate in
[production readiness checklist](../deployment/03-production-readiness-checklist.md); run
it there before the customer goes live.

## Related documents

- [Evaluation and testing](03-evaluation-and-testing.md) - the golden set that powers drift detection and upgrade gates
- [Agents and tools](02-agents-and-tools.md) - traces as the debugging surface for agent runs
- [Debugging methodology](../troubleshooting/01-debugging-methodology.md) - what to do when an alert fires
- [Data pipelines](../engineering/03-data-pipelines.md) - the upstream changes that arrive as quality drift
- [The engagement lifecycle](../customer/01-engagement-lifecycle.md) - who owns monitoring, triage, and feedback after handover
- [Production readiness checklist](../deployment/03-production-readiness-checklist.md) - where the readiness gate sits in the launch decision

## Further reading

- [OpenTelemetry](https://opentelemetry.io) - tracing conventions for spans that you can extend for model, retrieval, and tool calls
- [Prometheus](https://prometheus.io) - metrics collection and alerting rules
- [Grafana](https://grafana.com) - dashboards over the metrics and traces above
- [Google SRE](https://sre.google) - the alert-on-symptoms and error-budget philosophy this section borrows
