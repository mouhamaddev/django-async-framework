import asyncio
import json
import pytest
from django.http import HttpRequest
from django.test import AsyncRequestFactory, RequestFactory
from async_framework.middleware import async_error_middleware

from tests import django_config
django_config.configure()


@pytest.mark.django_db
def test_sync_view_exception_returns_json_response():
    def failing_view(request: HttpRequest):
        raise ValueError("Oops, sync!")

    middleware = async_error_middleware(failing_view)
    request = RequestFactory().get("/")

    response = middleware(request)

    assert response.status_code == 500
    json_data = json.loads(response.content.decode())
    assert json_data["error"] == "Oops, sync!"
    assert json_data["type"] == "ValueError"
    assert "trace" in json_data


@pytest.mark.asyncio
async def test_async_view_exception_returns_json_response():
    async def failing_view(request: HttpRequest):
        raise RuntimeError("Oops, async!")

    middleware = async_error_middleware(failing_view)

    from asgiref.compatibility import guarantee_single_callable
    from django.test.client import RequestFactory

    request = RequestFactory().get("/")
    request._is_coroutine = asyncio.coroutines._is_coroutine
    
    middleware = guarantee_single_callable(middleware)

    response = await middleware(request)

    assert response.status_code == 500
    json_data = json.loads(response.content.decode())
    assert json_data["error"] == "Oops, async!"
    assert json_data["type"] == "RuntimeError"
    assert "trace" in json_data
