"""
Pydantic data schemas for ETISE system.
Defines strict boundary validation for tickets, extraction, citations, and reviews.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


class DefectCategory(str, Enum):
    OUTAGE = "OUTAGE"
    BILLING = "BILLING"
    INTEGRATION_BUG = "INTEGRATION_BUG"
    COMPLIANCE = "COMPLIANCE"
    GENERAL_INQUIRY = "GENERAL_INQUIRY"


class SeverityLevel(str, Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class RoutingDecision(str, Enum):
    AUTOMATED_DISPATCH = "AUTOMATED_DISPATCH"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
    ESCALATED_P0 = "ESCALATED_P0"


class TicketIngestRequest(BaseModel):
    ticket_id: str = Field(..., description="Unique ticket identifier")
    account_id: str = Field(..., description="Customer enterprise account ID")
    raw_text: str = Field(..., min_length=5, description="Full ticket body or email body")
    source_channel: str = Field("email", description="Channel: email, webhook, or portal")
    idempotency_key: Optional[str] = Field(None, description="Client idempotency key")


class ExtractedTicketData(BaseModel):
    category: DefectCategory
    severity: SeverityLevel
    urgency_score: float = Field(..., ge=0.0, le=1.0)
    affected_system: str
    summary: str
    confidence: float = Field(..., ge=0.0, le=1.0)


class Citation(BaseModel):
    document_id: str
    section: str
    verbatim_quote: str
    is_verified: bool = False


class TriageResult(BaseModel):
    ticket_id: str
    account_id: str
    category: DefectCategory
    severity: SeverityLevel
    urgency_score: float
    affected_system: str
    summary: str
    confidence: float
    routing_decision: RoutingDecision
    draft_response: str
    citations: List[Citation] = []
    repair_attempts: int = 0
    processing_time_ms: float = 0.0


class OperatorReviewItem(BaseModel):
    ticket_id: str
    account_id: str
    triage_result: TriageResult
    created_at: float
    status: str = "PENDING"  # PENDING, APPROVED, OVERRIDDEN


class OperatorResolveRequest(BaseModel):
    ticket_id: str
    operator_id: str
    action: str = Field(..., description="APPROVE or OVERRIDE")
    corrected_category: Optional[DefectCategory] = None
    corrected_severity: Optional[SeverityLevel] = None
    override_notes: Optional[str] = None
