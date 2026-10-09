# Evaluation evidence and dataset provenance

This document separates source-derived observations from test fixtures. Reviewed on 2026-10-09 using the [source-check ledger](../../../research/source_checks_2026-10-09.json). A schema pass, citation substring match, or reachable dataset homepage cannot prove that a test case came from that dataset.

## Actual real-world observations

[CFPB metadata snapshot](real_data/cfpb_metadata_2026-10-09.json) contains five categorical complaint records returned by the official API, with source `date_received` timestamps on 2026-10-09. It retains complaint IDs, product and issue categories, public company names, response status, request URL, and a SHA-256 digest of the captured response.

The sample excludes complaint narratives, consumer identifiers, ZIP, state, and tags. Its purpose is to exercise ingestion, schema validation, and lineage. The five most recent results are not a random or representative population sample. Public complaint assertions are not independently adjudicated findings about the companies named.

No ETISE severity, routing, response correctness, or policy labels have been assigned to these records. They must not be silently converted into support tickets with invented expected outputs. The live endpoint can change; the committed categorical projection is the preserved artifact, while the original response hash records the capture. The full response is not redistributed.

The [market snapshot](../../../job-market/dataset/market_snapshot_2026-10-09.json) is another source-derived artifact, with immutable upstream Git revisions, input hashes, source-record references, and explicit source discrepancies. It describes job-listing observations, not customer triage quality.

## Legacy regression fixtures

`golden_dataset.json` is a historical filename retained for compatibility. All 25 cases are now labeled `unverified_legacy_fixture` and `regression`. They contain authored-looking Apex tickets and expected decisions. Their individual source records, raw text hashes, source revisions, curation transformations, annotation records, and reuse permissions are absent from this repository.

The former provenance document claimed CFPB complaint-ID mappings, Bitext intent IDs, and expert annotation. Those claims cannot be reproduced by `curate_eval_dataset.py`: it contains a field counter and a limited regex masker, not an acquisition or annotation pipeline. Those mappings are withdrawn from authenticated evidence. This audit does not establish whether every originally claimed record exists; it establishes that the claimed transformations are not evidenced here.

Use these fixtures to prevent behavioral regressions. Do not describe 25/25 known-case results as real-customer accuracy, independent validation, a zero-hallucination guarantee, or a production SLA. The TC-006 expected routing was deliberately changed to review when the classifier's artificial confidence floor was removed; it is a regression expectation, not a new human-adjudicated label.

## Bitext source correction

The [publisher's dataset card](https://huggingface.co/datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset) was retrieved on 2026-10-09. It explicitly describes a hybrid synthetic dataset generated through NLP/NLG technology and automated labeling. It lists 26,872 question/answer pairs and a `cdla-sharing-1.0` license field.

The earlier assertions that these were observed enterprise customer interactions and licensed under CC BY 4.0 were incorrect. This dataset is excluded from the guide's real-world-only evidence set. A public dataset's availability does not establish the right to redistribute it under this repository's MIT license.

## Apex sample policies

`src/pipeline/ingestion.py` contains locally authored Apex policy examples with simulated access roles. No acquisition artifacts show that these paragraphs are verbatim AWS, Stripe, Datadog, or European regulatory text. Those documents must not be cited as the source of these exact clauses, response times, refund terms, regional codes, or contract obligations.

The current exact quote check verifies membership in a local sample document and its cited section. It does not verify legal authority, factual correctness, retrieval relevance, completeness, or authorization. Production policies require approved customer documents with version IDs, effective dates, ownership, retention rules, and an access-control source.

## Requirements for accepting a real benchmark

We recommend admitting a record only after the following artifacts exist:

1. A stable source identifier, publication and collection dates, immutable revision or capture digest, and a source URL.
2. Dataset-specific terms or permission, intended use, privacy assessment, and redaction decisions. Regex masking alone is not anonymization.
3. A versioned transformation from source to evaluation input, retaining the parent record ID and explaining every removed or altered field.
4. A label specification and annotator/adjudication record. Unavailable ground truth stays unavailable.
5. A split by customer, document, incident, or time that prevents near-duplicate leakage. Tuned or previously inspected records are regression data.
6. Per-slice results, sample counts, uncertainty, retrieval requirements, abstention behavior, and explicit failure cases.

This is the admission contract for future evaluation data; it is not a claim that the legacy fixtures satisfy it.

## Run the existing checks

From the repository root:

```bash
python portfolio/reference-project/evals/curate_eval_dataset.py
python portfolio/reference-project/evals/run_evals.py --report /tmp/etise-regression.json
python -m pytest portfolio/reference-project/tests/ -v
```

The first command reports structure and evidence status. The regression runner gates routing, required document retrieval, exact quotations, and empty automated dispatches. It reports per-class metrics and local engine timing. Its descriptive intervals do not permit inference from nonrandom known fixtures to production.

## Related documents

- [Project README](../README.md) - capabilities and development workflow
- [Repository audit](../../../AUDIT.md) - withdrawn claims and confirmed defects
- [Market dataset](../../../job-market/dataset/README.md) - immutable-source reproduction

## Further reading

- [CFPB complaint database](https://www.consumerfinance.gov/data-research/consumer-complaints/) - official data and interpretation notices; accessed 2026-10-09
- [Bitext dataset card](https://huggingface.co/datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset) - publisher methodology and license; accessed 2026-10-09
- [OpenAI Evals](https://github.com/openai/evals/tree/8eac7a7de5215c907fbddc30efdaf316913eccdd) - evaluation framework and private-data practices; accessed 2026-10-09
