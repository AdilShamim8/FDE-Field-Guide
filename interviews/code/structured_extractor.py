"""
Self-healing structured field extractor demonstrating schema validation,
automated error-feedback retry loop, and refusal handling for ungrounded inputs.
"""

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple


class SeverityLevel(str, Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


@dataclass
class IncidentRecord:
    incident_id: str
    severity: SeverityLevel
    affected_service: str
    customer_impacted: bool
    summary: str
    confidence_score: float


class SchemaValidationError(Exception):
    def __init__(self, errors: List[str], raw_output: str):
        super().__init__("; ".join(errors))
        self.errors = errors
        self.raw_output = raw_output


def validate_incident_payload(data: Dict[str, Any]) -> IncidentRecord:
    """
    Strictly validates raw dictionary against IncidentRecord specification.
    Collects all errors rather than failing on the first one.
    """
    errors = []

    inc_id = data.get("incident_id")
    if not inc_id or not isinstance(inc_id, str) or not inc_id.startswith("INC-"):
        errors.append("incident_id must be a string starting with 'INC-'")

    raw_sev = data.get("severity")
    try:
        severity = SeverityLevel(raw_sev)
    except (ValueError, TypeError):
        errors.append(f"severity must be one of {[s.value for s in SeverityLevel]}, got '{raw_sev}'")
        severity = SeverityLevel.P3

    svc = data.get("affected_service")
    if not svc or not isinstance(svc, str) or len(svc.strip()) == 0:
        errors.append("affected_service must be a non-empty string")

    impact = data.get("customer_impacted")
    if impact is None or not isinstance(impact, bool):
        errors.append("customer_impacted must be an explicit boolean (true/false)")

    summary = data.get("summary")
    if not summary or not isinstance(summary, str) or len(summary.strip()) < 5:
        errors.append("summary must be a descriptive string of at least 5 characters")

    conf = data.get("confidence_score")
    if conf is None or not isinstance(conf, (int, float)) or not (0.0 <= conf <= 1.0):
        errors.append("confidence_score must be a float between 0.0 and 1.0")

    if errors:
        raise SchemaValidationError(errors, json.dumps(data))

    return IncidentRecord(
        incident_id=inc_id,
        severity=severity,
        affected_service=svc.strip(),
        customer_impacted=impact,
        summary=summary.strip(),
        confidence_score=float(conf),
    )


def extract_with_repair_loop(
    raw_incident_text: str,
    llm_mock_caller: Callable[[str, Optional[List[str]]], str],
    max_repair_attempts: int = 2,
) -> Tuple[Optional[IncidentRecord], List[str]]:
    """
    Extracts structured incident record from text.
    If the LLM generates invalid JSON or schema violations, the errors are fed
    back into the next prompt prompt iteration to self-correct.
    """
    feedback_errors: Optional[List[str]] = None
    all_trace_errors: List[str] = []

    for attempt in range(max_repair_attempts + 1):
        raw_response = llm_mock_caller(raw_incident_text, feedback_errors)

        # Check for explicit model refusal / out-of-scope trigger
        if "CANNOT_EXTRACT_INSUFFICIENT_INFORMATION" in raw_response:
            return None, ["Model declined: insufficient information in incident text"]

        try:
            parsed_json = json.loads(raw_response)
        except json.JSONDecodeError as jde:
            feedback_errors = [f"JSONDecodeError: {str(jde)}. You must output valid JSON only."]
            all_trace_errors.extend(feedback_errors)
            continue

        try:
            record = validate_incident_payload(parsed_json)
            return record, all_trace_errors
        except SchemaValidationError as sve:
            feedback_errors = sve.errors
            all_trace_errors.extend(sve.errors)
            continue

    return None, all_trace_errors
