# System design under customer constraints

Reviewed 2026-10-09. Design around the customer's identity, network, data, operational skills, and recovery requirements. The diagrams in this section are proposed architecture patterns; the local reference does not implement every depicted control.

## Reading order

1. [Architecture for customer systems](01-architecture-for-customer-systems.md) - constraints, boundaries, maintainability, and review
2. [Reference architectures](02-reference-architectures.md) - proposed document, retrieval, automation, and batch shapes
3. [Trade-offs and decision records](03-trade-offs-and-decision-records.md) - alternatives, consequences, revisit triggers, and the observed evidence-free dispatch decision

## What the reference establishes

[ETISE](../portfolio/reference-project/README.md) is a deterministic local teaching service with feature-hash/token-overlap retrieval, sample-policy exact quote checks, default role filtering, bounded replay state, and review. It has no LLM, learned embeddings, BM25, RRF, authenticated role middleware, immutable audit ledger, durable queue, or private-cloud deployment. Its tests prove selected failure boundaries inside one process.

The former statutory $1,000 escalation rule was unsupported. Customer policy and jurisdiction-specific law must be represented separately. The [official Regulation E section](https://www.consumerfinance.gov/rules-policy/regulations/1005/11/) contains conditional investigation, provisional-credit, and extension rules; a ten-day universal final-resolution deadline is not established.

## Design review outputs

Produce a boundary diagram with identity and egress flows, a source lineage manifest, a decision record with alternatives and reversible steps, a failure-and-recovery matrix, and a workload-specific cost/latency report. Identify the artifacts still missing. Keep planning assumptions out of measured-results tables.

## Related documents

- [Expert practicum](../learning-paths/expert-fde-practicum.md) - gated delivery evidence
- [Audit](../AUDIT.md) - original defects and remediation limits
- [Runbook](../portfolio/reference-project/docs/SLA_RUNBOOK.md) - actual local operations

## Further reading

- [Google SRE objectives](https://sre.google/sre-book/service-level-objectives/) - workload objectives and measurements
- [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/) - architectural review guidance
