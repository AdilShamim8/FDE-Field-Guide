# Communication with engineering evidence

Explain the result, the evidence supporting it, and the decision needed from the reader. Reviewed 2026-10-09. The earlier customer volumes, private-cloud milestones, statutory fines, and production performance examples had no supporting artifacts and are withdrawn as observed claims.

## Translate the consequence without expanding the guarantee

| Engineering observation | Customer-facing consequence | Limit to disclose |
|---|---|---|
| Concurrent identical local requests execute classification once | Retries avoid repeated local processing inside one running service | This does not establish durable exactly-once effects across workers or restarts |
| No exact policy quote causes strict-mode review | The service withholds evidence-free dispatch | The policies are authored examples; review capacity and factual/legal support remain unmeasured |
| September has 127 matching rows and 91 distinct IDs | Location duplication changes the apparent number of opportunities | IDs can still represent repostings; this is one source's coverage |
| 25 known cases pass a regression gate | The exercised behaviors remain consistent with known expectations | Provenance is unverified and the cases are not an independent holdout |

## A decision brief a reviewer can challenge

Lead with a concrete recommendation. State the workflow and the consequence of getting it wrong. Link each observation to the source revision, acquisition window, transformation, or test. Give the alternative and the cost of your choice. End with the missing evidence and the condition that would change your recommendation.

For example, the current market refresh produces 212 cumulative title matches and 237 monthly-union matches. Recommend publishing both with the [reconciliation method](../job-market/dataset/README.md), rather than forcing agreement. The figures come from different source membership and title observations. A reviewer can reproduce the mismatch; an unexplained universal count would conceal it.

## Weekly update and incident communication

Separate completed work, observed blockers, next actions, and decisions needed. Do not describe a pending test as passed, a draft as published, or a retrieval date as a collection date. Use exact timestamps and time zones for an actual incident. Quantify affected records only when logs or a reproducible query support the number.

When impact is unknown, say so and state the next measurement. Name the mitigation, its owner, and the next update trigger. Do not promise zero data loss without storage and recovery evidence. Do not translate a pattern mask into an anonymization guarantee or a private endpoint into proof that every egress path is closed.

## Demonstrate the failure boundary

Use the [reference project's commands](../portfolio/reference-project/README.md) to show one normal request, a payload-conflict replay, and an unrelated ticket routed to review. Run the regression evaluator and show its evidence-status field alongside its score. Explain that the five current CFPB metadata records have no ETISE outcome labels and do not establish classifier quality.

For a real customer pilot, present an independently labeled holdout, review workload, latency measured at the service boundary, total cost per accepted outcome, and a tested recovery plan. These artifacts remain required work; the local reference cannot stand in for them.

## Related documents

- [Specification exercise](../customer/02-requirements-to-spec.md) - acceptance inputs and current contracts
- [Expert practicum](../learning-paths/expert-fde-practicum.md) - required review artifacts
- [Reference project](../portfolio/reference-project/README.md) - bounded executable evidence

## Further reading

- [Google SRE incident management](https://sre.google/sre-book/managing-incidents/) - coordination and incident communication
- [Google SRE objectives](https://sre.google/sre-book/service-level-objectives/) - define the measurement before promising performance
