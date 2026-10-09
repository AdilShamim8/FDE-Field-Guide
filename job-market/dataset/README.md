# FDE market observations and source lineage

This directory is for engineers who need reproducible market measurements rather than headline statistics. The current source snapshot was retrieved and checked on 2026-10-09. Its latest underlying scrape is 2026-09-23; this is not an October 9 job-board crawl.

## Current verified snapshot

[market_snapshot_2026-10-09.json](market_snapshot_2026-10-09.json) records factual metadata from [AI Engineering Field Guide commit ed590319](https://github.com/alexeygrigorev/ai-engineering-field-guide/tree/ed590319553252e2b8275486597b144ac55a4f3c), with SHA-256 hashes for each input CSV. No LLM-generated skill or responsibility fields were used.

The cumulative CSV contains 8,051 unique job IDs. Applying its historical case-insensitive `FDE|forward deploy` title rule matches 212 IDs across 125 employer names. Using word-bounded `FDE` and accepting hyphenated `forward-deploy` titles matches 220 instead. This difference is definition sensitivity, not eight independently verified new vacancies.

The nine per-scrape files contain both geographic duplicates and changing titles. Distinguish these measurements:

| Observation date | Matching listing rows | Matching unique job IDs | All listing rows |
|---|---:|---:|---:|
| 2026-02-04 | 28 | 21 | 1,416 |
| 2026-02-27 | 41 | 33 | 2,057 |
| 2026-03-27 | 58 | 43 | 2,341 |
| 2026-04-22 | 65 | 47 | 2,473 |
| 2026-05-29 | 80 | 59 | 2,751 |
| 2026-06-25 | 108 | 78 | 3,024 |
| 2026-07-22 | 118 | 90 | 3,320 |
| 2026-08-25 | 140 | 103 | 3,946 |
| 2026-09-23 | 127 | 91 | 3,909 |

September's matching row share is 3.2%; its unique-ID share is 2.9% of 3,085 unique IDs. Geographic duplicates do not cancel equally in numerator and denominator. The latest sample declines from August in both measures; do not describe this series as uninterrupted growth.

## A source discrepancy that must remain visible

The union of monthly title matches contains 237 IDs, while the cumulative CSV title matches contain 212. The snapshot lists the 25 scrape-only IDs. Some titles changed; some IDs are absent from the cumulative CSV. Neither count can silently replace the other. A numeric ID can also survive a title change or change on a repost, so unique IDs are not proven unique hiring opportunities.

The upstream root has no license file at the pinned commit. This snapshot contains listing facts and source references, not upstream job-description prose. It grants no permission to redistribute upstream content under this repository's MIT license. Review the source and job-board terms before expanding redistribution.

## Reproduce and validate

From the repository root, validate internal accounting without network access:

```bash
python job-market/dataset/validate_market_snapshot.py
```

For full reproduction, obtain the upstream repository separately. Do not put its checkout inside this repository or assume moving `main` still contains the same data:

```bash
git clone https://github.com/alexeygrigorev/ai-engineering-field-guide.git /tmp/ai-engineering-field-guide
python job-market/dataset/refresh_market_snapshot.py \
  --upstream-dir /tmp/ai-engineering-field-guide \
  --commit ed590319553252e2b8275486597b144ac55a4f3c \
  --retrieved-on 2026-10-09 \
  --output /tmp/reproduced-market.json
python job-market/dataset/validate_market_snapshot.py \
  --upstream-dir /tmp/ai-engineering-field-guide
```

`--retrieved-on` records when these inputs were actually obtained. Preserve 2026-10-09 when reproducing this historical artifact; use the actual retrieval date for a new snapshot. The tool reads immutable Git objects, checks malformed records and future dates, and never invents omitted records. CSV record references are logical records including the header, not physical line numbers.

Offline validation checks internal consistency; it cannot independently authenticate the original job-board capture. Full reproduction additionally checks every published result and checksum against pinned upstream objects. Individual job URLs were not revisited to determine whether the vacancy remains open.

## Historical summary

[fde_market_data.json](fde_market_data.json) preserves the earlier February–July aggregate summary and older externally reported compensation claims. It is not a table of 146 original postings. Its schema validator checks arithmetic and conventions; it does not establish source authenticity, live vacancies, salaries paid, or a worldwide labor-market census.

Historical percentages elsewhere in the guide refer to that older 146-title sample. Do not apply them to the current 212-title cumulative sample. The upstream [extraction audit](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/ed590319553252e2b8275486597b144ac55a4f3c/job-market/_internal/eval/README.md) warns about unsupported inferred fields and evaluation reuse. Salary, skill, seniority, and responsibility estimates were not refreshed in this snapshot.

## Related documents

- [Market overview](../01-market-overview.md) - interpretation and scope limits
- [Repository audit](../../AUDIT.md) - evidence and engineering findings
- [Styling guide](../../STYLING.md) - factual claim standards

## Further reading

- [Pinned upstream CSVs](https://github.com/alexeygrigorev/ai-engineering-field-guide/tree/ed590319553252e2b8275486597b144ac55a4f3c/job-market/_internal/data) - source records and historical snapshots, accessed 2026-10-09
