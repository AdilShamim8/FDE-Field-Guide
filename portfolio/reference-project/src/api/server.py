"""
FastAPI application exposing production endpoints for ETISE:
- Health and metrics
- Ticket ingestion with idempotency check
- Human review queue management
- Knowledge base query
"""

import time
import hashlib
import json
from dataclasses import dataclass
from functools import wraps
from threading import RLock
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, Header, HTTPException, Query, status

from ..config import settings
from ..engine.agent import TriageAgent
from ..models.schemas import (
    OperatorResolveRequest,
    OperatorReviewItem,
    RoutingDecision,
    TicketIngestRequest,
    TriageResult,
)

app = FastAPI(
    title="Enterprise Ticket Intelligence and Grounded Synthesis Engine (ETISE)",
    version="1.0.0",
    description="Local deterministic triage reference; no authenticated tenant boundary",
)

# Application state
agent = TriageAgent()
@dataclass
class CachedResult:
    payload_hash: str
    expires_at: float
    result: Dict[str, Any]


# Process-local serialization, not a distributed lock or durable transaction.
state_lock = RLock()
MAX_IDEMPOTENCY_ENTRIES = 4096
idempotency_store: Dict[tuple, CachedResult] = {}


def serialized_state(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        with state_lock:
            return function(*args, **kwargs)
    return wrapped


def parse_roles(header):
    # Local role simulation only. A production gateway must supply verified identity.
    roles = ["support_tier1"] if header is None else sorted({r.strip() for r in header.split(",") if r.strip()})
    known = {"support_tier1", "support_tier2", "admin", "compliance"}
    if any(role not in known for role in roles):
        raise HTTPException(status_code=400, detail="Unknown simulated role")
    return roles

exception_queue: List[OperatorReviewItem] = []
feedback_ledger: List[Dict[str, Any]] = []

# Metrics state
metrics_data = {
    "total_processed": 0,
    "total_automated_dispatch": 0,
    "total_human_review_required": 0,
    "total_escalated_p0": 0,
    "total_idempotent_replays": 0,
    "total_operator_overrides": 0,
}


@app.get("/health", tags=["System"])
@serialized_state
def health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "service": settings.app_name,
        "environment": settings.environment,
        "indexed_chunks": len(agent.index.chunks),
        "queue_depth": len(exception_queue),
        "timestamp": time.time(),
    }


@app.get("/metrics", tags=["System"])
@serialized_state
def get_metrics() -> Dict[str, Any]:
    return {
        "metrics": metrics_data,
        "active_exception_queue_depth": len(exception_queue),
        "feedback_ledger_entries": len(feedback_ledger),
    }


@app.post(
    "/api/v1/tickets/process",
    response_model=TriageResult,
    status_code=status.HTTP_200_OK,
    tags=["Triage"],
)
@serialized_state
def process_ticket(
    payload: TicketIngestRequest,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key", min_length=1, max_length=128),
    user_roles_header: Optional[str] = Header(None, alias="X-User-Roles"),
) -> TriageResult:
    """
    Ingests, classifies, and synthesizes a citation-grounded draft for incoming tickets.
    Serializes local retries and expires cached results using a monotonic clock.
    Simulates document filtering via caller-supplied X-User-Roles; not authentication.
    """
    key = idempotency_key or payload.idempotency_key
    if key is not None and not key.strip():
        raise HTTPException(status_code=422, detail="Idempotency key must not be blank")
    roles = parse_roles(user_roles_header)
    cache_key = (payload.account_id, key, tuple(roles)) if key else None
    serialized = json.dumps(payload.model_dump(exclude={"idempotency_key"}), sort_keys=True, separators=(",", ":"))
    payload_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    now = time.monotonic()
    for expired_key in [k for k, record in idempotency_store.items() if record.expires_at <= now]:
        del idempotency_store[expired_key]
    if cache_key in idempotency_store:
        record = idempotency_store[cache_key]
        if record.payload_hash != payload_hash:
            raise HTTPException(status_code=409, detail="Idempotency key reused with conflicting payload")
        metrics_data["total_idempotent_replays"] += 1
        return TriageResult(**record.result)
    if cache_key and len(idempotency_store) >= MAX_IDEMPOTENCY_ENTRIES:
        raise HTTPException(status_code=503, detail="Local replay cache capacity reached")

    # Process ticket through agent
    result = agent.process_ticket(payload, user_roles=roles)

    # Update operational metrics
    metrics_data["total_processed"] += 1
    if result.routing_decision == RoutingDecision.AUTOMATED_DISPATCH:
        metrics_data["total_automated_dispatch"] += 1
    elif result.routing_decision == RoutingDecision.HUMAN_REVIEW_REQUIRED:
        metrics_data["total_human_review_required"] += 1
        # Route to exception queue
        review_item = OperatorReviewItem(
            ticket_id=result.ticket_id,
            account_id=result.account_id,
            triage_result=result,
            created_at=time.time(),
            status="PENDING",
        )
        exception_queue.append(review_item)
    elif result.routing_decision == RoutingDecision.ESCALATED_P0:
        metrics_data["total_escalated_p0"] += 1
        # P0 also enqueues for immediate supervisor review
        review_item = OperatorReviewItem(
            ticket_id=result.ticket_id,
            account_id=result.account_id,
            triage_result=result,
            created_at=time.time(),
            status="PENDING_ESCALATION",
        )
        exception_queue.append(review_item)

    # Store idempotent result
    if cache_key:
        idempotency_store[cache_key] = CachedResult(
            payload_hash=payload_hash,
            expires_at=time.monotonic() + settings.idempotency_ttl_seconds,
            result=result.model_dump(),
        )

    return result


@app.get(
    "/api/v1/queue/exceptions",
    response_model=List[OperatorReviewItem],
    tags=["Operator Oversight"],
)
@serialized_state
def get_exception_queue(
    status_filter: str = Query("PENDING", description="Status: PENDING, APPROVED, or OVERRIDDEN")
) -> List[OperatorReviewItem]:
    """
    Returns pending tickets awaiting human operator review.
    """
    return [item for item in exception_queue if item.status.startswith(status_filter)]


@app.post("/api/v1/queue/resolve", tags=["Operator Oversight"])
@serialized_state
def resolve_exception(resolve_req: OperatorResolveRequest) -> Dict[str, Any]:
    """
    Allows a human operator to approve or override an automated triage decision,
    recording an immutable feedback record for model evaluation.
    """
    target_item = None
    for item in exception_queue:
        if item.ticket_id == resolve_req.ticket_id and item.status.startswith("PENDING"):
            target_item = item
            break

    if not target_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pending review item for ticket {resolve_req.ticket_id} not found",
        )

    if resolve_req.action == "APPROVE":
        target_item.status = "APPROVED"
        action_recorded = "approved_without_changes"
    elif resolve_req.action == "OVERRIDE":
        target_item.status = "OVERRIDDEN"
        action_recorded = "overridden_by_operator"
        metrics_data["total_operator_overrides"] += 1

        # Record in feedback ledger
        feedback_entry = {
            "ticket_id": resolve_req.ticket_id,
            "operator_id": resolve_req.operator_id,
            "original_category": target_item.triage_result.category.value,
            "corrected_category": resolve_req.corrected_category.value if resolve_req.corrected_category else None,
            "original_severity": target_item.triage_result.severity.value,
            "corrected_severity": resolve_req.corrected_severity.value if resolve_req.corrected_severity else None,
            "override_notes": resolve_req.override_notes,
            "timestamp": time.time(),
        }
        feedback_ledger.append(feedback_entry)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid action '{resolve_req.action}'. Must be APPROVE or OVERRIDE",
        )

    return {
        "ticket_id": resolve_req.ticket_id,
        "action": action_recorded,
        "resolved_by": resolve_req.operator_id,
        "timestamp": time.time(),
    }


@app.get("/api/v1/knowledge/search", tags=["Knowledge Base"])
@serialized_state
def search_knowledge(
    q: str = Query(..., min_length=2, description="Search query"),
    top_k: int = Query(2, ge=1, le=5),
    user_roles_header: Optional[str] = Header(None, alias="X-User-Roles"),
) -> Dict[str, Any]:
    """
    Performs permission-aware hybrid search over indexed enterprise compliance and SLA manuals.
    """
    roles = parse_roles(user_roles_header)
    results = agent.index.search(q, top_k=top_k, user_roles=roles)
    return {
        "query": q,
        "results": [
            {
                "chunk_id": chunk.chunk_id,
                "document_id": chunk.document_id,
                "section": chunk.section,
                "title": chunk.title,
                "score": round(score, 3),
                "content": chunk.content,
            }
            for chunk, score in results
        ],
    }
