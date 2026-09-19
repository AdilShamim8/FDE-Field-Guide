"""
Google FDE "Vibe Coding" / Rapid Live Build Integration Runner.
Verified Source: YagyanshB Google FDE Prep Guide (github.com/YagyanshB/google-fde-interview-guide)
and Om Bharatiya AI Engineer Interview Questions (github.com/ombharatiya).

Simulates the 60-minute practical live build scenario:
1. Ingests dirty enterprise customer payloads (mixed JSON/CSV, missing keys, type inconsistencies).
2. Sanitizes, normalizes, and validates against a target schema.
3. Enforces tenant token rate limits and backpressure defense.
4. Produces a comprehensive run ledger with defect counts, repaired records, and trace IDs.
"""

import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class EnterpriseRecord:
    record_id: str
    tenant_id: str
    amount_cents: int
    currency: str
    event_timestamp: datetime
    raw_payload: Dict[str, Any]
    repaired: bool = False
    repair_notes: List[str] = field(default_factory=list)


@dataclass
class VibeCodingRunResult:
    total_processed: int = 0
    valid_records: List[EnterpriseRecord] = field(default_factory=list)
    rejected_records: List[Dict[str, Any]] = field(default_factory=list)
    rate_limited_records: List[Dict[str, Any]] = field(default_factory=list)
    defect_counts: Dict[str, int] = field(default_factory=dict)
    execution_time_ms: float = 0.0

    def record_defect(self, defect_type: str) -> None:
        self.defect_counts[defect_type] = self.defect_counts.get(defect_type, 0) + 1


class VibeCodingPipeline:
    """
    Production-grade rapid integration pipeline designed for live technical interviews.
    Emphasizes testable seams, defensive validation, and explicit defect accounting.
    """

    def __init__(self, tenant_quota_per_sec: int = 50, now_fn=None):
        self.tenant_quota_per_sec = tenant_quota_per_sec
        self.now_fn = now_fn or (lambda: time.time())
        self._tenant_buckets: Dict[str, Tuple[float, int]] = {}

    def _check_rate_limit(self, tenant_id: str) -> bool:
        """
        Token-bucket rate limiter to simulate upstream API/tenant boundary protection.
        """
        now = self.now_fn()
        last_check, tokens = self._tenant_buckets.get(tenant_id, (now, self.tenant_quota_per_sec))
        elapsed = now - last_check
        tokens = min(self.tenant_quota_per_sec, tokens + int(elapsed * self.tenant_quota_per_sec))
        if tokens > 0:
            self._tenant_buckets[tenant_id] = (now, tokens - 1)
            return True
        self._tenant_buckets[tenant_id] = (now, 0)
        return False

    def sanitize_amount(self, raw_val: Any) -> Tuple[Optional[int], Optional[str]]:
        """
        Handles dirty amounts (e.g. '$1,250.50', '1250.5', 125050, None).
        Returns (amount_in_cents, repair_note).
        """
        if raw_val is None or raw_val == "":
            return None, "missing_amount"

        if isinstance(raw_val, (int, float)):
            # If floating point dollars, convert to cents
            if isinstance(raw_val, float):
                return int(round(raw_val * 100)), "repaired_float_to_cents"
            # If int, assume cents if > 1000 or treat as dollars based on threshold
            return int(raw_val), None

        if isinstance(raw_val, str):
            clean = raw_val.strip().replace("$", "").replace(",", "").strip()
            try:
                if "." in clean:
                    val = float(clean)
                    return int(round(val * 100)), "repaired_string_dollars_to_cents"
                else:
                    val = int(clean)
                    return val, "repaired_string_int"
            except ValueError:
                return None, "unparseable_amount"

        return None, "invalid_amount_type"

    def parse_timestamp(self, raw_val: Any) -> Tuple[datetime, Optional[str]]:
        """
        Normalizes mixed timestamp formats (ISO-8601, epoch seconds, epoch millis).
        """
        if raw_val is None:
            return datetime.now(timezone.utc), "repaired_missing_ts_with_current_utc"

        if isinstance(raw_val, (int, float)):
            # Distinguish epoch seconds vs milliseconds
            if raw_val > 1e11:
                return datetime.fromtimestamp(raw_val / 1000.0, tz=timezone.utc), "repaired_epoch_millis"
            return datetime.fromtimestamp(raw_val, tz=timezone.utc), "repaired_epoch_seconds"

        if isinstance(raw_val, str):
            for fmt in [
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d",
            ]:
                try:
                    dt = datetime.strptime(raw_val.strip(), fmt)
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    return dt, None
                except ValueError:
                    continue
            # Try fromisoformat as fallback
            try:
                dt = datetime.fromisoformat(raw_val.strip().replace("Z", "+00:00"))
                return dt, "repaired_iso_fallback"
            except ValueError:
                return datetime.now(timezone.utc), "repaired_unparseable_ts_with_now"

        return datetime.now(timezone.utc), "repaired_unknown_ts_type"

    def process_record(self, raw: Dict[str, Any], result: VibeCodingRunResult) -> None:
        """
        Processes an individual record with schema validation and error handling.
        """
        record_id = str(raw.get("id") or raw.get("record_id") or "")
        tenant_id = str(raw.get("tenant_id") or raw.get("customer_id") or "DEFAULT_TENANT")

        if not record_id:
            result.record_defect("missing_record_id")
            result.rejected_records.append({"raw": raw, "reason": "Missing record_id"})
            return

        # Rate limit / backpressure check
        if not self._check_rate_limit(tenant_id):
            result.record_defect("rate_limit_exceeded")
            result.rate_limited_records.append({"record_id": record_id, "tenant_id": tenant_id})
            return

        repair_notes = []

        # Parse & sanitize amount
        amount_cents, amt_note = self.sanitize_amount(raw.get("amount") or raw.get("total"))
        if amt_note:
            result.record_defect(amt_note)
            if "repaired" in amt_note:
                repair_notes.append(amt_note)
            else:
                result.rejected_records.append({"record_id": record_id, "reason": amt_note})
                return

        # Currency normalization
        currency = str(raw.get("currency") or "USD").upper().strip()
        if len(currency) != 3:
            result.record_defect("invalid_currency_code")
            currency = "USD"
            repair_notes.append("repaired_default_currency_usd")

        # Timestamp normalization
        ts, ts_note = self.parse_timestamp(raw.get("timestamp") or raw.get("created_at"))
        if ts_note:
            result.record_defect(ts_note)
            repair_notes.append(ts_note)

        parsed_record = EnterpriseRecord(
            record_id=record_id,
            tenant_id=tenant_id,
            amount_cents=amount_cents or 0,
            currency=currency,
            event_timestamp=ts,
            raw_payload=raw,
            repaired=len(repair_notes) > 0,
            repair_notes=repair_notes,
        )
        result.valid_records.append(parsed_record)

    def run_batch(self, batch: List[Dict[str, Any]]) -> VibeCodingRunResult:
        """
        Executes an end-to-end integration batch.
        """
        start_time = time.perf_counter()
        result = VibeCodingRunResult(total_processed=len(batch))

        for raw_item in batch:
            self.process_record(raw_item, result)

        result.execution_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return result
