# Engineering cases and deployment patterns

Use these cases to practice tracing a decision to evidence. Reviewed 2026-10-09. Source-backed repository findings, architectural recommendations, and unverified field accounts have different evidence status; none establishes a customer deployment certification.

## Reading order

1. [Deployment patterns](01-deployment-patterns-in-the-wild.md) - organizational patterns and proposed defenses; confirm employer-specific practices against primary sources.
2. [Source-backed engineering cases](02-llm-deployment-cases.md) - actual market count reconciliation, dataset provenance correction, and evaluation failures.
3. [Observed failure investigations](03-failure-stories.md) - reproducible retry, chunking, grounding, and replay defects, including the source-refresh validation mistake.
4. [Regulated-industry playbook](04-regulated-industries-playbook.md) - review prompts for healthcare, finance, and defense. Guidance needs jurisdiction-specific legal and security review.
5. [Manufacturing account evidence review](05-enterprise-manufacturing-vaayu-pumps.md) - an uncorroborated account and the artifacts required before publishing customer outcomes.

## Runnable evidence

The [reference service](../portfolio/reference-project/src/api/server.py) exercises local replay, input validation, document filtering, and review. It lacks authenticated tenant identity and durable queues. The [evaluation runner](../portfolio/reference-project/evals/run_evals.py) checks legacy regression fixtures; their origins are unverified. Tests establish these bounded behaviors, not the successful deployment of every architecture described in the guide.

## Related documents

- [Audit](../AUDIT.md) - findings, corrections, and remaining limits
- [Expert practicum](../learning-paths/expert-practicum.md) - evidence required at each delivery gate
- [Reference project](../portfolio/reference-project/README.md) - commands and implementation boundaries

## Further reading

- [Google SRE](https://sre.google/sre-book/table-of-contents/) - reliability and operational review practices
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) - risk-management guidance, not project certification
