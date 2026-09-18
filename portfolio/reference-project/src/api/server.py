"""
FastAPI application exposing production endpoints for ETISE:
- Health and metrics
- Ticket ingestion with idempotency check
- Human review queue management
- Knowledge base query
"""

import time
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, Header, HTTPException, Query, status
from fastapi.responses import JSONResponse

from ..config import settings
from ..engine.agent import TriageAgent
from ..models.schemas import (
    OperatorResolveRequest,
    OperatorReviewItem,
    RoutingDecision,
    TicketIngestRequest,
    TriageResult,
)
from ..pipeline.ingestion import HybridKnowledgeIndex

app = FastAPI(
    title="Enterprise Ticket Intelligence and Grounded Synthesis Engine (ETISE)",
    version="1.0.0",
    description="Production-grade forward deployed triage and compliance synthesis API",
)

# Application state
agent = TriageAgent()
idempotency_store: Dict[str, Dict[str, Any]] = {}
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
def process_ticket(
    payload: TicketIngestRequest,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
    user_roles_header: Optional[str] = Header(None, alias="X-User-Roles"),
) -> TriageResult:
    """
    Ingests, classifies, and synthesizes a citation-grounded draft for incoming tickets.
    Guarantees idempotency via Idempotency-Key header or payload parameter.
    Enforces RBAC document filtering via X-User-Roles header.
    """
    key = idempotency_key or payload.idempotency_key

    # Check for idempotent cached result
    if key and key in idempotency_store:
        metrics_data["total_idempotent_replays"] += 1
        cached_result = idempotency_store[key]
        return TriageResult(**cached_result)

    roles = [r.strip() for r in user_roles_header.split(",")] if user_roles_header else None

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
    if key:
        idempotency_store[key] = result.model_dump()

    return result


@app.get(
    "/api/v1/queue/exceptions",
    response_model=List[OperatorReviewItem],
    tags=["Operator Oversight"],
)
def get_exception_queue(
    status_filter: str = Query("PENDING", description="Status: PENDING, APPROVED, or OVERRIDDEN")
) -> List[OperatorReviewItem]:
    """
    Returns pending tickets awaiting human operator review.
    """
    return [item for item in exception_queue if item.status.startswith(status_filter)]


@app.post("/api/v1/queue/resolve", tags=["Operator Oversight"])
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
def search_knowledge(
    q: str = Query(..., min_length=2, description="Search query"),
    top_k: int = Query(2, ge=1, le=5),
    user_roles_header: Optional[str] = Header(None, alias="X-User-Roles"),
) -> Dict[str, Any]:
    """
    Performs permission-aware hybrid search over indexed enterprise compliance and SLA manuals.
    """
    roles = [r.strip() for r in user_roles_header.split(",")] if user_roles_header else None
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
