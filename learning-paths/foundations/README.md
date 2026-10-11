# FDE foundations: one project, six lessons

Start here if the main guide assumes vocabulary or tools you have not learned yet. Reviewed 2026-10-11. Each lesson explains a small concept, runs it, gives you a task to try yourself, and ends with evidence you can keep. This is a foundation route; it does not replace professional programming practice or customer deployment experience.

## What you will build

Use a retained real CFPB metadata sample to write a Python summary and import it into SQLite safely. Then use the existing local ticket API to study request contracts, retrieval boundaries, evaluation, and handover. The API smoke tickets are authored test inputs, separate from the five real metadata records.

The data project runs without API credentials or external services. Lessons 0–2 use Python's standard library; Lesson 3 installs the tested reference dependencies. There is no paid model call, GPU, or cloud deployment requirement. Keep all commands in the repository root and your own work in `learning-artifacts`.

## Follow the sequence

| Lesson | What to learn | Work to keep | Move on when you can... |
|---|---|---|---|
| [0. Setup and first run](00-setup-and-first-run.md) | Terminal, paths, Git, virtual environment | Version and directory note | Run a script and locate its inputs |
| [1. Python and real data](01-python-and-real-data.md) | JSON, lists, dictionaries, loops, functions | Your counting script and data note | Count records and explain their dates/limits |
| [2. SQL and replay](02-sql-and-replay.md) | Tables, keys, parameters, transactions | Query and repeated-import results | Explain zero new rows on replay and rollback on conflict |
| [3. HTTP and validation](03-http-and-validation.md) | Methods, bodies, schemas, status codes | Successful and rejected requests | Reproduce 200, 409, and 422 |
| [4. Retrieval and AI](04-retrieval-and-ai.md) | Evidence selection, generation, applicable policy | Role-filtered results and design note | Explain when a model helps and why an exact quote may be insufficient |
| [5. Evaluation and handover](05-evaluation-and-handover.md) | Failure checks, regression limits, operator instructions | Tests, report, filled brief, peer feedback | Reproduce one success, one failure, and an honest next decision |

Read the [glossary](glossary.md) when a term gets in the way. Use the [customer brief worksheet](customer-brief-template.md) throughout; unknown customer needs remain questions rather than invented facts.

Plan one session to follow each lesson and another to repeat the task without copying. If functions or SQL are new, pause for the linked language exercises. This pacing is a study recommendation, not a completion or hiring forecast.

## Quick first run

With Python 3.12 installed, from the repository root:

```bash
python3 -m venv .venv
.venv/bin/python learning-paths/foundations/code/complaint_pipeline.py
```

Expect five records, one product category, and an October 9 source date. The worked reference solves the exercise; a passing reference check does not demonstrate that your own implementation works. Write, test, and explain your own version before treating it as portfolio evidence.

## Current information and data limits

The exact October 11 CFPB query returned zero records at capture time, with all shards successful and no timeout. That result is preserved in the [October 11 source ledger](../../research/source_checks_2026-10-11.json). The October 9 sample remains a dated teaching input; it is not relabeled as newly received data. All five records have one product category and no narratives or triage labels, so they cannot establish general classifier quality.

The ticket reference uses authored policy text, heuristic rules, and process-local state. Its role headers are simulation, not authentication. These lessons distinguish implemented behavior from future production work. The existing [expert practicum](../expert-fde-practicum.md) describes the additional gates.

## How this route was designed

Inspired by [AI Engineering from Scratch at commit 1c8e62b](https://github.com/rohitg00/ai-engineering-from-scratch/tree/1c8e62b526e78b8773559594aab3a3487d9998ac): shared prerequisites first, small build steps, visible failure checks, and retained work products before the specialist customer-deployment route. These lessons and the exercise implementation are original material; the inspiration repository's prose and code were not copied.

Python, Git, FastAPI, pytest, and the source route were checked against selected versioned or pinned primary sources on October 11. Several direct documentation requests were blocked; successful source mirrors and failures are both recorded. Tested versions are not claims about the latest releases.

## Related documents

- [Beginner path](../beginner-to-fde.md) - longer progression and adjacent-role preparation
- [Learning path selector](../README.md) - choose the next route by demonstrated skills
- [Reference project](../../portfolio/reference-project/README.md) - implemented API behavior and missing production controls

## Further reading

- [Pinned inspiration software foundations](https://github.com/rohitg00/ai-engineering-from-scratch/blob/1c8e62b526e78b8773559594aab3a3487d9998ac/learning-paths/software-engineering-fundamentals.json) - foundation ordering
- [Pinned inspiration customer-deployment route](https://github.com/rohitg00/ai-engineering-from-scratch/blob/1c8e62b526e78b8773559594aab3a3487d9998ac/learning-paths/forward-deployed-ai-engineer.json) - specialist overlay and evidence limits
