import pytest
import asyncio
import json

from django.test import RequestFactory
from django.http import JsonResponse
from async_framework.views.core import AsyncView

from tests import django_config
django_config.configure()


@pytest.mark.asyncio
async def test_async_handler_runs_successfully():
    class MyView(AsyncView):
        async def get(self, request):
            return JsonResponse({"message": "async success"})

    factory = RequestFactory()
    request = factory.get('/')

    view = MyView.as_view()

    response = await view(request)

    assert response.status_code == 200
    assert json.loads(response.content) == {"message": "async success"}


@pytest.mark.asyncio
async def test_sync_handler_raises_type_error():
    # Invalid case
    class MyView(AsyncView):
        def get(self, request):
            return JsonResponse({"message": "sync not allowed"})

    factory = RequestFactory()
    request = factory.get('/')

    view = MyView.as_view()

    with pytest.raises(TypeError) as excinfo:
        await view(request)

    assert "must be async" in str(excinfo.value)