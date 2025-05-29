import pytest
import asyncio
import time

from async_framework.orm import await_safe

from tests import django_config
django_config.configure()


def slow_sync_function(x: int) -> int:
    """Simulate a blocking sync function."""
    time.sleep(1)  # Blocking call
    return x * 2


@pytest.mark.asyncio
async def test_await_safe_wraps_sync_function():
    start = time.perf_counter()
    result = await await_safe(slow_sync_function)(5)
    end = time.perf_counter()

    assert result == 10
    assert (end - start) < 1.5  # Should run in ~1s, not block whole event loop


@pytest.mark.asyncio
async def test_await_safe_runs_concurrently():
    """Tests that two await_safe calls run in parallel, not sequentially."""

    async def run_task():
        return await await_safe(slow_sync_function)(3)

    start = time.perf_counter()
    results = await asyncio.gather(run_task(), run_task())
    end = time.perf_counter()

    assert results == [6, 6]
    assert (end - start) < 2.0  # Should not take 2s, both should run concurrently
