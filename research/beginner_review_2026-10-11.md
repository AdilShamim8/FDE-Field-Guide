# Beginner curriculum review - 2026-10-11

This review addresses the request to make the FDE Field Guide easier to follow from first principles while preserving expert evidence discipline. It builds on the [October 9 audit](../AUDIT.md); it does not replace historical source dates or certify every external citation.

## Scope and findings

The starting checkout at `9a1e45d50f8e1899d39460000d07119fe59e601a` had 141 tracked files. The inventory was read and hashed to identify the guide, runnable implementations, tests, dataset artifacts, and navigation. Detailed changes focus on beginner entry points, the learning-path index, the two linked roadmaps, executable foundations, and source-ledger discovery. Unaffected topic chapters retain their existing content and evidence windows.

The earlier beginner route lacked a first successful command and a connected project. The learning index mixed competing timelines with unsupported salaries, universal hiring conclusions, and implementation claims. Roadmaps described BM25, learned embeddings, authenticated permissions, repair loops, customer evaluations, productivity multipliers, and an 83-page case-study pack without corresponding verified artifacts.

The revision supplies six lessons with prerequisites, expected output, independent tasks, debugging checks, and exit criteria. A glossary and customer brief support both technical learning and customer discovery. The updated route selector separates foundations, background transitions, project plans, and expert acceptance gates.

The added Python/SQLite importer validates the retained real sample before opening a database, records a restricted fact projection with source lineage, replays unchanged IDs, rejects changed facts, and rolls back a partially attempted import. It uses parameterized SQL. These are local teaching guarantees, not distributed exactly-once effects, source authentication, or a complaint-resolution service.

## Inspiration and original work

The requested inspiration was inspected at [AI Engineering From Scratch commit 1c8e62b526e78b8773559594aab3a3487d9998ac](https://github.com/rohitg00/ai-engineering-from-scratch/tree/1c8e62b526e78b8773559594aab3a3487d9998ac), whose commit timestamp is 2026-10-10T16:02:29Z. Inspection covered its README, shared software foundations, FDE route, career practice, and selected setup, workflow, and RAG lessons.

Useful structural ideas were shared software foundations before specialization, staged builds, deliberate failure checks, and retained artifacts. The new lesson prose and code are original. That repository's lesson counts, outcomes, tool claims, and depth are not claimed as this guide's coverage. Its pinned source is credited in the course and route pages.

## Current source checks and real data

The [October 11 ledger](source_checks_2026-10-11.json) contains 25 retrieval checks: 16 successful and 9 explicitly failed. Eight documentation requests were blocked by the configured proxy, and one guessed Pro Git path returned 404. Successful versioned primary documentation mirrors were inspected through GitHub; the corrected Pro Git path is recorded separately. The network policy was not broadened for these checks.

The exact official CFPB query for records received on 2026-10-11 returned zero hits at 2026-10-11 04:16:47 UTC, with `relation: eq`, no timeout, and no failed shards. The query response hash is `377c57fad3e422b6f3341fdd098b566914669642b1b8b69e606d94e23afe8e4d`. This is a response at capture time, not a whole-day total or a worldwide observation.

The course therefore retains the [five real October 9 metadata records](../portfolio/reference-project/evals/real_data/cfpb_metadata_2026-10-09.json). All five have the same selected product and issue. They contain no narratives, independently adjudicated company facts, or ETISE severity/routing labels. No records were invented to fill a today-only dataset. The October 9 market artifacts likewise retain observation dates through September 23.

Authored API tickets, altered inputs, and regression fixtures are visibly separated from observed records. Invalid-input tests do not increase the real dataset size. Public availability and a matching hash do not establish unrestricted reuse, anonymity, or factual truth.

## Executed verification

- Constrained Python 3.12 installation remained dependency-consistent. Tested versions are recorded in the source ledger; they are not claims about the latest releases.
- The suite increased from 75 to 89 passing tests, with one visible Starlette TestClient deprecation warning. Eleven added foundation tests cover replay, conflicting updates, transaction rollback, parameters, invalid input before database creation, and CLI behavior. Three source-discovery tests ensure newer ledgers cannot be skipped and an empty inventory cannot pass.
- The published Python counting example produced five records and one product group. A fresh CLI import inserted five; its replay inserted zero and retained five. The published SQL query returned the expected group and source complaint ID/issue.
- The service was started independently on port 8011. The published billing request returned the expected routing and applicable quote; unchanged replay matched, changed payload returned 409, and missing account returned 422. Default-role compliance intake required review. Three search requests reproduced permitted/denied policy eligibility.
- All 25 existing ETISE regression contracts passed. They remain known cases with unverified origins; this is not an independent holdout or a production latency result.
- Interview, historical-market, pinned-snapshot, and evidence-ledger offline validators completed. Those checks validate structure and accounting, not every external source or license.
- Local Markdown targets were checked during each documentation update. CI now includes the foundation and research test directories alongside the existing runtime suites.

## Remaining work and interpretation

Six guided lessons are an entry point, not a complete computer science education or proof of ten years of delivery experience. Beginners must test their own implementation and obtain feedback on a handover. Timelines are planning recommendations; no job offer or universal title progression is implied.

The reference still needs authenticated authority, durable and tenant-isolated state, operational recovery, provider-specific measurement for any real model integration, and independently labeled customer evaluation before production claims. Those gates remain in the [expert practicum](../learning-paths/expert-fde-practicum.md). Optional SAP, cloud, learned retrieval, and multi-agent extensions are assignments, not completed customer deployments.

## Related documents

- [Foundations course](../learning-paths/foundations/README.md) - first command through evaluation and handover
- [Beginner route](../learning-paths/beginner-to-fde.md) - progression beyond the guided project
- [Evidence validator](validate_evidence.py) - deterministic discovery of all dated ledgers and metadata snapshots
- [Reference boundary](../portfolio/reference-project/README.md) - actual local behavior

## Further reading

- [Pinned CPython tutorial](https://github.com/python/cpython/tree/2abcf904b8dac8c999d2b3aac76681abb333798a/Doc/tutorial) - primary beginner language material
- [Pinned pytest getting started](https://github.com/pytest-dev/pytest/blob/cf470ec0bf7eb89cd97dd56df4859eae5db46447/doc/en/getting-started.rst) - executable assertion-based practice
