# Forward Deployed Engineering Field Guide

A field guide to discovering customer problems, building integrations, evaluating AI systems, and handing software over to operators. It combines learning material with runnable Python exercises, a local ticket intake reference, and dated source-derived data. Begin with the path that matches the work you need to demonstrate.

Evidence and implementation review: 2026-10-09. See the [audit](AUDIT.md) for confirmed defects, source limits, and the distinction between existing capabilities and production requirements.

## Choose a starting point

- New to the role: [what an FDE does](role/01-what-is-an-fde.md), then the [beginner path](learning-paths/beginner-to-fde.md).
- Already shipping software: use the [expert practicum](learning-paths/expert-fde-practicum.md) to demonstrate source lineage, holdout discipline, authority boundaries, recovery, economics, and handover.
- Preparing for interviews: start with the [interview guide](interviews/README.md) and [runnable exercises](interviews/code/). Practice rubrics are not authenticated company transcripts.
- Checking market claims: read the [market methodology](job-market/dataset/README.md) before using counts or salary reports.
- Developing the reference: follow the [ETISE README](portfolio/reference-project/README.md), including its missing production controls.

## Data you can trace

The [market snapshot retrieved on 2026-10-09](job-market/dataset/market_snapshot_2026-10-09.json) records immutable upstream revisions, input SHA-256 hashes, source-record references, and nine observation dates through 2026-09-23. Its cumulative title filter matches 212 job IDs across 125 employer names. September has 127 matching listing rows and 91 unique matching IDs. The monthly-file union differs from the cumulative source; the discrepancy is preserved rather than hidden.

The [CFPB metadata sample](portfolio/reference-project/evals/real_data/cfpb_metadata_2026-10-09.json) contains five actual complaint records received on 2026-10-09 and retrieved from the official API. It retains categorical metadata without narratives or locations. It is an ingestion and lineage sample, with no invented ETISE quality labels.

The [source-check ledger](research/source_checks_2026-10-09.json) records selected primary and publisher sources accessed today, including failed retrievals and claim-specific limits. Verification dates are separate from source publication and collection dates. Neither data collection is a worldwide census, an independently adjudicated customer benchmark, or evidence that every cited vacancy remains open.

The earlier [market summary](job-market/dataset/fde_market_data.json) is historical aggregate material, not 146 raw postings. Percentages quoted from that sample cannot be applied to the new sample. ETISE's 25 existing cases are explicitly marked as regression fixtures with unverified origins. Bitext is excluded from real-world-only evidence because its publisher describes it as hybrid synthetic. See the [provenance contract](portfolio/reference-project/evals/DATASET_PROVENANCE.md).

## Read the guide by topic

- [Role](role/README.md) - responsibilities and title boundaries
- [Skills](skills/README.md) - technical and customer-facing competencies
- [Engineering](engineering/README.md) - prototypes, APIs, pipelines, infrastructure, and security
- [Customer work](customer/README.md) - discovery, scope, constraints, and expectations
- [AI engineering](ai/README.md) - application patterns, tools, evaluation, and monitoring
- [Deployment](deployment/README.md) - promotion and readiness reviews
- [System design](system-design/README.md) - constrained architecture and decisions
- [Troubleshooting](troubleshooting/README.md) - diagnosis and incident response
- [Case studies](case-studies/README.md) - sourced material and clearly identified design exercises
- [Job market](job-market/README.md) - dated observations and interpretation limits
- [Learning paths](learning-paths/README.md) - background-specific routes and expert work products
- [Interviews](interviews/README.md) - preparation, rubrics, and code
- [Portfolio](portfolio/README.md) - project selection and evidence presentation
- [Resources](resources/README.md) - further tools, literature, and communities

Existing chapters contain historical claims and recommendations; the audit is not a certification of every external citation. Check evidence status before treating an illustrative scenario, code excerpt, or proposed deployment pattern as an implemented customer outcome.

## Install and verify

Use Linux and Python 3.12 for the dependency resolution verified in this review. From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r portfolio/reference-project/requirements.txt \
  -c portfolio/reference-project/requirements.lock
python -m pip check
python -m pytest interviews/code/ portfolio/reference-project/tests/ job-market/dataset/tests/ -v
python portfolio/reference-project/evals/run_evals.py --report /tmp/etise-regression.json
python portfolio/reference-project/evals/curate_eval_dataset.py
python interviews/dataset/validate_dataset.py
python interviews/dataset/ten_pass_verification.py
python job-market/dataset/validate_market_data.py
python job-market/dataset/validate_market_snapshot.py
python research/validate_evidence.py
```

The Python suite tests failure boundaries including payload conflicts, replay scopes, expiry, concurrent requests, exact quotation checks, empty evidence, retry delay, and chunk budgets. The regression report gates routing and required document retrieval as well as classification. It is a known-case regression check, with engine-only latency rather than production SLA measurement.

The interview and historical-market validators check structure and arithmetic. They do not authenticate interviews, company rubrics, source licenses, or a published salary claim. For full market reproduction against the pinned upstream objects, follow the [dataset runbook](job-market/dataset/README.md).

## Reference service boundary

ETISE uses deterministic rules, feature hashing, sample policies, and in-memory state. It does not call an LLM, implement BM25, authenticate a tenant, persist an audit log, or dispatch a response to a customer. Its role header is a local simulation. Run it locally with one worker; do not expose it to untrusted traffic.

Production use requires independently labeled customer data, authenticated authority, durable state, resource and retention budgets, operational telemetry, recovery drills, and an accountable handover. The expert practicum makes those gates explicit rather than claiming this repository has already crossed them.

## Contribute with evidence

Read [STYLING.md](STYLING.md). Change a claim only when the supporting artifact or implementation needs to change. Preserve historical observation dates, pin source revisions where available, report disagreements and failed checks, and distinguish observations from recommendations. Do not introduce invented datasets, production outcomes, quotes, or company-specific interview records.

## Related documents

- [Expert practicum](learning-paths/expert-fde-practicum.md) - experienced-engineer acceptance gates
- [Audit](AUDIT.md) - repository findings and remaining production work
- [Work in progress](_work-in-progress/README.md) - unresolved evidence and implementation gaps

## Further reading

- [AI Engineering Field Guide](https://github.com/alexeygrigorev/ai-engineering-field-guide/tree/ed590319553252e2b8275486597b144ac55a4f3c) - inspiration and source data, retrieved 2026-10-09
- [CFPB complaint catalog](https://www.consumerfinance.gov/data-research/consumer-complaints/) - original data and interpretation notices, checked 2026-10-09
