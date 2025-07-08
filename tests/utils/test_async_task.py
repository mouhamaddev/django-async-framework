import asyncio
import pytest
from async_framework.tasks import async_task, AsyncTask

from tests import django_config
django_config.configure()


@pytest.fixture(autouse=True)
def reset_async_task_state():
    AsyncTask._queue = asyncio.Queue()
    AsyncTask._worker_started = False


@pytest.mark.asyncio
async def test_async_task_runs_successfully(capsys):
    output = []

    @async_task()
    async def sample_task(x):
        output.append(x)

    sample_task.delay(10)

    await asyncio.sleep(0.1)

    assert output == [10]


@pytest.mark.asyncio
async def test_async_task_retries_on_failure(capsys):
    call_attempts = []

    @async_task(retries=2)
    async def flaky_task():
        call_attempts.append(1)
        raise ValueError("Boom!")

    flaky_task.delay()

    await asyncio.sleep(0.5)

    captured = capsys.readouterr()
    assert "Task failed, retrying attempt" in captured.out
    assert "Task failed after retries" in captured.out
    assert len(call_attempts) == 3  # original + 2 retries


@pytest.mark.asyncio
async def test_async_task_delay_executes_after_delay(monkeypatch):
    timestamps = []

    @async_task(delay=0.2)
    async def delayed_task():
        timestamps.append(asyncio.get_event_loop().time())

    start_time = asyncio.get_event_loop().time()
    delayed_task.delay()

    await asyncio.sleep(0.3)

    assert timestamps  # ensure the task ran
    assert timestamps[0] - start_time >= 0.2


def test_async_task_decorator_rejects_non_async():
    with pytest.raises(TypeError, match="only decorate async functions"):
        @async_task()
        def not_async():
            pass


@pytest.mark.asyncio
async def test_async_task_timeout(capsys):
    call_attempts = []

    @async_task(timeout=0.1, retries=1)
    async def slow_task():
        call_attempts.append(1)
        await asyncio.sleep(0.5)  # sleep longer than the timeout

    slow_task.delay()

    await asyncio.sleep(1)  # enough time for retries to complete

    captured = capsys.readouterr()
    assert "Task failed, retrying attempt" in captured.out
    assert "Task failed after retries" in captured.out
    assert len(call_attempts) == 2  # original + 1 retry
