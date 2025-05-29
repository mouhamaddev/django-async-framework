import pytest
import json
from django.http import HttpRequest
from django.test import AsyncRequestFactory
from django.http import JsonResponse
from asgiref.testing import ApplicationCommunicator
from django.core.handlers.asgi import ASGIRequest

from async_framework.views.api import AsyncAPIView

from tests import django_config
django_config.configure()


@pytest.mark.asyncio
async def test_throttle_allows():
    class AllowingThrottle:
        async def allow_request(self, request):
            return True

    class TestView(AsyncAPIView):
        throttle = AllowingThrottle

        async def dispatch(self, request, *args, **kwargs):
            return self.success("allowed")

    factory = AsyncRequestFactory()
    request = factory.get("/")
    view = TestView()
    response = await view.dispatch(request)

    assert response.status_code == 200
    assert json.loads(response.content) == {"success": True, "data": "allowed"}


@pytest.mark.asyncio
async def test_throttle_blocks():
    class BlockingThrottle:
        async def allow_request(self, request):
            return False

    class TestView(AsyncAPIView):
        throttle = BlockingThrottle

    factory = AsyncRequestFactory()
    request = factory.get("/")
    view = TestView()
    response = await view.dispatch(request)

    assert response.status_code == 429
    assert json.loads(response.content) == {"success": False, "error": "Rate limit exceeded"}
