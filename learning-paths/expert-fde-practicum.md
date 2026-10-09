# Expert FDE practicum: evidence, failure boundaries, and handover

This path is for experienced engineers who already ship APIs and need to demonstrate staff or principal judgment across customer deployments. It defines reviewable work products and rejection criteria, rather than promising expertise after a fixed number of weeks. Source observations were checked on 2026-10-09; the exercises and promotion criteria are recommendations.

## Start with two evidence-backed workstreams

The first workstream is a market observatory using the [source-pinned listing snapshot](../job-market/dataset/market_snapshot_2026-10-09.json). Its current cumulative filter finds 212 IDs, but its monthly ID union finds 237. September has 127 matching rows and 91 unique IDs. Explaining those differences is a stronger engineering exercise than copying the old 146-role headline.

The second workstream is a ticket intake reference using [today's five CFPB categorical records](../portfolio/reference-project/evals/real_data/cfpb_metadata_2026-10-09.json) for schema and lineage exercises, alongside ETISE for local failure-boundary tests. The CFPB records have no ETISE severity or routing labels and no retained narratives. They cannot establish classifier quality. The old 25-case set remains regression data with unverified origins.

Keep externally observed records separate from authored adversarial test inputs. Tests may deliberately create malformed requests to exercise contracts; those inputs are not a real-world dataset or a source of production accuracy estimates. Bitext is excluded from this path's real-world evidence because its publisher describes a hybrid synthetic generation method.

## Gate 1: define the decision before choosing a model

Inputs: a customer-approved workflow, an operator, constraints, and existing outcome measurements. Public datasets can teach engineering mechanics; they cannot supply a customer's business baseline.

Produce a one-page decision brief that names the user action, the counterfactual, the cost of a false positive and false negative, the review capacity, and the economic buyer. Separate measured facts from proposed targets. If the task is deterministic title filtering or metadata normalization, use deterministic code.

Acceptance: a reviewer can identify the decision your software changes and reproduce the baseline measurement. Reject invented ticket volumes, fines, ROI, or stakeholder quotes. If you cannot obtain a baseline, the next deliverable is instrumentation rather than an improvement claim.

## Gate 2: make data lineage executable

Inputs: source permissions, collection timestamps, stable record IDs, and versioned transformations.

For the observatory, reproduce the pinned source and compare its output:

```bash
python job-market/dataset/refresh_market_snapshot.py \
  --upstream-dir /tmp/ai-engineering-field-guide \
  --commit ed590319553252e2b8275486597b144ac55a4f3c \
  --retrieved-on 2026-10-09 --output /tmp/market-reproduction.json
python job-market/dataset/validate_market_snapshot.py \
  --upstream-dir /tmp/ai-engineering-field-guide
python research/validate_evidence.py
```

Obtain the source checkout using the instructions in the [dataset runbook](../job-market/dataset/README.md). The repository under development stays in its existing isolated task checkout; no Git worktree is needed.

Produce a data card recording what was actually observed, what was excluded, rights and privacy limits, and how source revisions change downstream results. Preserve both duplicate rows and unique-ID accounting. Record the 25 source-only IDs instead of silently imputing or deleting them. Compare the original title rule with the 220-match alternative before calling any difference market growth.

Acceptance: every published number traces to a source revision and a transformation. Offline accounting and live source authentication must be distinguished. Reject a refresh that overwrites collection dates with today's verification date or promotes inferred fields into raw observations.

## Gate 3: establish labels and holdout discipline

Inputs: an authorized, representative real customer dataset with an agreed label specification. This prerequisite is not supplied by the repository's metadata samples.

Separate development, regression, and untouched evaluation sets by customer, incident, document family, or time as appropriate. Review near-duplicate leakage before splitting. Record annotator disagreements, adjudication, exclusions, and missing ground truth. Freeze the evaluation set before model or threshold selection.

Produce a baseline comparison with per-class precision and recall, abstention coverage, risk-weighted errors, and slice sample counts. Show how performance changes on changed policy versions, new customer segments, and unseen input formats. A calibrated probability must be checked against outcomes; cosine similarity and hand-written confidence constants are not probabilities.

Acceptance: the reviewer can rerun the baseline, identify inspected records, and see every failure case. Reusing an inspected holdout turns it into regression data. Descriptive Wilson intervals on 25 known examples do not justify deployment inference. A zero-citation run must say that grounding was not evaluated.

## Gate 4: test authority and mutation boundaries

Inputs: a threat model, an authenticated identity provider, customer-approved role mappings, and a list of reversible and irreversible operations.

Treat retrieved text and model output as untrusted data. An instruction inside a ticket or policy document cannot grant a role, change a tenant, approve a refund, or authorize a tool call. Validate tool arguments and check object-level permissions immediately before executing a mutation. Use explicit human approval for actions whose impact requires it under the customer's policy.

Produce a boundary-test matrix covering cross-account reads, role changes, revoked permissions, conflicting replay payloads, concurrent requests, and corrupted citations. Include attempts to inject instructions through retrieved documents. Run the local reference tests:

```bash
python -m pytest portfolio/reference-project/tests/ -v
```

Acceptance: each protected operation has an authenticated principal and an authorization decision tied to the affected object. ETISE's caller-supplied role simulation does not satisfy this gate; its current tests establish local filtering and replay semantics only. Document the remaining gap rather than call it multi-tenant security.

## Gate 5: make recovery more precise than the happy path

Inputs: durable state, retention policy, queue ownership, and the customer's acceptable loss and recovery windows.

Record what happens if a process crashes between intake, side effect, and acknowledgement. Use durable uniqueness and an appropriate transaction or outbox boundary when a real downstream mutation exists. Specify retryable failures, poison-record handling, replay permissions, and what a restored system can safely resend. Do not promise exactly-once effects across an uncontrolled network.

Produce failure drills for expiration, duplicate delivery, downstream timeouts after a successful mutation, unavailable storage, and restored queues. ETISE currently serializes an in-process reference and loses state on restart; it does not provide distributed locks, durable jobs, or an immutable audit ledger.

Acceptance: an operator other than the author completes a restore and replay drill from a tested runbook. Reject a runbook containing nonexistent endpoints, fallback switches, rebuild commands, or recovery guarantees that were not exercised.

## Gate 6: measure latency and economics under a stated workload

Inputs: actual arrival distributions, concurrency, payload sizes, token usage when a model exists, and current provider or infrastructure prices.

Measure the full request path separately from engine CPU time. Include queue wait, retries, timeouts, retrieval, model inference, and human review. Report p50/p95/p99, throughput, error rates, and the workload that generated them. A global process lock may be correct for a teaching service while limiting throughput; measure before choosing distributed infrastructure.

Produce a unit-economics model using observed billable usage and price effective dates. Add reviewer time, storage, egress, failed attempts, and operational labor. Separate measured costs from scenario assumptions. Compare deterministic code, a simpler model, and a more capable model on the same approved task and untouched evaluation set.

Acceptance: costs and latency reproduce under the declared load and satisfy customer-approved targets. Reject extrapolating the reference's sub-millisecond CPU timing to production HTTP latency or multiplying an illustrative volume into claimed savings.

## Gate 7: turn a customer deployment into a reusable product boundary

Inputs: at least one documented deployment constraint and a named owner for the shared primitive.

Separate customer configuration, domain policy, connector behavior, and reusable platform code. Keep policy revisions explicit and reviewable. Record which exceptions remain bespoke and why. State the migration and deprecation behavior for customers on an older contract or data schema.

Produce an architecture decision record with alternatives, negative consequences, falsification conditions, ownership, and a release contract. A generic framework is only justified when repeated requirements exist; one deployment is not evidence of a universal platform need.

Acceptance: another engineer can deploy or extend the seam without relying on private conversations with the author. Reject invented adoption figures or claims that an example design was implemented for a named enterprise.

## Gate 8: hand over evidence and a bounded go-live decision

Inputs: completed checks, unresolved risks, an operator, and an accountable customer decision-maker.

Deliver source and release manifests, an evaluation report with failures, an authorization matrix, tested operating and rollback procedures, monitoring ownership, and a residual-risk record. Separate proposed SLOs from measured service indicators and contractual SLAs. Record waivers with owners and expiry dates; passing a checklist does not manufacture compliance.

Acceptance: the customer operator demonstrates recovery, explains the metrics and alerts, and knows which decisions require escalation. The expert signal is an independently usable system with honest limits, not the number of tools or acronyms in its README.

## Related documents

- [Repository audit](../AUDIT.md) - current evidence gaps and corrected defects
- [Production readiness](../deployment/03-production-readiness-checklist.md) - deployment review topics
- [Trade-offs and decisions](../system-design/03-trade-offs-and-decision-records.md) - decision record structure
- [Dataset provenance](../portfolio/reference-project/evals/DATASET_PROVENANCE.md) - real-data admission contract

## Further reading

- [Upstream extraction audit](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/ed590319553252e2b8275486597b144ac55a4f3c/job-market/_internal/eval/README.md) - evaluator drift and reuse limits, checked 2026-10-09
- [OWASP 2026 source](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/tree/9253e38ade58e959b531c0c5c9a4842272c9cd0e/2026/final) - current threat guidance, release identified from the official README on 2026-10-09
- [Google SRE objectives](https://sre.google/sre-book/service-level-objectives/) - measurement and objective selection, checked 2026-10-09
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) - risk governance and framework/profile dates, checked 2026-10-09
