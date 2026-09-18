"""
Unit tests for resilient caller with exponential backoff and full jitter.
"""

import pytest
from resilient_client import RateLimitExceeded, ResilientCaller, ServerError


def test_immediate_success():
    client = ResilientCaller()
    result, attempts = client.execute(lambda: "success")
    assert result == "success"
    assert attempts == 1
    assert len(client.sleep_history) == 0


def test_retries_transient_failures_until_success():
    calls = 0
    delays_recorded = []

    def op():
        nonlocal calls
        calls += 1
        if calls < 3:
            raise RateLimitExceeded("429 Too Many Requests")
        return {"data": "loaded"}

    # Mock random func to return deterministic fraction of ceiling
    mock_random = lambda low, high: high * 0.5
    mock_sleep = lambda d: delays_recorded.append(d)

    client = ResilientCaller(
        base_delay_sec=1.0,
        max_retries=3,
        sleep_func=mock_sleep,
        random_func=mock_random,
    )

    result, attempts = client.execute(op)
    assert result == {"data": "loaded"}
    assert attempts == 3
    assert len(delays_recorded) == 2
    # Attempt 0: ceiling = 1.0 * (2^0) = 1.0 -> sleep = 0.5
    assert delays_recorded[0] == 0.5
    # Attempt 1: ceiling = 1.0 * (2^1) = 2.0 -> sleep = 1.0
    assert delays_recorded[1] == 1.0


def test_exhausted_retries_raises_exception():
    client = ResilientCaller(max_retries=2)
    with pytest.raises(ServerError):
        client.execute(lambda: (_ for _ in ()).throw(ServerError("503 Service Unavailable")))
    assert len(client.sleep_history) == 2


def test_unretryable_exception_fails_immediately():
    client = ResilientCaller(max_retries=3)
    with pytest.raises(ValueError):
        client.execute(lambda: (_ for _ in ()).throw(ValueError("400 Bad Request: Invalid schema")))
    assert len(client.sleep_history) == 0
