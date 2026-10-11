# Awesome FDE resources

A resource directory for learning Forward Deployed Engineering, building a small system, and progressing toward customer delivery. Choose a starting point below, then use the topic links to close a specific gap. Keep a working project alongside your reading.

Navigation and repository descriptions reviewed 2026-10-11. External resources retain their own publication and verification dates; this update does not recertify every linked source. See the [dated beginner review](research/beginner_review_2026-10-11.md) and [repository audit](AUDIT.md) for the evidence behind the current material.

## Contents

- [Choose a starting point](#choose-a-starting-point)
- [Beginner foundations](#beginner-foundations)
- [Build and evaluate software](#build-and-evaluate-software)
- [Customer work and operations](#customer-work-and-operations)
- [Expert practice and portfolio](#expert-practice-and-portfolio)
- [Real data and engineering cases](#real-data-and-engineering-cases)
- [Interview practice](#interview-practice)
- [Books and external learning](#books-and-external-learning)
- [Evidence and maintenance](#evidence-and-maintenance)

## Choose a starting point

| Your goal | Start here | Work to keep |
|---|---|---|
| Learn to program through a small project | [First run](learning-paths/foundations/00-setup-and-first-run.md), then [foundations](learning-paths/foundations/README.md) | Your script, query, failure test, and data note |
| Understand the FDE role | [Role overview](role/01-what-is-an-fde.md) and [role boundaries](role/03-fde-vs-other-roles.md) | A description of the responsibilities you want to practice |
| Transition from an adjacent role | [Learning-path selector](learning-paths/README.md) | A project targeting your current delivery gap |
| Develop the local reference | [ETISE README](portfolio/reference-project/README.md) | Reproduced behavior and a tested change |
| Demonstrate experienced delivery | [Expert practicum](learning-paths/expert-fde-practicum.md) | Independent evaluation, authority checks, recovery, and handover evidence |
| Prepare for an interview | [Interview guide](interviews/README.md) | A timed implementation and an explained failure |
| Research market or dataset claims | [Market methodology](job-market/dataset/README.md) | Source dates, denominators, and reproducible counts |

The [beginner route](learning-paths/beginner-to-fde.md) describes progression beyond the first project. The [90-day plan](learning-paths/90-day-fde-roadmap.md) and [24-week plan](learning-paths/24-week-enterprise-fde-roadmap.md) assume programming foundations. Their schedules are recommendations; optional AI, cloud, and ERP extensions require their own implementation and verification.

## Beginner foundations

Follow these six lessons in order. Lessons 0–2 use Python's standard library; later lessons use the tested local reference dependencies. No paid model calls or cloud services are required.

| Lesson | Practice | Completion evidence |
|---|---|---|
| [0. Setup and first run](learning-paths/foundations/00-setup-and-first-run.md) | Terminal, paths, Git, and a Python environment | Run the data summary and identify its input |
| [1. Python and real data](learning-paths/foundations/01-python-and-real-data.md) | JSON, lists, dictionaries, loops, and functions | Count records with your own function |
| [2. SQL and replay](learning-paths/foundations/02-sql-and-replay.md) | Keys, parameters, transactions, and repeat imports | Explain zero new rows on replay and rollback on conflict |
| [3. HTTP and validation](learning-paths/foundations/03-http-and-validation.md) | Request bodies, schemas, and status codes | Reproduce 200, 409, and 422 responses |
| [4. Retrieval and AI](learning-paths/foundations/04-retrieval-and-ai.md) | Evidence selection and generation choices | Explain role filtering and when a model would help |
| [5. Evaluation and handover](learning-paths/foundations/05-evaluation-and-handover.md) | Assertions, deliberate defects, and operating instructions | Test your own code and retain a peer walkthrough |

Use the [glossary](learning-paths/foundations/glossary.md) for unfamiliar terms and the [customer brief worksheet](learning-paths/foundations/customer-brief-template.md) to record assumptions and acceptance criteria. Keep original learner work in the ignored `learning-artifacts/` directory. A passing reference test does not verify your independent implementation.

## Build and evaluate software

### Runnable material

- [Complaint importer](learning-paths/foundations/code/complaint_pipeline.py) - validate the retained real metadata, summarize it, and import it into local SQLite with unchanged-ID replay and transaction rollback.
- [Importer tests](learning-paths/foundations/code/test_complaint_pipeline.py) - invalid input, changed facts, rollback, SQL parameters, and CLI behavior. Mutated inputs are authored tests.
- [Coding exercises](interviews/code/) - parsing, retries, rate limiting, bounded chunking, structured extraction, and webhook contracts. Inspect each implementation's supported boundary.
- [ETISE reference](portfolio/reference-project/README.md) - local FastAPI intake with deterministic rules, feature hashing, applicable-policy checks, and process-local state. Role headers simulate permissions; the service has no LLM calls, BM25, authenticated tenant identity, or durable dispatch.
- [Regression runner](portfolio/reference-project/evals/run_evals.py) - 25 known routing and citation contracts with unverified fixture origins. Passing results do not establish unseen customer accuracy or production latency.
- [Verification workflow](.github/workflows/verify.yml) - dependency checks, runtime tests, regression contracts, dataset accounting, and portable local links.

### Engineering and AI concepts

- [Core technical skills](skills/01-core-technical-skills.md) - programming, APIs, data, and deployment topics.
- [APIs and integrations](engineering/02-apis-and-integrations.md) - authentication, retries, replay, and system-of-record interfaces.
- [Data pipelines](engineering/03-data-pipelines.md) - ingestion, data quality, and schema changes.
- [Cloud and infrastructure](engineering/04-cloud-and-infrastructure.md) - deployment constraints and infrastructure choices.
- [Security and compliance](engineering/05-security-and-compliance.md) - threat modeling, access boundaries, and review requirements.
- [LLM application patterns](ai/01-llm-application-patterns.md) - extraction, retrieval, generation, and deterministic alternatives.
- [Agents and tools](ai/02-agents-and-tools.md) - tool-use and orchestration design options; diagrams do not establish implementation.
- [Evaluation and testing](ai/03-evaluation-and-testing.md) - labels, regression, holdouts, and acceptance criteria.
- [Monitoring and reliability](ai/04-monitoring-and-reliability.md) - operational signals, model usage, and failure diagnosis.

### Architecture decisions

- [Customer-system architecture](system-design/01-architecture-for-customer-systems.md) - design around network, storage, and compute constraints.
- [Reference architectures](system-design/02-reference-architectures.md) - proposed application blueprints to adapt and test.
- [Trade-offs and decision records](system-design/03-trade-offs-and-decision-records.md) - record context, alternatives, and consequences.
- [Implemented reference architecture](portfolio/reference-project/docs/ARCHITECTURE.md) - the actual local data flow and missing production controls.

## Customer work and operations

Start with the workflow and its owner before choosing an AI tool. For each proposed change, record the current process, the acceptance check, the failure path, and who handles exceptions.

- [Engagement lifecycle](customer/01-engagement-lifecycle.md) - discovery through delivery and handover.
- [Discovery and requirements](skills/02-discovery-and-requirements.md) - ask about the work, constraints, and measurable outcomes.
- [Requirements to specification](customer/02-requirements-to-spec.md) - turn a request into testable behavior.
- [Working in customer environments](customer/03-working-in-customer-environments.md) - access, network, and operating constraints.
- [Managing expectations](customer/04-managing-expectations.md) - scope, uncertainty, and delivery communication.
- [Stakeholder management](skills/04-stakeholder-management.md) - decisions and escalation ownership.
- [Ambiguity and prioritization](skills/05-ambiguity-and-prioritization.md) - choose the next useful, reviewable increment.
- [Deployment guide](deployment/README.md) - release planning, readiness, and ownership.
- [Troubleshooting guide](troubleshooting/README.md) - diagnosis and incident practice.
- [Local reference runbook](portfolio/reference-project/docs/SLA_RUNBOOK.md) - commands supported by ETISE and state lost on restart.

## Expert practice and portfolio

Use the [expert practicum](learning-paths/expert-fde-practicum.md) when you can already build and operate software. It asks for source lineage, independent evaluation, authenticated authority, durable recovery, measured economics, and operator acceptance. Tool count and elapsed study time do not demonstrate those capabilities.

- [What to build](portfolio/01-what-to-build.md) - select a useful problem with a testable boundary.
- [Project ideas](portfolio/02-project-ideas.md) - proposed projects that need permitted data and demonstrated results.
- [Project presentation](portfolio/03-presenting-projects.md) - show the decision, implementation, failure, and recovery.
- [Project selection](portfolio/04-project-selection-masterclass.md) - compare candidate workflows and review data suitability.

Before claiming delivery readiness, retain evidence that another person can reproduce the system, the tests exercise your code, evaluation labels fit the decision, access controls match the threat model, and recovery instructions work. Label role-plays and peer walkthroughs as practice; record real operator acceptance only when it happened.

## Real data and engineering cases

### Dataset directory

| Resource | What it contains | Interpretation limit |
|---|---|---|
| [CFPB metadata sample](portfolio/reference-project/evals/real_data/cfpb_metadata_2026-10-09.json) | Five actual categorical records received and captured on 2026-10-09 | Selected sample, one product category, no narratives or triage labels |
| [Pinned market snapshot](job-market/dataset/market_snapshot_2026-10-09.json) | Source references, hashes, and 212 cumulative title-matched IDs across 125 employer names | Observation dates run through 2026-09-23; not today's open vacancies or a worldwide census |
| [Market dataset runbook](job-market/dataset/README.md) | Definitions, row/ID accounting, historical aggregates, and reproduction steps | The earlier 146-role summary is aggregate material, not 146 retained raw postings |
| [Evaluation provenance](portfolio/reference-project/evals/DATASET_PROVENANCE.md) | Admission rules and evidence status of inputs and fixtures | The 25 legacy cases have unverified origins and are not an independent customer holdout |

The exact official CFPB query for 2026-10-11 returned zero hits at capture time. The [October 11 ledger](research/source_checks_2026-10-11.json) records that response and selected documentation checks, including failed retrievals. Keep the older sample's dates intact; do not manufacture records or labels to make it look current.

### Cases to investigate

- [Source-backed engineering cases](case-studies/02-llm-deployment-cases.md) - market reconciliation, provenance correction, and evaluation findings.
- [Observed failure investigations](case-studies/03-failure-stories.md) - reproducible code failures and the limits of their fixes.
- [Deployment patterns](case-studies/01-deployment-patterns-in-the-wild.md) - organizational patterns and proposed defenses.
- [Regulated-industry playbook](case-studies/04-regulated-industries-playbook.md) - domain review questions requiring applicable legal and security guidance.
- [Manufacturing evidence review](case-studies/05-enterprise-manufacturing-vaayu-pumps.md) - the uncorroborated Vaayu account and artifacts needed to establish a real outcome. The claimed 83-page document pack is not authenticated in this repository.

For market interpretation, use the [market overview](job-market/01-market-overview.md) and [compensation chapter](job-market/02-compensation.md) with their stated source windows. Salary reporting and a historical title filter do not establish a universal hiring rule.

## Interview practice

These resources are preparation material. Authored prompts, sample responses, and scoring rubrics are not authenticated company transcripts or hiring policies.

- [Interview process](interviews/01-interview-process.md) - reported formats and preparation guidance; confirm the actual process with the employer.
- [Coding and technical rounds](interviews/02-coding-and-technical.md) - implementation and debugging practice.
- [System design rounds](interviews/03-system-design.md) - explain capacity, constraints, and failure behavior.
- [Customer scenarios](interviews/04-customer-scenarios.md) - role-play discovery, pushback, and incident communication.
- [Behavioral rounds](interviews/05-behavioral.md) - explain real ownership decisions without inventing outcomes.
- [Take-home assignments](interviews/06-take-homes.md) - timed practice and an authored review rubric.
- [Question bank](interviews/07-question-bank.md) - curated prompts with unverified company attributions.
- [Coding solutions](interviews/08-coding-solutions.md) - worked implementations to compare after your own attempt.
- [Practice dataset](interviews/dataset/README.md) - 17 authored records; its ten-pass validator checks structure and declarations, not company usage or predictive validity.

## Books and external learning

### Read by the gap in your project

These are reading recommendations, not prerequisites to complete before building. The [reading list](resources/02-reading.md) provides broader context; preserve the evidence status of historical reports and attributed accounts there.

| Book | Author(s) | Use it for |
|---|---|---|
| Designing Data-Intensive Applications | Martin Kleppmann | Data modeling, replication, and failure trade-offs |
| Designing Machine Learning Systems | Chip Huyen | Data, evaluation, and model-system operation |
| Site Reliability Engineering | Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy, editors | SLOs, error budgets, and incident response |
| Accelerate | Nicole Forsgren, Jez Humble, Gene Kim | Delivery measurement and improvement |
| Continuous Delivery | Jez Humble, David Farley | Release and deployment practices |
| The Trusted Advisor | David Maister, Charles Green, Robert Galford | Trust and advisory relationships |
| Never Split the Difference | Chris Voss, Tahl Raz | Negotiation and difficult conversations |
| Team of Teams | Stanley McChrystal and coauthors | Coordination across organizational boundaries |
| The Mythical Man-Month | Frederick Brooks | Planning and software-project coordination |

### Optional videos

These previously listed resources are retained for exploration. Their contents, speaker affiliations, and outcome claims were not reverified in this index update. Compare technical advice with primary documentation and your own measured workload.

- [Forward Deployed Engineering 101](https://www.youtube.com/watch?v=KwhgfwOSToQ) - previously attributed to Kevin Bai.
- [This Is How Forward Deployed Engineering Is Actually Done](https://www.youtube.com/watch?v=AD-EmZ3v6-g) - previously listed as an AI LABS discussion.
- [What is the FDE role?](https://www.youtube.com/watch?v=7JlEs6zyB_U) - previously attributed to Piyush Garg.
- [Codebasics FDE roadmap](https://www.youtube.com/watch?v=uE4HTkDtp48) - external roadmap discussion, separate from this guide's recommended schedule.
- [FDE Academy channel](https://www.youtube.com/@fdeacademy) - additional project and interview discussions.

### Ongoing reading and communities

Choose a source for a specific question; publication recency alone does not establish correctness.

- [Chip Huyen's blog](https://huyenchip.com) - AI engineering essays.
- [The Pragmatic Engineer](https://newsletter.pragmaticengineer.com) - engineering-industry reporting.
- [MLOps discussions](https://www.reddit.com/r/mlops) - community questions and experience reports.
- [Plank](https://joinplank.com) - hiring platform; review individual listings and their dates rather than copying uncorroborated headline counts.
- [SAP Business Accelerator Hub](https://api.sap.com) - official API catalog; verify current sandbox access, credentials, limits, and terms before an exercise.

## Evidence and maintenance

Read primary documentation for the specific software version you use. Distinguish a resource recommendation, an authored exercise, a measured result, and a proposed architecture. A working link or matching hash alone cannot authenticate a quotation, customer outcome, or dataset license.

- [October 9 source checks](research/source_checks_2026-10-09.json) - earlier dated retrievals and claim-specific limits.
- [October 11 source checks](research/source_checks_2026-10-11.json) - pinned beginner documentation, inspiration, the current CFPB query, and explicit retrieval failures.
- [Evidence validator](research/validate_evidence.py) - offline checks that discover all saved dated ledgers and metadata snapshots; it does not refetch live sources.
- [Contribution rules](STYLING.md) - dates, source admission, implementation boundaries, and writing conventions.

When proposing a resource, include its purpose, intended prerequisite, exact source location, and known limits. Pin source revisions where possible and retain publication, collection, retrieval, and review dates separately. Update a description when its supporting source or implementation changes.

## Related documents

- [Guide overview](README.md) - repository navigation and verification commands.
- [Learning paths](learning-paths/README.md) - choose the next route by demonstrated skills.
- [Resource toolbox](resources/01-tools.md) - tools to investigate for a specific delivery need.
- [Communities and people](resources/03-communities-and-people.md) - additional directories; attributed accounts need source-specific review.
- [Repository audit](AUDIT.md) - confirmed findings and remaining production work.

## Further reading

- [Pinned AI Engineering From Scratch](https://github.com/rohitg00/ai-engineering-from-scratch/tree/1c8e62b526e78b8773559594aab3a3487d9998ac) - inspiration for shared foundations and staged practice, inspected 2026-10-11; the new FDE lessons are original.
- [Pinned Python tutorial](https://github.com/python/cpython/tree/2abcf904b8dac8c999d2b3aac76681abb333798a/Doc/tutorial) - primary language documentation for the tested interpreter version.
- [Pinned pytest getting started](https://github.com/pytest-dev/pytest/blob/cf470ec0bf7eb89cd97dd56df4859eae5db46447/doc/en/getting-started.rst) - assertions and executable failure checks.
- [Google SRE book](https://sre.google/sre-book/table-of-contents/) - operational reliability literature.
- [OWASP LLM security project](https://owasp.org/www-project-top-10-for-large-language-model-applications/) - security guidance to review against a stated threat model and release.
