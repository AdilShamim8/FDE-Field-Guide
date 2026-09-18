"""
Defensive CSV/data export parser for customer systems with mixed encodings and defects.
Follows the FDE discipline: never fail silently, account for every dropped or repaired row.
"""

import csv
import io
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class ParseReport:
    total_raw_records: int = 0
    valid_records: int = 0
    repaired_records: int = 0
    dropped_records: int = 0
    defect_counts: Dict[str, int] = field(default_factory=dict)
    dropped_reasons: List[Dict[str, Any]] = field(default_factory=list)

    def record_defect(self, defect_type: str) -> None:
        self.defect_counts[defect_type] = self.defect_counts.get(defect_type, 0) + 1


def decode_bytes_safely(raw_bytes: bytes) -> Tuple[str, str]:
    """
    Attempts decoding with UTF-8-sig (for BOM), UTF-8, then Latin-1/Windows-1252.
    Returns (decoded_text, encoding_used).
    """
    if raw_bytes.startswith(b"\xef\xbb\xbf"):
        return raw_bytes.decode("utf-8-sig"), "utf-8-sig"
    encodings = ["utf-8", "cp1252", "latin-1"]
    for enc in encodings:
        try:
            return raw_bytes.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return raw_bytes.decode("latin-1", errors="replace"), "latin-1-lossy"


def parse_timestamp(raw_val: str) -> Optional[datetime]:
    """
    Tolerates ISO 8601, slash, and dash date variations commonly found in customer exports.
    """
    if not raw_val or not raw_val.strip():
        return None
    val = raw_val.strip()
    formats = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(val, fmt)
        except ValueError:
            continue
    return None


def parse_numeric(raw_val: str) -> Tuple[Optional[float], bool]:
    """
    Normalizes currencies, commas, and whitespace. Returns (parsed_value, was_repaired).
    """
    if not raw_val or not raw_val.strip():
        return None, False
    val = raw_val.strip().replace("$", "").replace("€", "").replace(",", "")
    try:
        num = float(val)
        was_repaired = (val != raw_val.strip())
        return num, was_repaired
    except ValueError:
        return None, False


def parse_customer_export(raw_bytes: bytes) -> Tuple[List[Dict[str, Any]], ParseReport]:
    """
    Parses messy customer export byte stream, reporting all anomalies.
    Required target schema:
      - record_id: str (unique, non-empty)
      - customer_name: str (non-empty)
      - amount: float
      - timestamp: datetime
    """
    report = ParseReport()
    text, used_enc = decode_bytes_safely(raw_bytes)
    if used_enc != "utf-8":
        report.record_defect(f"non_standard_encoding_{used_enc}")

    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        report.record_defect("empty_or_missing_header")
        return [], report

    normalized_fields = {f.strip().lower(): f for f in reader.fieldnames if f}

    id_col = normalized_fields.get("record_id") or normalized_fields.get("id")
    name_col = normalized_fields.get("customer_name") or normalized_fields.get("name")
    amount_col = normalized_fields.get("amount") or normalized_fields.get("total")
    ts_col = normalized_fields.get("timestamp") or normalized_fields.get("date") or normalized_fields.get("created_at")

    if not all([id_col, name_col, amount_col, ts_col]):
        report.record_defect("missing_required_schema_columns")
        return [], report

    seen_ids = set()
    valid_results: List[Dict[str, Any]] = []

    for row_idx, row in enumerate(reader, start=1):
        report.total_raw_records += 1
        raw_id = (row.get(id_col) or "").strip()
        raw_name = (row.get(name_col) or "").strip()
        raw_amount = (row.get(amount_col) or "").strip()
        raw_ts = (row.get(ts_col) or "").strip()

        if not raw_id:
            report.dropped_records += 1
            report.record_defect("missing_primary_key")
            report.dropped_reasons.append({"row": row_idx, "reason": "missing_primary_key", "raw": row})
            continue

        if raw_id in seen_ids:
            report.dropped_records += 1
            report.record_defect("duplicate_primary_key")
            report.dropped_reasons.append({"row": row_idx, "reason": "duplicate_primary_key", "id": raw_id})
            continue

        if not raw_name:
            report.dropped_records += 1
            report.record_defect("empty_customer_name")
            report.dropped_reasons.append({"row": row_idx, "reason": "empty_customer_name", "id": raw_id})
            continue

        amount_val, amount_repaired = parse_numeric(raw_amount)
        if amount_val is None:
            report.dropped_records += 1
            report.record_defect("invalid_numeric_amount")
            report.dropped_reasons.append({"row": row_idx, "reason": "invalid_numeric_amount", "id": raw_id})
            continue

        ts_val = parse_timestamp(raw_ts)
        if ts_val is None:
            report.dropped_records += 1
            report.record_defect("invalid_or_missing_timestamp")
            report.dropped_reasons.append({"row": row_idx, "reason": "invalid_or_missing_timestamp", "id": raw_id})
            continue

        is_repaired = amount_repaired
        if is_repaired:
            report.repaired_records += 1
            report.record_defect("numeric_formatting_repaired")

        seen_ids.add(raw_id)
        report.valid_records += 1
        valid_results.append({
            "record_id": raw_id,
            "customer_name": raw_name,
            "amount": amount_val,
            "timestamp": ts_val,
        })

    return valid_results, report
