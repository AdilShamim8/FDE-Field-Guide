"""
Integration test suite for ETISE FastAPI server endpoints.
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.api.server import app, exception_queue, idempotency_store, metrics_data

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    exception_queue.clear()
    idempotency_store.clear()
    metrics_data["total_processed"] = 0
    metrics_data["total_automated_dispatch"] = 0
    metrics_data["total_human_review_required"] = 0
    metrics_data["total_escalated_p0"] = 0
    metrics_data["total_idempotent_replays"] = 0
    metrics_data["total_operator_overrides"] = 0


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["indexed_chunks"] >= 5


def test_process_ticket_automated_dispatch():
    payload = {
        "ticket_id": "TKT-TEST-001",
        "account_id": "ACC-TEST",
        "raw_text": "Requesting fee waiver and credit on invoice INV-9901 as per Section 5.4 billing policy.",
        "source_channel": "email",
        "idempotency_key": "idem-key-001",
    }
    response = client.post("/api/v1/tickets/process", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "BILLING"
    assert data["severity"] == "P2"
    assert data["routing_decision"] == "AUTOMATED_DISPATCH"
    assert len(data["citations"]) > 0
    assert data["citations"][0]["is_verified"] is True


def test_idempotent_replay():
    payload = {
        "ticket_id": "TKT-TEST-IDEM",
        "account_id": "ACC-IDEM",
        "raw_text": "Need assistance with GDPR data residency compliance under Section 11.3.",
        "source_channel": "portal",
        "idempotency_key": "fixed-idempotent-token",
    }
    # First call
    resp1 = client.post("/api/v1/tickets/process", json=payload)
    assert resp1.status_code == 200

    # Second call with same idempotency token
    resp2 = client.post("/api/v1/tickets/process", json=payload)
    assert resp2.status_code == 200
    assert resp2.json()["ticket_id"] == "TKT-TEST-IDEM"

    # Verify metrics tracked replay
    metrics = client.get("/metrics").json()
    assert metrics["metrics"]["total_idempotent_replays"] == 1


def test_exception_queue_routing_and_operator_resolution():
    # Ticket with low confidence / vague input
    payload = {
        "ticket_id": "TKT-VAGUE-001",
        "account_id": "ACC-VAGUE",
        "raw_text": "vague test error",
        "source_channel": "email",
    }
    resp = client.post("/api/v1/tickets/process", json=payload)
    assert resp.status_code == 200
    assert resp.json()["routing_decision"] == "HUMAN_REVIEW_REQUIRED"

    # Check exception queue
    queue_resp = client.get("/api/v1/queue/exceptions")
    assert queue_resp.status_code == 200
    items = queue_resp.json()
    assert len(items) == 1
    assert items[0]["ticket_id"] == "TKT-VAGUE-001"

    # Operator overrides category to BILLING
    resolve_payload = {
        "ticket_id": "TKT-VAGUE-001",
        "operator_id": "OP-SARAH-9",
        "action": "OVERRIDE",
        "corrected_category": "BILLING",
        "corrected_severity": "P2",
        "override_notes": "Customer confirmed this was an unrecorded invoice dispute.",
    }
    resolve_resp = client.post("/api/v1/queue/resolve", json=resolve_payload)
    assert resolve_resp.status_code == 200
    assert resolve_resp.json()["action"] == "overridden_by_operator"

    # Verify queue is now empty of pending items
    updated_queue = client.get("/api/v1/queue/exceptions").json()
    assert len(updated_queue) == 0


def test_hybrid_knowledge_search():
    resp = client.get("/api/v1/knowledge/search?q=Section%203.1%20critical%20outage")
    assert resp.status_code == 200
    results = resp.json()["results"]
    assert len(results) > 0
    assert results[0]["document_id"] == "APEX-SLA-2026"
    assert "Section 3.1" in results[0]["content"]


def test_permission_aware_rbac_filtering():
    query_url = "/api/v1/knowledge/search?q=GDPR%20data%20residency%20Section%2011.3"

    # Unauthorized role (support_tier1 lacks compliance or admin role for Section 11.3)
    unauth_resp = client.get(query_url, headers={"X-User-Roles": "support_tier1"})
    assert unauth_resp.status_code == 200
    unauth_results = unauth_resp.json()["results"]
    assert not any(r["document_id"] == "APEX-COMPLIANCE-DOC" for r in unauth_results)

    # Authorized role (compliance officer has access)
    auth_resp = client.get(query_url, headers={"X-User-Roles": "compliance"})
    assert auth_resp.status_code == 200
    auth_results = auth_resp.json()["results"]
    assert any(r["document_id"] == "APEX-COMPLIANCE-DOC" for r in auth_results)


def test_dense_vector_cosine_similarity():
    from src.pipeline.ingestion import compute_dense_embedding, cosine_similarity

    v1 = compute_dense_embedding("P0 critical outage payment failure")
    v2 = compute_dense_embedding("total production downtime billing crash")
    v3 = compute_dense_embedding("general weather forecast in Paris")

    sim_related = cosine_similarity(v1, v2)
    sim_unrelated = cosine_similarity(v1, v3)

    assert sim_related > sim_unrelated
    assert sim_related > 0.30
