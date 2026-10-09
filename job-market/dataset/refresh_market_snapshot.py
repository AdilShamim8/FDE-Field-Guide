#!/usr/bin/env python3
"""Recompute factual market observations from immutable upstream Git objects.

No LLM extraction, private credentials, job-description copying, or network requests.
Clone the cited source separately; this tool reads objects at a full commit SHA.
"""

import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_COMMIT = "ed590319553252e2b8275486597b144ac55a4f3c"
SOURCE_REPOSITORY = "https://github.com/alexeygrigorev/ai-engineering-field-guide"
DATA_ROOT = "job-market/_internal/data/"
TITLE_PATTERN = r"FDE|forward deploy"
SENSITIVITY_PATTERN = r"\bFDE\b|forward[\s-]+deploy"


def git(source_dir, *args):
    return subprocess.run(
        ["git", "-C", str(source_dir), *args], check=True, capture_output=True
    ).stdout


def job_id(row):
    parsed = urlparse(row["link"])
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("Job record needs an HTTPS source URL")
    value = row.get("id") or parsed.path.rstrip("/").rsplit("/", 1)[-1]
    if not value.isdigit():
        raise ValueError(f"Job ID is not numeric: {value!r}")
    return value


def build_snapshot(source_dir, commit, retrieved_on):
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Supply a full immutable Git commit SHA")
    verified_date = date.fromisoformat(retrieved_on)
    git(source_dir, "cat-file", "-e", commit + "^{commit}")
    paths = git(source_dir, "ls-tree", "-r", "--name-only", commit, DATA_ROOT).decode().splitlines()
    scrape_paths = sorted(p for p in paths if re.fullmatch(
        re.escape(DATA_ROOT) + r"scrapes/\d{4}-\d{2}-\d{2}/all_jobs\.csv", p
    ))
    if not scrape_paths:
        raise ValueError("Source commit contains no supported scrape snapshots")
    sources = []

    def read(path):
        raw = git(source_dir, "show", f"{commit}:{path}")
        rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
        if not rows or not {"title", "company", "link"}.issubset(rows[0]):
            raise ValueError(f"Empty or unsupported CSV: {path}")
        for row in rows:
            if not row["title"].strip() or not row["company"].strip():
                raise ValueError(f"Missing title or employer: {path}")
            job_id(row)
        sources.append({
            "path": path,
            "url": f"{SOURCE_REPOSITORY}/blob/{commit}/{path}",
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw), "rows": len(rows),
        })
        return rows

    matches = lambda row: bool(re.search(TITLE_PATTERN, row["title"], re.IGNORECASE))
    trend = []
    for path in scrape_paths:
        observed_on = path.split("/")[-2]
        if date.fromisoformat(observed_on) > verified_date:
            raise ValueError("Observation date is later than retrieval date")
        rows = read(path)
        matched = [r for r in rows if matches(r)]
        all_ids = {job_id(r) for r in rows}
        fde_ids = sorted({job_id(r) for r in matched})
        trend.append({
            "observed_on": observed_on, "source_path": path,
            "all_listing_rows": len(rows), "all_unique_job_ids": len(all_ids),
            "fde_listing_rows": len(matched), "fde_unique_job_ids": len(fde_ids),
            "fde_row_share_percentage": round(len(matched) / len(rows) * 100, 1),
            "fde_unique_share_percentage": round(len(fde_ids) / len(all_ids) * 100, 1),
            "fde_job_ids": fde_ids,
        })

    cumulative_path = DATA_ROOT + "all_jobs_dedup.csv"
    rows = read(cumulative_path)
    if len({job_id(r) for r in rows}) != len(rows):
        raise ValueError("Cumulative source has duplicate job IDs")
    records = []
    for source_row, row in enumerate(rows, start=2):
        if not matches(row):
            continue
        observed = row.get("scraped_date", "")
        if not observed or date.fromisoformat(observed) > verified_date:
            raise ValueError("Missing or future source observation date")
        records.append({
            "job_id": job_id(row), "title": row["title"], "company": row["company"],
            "source_observed_on": observed, "job_url": row["link"],
            "source_path": cumulative_path, "source_csv_record_number": source_row,
        })
    cumulative_ids = {r["job_id"] for r in records}
    observed_ids = {i for sample in trend for i in sample["fde_job_ids"]}
    employers = Counter(r["company"] for r in records)
    sensitivity_count = sum(bool(re.search(SENSITIVITY_PATTERN, r["title"], re.IGNORECASE)) for r in rows)
    return {
        "metadata": {
            "schema_version": 1, "retrieved_on": retrieved_on,
            "source_repository": SOURCE_REPOSITORY, "source_commit": commit,
            "collection_start": trend[0]["observed_on"], "collection_end": trend[-1]["observed_on"],
            "status": "source-derived observations; job URLs not revalidated as live vacancies",
            "rights": "Factual listing metadata only; upstream has no root license file at this commit. No job descriptions or source files redistributed; do not infer a license grant for upstream materials.",
        },
        "methodology": {
            "title_pattern": TITLE_PATTERN, "case_sensitive": False,
            "deduplication_key": "numeric job ID; derive from final URL path segment when ID field is absent",
            "csv_record_number": "1-based logical CSV record number including header; not a physical line number",
            "scope": "source's builtin.com scrape coverage, not a worldwide census",
            "limitations": [
                "Distinct job IDs can still describe repostings of one vacancy.",
                "Location duplicates inflate listing-row counts; unique IDs are reported separately.",
                "Title matching misses equivalent work under other titles and can include adjacent roles.",
                "No current salary, responsibility, skill, hiring-conversion, or seniority inference is made.",
                "The cumulative CSV and monthly ID union differ; reconciliation reports this source discrepancy without inventing missing records.",
                "Collection dates are historical; retrieval today does not create a today-only scrape.",
            ],
        },
        "sources": sources, "trend": trend,
        "source_reconciliation": {
            "scrape_union_unique_fde_ids": len(observed_ids),
            "cumulative_unique_fde_ids": len(cumulative_ids),
            "scrape_only_ids": sorted(observed_ids - cumulative_ids),
            "cumulative_only_ids": sorted(cumulative_ids - observed_ids),
        },
        "summary": {
            "all_unique_job_ids": len(rows), "fde_unique_job_ids": len(records),
            "fde_unique_employer_names": len(employers),
            "top_employers": [{"company": name, "unique_job_ids": count}
                              for name, count in sorted(employers.items(), key=lambda x: (-x[1], x[0]))[:10]],
        },
        "title_sensitivity": {"alternative_pattern": SENSITIVITY_PATTERN,
                              "alternative_unique_job_ids": sensitivity_count},
        "records": records,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream-dir", type=Path, required=True)
    parser.add_argument("--commit", default=DEFAULT_COMMIT)
    parser.add_argument("--retrieved-on", required=True, help="Actual retrieval date, YYYY-MM-DD")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build_snapshot(args.upstream_dir, args.commit, args.retrieved_on)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
