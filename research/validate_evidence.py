#!/usr/bin/env python3
"""Check source-ledger structure and retained real-data metadata offline.

This checks local accounting, not independent source authenticity or licensing.
"""

import hashlib
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_cfpb(snapshot):
    metadata = snapshot["metadata"]
    captured = date.fromisoformat(metadata["retrieved_on"])
    source = metadata["source"]
    require(source["url"].startswith("https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/?"), "Unexpected complaint API source")
    require(re.fullmatch(r"[0-9a-f]{64}", source["response_sha256"]), "Missing source response digest")
    require(source["retrieved_on"] == metadata["retrieved_on"], "Capture date mismatch")
    records = snapshot["records"]
    require(bool(records), "Empty complaint sample")
    expected = {"complaint_id", "date_received", "product", "sub_product", "issue", "sub_issue", "company", "submitted_via", "company_response", "timely"}
    seen = set()
    for record in records:
        require(set(record) == expected, "Unexpected or missing retained metadata fields")
        ident = str(record["complaint_id"])
        require(ident.isdigit() and ident not in seen, "Duplicate or invalid complaint ID")
        seen.add(ident)
        stamp = datetime.fromisoformat(record["date_received"].replace("Z", "+00:00"))
        require(stamp.tzinfo is not None and stamp.astimezone(timezone.utc).date() == captured, "Complaint not received on the source capture date")
        require(all(isinstance(record[key], str) and record[key].strip() for key in ["product", "issue", "company"]), "Missing categorical label")
    return len(records)


def validate_source_ledger(ledger):
    date.fromisoformat(ledger["checked_on"])
    require(ledger["schema_version"] == 1 and ledger["checks"], "Empty or unsupported source ledger")
    seen = set()
    passed = failed = 0
    for check in ledger["checks"]:
        require(check["id"] not in seen, "Duplicate source check")
        seen.add(check["id"])
        require(check["checked_on"] == ledger["checked_on"], "Check date mismatch")
        require(check["observations"] and check["verification_scope"], "Missing verification limits")
        if check.get("status") == 200:
            checksum = check.get("sha256") or check.get("response_sha256")
            require(re.fullmatch(r"[0-9a-f]{64}", checksum or ""), "Successful retrieval without content digest")
            passed += 1
        else:
            require(check.get("error"), "Unexplained retrieval outcome")
            failed += 1
    return passed, failed


def validate_saved_evidence(root):
    """Include every dated artifact so new reviews cannot silently skip CI."""
    ledgers = sorted((root / "research").glob("source_checks_*.json"))
    samples = sorted((root / "portfolio/reference-project/evals/real_data").glob("cfpb_metadata_*.json"))
    require(bool(ledgers), "No source ledgers discovered")
    require(bool(samples), "No CFPB metadata samples discovered")
    reports = []
    for path in ledgers:
        passed, failed = validate_source_ledger(json.loads(path.read_text(encoding="utf-8")))
        reports.append({"file": path.name, "kind": "source_ledger", "successful": passed, "failed": failed})
    for path in samples:
        count = validate_cfpb(json.loads(path.read_text(encoding="utf-8")))
        reports.append({"file": path.name, "kind": "cfpb_metadata", "records": count})
    return reports


def main():
    for report in validate_saved_evidence(ROOT):
        if report["kind"] == "source_ledger":
            print(f"{report['file']}: {report['successful']} successful retrievals, {report['failed']} explicitly failed retrievals.")
        else:
            print(f"{report['file']}: {report['records']} unique source-date metadata records; restricted field projection checked.")
    print("Offline structure checks passed; live sources and licenses are not refetched by this command.")


if __name__ == "__main__":
    main()
