"""
Inspect legacy regression fixture structure.
This file contains no source acquisition or reproducible curation pipeline.
It cannot authenticate CFPB, Bitext, or external policy provenance.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List


def scrub_pii(text: str) -> str:
    """
    Deterministic PII scrubbing utility:
    Masks a few identifier patterns. Names, addresses, indirect identifiers, and
    many international formats remain; this is not validated anonymization.
    """
    # Scrub credit cards / long digits
    text = re.sub(r"\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b", "[REDACTED_CARD]", text)
    # Scrub Social Security Numbers
    text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]", text)
    # Scrub email addresses
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[REDACTED_EMAIL]", text)
    # Scrub telephone numbers
    text = re.sub(r"\b(\+?1[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b", "[REDACTED_PHONE]", text)
    return text


def verify_golden_dataset(dataset_path: Path) -> Dict[str, Any]:
    """
    Validates golden dataset integrity, schema completeness, and provenance fields.
    """
    if not dataset_path.exists():
        raise FileNotFoundError(f"Golden dataset not found at {dataset_path}")

    with open(dataset_path, "r", encoding="utf-8") as f:
        cases: List[Dict[str, Any]] = json.load(f)

    if not isinstance(cases, list) or not cases:
        raise ValueError("Require a nonempty case list")
    seen_ids = set()
    report = {
        "total_cases": len(cases),
        "categories": {},
        "severities": {},
        "routings": {},
        "grounding_docs": {},
        "evidence_statuses": {},
        "provenance_authenticated": False,
    }

    required_fields = [
        "id",
        "ticket_id",
        "account_id",
        "raw_text",
        "expected_category",
        "expected_severity",
        "expected_routing",
    ]

    for idx, case in enumerate(cases):
        if case.get("id") in seen_ids:
            raise ValueError("Duplicate case ID")
        seen_ids.add(case.get("id"))
        for field in required_fields:
            if field not in case:
                raise ValueError(f"Case index {idx} ({case.get('id')}) missing mandatory field: {field}")

        evidence = case.get("evidence_status", "unspecified")
        report["evidence_statuses"][evidence] = report["evidence_statuses"].get(evidence, 0) + 1
        cat = case["expected_category"]
        sev = case["expected_severity"]
        routing = case["expected_routing"]
        doc = case.get("expected_citation_doc")

        report["categories"][cat] = report["categories"].get(cat, 0) + 1
        report["severities"][sev] = report["severities"].get(sev, 0) + 1
        report["routings"][routing] = report["routings"].get(routing, 0) + 1
        if doc:
            report["grounding_docs"][doc] = report["grounding_docs"].get(doc, 0) + 1

    return report


if __name__ == "__main__":
    golden_path = Path(__file__).parent / "golden_dataset.json"
    verification = verify_golden_dataset(golden_path)
    print("======================================================================")
    print("LEGACY REGRESSION FIXTURE STRUCTURE REPORT")
    print("======================================================================")
    print(f"Total Regression Cases: {verification['total_cases']}")
    print(f"Category Distribution:     {json.dumps(verification['categories'])}")
    print(f"Severity Distribution:     {json.dumps(verification['severities'])}")
    print(f"Routing Distribution:      {json.dumps(verification['routings'])}")
    print(f"Knowledge Documents:       {json.dumps(verification['grounding_docs'])}")
    print("======================================================================")
    print(f"Evidence Statuses: {json.dumps(verification["evidence_statuses"])}")
    print("Structure checks passed. Source provenance is not authenticated.")
