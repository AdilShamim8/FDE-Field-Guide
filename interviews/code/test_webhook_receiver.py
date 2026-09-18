"""
Unit tests for idempotent webhook receiver.
"""

from webhook_receiver import IdempotentWebhookReceiver


def test_first_time_execution():
    receiver = IdempotentWebhookReceiver()
    calls = []

    def handler(payload):
        calls.append(payload)
        return {"order_status": "created", "order_id": payload["id"]}

    status, body = receiver.process_webhook("key-123", {"id": "ord-99"}, handler)
    assert status == 200
    assert body["status"] == "executed"
    assert body["result"]["order_id"] == "ord-99"
    assert len(calls) == 1


def test_idempotent_replay_does_not_reexecute():
    receiver = IdempotentWebhookReceiver()
    calls = []

    def handler(payload):
        calls.append(payload)
        return {"payment_status": "settled"}

    payload = {"account": "acc-1", "amount": 500}
    status1, body1 = receiver.process_webhook("idem-001", payload, handler)
    assert status1 == 200
    assert len(calls) == 1

    # Replay with same key and payload
    status2, body2 = receiver.process_webhook("idem-001", payload, handler)
    assert status2 == 200
    assert body2["status"] == "cached_idempotent_replay"
    assert body2["result"]["payment_status"] == "settled"
    # Handler was NOT called again
    assert len(calls) == 1


def test_conflicting_payload_returns_409():
    receiver = IdempotentWebhookReceiver()
    handler = lambda p: {"ok": True}

    status1, _ = receiver.process_webhook("idem-conflict", {"amount": 100}, handler)
    assert status1 == 200

    # Same key, altered payload
    status2, body2 = receiver.process_webhook("idem-conflict", {"amount": 200}, handler)
    assert status2 == 409
    assert "conflicting payload" in body2["error"]
