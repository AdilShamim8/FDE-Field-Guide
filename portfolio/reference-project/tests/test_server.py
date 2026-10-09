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


def sample_ticket(**overrides):
    payload = {
        "ticket_id": "TKT-BOUNDARY", "account_id": "ACC-BOUNDARY",
        "raw_text": "Requesting fee waiver and credit on invoice INV-9901 as per Section 5.4 billing policy.",
        "idempotency_key": "boundary-key",
    }
    payload.update(overrides)
    return payload


def test_conflicting_idempotency_payload_rejected():
    assert client.post("/api/v1/tickets/process", json=sample_ticket()).status_code == 200
    conflict = client.post("/api/v1/tickets/process", json=sample_ticket(raw_text="A different billing request"))
    assert conflict.status_code == 409
    assert metrics_data["total_processed"] == 1
    assert metrics_data["total_idempotent_replays"] == 0


def test_idempotency_key_is_account_scoped():
    first = client.post("/api/v1/tickets/process", json=sample_ticket())
    second = client.post("/api/v1/tickets/process", json=sample_ticket(account_id="ACC-OTHER"))
    assert first.status_code == second.status_code == 200
    assert second.json()["account_id"] == "ACC-OTHER"
    assert metrics_data["total_processed"] == 2


def test_role_scope_prevents_privileged_cache_replay():
    payload = sample_ticket(raw_text="Need GDPR data residency compliance safeguards under Section 11.3.")
    privileged = client.post("/api/v1/tickets/process", json=payload, headers={"X-User-Roles": "compliance"})
    unprivileged = client.post("/api/v1/tickets/process", json=payload)
    assert privileged.status_code == unprivileged.status_code == 200
    assert any(c["document_id"] == "APEX-COMPLIANCE-DOC" for c in privileged.json()["citations"])
    assert not any(c["document_id"] == "APEX-COMPLIANCE-DOC" for c in unprivileged.json()["citations"])
    assert metrics_data["total_processed"] == 2


def test_expired_replay_is_processed_again(monkeypatch):
    from src.api import server
    monkeypatch.setattr(server.settings, "idempotency_ttl_seconds", 1)
    before = server.time.monotonic()
    assert client.post("/api/v1/tickets/process", json=sample_ticket()).status_code == 200
    record = next(iter(idempotency_store.values()))
    assert before + 1 <= record.expires_at <= server.time.monotonic() + 1
    record.expires_at = -1
    assert client.post("/api/v1/tickets/process", json=sample_ticket()).status_code == 200
    assert metrics_data["total_processed"] == 2
    assert metrics_data["total_idempotent_replays"] == 0


def test_concurrent_retries_process_once(monkeypatch):
    import time
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    from src.api import server
    original = server.agent.process_ticket
    barrier = Barrier(8)
    calls = []

    def slow_process(*args, **kwargs):
        calls.append(1)
        time.sleep(0.02)
        return original(*args, **kwargs)

    monkeypatch.setattr(server.agent, "process_ticket", slow_process)

    def send(_):
        barrier.wait(timeout=5)
        with TestClient(app) as local_client:
            return local_client.post("/api/v1/tickets/process", json=sample_ticket())

    with ThreadPoolExecutor(max_workers=8) as pool:
        responses = list(pool.map(send, range(8)))
    assert all(r.status_code == 200 for r in responses)
    assert all(r.json() == responses[0].json() for r in responses)
    assert len(calls) == metrics_data["total_processed"] == 1
    assert metrics_data["total_idempotent_replays"] == 7


def test_replay_cache_capacity_is_bounded(monkeypatch):
    from src.api import server
    monkeypatch.setattr(server, "MAX_IDEMPOTENCY_ENTRIES", 1)
    assert client.post("/api/v1/tickets/process", json=sample_ticket()).status_code == 200
    assert client.post("/api/v1/tickets/process", json=sample_ticket(idempotency_key="next")).status_code == 503
    assert client.post("/api/v1/tickets/process", json=sample_ticket()).status_code == 200
    assert len(idempotency_store) == 1


@pytest.mark.parametrize("overrides", [
    {"account_id": " "}, {"ticket_id": ""}, {"idempotency_key": " "}, {"raw_text": "x" * 20001},
])
def test_invalid_ticket_boundaries(overrides):
    assert client.post("/api/v1/tickets/process", json=sample_ticket(**overrides)).status_code == 422


def test_missing_and_empty_role_headers_do_not_bypass_filtering():
    query = "/api/v1/knowledge/search?q=GDPR%20data%20residency%20Section%2011.3"
    default = client.get(query)
    empty = client.get(query, headers={"X-User-Roles": ""})
    assert not any(r["document_id"] == "APEX-COMPLIANCE-DOC" for r in default.json()["results"])
    assert empty.json()["results"] == []
    assert client.get(query, headers={"X-User-Roles": "invented-role"}).status_code == 400


def test_operator_action_is_schema_validated():
    response = client.post("/api/v1/queue/resolve", json={
        "ticket_id": "TKT-UNKNOWN", "operator_id": "OP-TEST", "action": "DELETE",
    })
    assert response.status_code == 422
