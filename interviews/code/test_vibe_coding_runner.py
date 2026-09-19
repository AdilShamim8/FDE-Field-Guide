"""
Unit tests for Google FDE Vibe Coding Integration Runner.
Validates defensive parsing, rate limiting backpressure, and defect ledger accuracy.
"""

from datetime import datetime, timezone
import pytest

from interviews.code.vibe_coding_runner import (
    EnterpriseRecord,
    VibeCodingPipeline,
    VibeCodingRunResult,
)


def test_clean_record_processing():
    pipeline = VibeCodingPipeline(tenant_quota_per_sec=10)
    batch = [
        {
            "id": "rec_001",
            "tenant_id": "cust_alpha",
            "amount": 15000,
            "currency": "USD",
            "timestamp": "2026-09-19T10:00:00Z",
        }
    ]
    result = pipeline.run_batch(batch)
    assert result.total_processed == 1
    assert len(result.valid_records) == 1
    assert len(result.rejected_records) == 0
    rec = result.valid_records[0]
    assert rec.record_id == "rec_001"
    assert rec.amount_cents == 15000
    assert rec.currency == "USD"
    assert rec.repaired is False


def test_dirty_amount_and_timestamp_repair():
    pipeline = VibeCodingPipeline(tenant_quota_per_sec=10)
    batch = [
        {
            "id": "rec_dirty_01",
            "tenant_id": "cust_beta",
            "amount": " $1,250.75 ",
            "currency": "usd",
            "timestamp": 1789725600,  # epoch seconds
        },
        {
            "id": "rec_dirty_02",
            "tenant_id": "cust_beta",
            "amount": 49.99,  # float dollars
            "currency": "INVALID_CODE",
            "timestamp": None,
        },
    ]
    result = pipeline.run_batch(batch)
    assert len(result.valid_records) == 2
    rec1 = result.valid_records[0]
    assert rec1.amount_cents == 125075
    assert rec1.currency == "USD"
    assert rec1.repaired is True
    assert "repaired_string_dollars_to_cents" in rec1.repair_notes

    rec2 = result.valid_records[1]
    assert rec2.amount_cents == 4999
    assert rec2.currency == "USD"
    assert rec2.repaired is True
    assert "repaired_default_currency_usd" in rec2.repair_notes


def test_missing_id_and_unparseable_rejections():
    pipeline = VibeCodingPipeline(tenant_quota_per_sec=10)
    batch = [
        {"amount": 100},  # missing id
        {"id": "rec_bad_amt", "amount": "NOT_A_NUMBER"},
    ]
    result = pipeline.run_batch(batch)
    assert len(result.valid_records) == 0
    assert len(result.rejected_records) == 2
    assert "missing_record_id" in result.defect_counts
    assert "unparseable_amount" in result.defect_counts


def test_tenant_rate_limiting_backpressure():
    fake_time = 1000.0
    pipeline = VibeCodingPipeline(tenant_quota_per_sec=2, now_fn=lambda: fake_time)

    batch = [
        {"id": f"rec_{i}", "tenant_id": "tenant_flood", "amount": 100}
        for i in range(5)
    ]
    result = pipeline.run_batch(batch)
    # Only 2 should pass within the immediate bucket
    assert len(result.valid_records) == 2
    assert len(result.rate_limited_records) == 3
    assert result.defect_counts.get("rate_limit_exceeded") == 3
