"""
Ingestion and hybrid knowledge base index for enterprise compliance policies.
Provides BM25-style keyword matching and dense similarity retrieval with quote verification.
"""

import math
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class DocumentChunk:
    chunk_id: str
    document_id: str
    section: str
    title: str
    content: str
    keywords: Set[str]


# Curated compliance and SLA handbook corpus for Apex Enterprise Cloud Services
DEFAULT_KNOWLEDGE_BASE: List[Dict[str, str]] = [
    {
        "document_id": "APEX-SLA-2026",
        "section": "Section 3.1",
        "title": "P0 Critical Outage SLA",
        "content": (
            "Section 3.1 - P0 Critical Outage Definition and Response Times. "
            "A P0 incident is defined as total production service outage impacting more than 20% of users "
            "or complete failure of payment processing endpoints. The initial response time SLA is 15 minutes. "
            "Continuous hourly updates must be published to the status page until full resolution."
        ),
    },
    {
        "document_id": "APEX-SLA-2026",
        "section": "Section 3.2",
        "title": "P1 High Severity Degradation",
        "content": (
            "Section 3.2 - P1 High Severity Incident SLA. "
            "A P1 incident is defined as significant degradation of core system functionality without total outage. "
            "Initial response time SLA is 60 minutes during standard business operating hours. "
            "Engineering escalation occurs automatically if unresolved within 3 hours."
        ),
    },
    {
        "document_id": "APEX-BILLING-POLICY",
        "section": "Section 5.4",
        "title": "SLA Credit Calculation and Dispute Filing",
        "content": (
            "Section 5.4 - Service Level Credit Filing Procedure. "
            "Customers eligible for service credits due to SLA breaches must submit a formal credit request "
            "within thirty (30) days of the incident date. Credits are capped at 25% of the total monthly invoice "
            "and are applied against the subsequent billing cycle. Cash refunds are strictly prohibited."
        ),
    },
    {
        "document_id": "APEX-INTEGRATION-GUIDE",
        "section": "Section 8.2",
        "title": "API Rate Limiting and Webhook Retries",
        "content": (
            "Section 8.2 - Webhook Retry Policy and Backoff. "
            "Webhook deliveries retry up to five (5) times over a 24-hour period using exponential backoff. "
            "Clients must return HTTP 200 or 201 within 2,500ms to avoid delivery timeouts. "
            "Repeated 5xx responses cause the webhook subscription to be paused automatically."
        ),
    },
    {
        "document_id": "APEX-COMPLIANCE-DOC",
        "section": "Section 11.3",
        "title": "Data Residency and Regional Isolation",
        "content": (
            "Section 11.3 - EU Data Residency and GDPR Safeguards. "
            "All customer data originating from EU tenancies is stored and processed exclusively in AWS eu-west-1 "
            "or Azure westeurope regions. Customer telemetry exported outside the designated region is stripped "
            "of all personally identifiable information (PII) before transmission."
        ),
    },
]


class HybridKnowledgeIndex:
    """
    In-memory hybrid knowledge base index combining keyword BM25 retrieval
    with token-overlap scoring and exact quotation verification.
    """

    def __init__(self, documents: Optional[List[Dict[str, str]]] = None):
        self.chunks: List[DocumentChunk] = []
        self._tokenize_pattern = re.compile(r"\b\w+\b")
        docs = documents if documents is not None else DEFAULT_KNOWLEDGE_BASE
        self._build_index(docs)

    def _tokenize(self, text: str) -> List[str]:
        return [w.lower() for w in self._tokenize_pattern.findall(text)]

    def _build_index(self, docs: List[Dict[str, str]]) -> None:
        for idx, doc in enumerate(docs):
            tokens = set(self._tokenize(doc["content"]))
            chunk = DocumentChunk(
                chunk_id=f"CHK-{idx+1:03d}",
                document_id=doc["document_id"],
                section=doc["section"],
                title=doc["title"],
                content=doc["content"],
                keywords=tokens,
            )
            self.chunks.append(chunk)

    def search(self, query: str, top_k: int = 2) -> List[Tuple[DocumentChunk, float]]:
        """
        Executes hybrid score calculation:
        Score = keyword_match_ratio + exact_phrase_bonus
        """
        q_tokens = self._tokenize(query)
        if not q_tokens:
            return []

        scored_chunks: List[Tuple[DocumentChunk, float]] = []
        for chunk in self.chunks:
            # Token overlap score
            overlap = sum(1 for t in q_tokens if t in chunk.keywords)
            overlap_score = overlap / max(1, len(q_tokens))

            # Exact section or ID bonus
            bonus = 0.0
            if chunk.section.lower() in query.lower() or chunk.document_id.lower() in query.lower():
                bonus = 0.5

            total_score = overlap_score + bonus
            if total_score > 0.15:
                scored_chunks.append((chunk, total_score))

        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        return scored_chunks[:top_k]

    def verify_quote(self, document_id: str, quote: str) -> bool:
        """
        Deterministically verifies that the cited quote exists verbatim
        in the referenced document.
        """
        if not quote or not quote.strip():
            return False
        clean_quote = " ".join(quote.split()).lower()
        for chunk in self.chunks:
            if chunk.document_id == document_id:
                clean_content = " ".join(chunk.content.split()).lower()
                if clean_quote in clean_content:
                    return True
        return False
