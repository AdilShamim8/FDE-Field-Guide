"""Real-data happy paths and authored mutations test the import contract.

Mutated inputs below are not additional observations or classifier labels.
"""

import copy
import json
from pathlib import Path
import sqlite3
import subprocess
import sys

import pytest

from complaint_pipeline import DEFAULT_SNAPSHOT, load_snapshot, store_snapshot, summarize

SCRIPT = Path(__file__).with_name("complaint_pipeline.py")


@pytest.fixture
def snapshot():
    return load_snapshot(DEFAULT_SNAPSHOT)


def test_actual_metadata_summary_preserves_observation_date(snapshot):
    report = summarize(snapshot)
    assert report["received_date_utc"] == "2026-10-09"
    assert report["records_read"] == 5
    assert report["products"] == {"Credit reporting or other personal consumer reports": 5}
    assert report["source_response_sha256"] == snapshot["metadata"]["source"]["response_sha256"]


def test_repeated_import_does_not_duplicate_source_ids(snapshot, tmp_path):
    database = tmp_path / "complaints.sqlite"
    first = store_snapshot(snapshot, database)
    second = store_snapshot(snapshot, database)
    assert first["inserted"] == first["total_stored"] == 5
    assert second["inserted"] == 0
    assert second["replayed"] == second["total_stored"] == 5
    with sqlite3.connect(database) as connection:
        assert connection.execute("SELECT COUNT(DISTINCT source_response_sha256) FROM complaints").fetchone()[0] == 1


def test_changed_existing_row_rolls_back_earlier_new_row(snapshot, tmp_path):
    database = tmp_path / "complaints.sqlite"
    store_snapshot(snapshot, database)
    mutated = copy.deepcopy(snapshot)
    new_record = dict(mutated["records"][0], complaint_id="99999999")
    mutated["records"].insert(0, new_record)
    mutated["records"][-1]["issue"] = "Authored conflicting issue"
    with pytest.raises(ValueError, match="Conflicting projection"):
        store_snapshot(mutated, database)
    with sqlite3.connect(database) as connection:
        assert connection.execute("SELECT COUNT(*) FROM complaints").fetchone()[0] == 5
        assert connection.execute("SELECT COUNT(*) FROM complaints WHERE complaint_id = ?", ("99999999",)).fetchone()[0] == 0


def test_sql_characters_are_stored_as_data(snapshot, tmp_path):
    mutated = copy.deepcopy(snapshot)
    text = "Customer's issue'); DROP TABLE complaints; --"
    mutated["records"][0]["issue"] = text
    database = tmp_path / "complaints.sqlite"
    store_snapshot(mutated, database)
    with sqlite3.connect(database) as connection:
        assert connection.execute("SELECT issue FROM complaints WHERE complaint_id = ?", (str(mutated["records"][0]["complaint_id"]),)).fetchone()[0] == text
        assert connection.execute("SELECT COUNT(*) FROM complaints").fetchone()[0] == 5


@pytest.mark.parametrize("defect", ["empty", "duplicate", "wrong_date", "narrative", "missing_digest"])
def test_invalid_input_is_rejected_before_database_creation(snapshot, tmp_path, defect):
    mutated = copy.deepcopy(snapshot)
    if defect == "empty":
        mutated["records"] = []
    elif defect == "duplicate":
        mutated["records"].append(mutated["records"][0])
    elif defect == "wrong_date":
        mutated["records"][0]["date_received"] = "2026-10-11T00:00:00Z"
    elif defect == "narrative":
        mutated["records"][0]["consumer_complaint_narrative"] = "Authored extra field"
    else:
        mutated["metadata"]["source"]["response_sha256"] = ""
    database = tmp_path / "complaints.sqlite"
    with pytest.raises(ValueError):
        store_snapshot(mutated, database)
    assert not database.exists()


def test_cli_runs_outside_checkout_and_is_read_only_by_default(tmp_path):
    result = subprocess.run([sys.executable, str(SCRIPT)], cwd=tmp_path, capture_output=True, text=True, check=True)
    report = json.loads(result.stdout)
    assert report["records_read"] == 5
    assert "database" not in report
    assert list(tmp_path.iterdir()) == []


def test_cli_invalid_json_exits_nonzero_without_database(tmp_path):
    invalid = tmp_path / "invalid.json"
    invalid.write_text("{invalid JSON}")
    database = tmp_path / "complaints.sqlite"
    result = subprocess.run([sys.executable, str(SCRIPT), "--snapshot", str(invalid), "--db", str(database)], capture_output=True, text=True)
    assert result.returncode == 2
    assert "Input/import failed" in result.stderr
    assert not database.exists()
