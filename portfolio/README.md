# Portfolio evidence and reference project

Build a portfolio a reviewer can reproduce and challenge. Reviewed 2026-10-09. Senior engineering evidence comes from explicit constraints, measured failures, source lineage, and working recovery procedures; a larger feature list does not demonstrate production experience.

## Choose and present a project

- [What to build](01-what-to-build.md) - choose a workflow and measurable acceptance criteria
- [Project ideas](02-project-ideas.md) - proposed specifications, not completed customer engagements
- [Presenting projects](03-presenting-projects.md) - explain the decision, evidence, and limits
- [Project selection](04-project-selection-masterclass.md) - architecture options; verify dataset permissions and access before committing to a domain
- [Expert practicum](../learning-paths/expert-practicum.md) - source admission, independent evaluation, authenticated authority, recovery, economics, and handover

## Executable reference

[ETISE](reference-project/README.md) is a local deterministic FastAPI teaching service. It demonstrates typed intake, feature-hash and token-overlap retrieval, exact sample-policy quote checks, bounded replay caching, and human review. It does not call an LLM, implement BM25 or reciprocal rank fusion, authenticate role headers, persist queues, or isolate tenants.

- [API](reference-project/src/api/server.py) and [tests](reference-project/tests/test_server.py) - payload conflicts, role/account cache context, expiry, and local concurrent replay
- [Retrieval](reference-project/src/pipeline/ingestion.py) - locally authored policy corpus and exact section quote checks
- [Regression evaluation](reference-project/evals/run_evals.py) - routing, required documents, nonempty citations, per-class metrics, and failure reports
- [Data provenance](reference-project/DATASET_PROVENANCE.md) - legacy fixtures with unverified origins; Bitext excluded from real-only evidence
- [Runbook](reference-project/docs/SLA_RUNBOOK.md) - supported startup, investigation, and restart procedures

## Real-world data

The [market snapshot](../job-market/dataset/README.md) preserves 212 cumulative matching job IDs and the discrepancy with 237 monthly-union IDs. Its underlying observations end September 23. The [CFPB metadata sample](reference-project/evals/real_data/cfpb_metadata_2026-10-09.json) contains five actual records received October 9, without narratives or invented ETISE labels. These are different populations and cannot be combined into a model-quality score.

## Related documents

- [Audit](../AUDIT.md) - why previous production and provenance claims were unsupported
- [Specification](../customer/02-requirements-to-spec.md) - turn observed behavior into reviewable requirements
- [Learning paths](../learning-paths/README.md) - background-specific preparation

## Further reading

- [CFPB complaint database](https://www.consumerfinance.gov/data-research/consumer-complaints/) - official data and interpretation limits
- [OpenAI Evals](https://github.com/openai/evals) - evaluation tooling and contributions
