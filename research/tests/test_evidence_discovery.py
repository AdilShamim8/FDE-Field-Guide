"""A later dated artifact must be checked rather than silently ignored."""

import json
from pathlib import Path
import shutil
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from research.validate_evidence import validate_saved_evidence


def prepare(root):
    (root / "research").mkdir()
    samples = root / "portfolio/reference-project/evals/real_data"
    samples.mkdir(parents=True)
    shutil.copyfile(ROOT / "research/source_checks_2026-10-09.json", root / "research/source_checks_2026-10-09.json")
    shutil.copyfile(ROOT / "portfolio/reference-project/evals/real_data/cfpb_metadata_2026-10-09.json", samples / "cfpb_metadata_2026-10-09.json")


def test_all_dated_ledgers_are_included(tmp_path):
    prepare(tmp_path)
    shutil.copyfile(ROOT / "research/source_checks_2026-10-11.json", tmp_path / "research/source_checks_2026-10-11.json")
    reports = validate_saved_evidence(tmp_path)
    assert {r["file"] for r in reports} == {
        "source_checks_2026-10-09.json", "source_checks_2026-10-11.json", "cfpb_metadata_2026-10-09.json",
    }


def test_bad_new_ledger_fails_even_when_the_old_ledger_is_valid(tmp_path):
    prepare(tmp_path)
    ledger = json.loads((ROOT / "research/source_checks_2026-10-11.json").read_text())
    next(c for c in ledger["checks"] if c.get("status") == 200)["sha256"] = "invalid digest"
    (tmp_path / "research/source_checks_2026-10-11.json").write_text(json.dumps(ledger))
    with pytest.raises(ValueError, match="without content digest"):
        validate_saved_evidence(tmp_path)


def test_empty_artifact_inventory_cannot_pass(tmp_path):
    with pytest.raises(ValueError, match="No source ledgers"):
        validate_saved_evidence(tmp_path)
