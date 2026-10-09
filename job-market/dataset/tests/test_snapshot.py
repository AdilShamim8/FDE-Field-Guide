"""Regression mutations of the committed source-derived snapshot."""

import copy
import json
import sys
from pathlib import Path

import pytest

DATASET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DATASET))
from validate_market_snapshot import validate_snapshot

SNAPSHOT = json.loads((DATASET / "market_snapshot_2026-10-09.json").read_text())


def test_source_derived_snapshot_accounting():
    assert validate_snapshot(SNAPSHOT) == 212
    assert SNAPSHOT["trend"][-1]["fde_listing_rows"] == 127
    assert SNAPSHOT["trend"][-1]["fde_unique_job_ids"] == 91
    assert len(SNAPSHOT["source_reconciliation"]["scrape_only_ids"]) == 25


@pytest.mark.parametrize("defect", ["duplicate", "employer", "future", "share", "union", "unpinned", "empty"])
def test_corrupted_accounting_is_rejected(defect):
    snapshot = copy.deepcopy(SNAPSHOT)
    if defect == "duplicate":
        snapshot["records"][1]["job_id"] = snapshot["records"][0]["job_id"]
    elif defect == "employer":
        snapshot["summary"]["fde_unique_employer_names"] += 1
    elif defect == "future":
        snapshot["records"][0]["source_observed_on"] = "2099-01-01"
    elif defect == "share":
        snapshot["trend"][-1]["fde_unique_share_percentage"] += 1
    elif defect == "union":
        snapshot["source_reconciliation"]["scrape_only_ids"] = []
    elif defect == "unpinned":
        snapshot["metadata"]["source_commit"] = "main"
    elif defect == "empty":
        snapshot["records"] = []
    with pytest.raises(ValueError):
        validate_snapshot(snapshot)
