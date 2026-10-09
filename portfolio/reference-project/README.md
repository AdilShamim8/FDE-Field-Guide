# ETISE: deterministic ticket intake reference

ETISE is a local teaching application for ticket classification, sample-policy retrieval, and operator review. The implementation and data claims were audited on 2026-10-09. It is a development reference, with explicit production gaps rather than a claimed customer deployment.

## Implemented behavior

- FastAPI intake with bounded ticket fields and Pydantic validation.
- Keyword classification with feature-hashed cosine similarity for fallback scoring. Confidence values are uncalibrated heuristics.
- Retrieval using token overlap and feature-hash vectors over locally authored Apex policies. This is not BM25, a trained embedding model, or a vector database.
- Exact quotation membership checks against the cited sample section. Strict mode routes missing evidence to review; P0 incidents escalate even without evidence.
- In-process replay handling scoped to account, key, and simulated role, with payload conflict detection, TTL, a bounded cache, and serialized state changes.
- In-memory exception review, operator resolutions, feedback records, and counters.

`AUTOMATED_DISPATCH` is a returned routing label. The service does not send replies, charge money, mutate a customer's ticketing platform, call an LLM, or run an extraction repair loop.

## Data and evidence status

The [five CFPB metadata records](evals/real_data/cfpb_metadata_2026-10-09.json) were returned by the official API and received on 2026-10-09. They contain categorical fields for ingestion and lineage exercises, with no narratives or ETISE ground-truth labels.

The historical `golden_dataset.json` filename refers to 25 known regression fixtures with unverified origins. The Apex policies are sample text. Passing those cases demonstrates regression behavior; it does not authenticate consumer records, provider contracts, legal compliance, or production accuracy. See [dataset provenance](evals/DATASET_PROVENANCE.md).

## Local setup

From the repository root, use Linux and Python 3.12 for the verified dependency resolution:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r portfolio/reference-project/requirements.txt \
  -c portfolio/reference-project/requirements.lock
python -m pip check
```

Application defaults suffice for local development. A project-local `.env` is optional and is read when the project is the working directory. Keep credentials out of Git. The sample API secret setting is not used to authenticate requests; changing it does not secure the service.

## Tests and regression evaluation

From the repository root:

```bash
python -m pytest interviews/code/ portfolio/reference-project/tests/ job-market/dataset/tests/ -v
python portfolio/reference-project/evals/curate_eval_dataset.py
python portfolio/reference-project/evals/run_evals.py --report /tmp/etise-regression.json
python research/validate_evidence.py
```

The evaluation gates category and severity accuracy, exact expected routing, required document retrieval, independently rechecked quotes, and empty automated dispatches. Reports include per-class metrics, failure cases, and local engine CPU timing. This timing excludes HTTP, queueing, external inference, and operator review.

## Start and check the API

From the project directory:

```bash
cd portfolio/reference-project
../../.venv/bin/python -m uvicorn src.api.server:app --host 127.0.0.1 --port 8000
```

In another terminal, check `/health`, process a sample ticket, and inspect `/metrics`. The automated API tests include functional billing triage, replay conflicts, account and simulated-role scopes, expiry, concurrent delivery, review resolution, and knowledge filtering. Use the [runbook](docs/SLA_RUNBOOK.md) for concrete requests.

The Dockerfile and Compose file are optional packaging examples. Their builds have not been validated by this audit. A container does not add the missing controls below.

## Production boundary

Do not expose this service to untrusted traffic. It has no authenticated tenant identity, operator authorization, durable queue or audit storage, distributed lock, telemetry redaction, ingress byte ceiling, retention enforcement, model-quality holdout, or measured availability objective. Ticket field limits do not bound every incoming request resource or persistent queue.

`X-User-Roles` is a caller-supplied role simulation. Omitting it defaults to `support_tier1`; a caller can still supply `admin`. Account IDs are request data, not authenticated tenant identity. The queues and feedback endpoint behavior are not tenant-isolated. Restarting loses all in-memory state, and multiple workers create independent state stores.

Use one local worker. The process lock intentionally serializes this small CPU-only example; it is not a distributed transaction or exactly-once guarantee. A real deployment must address these boundaries and complete the [expert practicum](../../learning-paths/expert-fde-practicum.md).

## Related documents

- [Architecture and threat model](docs/ARCHITECTURE.md) - actual boundaries and required controls
- [Decision record](docs/ADR-001.md) - retrieval trade-offs and known limitations
- [Pilot scope template](docs/SOW.md) - proposed deliverables, not a real engagement
- [Operations runbook](docs/SLA_RUNBOOK.md) - tested local operating procedures

## Further reading

- [CFPB data catalog](https://www.consumerfinance.gov/data-research/consumer-complaints/) - source interpretation notices, checked 2026-10-09
- [OWASP 2026 guidance](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/tree/9253e38ade58e959b531c0c5c9a4842272c9cd0e/2026/final) - threat guidance; reference controls still require implementation and review
