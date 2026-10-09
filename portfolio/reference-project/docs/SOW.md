# Pilot scope template for a ticket intake service

This is a proposal template reviewed on 2026-10-09, not an executed engagement or a record of customer outcomes. Fill its open requirements using authorized customer evidence. The repository supplies a local teaching implementation and public metadata samples, not a customer's baseline, contractual SLA, or approved policies.

## Required discovery inputs

Before promising automation, obtain the workflow owner, approved data access, actual arrival and payload distributions, existing error and resolution rates, reviewed policies, operator capacity, and applicable legal interpretation. Record source dates and uncertainty. Do not fill missing fields with invented volumes, fines, savings, or statutory thresholds.

## Proposed scope

- Validate and normalize agreed intake fields with a documented rejection contract.
- Compare a deterministic baseline with any proposed model on an independently labeled customer holdout.
- Retrieve approved policy versions with authenticated access controls and explicit abstention behavior.
- Offer review suggestions and capture authorized operator decisions.
- Measure the full request path, review workload, reliability, and costs under a declared workload.
- Deliver a tested recovery and rollback runbook with named operational ownership.

No irreversible customer action should be introduced without an approved authorization and review policy. A local `AUTOMATED_DISPATCH` label is not permission to send a message or alter a financial record.

## Acceptance gates to agree with the customer

Define numeric thresholds after the baseline exists. Each gate needs a metric, measurement window, representative sample, accountable owner, and documented exception policy:

1. Data: traceable authorized source records, required-field validation, accounted-for exclusions, and privacy review.
2. Quality: per-slice precision/recall, risk-weighted errors, abstention coverage, and retrieval evidence on an untouched evaluation set.
3. Authority: authenticated tenant and operator permissions, denied cross-tenant requests, and revocation checks.
4. Reliability: agreed latency and availability objectives, durable recovery, replay behavior, and operator-completed failure drills.
5. Economics: measured cost and review capacity compared with the pre-build workflow.
6. Handover: a customer operator can explain the reports and perform recovery without the author.

The five CFPB categorical records are an ingestion exercise only; they cannot replace the customer's sample or labeling. The 25 legacy regression fixtures cannot sign off customer quality.

## Current reference and excluded capabilities

The reference implements bounded ticket fields, sample retrieval, exact quotation checks, local replay semantics, and in-memory operator review. It does not implement authentication, durable queues, model inference, customer-system integration, production observability, or measured service availability. Those require separate deliverables and review.

## Related documents

- [Project README](../README.md) - implemented reference behavior
- [Architecture](ARCHITECTURE.md) - missing production boundaries
- [Requirements to spec](../../../customer/02-requirements-to-spec.md) - agreement structure

## Further reading

- [Google SRE objectives](https://sre.google/sre-book/service-level-objectives/) - indicators, objectives, and contractual agreements, checked 2026-10-09
