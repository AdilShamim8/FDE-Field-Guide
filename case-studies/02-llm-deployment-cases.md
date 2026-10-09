# Source-backed engineering cases

These cases are observed source and repository findings checked on 2026-10-09. They demonstrate reproducible engineering analysis, not undocumented customer deployments. The former financial, SEC, and healthcare production stories had no customer artifacts or reproducible outcome measurements and are withdrawn as empirical claims.

## Case 1: market growth depends on the unit of observation

Situation: the guide's market article described seven scrape dates and 146 historical titles. The current pinned source also contains August and September CSVs.

Constraints: the files contain location duplicates, changing titles, and inconsistent cumulative membership. Public availability does not grant a blanket license to copy all job-description text.

Observed evidence: the cumulative title rule matches 212 IDs across 125 employer names. September contains 127 matching rows and 91 unique matching IDs. The monthly union has 237 matching IDs, with 25 not represented by the cumulative title matches. The alternative hyphen-aware rule matches 220 cumulative IDs.

Move-by-move: pin the source revision, hash each input, publish row and unique-ID counts, preserve the discrepant IDs, and make the result reproducible with a validator. Do not silently combine denominators or call this a worldwide hiring census.

What good looks like: [the snapshot and runbook](../job-market/dataset/README.md) preserve both observations and limits. The latest underlying observation is September 23, not the October 9 retrieval date.

## Case 2: a dataset name is not provenance

Situation: the old ETISE provenance document described Bitext as real customer interactions under CC BY 4.0.

Constraints: adopting a public dataset requires understanding its generation method, version, permissions, and fitness for the intended claim.

Observed evidence: the publisher's [dataset card](https://huggingface.co/datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset), accessed today, describes hybrid synthetic NLP/NLG generation and lists `cdla-sharing-1.0`. The local fixture collection contains no reproducible transform from that dataset.

Move-by-move: correct the source description, withdraw the unauditable fixture mappings, and exclude the synthetic collection from real-world-only evidence. Preserve the legacy cases as regression fixtures without relabeling them as newly observed data.

What good looks like: [the provenance contract](../portfolio/reference-project/evals/DATASET_PROVENANCE.md) states what a future real benchmark must record. The actual today-dated CFPB sample contains categorical metadata, not invented ETISE labels or customer narratives.

## Case 3: perfect classification can conceal a failed routing gate

Situation: the original evaluation runner printed routing accuracy but omitted it from acceptance. It could also report perfect grounding when no citations were emitted.

Constraints: known hand-curated examples do not supply an independent customer holdout. The local engine has no model inference, authentic policy source, or production timing workload.

Observed evidence: adversarial tests now preserve correct category and severity while forcing wrong routing, remove all citations, forge quote flags, or change the required source document. Each condition makes acceptance fail.

Move-by-move: recheck exact quotes and sections against the index, gate expected routing and document retrieval, reject empty/duplicate runs, and report missing grounding as unevaluated. Keep per-class metrics and failure IDs visible.

What good looks like: the [regression runner](../portfolio/reference-project/evals/run_evals.py) and [failure tests](../portfolio/reference-project/tests/test_regression_gates.py) establish these contracts. Passing all 25 known fixtures remains regression evidence rather than a production SLA or population accuracy estimate.

## Related documents

- [Audit](../AUDIT.md) - repository findings and scope
- [Market methodology](../job-market/dataset/README.md) - source reproduction and limitations
- [Expert practicum](../learning-paths/expert-fde-practicum.md) - customer-ready acceptance gates

## Further reading

- [Upstream extraction audit](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/ed590319553252e2b8275486597b144ac55a4f3c/job-market/_internal/eval/README.md) - label drift and known-seed limitations, checked 2026-10-09
