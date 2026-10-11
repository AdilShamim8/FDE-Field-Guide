# FDE roadmap

Use this map to choose the next responsibility you can demonstrate, from a first script to reviewed customer delivery. Reviewed 2026-10-11. The stages are learning recommendations with exit checks; the 90-day and 24-week schedules below are study plans, not hiring guarantees or proof of production experience.

## Choose your route

| Starting point | Start here | Next decision |
|---|---|---|
| New to programming | [Six foundation lessons](learning-paths/foundations/README.md), then the [beginner route](learning-paths/beginner-to-fde.md) | Can you write, test, and explain your own small implementation? |
| Already writing basic code | [90-day transition plan](learning-paths/90-day-fde-roadmap.md) | Which integration, evaluation, or customer-delivery gap needs work? |
| Seeking broader enterprise practice | [24-week enterprise plan](learning-paths/24-week-enterprise-fde-roadmap.md) | Which infrastructure and domain extensions does the workflow actually need? |
| Already shipping and operating software | [Expert practicum](learning-paths/expert-fde-practicum.md) | Can you demonstrate authority, independent evaluation, recovery, economics, and handover? |

Use the [FDE glossary](GLOSSARY.md) alongside any route. Customer discovery starts with the first useful project, even when a longer plan organizes it in a later phase.

## Stage 1: build your foundations

Follow the [first-run lesson](learning-paths/foundations/00-setup-and-first-run.md) through Python, JSON, SQL, HTTP, retrieval, and evaluation. Use the retained real metadata; separate it from authored API tickets and deliberately invalid test inputs.

Keep your own script, source-date note, query, and failure test. Exit when you can run your implementation, explain the source fields and dates, reproduce a failure, and verify its repair. Passing the supplied reference tests alone does not meet this gate.

## Stage 2: understand the customer workflow

Use the [customer brief](learning-paths/foundations/customer-brief-template.md) and [discovery guidance](skills/02-discovery-and-requirements.md). Identify the user, current process, problem, permitted inputs, acceptance criteria, and exception owner before choosing a model.

Keep a workflow description and a small scope. Exit when each requirement has a reviewable check and unconfirmed needs remain labeled assumptions. A peer interview or role-play is practice; record real customer confirmation only when it occurred.

## Stage 3: build a reliable integration

Study [APIs and integrations](engineering/02-apis-and-integrations.md), [data pipelines](engineering/03-data-pipelines.md), and the [runnable coding exercises](interviews/code/). Implement input validation, bounded retries, replay scope, conflict handling, and a declared update policy. Derive permissions from verified identity when access is required.

Keep working code, a contract, lineage records, and failure checks. Exit when a retry does not duplicate the intended effect, changed inputs are handled deliberately, and a failed operation has an accountable recovery path. Local SQLite and simulated roles do not establish distributed durability or tenant authorization.

## Stage 4: add AI where it helps

Use [retrieval before generation](learning-paths/foundations/04-retrieval-and-ai.md) and [application patterns](ai/01-llm-application-patterns.md). Compare a deterministic baseline, retrieval, and generation for the same decision. Add models or tools only with permitted data, defined authority, and measurable benefit.

Keep a design decision and traces of any actual model experiment. Exit when you can test missing evidence, irrelevant citations, invalid output, and unapproved actions. If you make provider calls, preserve model/version, usage, latency, cost, and reviewer outcomes; do not invent those measurements for the deterministic local reference.

## Stage 5: evaluate and operate

Study [evaluation](ai/03-evaluation-and-testing.md), [monitoring](ai/04-monitoring-and-reliability.md), and [deployment](deployment/README.md). Separate known contract tests from independently labeled evaluation. Specify the workload, service indicators, retention, and failure/recovery responsibilities.

Keep a test report, justified acceptance criteria, an untouched evaluation set when required, and an executed recovery drill. Exit when another person can identify a failure and follow the runbook. The 25 legacy ETISE fixtures have unverified origins and do not establish customer accuracy or an SLA.

## Stage 6: hand over and present the work

Use the [handover lesson](learning-paths/foundations/05-evaluation-and-handover.md), [project presentation guide](portfolio/03-presenting-projects.md), and [expert practicum](learning-paths/expert-fde-practicum.md). Review the scope, decisions, implemented controls, operating limits, and next owner.

Keep the README, decision record, runbook, demonstrated failure/recovery, and actual acceptance or practice feedback. Exit when another person can reproduce the work and understand what remains unready. Present practice honestly; describe real delivery with its evidence rather than a tool list or elapsed study time.

## Use a schedule after checking prerequisites

- [90-day plan](learning-paths/90-day-fde-roadmap.md): Weeks 1–4 integration foundations, Weeks 5–8 retrieval/extraction options and evaluation, Weeks 9–12 system design, customer scenarios, and portfolio practice. It assumes basic programming.
- [24-week plan](learning-paths/24-week-enterprise-fde-roadmap.md): Weeks 1–16 technical practice, Weeks 17–24 deeper discovery, specification, adoption, and handover. Begin customer questions earlier; SAP, orchestration, and cloud extensions depend on the project.
- [Background routes](learning-paths/README.md): adapt the work to existing software, ML, data, solutions, or consulting skills.

Adjust the pace to your own demonstrated gaps. Choose current individual vacancies when planning applications; a historical title sample does not define every employer entry route.

## Related documents

- [FDE glossary](GLOSSARY.md) - vocabulary for the stages
- [Learning paths](learning-paths/README.md) - background-specific routes
- [Foundations course](learning-paths/foundations/README.md) - guided first project
- [Repository audit](AUDIT.md) - evidence status and remaining production work

## Further reading

- [Pinned AI Engineering From Scratch](https://github.com/rohitg00/ai-engineering-from-scratch/tree/1c8e62b526e78b8773559594aab3a3487d9998ac) - shared foundations followed by specialist practice; the stages here are original recommendations
- [Google SRE book](https://sre.google/sre-book/table-of-contents/) - reliability and operator ownership
