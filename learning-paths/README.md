# Learning paths

Choose a route by the work you can already demonstrate. Everyone needs software foundations; forward deployed engineering adds customer discovery, integration constraints, evaluation, and operator handover. Learning-path navigation reviewed 2026-10-11.

## Start with a working system

If you are new to programming, start with the [six foundations lessons](foundations/README.md), beginning at [setup and first run](foundations/00-setup-and-first-run.md). Follow one project through real JSON metadata, Python, SQL, HTTP, retrieval, and evaluation. Each lesson has expected output, a task to attempt, a debugging check, and an exit check.

Continue with [beginner to FDE](beginner-to-fde.md) for the longer progression toward reviewed delivery work. Use the [glossary](foundations/glossary.md) and [customer brief worksheet](foundations/customer-brief-template.md) throughout. Passing reference tests is not evidence that an independent implementation works.

## Choose a background route

| Your current experience | Route | Responsibility to strengthen |
|---|---|---|
| Little programming or delivery experience | [Beginner](beginner-to-fde.md) | Build, test, debug, and explain a small system |
| Shipping software | [Software engineer](from-software-engineer.md) | Customer discovery and deployment evaluation |
| Models, research, or ML workflows | [AI / ML engineer](from-ai-ml-engineer.md) | APIs, integration, and operation outside notebooks |
| Data pipelines and SQL | [Data engineer](from-data-engineer.md) | Interactive applications and customer scoping |
| Technical demos and pre-sales | [Solutions engineer](from-solutions-engineer.md) | Implementation ownership and recovery |
| Advisory work and stakeholder management | [Consultant](from-consultant.md) | Reviewed code and hands-on diagnosis |
| Reliable delivery already demonstrated | [Expert practicum](expert-fde-practicum.md) | Independent evaluation, authority, durable recovery, economics, and handover |

The background chapters retain historical source windows and recommendations. Salary reports, old skill percentages, and old title samples are not newly measured employer requirements. Read the [market methodology](../job-market/dataset/README.md) before using those figures.

## Glossary and roadmap

Use the [FDE glossary](../GLOSSARY.md) for customer, integration, AI, evaluation, trust, and operating vocabulary. The [FDE roadmap](../ROADMAP.md) connects six stages to retained work and exit checks, with entry routes for beginners and experienced engineers.

## Plan the next project

- [90-day roadmap](90-day-fde-roadmap.md): a compact planning sequence for people who already write basic code. Implementations beyond the local reference are assignments.
- [24-week enterprise roadmap](24-week-enterprise-fde-roadmap.md): a longer project plan covering integrations, AI options, operations, discovery, and adoption. Specialist infrastructure and ERP work depend on the actual deployment.
- [Expert practicum](expert-fde-practicum.md): acceptance gates for experienced engineers. Readiness depends on evidence rather than elapsed time or tool count.

Select a small workflow with permitted data. Write a problem statement before selecting a model. Record the baseline, acceptance criteria, failure handling, and owner. Keep the first deliverable useful even if a generator is unavailable.

## Use the runnable material honestly

The [foundations pipeline](foundations/code/complaint_pipeline.py) imports the frozen five-record CFPB metadata sample into local SQLite. It validates input, preserves lineage, prevents duplicate insertion, and rolls back changed facts. It is a local teaching exercise, not a distributed ingestion service.

The [ETISE reference](../portfolio/reference-project/README.md) uses rules, feature hashing, authored policies, and in-memory state. It does not call an LLM or authenticate a tenant. Its 25 regression cases have unverified origins and are not an independent customer benchmark. Build and test missing production controls before claiming them.

Retain a small set of reviewable artifacts: a data note, working code, failure tests, a decision record, and a runbook. Ask another person to reproduce the result and report where the instructions fail. Label simulated interviews, discovery, and handover as practice.

## Related documents

- [Role overview](../role/01-what-is-an-fde.md) - responsibilities and title boundaries
- [Coding exercises](../interviews/code/) - additional implementation practice
- [Portfolio guide](../portfolio/README.md) - presenting evidence without overstating it
- [Repository audit](../AUDIT.md) - confirmed findings and remaining work

## Further reading

- [Pinned AI Engineering From Scratch](https://github.com/rohitg00/ai-engineering-from-scratch/tree/1c8e62b526e78b8773559594aab3a3487d9998ac) - shared software foundations and staged build/failure practice, inspected 2026-10-11; this guide's new lessons are original
- [CFPB complaint catalog](https://www.consumerfinance.gov/data-research/consumer-complaints/) - source and interpretation limits for the beginner metadata sample
