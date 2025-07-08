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


@pytest.mark.asyncio
async def test_async_setup_sets_value():
    class MyView(AsyncView):
        async def async_setup(self, request, *args, **kwargs):
            self.foo = "bar"

        async def get(self, request):
            return JsonResponse({"foo": self.foo})

    request = RequestFactory().get('/')
    response = await MyView.as_view()(request)

    assert response.status_code == 200
    assert json.loads(response.content) == {"foo": "bar"}


@pytest.mark.asyncio
async def test_async_setup_with_await():
    async def fake_db_call():
        return "data123"

    class MyView(AsyncView):
        async def async_setup(self, request, *args, **kwargs):
            self.data = await fake_db_call()

        async def get(self, request):
            return JsonResponse({"data": self.data})

    request = RequestFactory().get('/')
    response = await MyView.as_view()(request)

    assert response.status_code == 200
    assert json.loads(response.content) == {"data": "data123"}


@pytest.mark.asyncio
async def test_async_setup_can_block_request():
    class MyView(AsyncView):
        async def async_setup(self, request, *args, **kwargs):
            self.block = True

        async def get(self, request):
            if self.block:
                return JsonResponse({"error": "Blocked"}, status=403)
            return JsonResponse({"ok": True})

    request = RequestFactory().get('/')
    response = await MyView.as_view()(request)

    assert response.status_code == 403
    assert json.loads(response.content) == {"error": "Blocked"}


@pytest.mark.asyncio
async def test_async_setup_default_noop():
    class MyView(AsyncView):
        async def get(self, request):
            return JsonResponse({"ok": True})

    request = RequestFactory().get('/')
    response = await MyView.as_view()(request)

    assert response.status_code == 200
    assert json.loads(response.content) == {"ok": True}


@pytest.mark.asyncio
async def test_services_are_resolved_and_accessible():
    class MockService:
        async def get_data(self):
            return "mocked"

    class MyView(AsyncView):
        services = {
            "my_service": lambda: MockService()
        }

        async def get(self, request):
            result = await self.services["my_service"].get_data()
            return JsonResponse({"result": result})

    request = RequestFactory().get('/')
    response = await MyView.as_view()(request)

    assert response.status_code == 200
    assert json.loads(response.content) == {"result": "mocked"}


@pytest.mark.asyncio
async def test_custom_services_attr_is_honored():
    class CustomService:
        async def hello(self):
            return "world"

    class MyView(AsyncView):
        services_attr = "deps"
        deps = {
            "svc": lambda: CustomService()
        }

        async def get(self, request):
            msg = await self.deps["svc"].hello()
            return JsonResponse({"msg": msg})

    request = RequestFactory().get('/')
    response = await MyView.as_view()(request)

    assert response.status_code == 200
    assert json.loads(response.content) == {"msg": "world"}


@pytest.mark.asyncio
async def test_services_resolved_after_async_setup():
    class MyView(AsyncView):
        async def async_setup(self, request, *args, **kwargs):
            self.services = {
                "svc": lambda: type("DynamicService", (), {
                    "get": lambda self: "configured"
                })()
            }

        async def get(self, request):
            return JsonResponse({"value": self.services["svc"].get()})

    request = RequestFactory().get('/')
    response = await MyView.as_view()(request)

    assert response.status_code == 200
    assert json.loads(response.content) == {"value": "configured"}
