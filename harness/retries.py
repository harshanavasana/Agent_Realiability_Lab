import time
from typing import Callable, Any


def execute_with_retry(
    func: Callable[[], Any],
    max_retries: int = 3,
    initial_delay: float = 0.2,
    backoff_factor: float = 2.0,
) -> Any:
    delay = initial_delay
    last_exception = None

    for attempt in range(1, max_retries + 1):
        try:
            return func()
        except Exception as e:
            last_exception = e
            if attempt == max_retries:
                break
            time.sleep(delay)
            delay *= backoff_factor

    raise RuntimeError(f"Operation failed after {max_retries} attempts. Last error: {str(last_exception)}")