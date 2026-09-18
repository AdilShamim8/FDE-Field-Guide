import pytest
from rate_limiter import SlidingWindowRateLimiter


def test_rate_limiter_allows_under_quota():
    simulated_time = 1000.0
    limiter = SlidingWindowRateLimiter(
        window_sec=60.0,
        tier_limits={"free": 5},
        time_func=lambda: simulated_time,
    )

    # First 5 requests should be allowed
    for i in range(5):
        status = limiter.check_rate_limit(tenant_id="tenant_a", tier="free")
        assert status.allowed is True
        assert status.remaining == 4 - i
        assert status.retry_after_sec is None


def test_rate_limiter_blocks_and_calculates_retry_after():
    simulated_time = 1000.0
    limiter = SlidingWindowRateLimiter(
        window_sec=60.0,
        tier_limits={"free": 3},
        time_func=lambda: simulated_time,
    )

    # Consume all 3 units
    limiter.check_rate_limit(tenant_id="tenant_b", tier="free")
    simulated_time += 10.0
    limiter.check_rate_limit(tenant_id="tenant_b", tier="free")
    simulated_time += 10.0
    limiter.check_rate_limit(tenant_id="tenant_b", tier="free")

    # 4th request must be blocked
    status = limiter.check_rate_limit(tenant_id="tenant_b", tier="free")
    assert status.allowed is False
    assert status.remaining == 0
    assert status.retry_after_sec is not None
    # Oldest request was at 1000.0, current time is 1020.0, window is 60.0
    # Next slot opens at 1060.0 -> retry_after should be 40.0
    assert status.retry_after_sec == pytest.approx(40.0, 0.1)


def test_rate_limiter_window_slide_resets_quota():
    simulated_time = 1000.0
    limiter = SlidingWindowRateLimiter(
        window_sec=60.0,
        tier_limits={"standard": 2},
        time_func=lambda: simulated_time,
    )

    limiter.check_rate_limit(tenant_id="tenant_c", tier="standard")
    limiter.check_rate_limit(tenant_id="tenant_c", tier="standard")
    assert limiter.check_rate_limit(tenant_id="tenant_c", tier="standard").allowed is False

    # Advance time past the 60-second window
    simulated_time += 61.0

    status = limiter.check_rate_limit(tenant_id="tenant_c", tier="standard")
    assert status.allowed is True
    assert status.remaining == 1


def test_tiered_limits_isolation():
    simulated_time = 1000.0
    limiter = SlidingWindowRateLimiter(
        window_sec=60.0,
        tier_limits={"free": 2, "enterprise": 10},
        time_func=lambda: simulated_time,
    )

    # Free tier tenant exhausts quickly
    limiter.check_rate_limit("free_tenant", tier="free")
    limiter.check_rate_limit("free_tenant", tier="free")
    assert limiter.check_rate_limit("free_tenant", tier="free").allowed is False

    # Enterprise tenant has separate quota
    for _ in range(8):
        status = limiter.check_rate_limit("enterprise_tenant", tier="enterprise")
        assert status.allowed is True
    assert limiter.check_rate_limit("enterprise_tenant", tier="enterprise").remaining == 1
