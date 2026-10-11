"""A small, offline JSON-to-SQL exercise using retained CFPB metadata.

Run from any directory. This reads source categories; it does not classify
complaints, adjudicate them, or assign ETISE severity/routing labels.
"""

import argparse
from collections import Counter
from contextlib import closing
import hashlib
import json
from pathlib import Path
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

# Reuse the repository's existing sample contract rather than duplicate it.
from research.validate_evidence import validate_cfpb

DEFAULT_SNAPSHOT = (
    ROOT / "portfolio/reference-project/evals/real_data/cfpb_metadata_2026-10-09.json"
)


def load_snapshot(path):
    """Reject invalid or empty samples before creating a database."""
    snapshot = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_cfpb(snapshot)
    return snapshot


def summarize(snapshot):
    """Count observed source categories without inventing quality labels."""
    records = snapshot["records"]
    return {
        "records_read": len(records),
        "received_date_utc": snapshot["metadata"]["retrieved_on"],
        "products": dict(sorted(Counter(row["product"] for row in records).items())),
        "source_response_sha256": snapshot["metadata"]["source"]["response_sha256"],
        "evidence_limit": "Small selected metadata sample; not representative or independently adjudicated",
    }


def store_snapshot(snapshot, database):
    """Import a four-field projection atomically; unchanged IDs replay safely.

    A changed projection for an existing ID is a conflict, not a silent update.
    The first capture's response digest stays attached to the stored row.
    This is local SQLite behavior, not a distributed delivery guarantee.
    """
    validate_cfpb(snapshot)
    database = Path(database)
    database.parent.mkdir(parents=True, exist_ok=True)
    digest = snapshot["metadata"]["source"]["response_sha256"]
    inserted = replayed = 0
    with closing(sqlite3.connect(database)) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                complaint_id TEXT PRIMARY KEY,
                received_at TEXT NOT NULL,
                product TEXT NOT NULL,
                issue TEXT NOT NULL,
                source_response_sha256 TEXT NOT NULL
            )
        """)
        with connection:
            for record in snapshot["records"]:
                values = (
                    str(record["complaint_id"]), record["date_received"],
                    record["product"], record["issue"],
                )
                existing = connection.execute(
                    "SELECT complaint_id, received_at, product, issue FROM complaints WHERE complaint_id = ?",
                    (values[0],),
                ).fetchone()
                if existing is not None:
                    if existing != values:
                        raise ValueError(f"Conflicting projection for complaint ID {values[0]}")
                    replayed += 1
                    continue
                connection.execute(
                    "INSERT INTO complaints VALUES (?, ?, ?, ?, ?)", (*values, digest),
                )
                inserted += 1
        total = connection.execute("SELECT COUNT(*) FROM complaints").fetchone()[0]
        products = dict(connection.execute(
            "SELECT product, COUNT(*) FROM complaints GROUP BY product ORDER BY product"
        ).fetchall())
    return {"inserted": inserted, "replayed": replayed, "total_stored": total, "products": products}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--db", type=Path, help="Optional local SQLite destination; omit for a read-only summary")
    args = parser.parse_args(argv)
    try:
        snapshot = load_snapshot(args.snapshot)
        report = summarize(snapshot)
        report["snapshot_sha256"] = hashlib.sha256(args.snapshot.read_bytes()).hexdigest()
        if args.db is not None:
            report["database"] = store_snapshot(snapshot, args.db)
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error) as error:
        print(f"Input/import failed: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
