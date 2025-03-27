import time
import functools
import logging
from memory_profiler import memory_usage

logger = logging.getLogger(__name__)


def profile(func):
    """
    A decorator to measure the execution time and memory usage of a function.

    Args:
        func (callable): The function to be profiled.

    Returns:
        callable: The wrapped function with profiling capabilities.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Measure memory usage
        mem_usage = memory_usage((func, args, kwargs))

        # Measure execution time
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start_time

        logger.info(
            f"{func.__name__} - Time: {elapsed:.4f}s, "
            f"Memory: {max(mem_usage):.2f} MiB"
        )
        return result

    return wrapper