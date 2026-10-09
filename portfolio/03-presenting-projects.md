# Present projects with evidence a reviewer can reproduce

Reviewed 2026-10-09. Explain what runs, which decisions it supports, and what evidence is missing. The former example pitch claimed authenticated CFPB/Bitext fixtures, deployed private-cloud controls, automatic schema repair, and measured customer outcomes that this repository does not establish; those claims are withdrawn.

## Lead with a bounded result

State the workflow, implementation, and strongest observed result in a few sentences. For ETISE, say that it is a deterministic local ticket-intake reference. It checks typed inputs, applicable sample-policy quotes, replay conflicts, and review paths. It does not invoke a model or mutate a customer's systems.

For the market observatory, state the source revision and counting method. The cumulative filter produces 212 IDs; the monthly matching union produces 237. Show the reconciliation rather than hiding it. The underlying observations end September 23, even though the sources were retrieved October 9.

## Organize the repository for review

1. Put the supported quick-start and exact verification commands near the top.
2. Link the source manifest, transformations, permissions scope, and observation dates.
3. Explain the architecture boundary and one consequential decision with alternatives.
4. Publish a report with test scope, failure cases, and limitations alongside its scores.
5. Include a runbook an operator can execute, including state-loss and recovery behavior.

Do not claim a database, model, cloud resource, or authentication control merely because it appears in a diagram. Do not claim an imagined customer signed a specification. Record optional packaging and deployment checks as unrun until executed.

## Demonstrate three concrete boundaries

Use the [reference commands](reference-project/README.md) to show normal billing intake, replay of the same request, and a payload conflict returning 409. Then show a compliance request without access to its applicable policy routing to review, followed by the simulated compliance-role path. Explain that role headers are not authentication and all state disappears on restart.

Run [regression evaluation](reference-project/evals/run_evals.py) and display evidence status as well as category, severity, routing, required-document, and quote checks. Known fixtures can prevent regressions but cannot measure unseen customer quality. Engine CPU timings exclude HTTP, inference, queueing, and operator review.

## Answer difficult follow-up questions honestly

| Reviewer question | Evidence to present |
|---|---|
| Where did the data come from? | Stable source IDs, pinned revision or response hash, transformations, and permissions scope |
| How do you know it generalizes? | Independently collected and adjudicated holdout; otherwise state that generalization is unmeasured |
| What happens on a retry or restart? | Replay/conflict/expiry tests plus a recovery demonstration; ETISE currently loses state on restart |
| What prevents unauthorized actions? | Authenticated identity and authorization tests; these are missing from the reference |
| What does it cost per accepted outcome? | Declared workload, infrastructure/inference/review cost, and counterfactual baseline; not an invented ROI number |

## Data hygiene

The [five CFPB records](reference-project/evals/real_data/cfpb_metadata_2026-10-09.json) are actual categorical metadata received today, without narratives or ETISE outcome labels. The old 25-case file has unverified origins. Bitext is publisher-described hybrid synthetic and excluded from real-only evidence. Public availability does not grant unrestricted reuse; read the [provenance contract](reference-project/evals/DATASET_PROVENANCE.md).

## Related documents

- [Reference project](reference-project/README.md) - runnable implementation and limits
- [Expert practicum](../learning-paths/expert-fde-practicum.md) - deliverable and rejection gates
- [Market method](../job-market/dataset/README.md) - reproducible count reconciliation

## Further reading

- [CFPB official catalog](https://www.consumerfinance.gov/data-research/consumer-complaints/) - data and interpretation limits
- [Google SRE objectives](https://sre.google/sre-book/service-level-objectives/) - define meaningful service measurements
