"""
Unit tests for defensive customer export parser.
"""

from datetime import datetime
from parser import parse_customer_export


def test_clean_export():
    csv_data = b"record_id,customer_name,amount,timestamp\nREC-001,Acme Corp,1250.50,2026-09-18T10:00:00Z\n"
    records, report = parse_customer_export(csv_data)
    assert len(records) == 1
    assert report.total_raw_records == 1
    assert report.valid_records == 1
    assert report.dropped_records == 0
    assert records[0]["record_id"] == "REC-001"
    assert records[0]["amount"] == 1250.50
    assert records[0]["timestamp"] == datetime(2026, 9, 18, 10, 0, 0)


def test_messy_export_repairs_and_drops():
    csv_data = (
        "id,name,total,date\n"
        # Contains non-UTF8 byte in CP1252 (e.g. accented e: \xe9)
        "REC-101,Global Log\xe9stics,\"$4,500.00\",2026-08-01\n"  # Repaired currency & format
        "REC-102,,120.00,2026-08-02\n"                        # Dropped: empty name
        "REC-101,Duplicate ID,50.00,2026-08-03\n"              # Dropped: duplicate id
        "REC-103,Beta LLC,invalid_num,2026-08-04\n"            # Dropped: invalid amount
        ",No ID Company,300.00,2026-08-05\n"                   # Dropped: missing PK
        "REC-104,Delta Co,750.25,bad_date\n"                   # Dropped: invalid timestamp
    ).encode("cp1252")

    records, report = parse_customer_export(csv_data)
    assert len(records) == 1
    assert report.total_raw_records == 6
    assert report.valid_records == 1
    assert report.repaired_records == 1
    assert report.dropped_records == 5

    assert records[0]["record_id"] == "REC-101"
    assert records[0]["amount"] == 4500.00

    assert "non_standard_encoding_cp1252" in report.defect_counts
    assert report.defect_counts["empty_customer_name"] == 1
    assert report.defect_counts["duplicate_primary_key"] == 1
    assert report.defect_counts["invalid_numeric_amount"] == 1
    assert report.defect_counts["missing_primary_key"] == 1
    assert report.defect_counts["invalid_or_missing_timestamp"] == 1
