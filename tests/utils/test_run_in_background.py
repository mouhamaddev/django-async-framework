import asyncio
import pytest
from unittest.mock import AsyncMock
from async_framework.utils import run_in_background

from tests import django_config
django_config.configure()


@pytest.mark.asyncio
async def test_run_in_background_executes_task(monkeypatch):
    mock_coro = AsyncMock()

    original_create_task = asyncio.create_task
    monkeypatch.setattr("asyncio.create_task", lambda coro: original_create_task(coro))

    run_in_background(mock_coro, 42, foo="bar")

    await asyncio.sleep(0.1)

    mock_coro.assert_called_once_with(42, foo="bar")


@pytest.mark.asyncio
async def test_run_in_background_handles_exceptions(monkeypatch, capsys):
    async def failing_coro():
        raise ValueError("Oops!")

    original_create_task = asyncio.create_task
    monkeypatch.setattr("asyncio.create_task", lambda coro: original_create_task(coro))

    run_in_background(failing_coro)

    await asyncio.sleep(0.1)

    captured = capsys.readouterr()
    assert "[Background Task Error]" in captured.out
    assert "Oops!" in captured.out