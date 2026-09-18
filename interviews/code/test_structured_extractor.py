"""
Unit tests for self-healing structured field extractor.
"""

import json
from structured_extractor import (
    IncidentRecord,
    SeverityLevel,
    extract_with_repair_loop,
)


def test_clean_extraction_first_attempt():
    valid_payload = {
        "incident_id": "INC-9402",
        "severity": "P1",
        "affected_service": "payment-gateway",
        "customer_impacted": True,
        "summary": "Elevated 504 error rate on checkout endpoint",
        "confidence_score": 0.95,
    }

    def mock_llm(prompt, feedback):
        return json.dumps(valid_payload)

    record, errors = extract_with_repair_loop("raw text", mock_llm)
    assert record is not None
    assert record.incident_id == "INC-9402"
    assert record.severity == SeverityLevel.P1
    assert record.customer_impacted is True
    assert len(errors) == 0


def test_self_healing_feedback_loop_recovers():
    attempts = 0

    def mock_llm(prompt, feedback):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            # First attempt: invalid ID format and missing boolean
            return json.dumps({
                "incident_id": "9402",  # Missing 'INC-' prefix
                "severity": "P0",
                "affected_service": "auth-service",
                "customer_impacted": "yes",  # String instead of boolean
                "summary": "Database locked",
                "confidence_score": 0.88,
            })
        else:
            # Second attempt: feedback provided, fixed
            assert feedback is not None
            assert any("INC-" in err for err in feedback)
            return json.dumps({
                "incident_id": "INC-9402",
                "severity": "P0",
                "affected_service": "auth-service",
                "customer_impacted": True,
                "summary": "Database locked",
                "confidence_score": 0.88,
            })

    record, errors = extract_with_repair_loop("raw text", mock_llm, max_repair_attempts=2)
    assert attempts == 2
    assert record is not None
    assert record.incident_id == "INC-9402"
    assert record.customer_impacted is True
    assert len(errors) == 2  # The 2 initial errors that were corrected


def test_refusal_on_insufficient_information():
    def mock_llm(prompt, feedback):
        return "CANNOT_EXTRACT_INSUFFICIENT_INFORMATION"

    record, errors = extract_with_repair_loop("The weather is nice today.", mock_llm)
    assert record is None
    assert "insufficient information" in errors[0]
