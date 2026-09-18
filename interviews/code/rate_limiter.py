"""
Production rate limiter using a sliding window counter algorithm.
Provides tenant-isolated quotas, multi-tier rate limiting, and retry-after calculations.
"""

import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class RateLimitStatus:
    allowed: bool
    limit: int
    remaining: int
    reset_after_sec: float
    retry_after_sec: Optional[float] = None


class SlidingWindowRateLimiter:
    """
    In-memory sliding window counter rate limiter.
    Enforces per-tenant rate limits across configurable time windows.
    Tracks individual timestamped request weights to prevent boundary-burst attacks.
    """

    DEFAULT_TIERS: Dict[str, int] = {
        "free": 10,
        "standard": 60,
        "enterprise": 300,
    }

    def __init__(
        self,
        window_sec: float = 60.0,
        tier_limits: Optional[Dict[str, int]] = None,
        time_func: Optional[callable] = None,
    ):
        self.window_sec = window_sec
        self.tier_limits = tier_limits or self.DEFAULT_TIERS
        self.time_func = time_func or time.time
        # Store tenant_id -> list of (timestamp, cost)
        self._history: Dict[str, List[Tuple[float, int]]] = {}

    def _prune_history(self, tenant_id: str, current_time: float) -> None:
        """Removes entries older than the current sliding window."""
        if tenant_id not in self._history:
            return
        cutoff = current_time - self.window_sec
        self._history[tenant_id] = [
            (ts, cost) for ts, cost in self._history[tenant_id] if ts > cutoff
        ]
        if not self._history[tenant_id]:
            del self._history[tenant_id]

    def check_rate_limit(
        self,
        tenant_id: str,
        tier: str = "standard",
        cost: int = 1,
    ) -> RateLimitStatus:
        """
        Evaluates whether a request with a given cost is allowed under the tenant's tier quota.
        If allowed, records the request timestamp and cost.
        If rejected, computes the exact retry_after_sec until sufficient quota clears.
        """
        now = self.time_func()
        self._prune_history(tenant_id, now)

        limit = self.tier_limits.get(tier, self.tier_limits.get("standard", 60))
        history = self._history.get(tenant_id, [])
        current_usage = sum(c for _, c in history)

        if current_usage + cost <= limit:
            # Request allowed
            if tenant_id not in self._history:
                self._history[tenant_id] = []
            self._history[tenant_id].append((now, cost))
            remaining = limit - (current_usage + cost)

            oldest_ts = history[0][0] if history else now
            reset_after = max(0.0, (oldest_ts + self.window_sec) - now)

            return RateLimitStatus(
                allowed=True,
                limit=limit,
                remaining=remaining,
                reset_after_sec=round(reset_after, 3),
                retry_after_sec=None,
            )

        # Request rejected: calculate retry_after
        needed_clearance = (current_usage + cost) - limit
        cleared = 0
        retry_after = self.window_sec

        for ts, c in history:
            cleared += c
            if cleared >= needed_clearance:
                retry_after = max(0.1, (ts + self.window_sec) - now)
                break

        oldest_ts = history[0][0] if history else now
        reset_after = max(0.0, (oldest_ts + self.window_sec) - now)

        return RateLimitStatus(
            allowed=False,
            limit=limit,
            remaining=0,
            reset_after_sec=round(reset_after, 3),
            retry_after_sec=round(retry_after, 3),
        )
