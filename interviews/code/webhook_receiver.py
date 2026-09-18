"""
Idempotent webhook receiver demonstrating enterprise delivery semantics.
Guarantees at-least-once tolerance, deduplication within a time window,
and payload checksum verification.
"""

import hashlib
import json
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, Optional, Tuple


class ProcessingState(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class ExecutionRecord:
    state: ProcessingState
    payload_hash: str
    response: Optional[Dict[str, Any]]
    created_at: float
    updated_at: float


class IdempotentWebhookReceiver:
    """
    In-memory reference implementation of an idempotent webhook receiver.
    In production, this backed by Redis with SETNX and TTL or PostgreSQL ON CONFLICT DO UPDATE.
    """

    def __init__(self, ttl_seconds: int = 86400):
        self.ttl_seconds = ttl_seconds
        self._store: Dict[str, ExecutionRecord] = {}

    def _hash_payload(self, payload: Dict[str, Any]) -> str:
        serialized = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def process_webhook(
        self,
        idempotency_key: str,
        payload: Dict[str, Any],
        handler: Callable[[Dict[str, Any]], Dict[str, Any]],
    ) -> Tuple[int, Dict[str, Any]]:
        """
        Processes incoming webhook.
        Returns (http_status_code, response_body).
        - 200/201: Successfully executed or previously completed (idempotent replay)
        - 409: Duplicate key with conflicting payload or concurrent in-flight execution
        - 500: Handler failed (allows downstream vendor retry)
        """
        if not idempotency_key or not idempotency_key.strip():
            return 400, {"error": "Missing required Idempotency-Key header"}

        now = time.time()
        payload_hash = self._hash_payload(payload)

        # Evict expired keys (simple TTL hygiene)
        if idempotency_key in self._store:
            record = self._store[idempotency_key]
            if now - record.created_at > self.ttl_seconds:
                del self._store[idempotency_key]

        # Check existing state
        if idempotency_key in self._store:
            record = self._store[idempotency_key]

            # Conflict: same key, different payload
            if record.payload_hash != payload_hash:
                return 409, {
                    "error": "Idempotency key reused with conflicting payload",
                    "idempotency_key": idempotency_key,
                }

            # In-flight lock: another worker is executing
            if record.state == ProcessingState.PENDING:
                return 409, {
                    "error": "Concurrent request in progress for this idempotency key",
                    "status": "in_flight",
                }

            # Already successfully processed
            if record.state == ProcessingState.COMPLETED:
                return 200, {
                    "status": "cached_idempotent_replay",
                    "result": record.response,
                }

            # Previously failed: allow retry by proceeding below

        # Mark as PENDING (atomic lock acquisition in production)
        self._store[idempotency_key] = ExecutionRecord(
            state=ProcessingState.PENDING,
            payload_hash=payload_hash,
            response=None,
            created_at=now,
            updated_at=now,
        )

        try:
            result = handler(payload)
            self._store[idempotency_key].state = ProcessingState.COMPLETED
            self._store[idempotency_key].response = result
            self._store[idempotency_key].updated_at = time.time()
            return 200, {"status": "executed", "result": result}
        except Exception as exc:
            self._store[idempotency_key].state = ProcessingState.FAILED
            self._store[idempotency_key].updated_at = time.time()
            return 500, {
                "error": "Webhook processing failed",
                "details": str(exc),
            }
