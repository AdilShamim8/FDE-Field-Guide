# FDE market overview

Reviewed and source-checked 2026-10-09. This guide separates the current reproducible job-source snapshot from historical summaries and secondary reporting. The latest underlying job scrape is 2026-09-23; no October 9 worldwide scrape was found, and retrieval today does not make those postings today's vacancies.

## Current source-derived observations

The [snapshot](dataset/market_snapshot_2026-10-09.json) pins upstream commit `ed590319553252e2b8275486597b144ac55a4f3c`, input hashes, title matching, and deduplication. The cumulative file contains 8,051 unique IDs. The historical case-insensitive `FDE|forward deploy` title rule matches 212 IDs across 125 employer names. A hyphen-aware, word-bounded alternative matches 220, showing sensitivity to the role definition.

| Collection date | All listing rows | FDE matching rows | Distinct matching IDs | All distinct IDs |
|---|---:|---:|---:|---:|
| 2026-02-04 | 1,416 | 28 | 21 | 981 |
| 2026-02-27 | 2,057 | 41 | 33 | 1,667 |
| 2026-03-27 | 2,341 | 58 | 43 | 1,891 |
| 2026-04-22 | 2,473 | 65 | 47 | 1,980 |
| 2026-05-29 | 2,751 | 80 | 59 | 2,207 |
| 2026-06-25 | 3,024 | 108 | 78 | 2,394 |
| 2026-07-22 | 3,320 | 118 | 90 | 2,636 |
| 2026-08-25 | 3,946 | 140 | 103 | 3,117 |
| 2026-09-23 | 3,909 | 127 | 91 | 3,085 |

September's matching share is 3.2% of rows and 2.9% of unique IDs. Both matching rows and IDs declined from August. A description of uninterrupted growth would misstate these observations. Raw listing rows include location duplication and are not equivalent to distinct vacancies; distinct IDs can still include repostings.

The monthly matching-ID union contains 237 IDs, including 25 absent from cumulative title matches. Titles and cumulative membership differ between source files. The artifact preserves the discrepancy instead of treating the files as interchangeable. Read the [reproduction and rights notes](dataset/README.md) before reuse; no job-description text is redistributed.

## Historical measurements and salary reporting

The [archived summary](dataset/fde_market_data.json) describes February–July, 146 cumulative matches, and 94 employer names. Its extracted skills, responsibilities, and seniority labels have not been remeasured on the 212-ID snapshot. Upstream's extraction audit flags unsupported inferred fields and an inspected evaluation seed. Keep the historical denominator attached wherever those labels are quoted.

[Fortune's September 3 article](https://fortune.com/2026/09/03/forward-deployed-engineers-fast-growing-six-figure-silicon-valley-job-integrate-ai-with-customers-tech-careers-palantir/), checked today, reports Lightcast's more-than-1,000% January–August year-over-year posting growth and an advertised median salary of more than $188,000. This verifies what the publisher reported, not Lightcast's underlying methodology or actual paid compensation. The figure is a lower-bound statement, not an exact $188,000 median.

The previously quoted Plank 982-posting/462-company counts are not corroborated by the current homepage. The historical JSON retains them with an unverified status for traceability; do not promote them into current market measurements. Sources with different boards, windows, title rules, and deduplication methods cannot be merged into one census or salary distribution.

## How to use this evidence

Use the snapshot to inspect actual title and employer metadata and reproduce counting decisions. Consult the original employer posting before applying; source URLs have not been checked as currently live vacancies. Search adjacent titles deliberately, but do not add them to this cohort without versioning the role definition.

Job-board coverage omits referral and internal hiring and can skew by language and employer mix. Missing a junior title marker is not proof of a particular experience requirement. The data does not establish hiring conversion rates, current staffing, worldwide demand, paid salary, or customer outcomes.

## Related documents

- [Market dataset](dataset/README.md) - acquisition, method, sensitivity, and reconciliation
- [Compensation](02-compensation.md) - historical reporting; confirm current offers with primary sources
- [Getting hired](03-getting-hired.md) - practical application guidance
- [Expert practicum](../learning-paths/expert-fde-practicum.md) - use the discrepancy as an engineering exercise

## Further reading

- [Pinned upstream source](https://github.com/alexeygrigorev/ai-engineering-field-guide/tree/ed590319553252e2b8275486597b144ac55a4f3c) - collection files and historical analysis
- [Pinned extraction audit](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/ed590319553252e2b8275486597b144ac55a4f3c/job-market/_internal/eval/README.md) - unsupported labels and holdout limits
