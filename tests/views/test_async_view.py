import pytest
import asyncio
import json

from django.test import RequestFactory
from django.http import JsonResponse
from daf.views.core import AsyncView

from tests.utils import django_config
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


# TODO: Fix this test once we have a way to handle method not allowed in async views
# @pytest.mark.asyncio
# async def test_http_method_not_allowed():
#     class MyView(AsyncView):
#         async def get(self, request):
#             return JsonResponse({"message": "get called"})

#     factory = RequestFactory()
#     request = factory.post('/')  # POST not defined, should call http_method_not_allowed

#     view = MyView.as_view()

#     response = await view(request)
#     assert response.status_code == 405 # Method Not Allowed