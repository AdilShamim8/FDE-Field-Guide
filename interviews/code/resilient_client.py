"""
Resilient HTTP/RPC client implementation featuring exponential backoff with full jitter,
retry budget, and dependency-injected clock for deterministic testing.
Follows AWS architecture recommendations (Marc Brooker, Full Jitter).
"""

import random
from typing import Any, Callable, List, Optional, Tuple


class RateLimitExceeded(Exception):
    pass


class ServerError(Exception):
    pass


class ResilientCaller:
    """
    Executes calls with exponential backoff, full jitter, and maximum retry budget.
    """

    def __init__(
        self,
        base_delay_sec: float = 0.5,
        max_delay_sec: float = 30.0,
        max_retries: int = 4,
        sleep_func: Optional[Callable[[float], None]] = None,
        random_func: Optional[Callable[[float, float], float]] = None,
    ):
        self.base_delay_sec = base_delay_sec
        self.max_delay_sec = max_delay_sec
        self.max_retries = max_retries
        self.sleep_func = sleep_func or (lambda d: None)
        self.random_func = random_func or random.uniform
        self.sleep_history: List[float] = []

    def _calculate_sleep_duration(self, attempt: int) -> float:
        """
        Calculates Full Jitter: Sleep = uniform(0, min(max_delay, base * 2 ** attempt))
        Prevents thundering herd synchronization against rate-limited APIs.
        """
        ceiling = min(self.max_delay_sec, self.base_delay_sec * (2 ** attempt))
        sleep_duration = self.random_func(0, ceiling)
        return sleep_duration

    def execute(self, operation: Callable[[], Any]) -> Tuple[Any, int]:
        """
        Executes operation with retry logic.
        Returns (result, attempts_count).
        Raises last exception if all retries are exhausted.
        """
        attempts = 0
        while True:
            try:
                result = operation()
                return result, attempts + 1
            except (RateLimitExceeded, ServerError) as exc:
                if attempts >= self.max_retries:
                    raise exc
                delay = self._calculate_sleep_duration(attempts)
                self.sleep_history.append(delay)
                self.sleep_func(delay)
                attempts += 1
            except Exception as unretryable_exc:
                # Client errors (4xx other than 429) fail immediately
                raise unretryable_exc
