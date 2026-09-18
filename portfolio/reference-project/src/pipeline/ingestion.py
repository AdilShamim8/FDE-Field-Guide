"""
Ingestion, dense vector embedding, and hybrid knowledge base index for enterprise compliance policies.
Provides dense vector cosine similarity, BM25-style sparse keyword matching,
role-based access control (RBAC) filtering, and deterministic quote verification.
"""

import hashlib
import math
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple


SEMANTIC_CLUSTERS: Dict[int, List[str]] = {
    0: ["outage", "down", "downtime", "crash", "failure", "emergency", "p0", "degradation", "timeout", "unresponsive", "broken"],
    16: ["billing", "invoice", "credit", "fee", "refund", "charge", "dispute", "surcharge", "waiver", "ledger", "seat"],
    32: ["api", "webhook", "sdk", "token", "auth", "endpoint", "rate", "429", "401", "retry", "gateway", "post", "connection"],
    48: ["compliance", "gdpr", "residency", "pii", "audit", "safeguard", "isolation", "baa", "security", "encryption", "region"],
    64: ["inquiry", "question", "help", "information", "hours", "support", "roadmap", "general", "branch", "portal"],
}


def compute_dense_embedding(text: str, dim: int = 128) -> List[float]:
    """
    Computes a normalized dense vector embedding (dim=128) from text.
    Combines n-gram feature hashing with semantic cluster subspace projection and L2 normalization.
    Guarantees deterministic, zero-external-dependency semantic embeddings.
    """
    tokens = [w.lower() for w in re.findall(r"\b\w+\b", text)]
    if not tokens:
        return [0.0] * dim

    vector = [0.0] * dim

    # 1. Semantic cluster subspace projection
    for base_dim, cluster_words in SEMANTIC_CLUSTERS.items():
        for token in tokens:
            if token in cluster_words:
                # Spread activation across subspace
                for offset in range(12):
                    vector[(base_dim + offset) % dim] += 2.0

    # 2. Unigram and bigram n-gram hashing
    for idx, token in enumerate(tokens):
        h = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16)
        vector[h % dim] += 1.0

        if idx > 0:
            bigram = f"{tokens[idx-1]}_{token}"
            h_bi = int(hashlib.md5(bigram.encode("utf-8")).hexdigest(), 16)
            vector[h_bi % dim] += 1.5

    # 3. L2 normalization
    norm = math.sqrt(sum(v * v for v in vector))
    if norm > 0.0:
        vector = [v / norm for v in vector]
    return vector


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Calculates cosine similarity between two normalized vectors."""
    dot = sum(a * b for a, b in zip(v1, v2))
    return max(0.0, min(1.0, dot))


@dataclass
class DocumentChunk:
    chunk_id: str
    document_id: str
    section: str
    title: str
    content: str
    keywords: Set[str]
    dense_vector: List[float] = field(default_factory=list)
    allowed_roles: List[str] = field(default_factory=lambda: ["support_tier1", "support_tier2", "admin", "compliance"])


# Curated compliance and SLA handbook corpus with document-level security ACLs
DEFAULT_KNOWLEDGE_BASE: List[Dict[str, Any]] = [
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
        "allowed_roles": ["support_tier1", "support_tier2", "admin", "compliance"],
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
        "allowed_roles": ["support_tier1", "support_tier2", "admin", "compliance"],
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
        "allowed_roles": ["support_tier1", "support_tier2", "admin", "billing_specialist"],
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
        "allowed_roles": ["support_tier1", "support_tier2", "admin", "developer_support"],
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
        "allowed_roles": ["compliance", "admin"],  # Strict ACL: tier 1 support excluded
    },
]


class HybridKnowledgeIndex:
    """
    Enterprise hybrid knowledge index combining dense vector cosine similarity
    with BM25-style keyword matching and role-based access control (RBAC).
    """

    def __init__(self, documents: Optional[List[Dict[str, Any]]] = None):
        self.chunks: List[DocumentChunk] = []
        self._tokenize_pattern = re.compile(r"\b\w+\b")
        docs = documents if documents is not None else DEFAULT_KNOWLEDGE_BASE
        self._build_index(docs)

    def _tokenize(self, text: str) -> List[str]:
        return [w.lower() for w in self._tokenize_pattern.findall(text)]

    def _build_index(self, docs: List[Dict[str, Any]]) -> None:
        for idx, doc in enumerate(docs):
            tokens = set(self._tokenize(doc["content"]))
            dense_vec = compute_dense_embedding(doc["content"])
            roles = doc.get("allowed_roles", ["support_tier1", "support_tier2", "admin", "compliance"])
            chunk = DocumentChunk(
                chunk_id=f"CHK-{idx+1:03d}",
                document_id=doc["document_id"],
                section=doc["section"],
                title=doc["title"],
                content=doc["content"],
                keywords=tokens,
                dense_vector=dense_vec,
                allowed_roles=roles,
            )
            self.chunks.append(chunk)

    def search(
        self,
        query: str,
        top_k: int = 2,
        user_roles: Optional[List[str]] = None,
    ) -> List[Tuple[DocumentChunk, float]]:
        """
        Executes permission-aware hybrid search:
        1. Pre-retrieval security filter: checks user_roles against chunk.allowed_roles.
        2. Sparse overlap score + exact code bonus.
        3. Dense cosine similarity vector score.
        Total Hybrid Score = 0.5 * sparse + 0.5 * dense.
        """
        q_tokens = self._tokenize(query)
        if not q_tokens:
            return []

        q_vec = compute_dense_embedding(query)
        scored_chunks: List[Tuple[DocumentChunk, float]] = []

        for chunk in self.chunks:
            # RBAC permission filter: if user_roles provided, verify ACL intersection
            if user_roles is not None:
                has_access = any(r in chunk.allowed_roles for r in user_roles)
                if not has_access:
                    continue  # Filter out unauthorized chunk at pre-retrieval

            # Sparse score
            overlap = sum(1 for t in q_tokens if t in chunk.keywords)
            sparse_score = overlap / max(1, len(q_tokens))
            if chunk.section.lower() in query.lower() or chunk.document_id.lower() in query.lower():
                sparse_score += 0.5

            # Dense cosine vector score
            dense_score = cosine_similarity(q_vec, chunk.dense_vector)

            # Combined hybrid score
            hybrid_score = (0.5 * sparse_score) + (0.5 * dense_score)
            if hybrid_score > 0.15:
                scored_chunks.append((chunk, hybrid_score))

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
