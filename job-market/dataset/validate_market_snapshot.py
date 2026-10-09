#!/usr/bin/env python3
"""Validate snapshot accounting offline; optionally reproduce pinned source objects."""

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

from refresh_market_snapshot import SOURCE_REPOSITORY, TITLE_PATTERN, build_snapshot


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_snapshot(snapshot):
    meta = snapshot["metadata"]
    retrieved = date.fromisoformat(meta["retrieved_on"])
    require(meta["schema_version"] == 1, "Unsupported snapshot schema")
    require(re.fullmatch(r"[0-9a-f]{40}", meta["source_commit"]), "Unpinned source")
    require(meta["source_repository"] == SOURCE_REPOSITORY, "Unexpected source repository")
    require(snapshot["methodology"]["title_pattern"] == TITLE_PATTERN, "Title definition changed")
    sources = {s["path"]: s for s in snapshot["sources"]}
    require(len(sources) == len(snapshot["sources"]), "Duplicate source path")
    for source in sources.values():
        require(re.fullmatch(r"[0-9a-f]{64}", source["sha256"]), "Invalid source checksum")
        require(source["bytes"] > 0 and source["rows"] > 0, "Empty source")
        require(source["url"] == f'{SOURCE_REPOSITORY}/blob/{meta["source_commit"]}/{source["path"]}', "Source URL is not pinned")

    records = snapshot["records"]
    require(bool(records), "Empty FDE record collection")
    ids = set()
    for record in records:
        require(record["job_id"].isdigit() and record["job_id"] not in ids, "Invalid or duplicate job ID")
        ids.add(record["job_id"])
        require(bool(re.search(TITLE_PATTERN, record["title"], re.I)), "Record does not match title definition")
        require(record["company"].strip(), "Missing employer")
        observed = date.fromisoformat(record["source_observed_on"])
        require(date.fromisoformat(meta["collection_start"]) <= observed <= date.fromisoformat(meta["collection_end"]) <= retrieved, "Observation outside collection window")
        source = sources[record["source_path"]]
        require(2 <= record["source_csv_record_number"] <= source["rows"] + 1, "Invalid logical CSV record number")
        require(record["job_url"].startswith("https://"), "Invalid record URL")

    employers = Counter(r["company"] for r in records)
    summary = snapshot["summary"]
    require(summary["fde_unique_job_ids"] == len(ids), "Cumulative count mismatch")
    require(summary["fde_unique_employer_names"] == len(employers), "Employer count mismatch")
    cumulative_source = sources[records[0]["source_path"]]
    require(summary["all_unique_job_ids"] == cumulative_source["rows"], "Cumulative source row mismatch")
    expected_top = [{"company": n, "unique_job_ids": c} for n, c in sorted(employers.items(), key=lambda x: (-x[1], x[0]))[:10]]
    require(summary["top_employers"] == expected_top, "Employer ranking mismatch")
    trend = snapshot["trend"]
    require(bool(trend), "No scrape observations")
    dates = [s["observed_on"] for s in trend]
    require(dates == sorted(set(dates)), "Unordered or duplicate scrape dates")
    require((dates[0], dates[-1]) == (meta["collection_start"], meta["collection_end"]), "Collection bounds mismatch")
    union = set()
    for sample in trend:
        require(date.fromisoformat(sample["observed_on"]) <= retrieved, "Future scrape")
        require(sample["all_listing_rows"] == sources[sample["source_path"]]["rows"], "Scrape source row mismatch")
        require(0 < sample["all_unique_job_ids"] <= sample["all_listing_rows"], "Invalid denominator")
        require(0 <= sample["fde_unique_job_ids"] <= sample["fde_listing_rows"] <= sample["all_listing_rows"], "Invalid FDE counts")
        sample_ids = sample["fde_job_ids"]
        require(len(set(sample_ids)) == len(sample_ids) == sample["fde_unique_job_ids"], "Scrape ID count mismatch")
        require(sample["fde_row_share_percentage"] == round(sample["fde_listing_rows"] / sample["all_listing_rows"] * 100, 1), "Row share mismatch")
        require(sample["fde_unique_share_percentage"] == round(sample["fde_unique_job_ids"] / sample["all_unique_job_ids"] * 100, 1), "Unique share mismatch")
        union.update(sample_ids)
    require(snapshot["source_reconciliation"] == {
        "scrape_union_unique_fde_ids": len(union), "cumulative_unique_fde_ids": len(ids),
        "scrape_only_ids": sorted(union - ids), "cumulative_only_ids": sorted(ids - union),
    }, "Source reconciliation mismatch")
    return len(records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=Path(__file__).with_name("market_snapshot_2026-10-09.json"))
    parser.add_argument("--upstream-dir", type=Path)
    args = parser.parse_args()
    snapshot = json.loads(args.path.read_text(encoding="utf-8"))
    count = validate_snapshot(snapshot)
    if args.upstream_dir:
        meta = snapshot["metadata"]
        reproduced = build_snapshot(args.upstream_dir, meta["source_commit"], meta["retrieved_on"])
        require(reproduced == snapshot, "Snapshot differs from pinned upstream Git objects")
        print("Pinned source reproduction passed, including all SHA-256 hashes.")
    else:
        print("Offline accounting passed; source hashes are recorded but not refetched.")
    print(f"Validated {count} cumulative title matches; source discrepancies remain explicit.")


if __name__ == "__main__":
    main()
