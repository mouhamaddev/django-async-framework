import asyncio
import time
from django.http import JsonResponse
from async_framework.orm import await_safe
from async_framework.views.core import AsyncView


class FakeUser:
    def __init__(self, id, username):
        self.id = id
        self.username = username

class FakeUserQuerySet:
    def get(self, id):
        # simulating a blocking db call
        import time
        time.sleep(0.2)
        return FakeUser(id=id, username="mocked_user")

    def filter(self, active=True):
        class Filtered:
            def first(self_inner):
                time.sleep(0.1)
                return FakeUser(id=2, username="first_active_user")
        return Filtered()


class AwaitSafeExampleView:
    # get by ID
    async def get_by_id(self, request):
        user = await await_safe(FakeUserQuerySet().get)(id=5)
        return JsonResponse({"username": user.username})

    # chained .filter().first()
    async def get_first_active(self, request):
        first = await await_safe(FakeUserQuerySet().filter(active=True).first)()
        return JsonResponse({"username": first.username})


class AwaitSafeView(AsyncView):
    async def get(self, request):
        mode = request.GET.get("mode")
        if mode == "id":
            return await AwaitSafeExampleView().get_by_id(request)
        elif mode == "first":
            return await AwaitSafeExampleView().get_first_active(request)
        return JsonResponse({"error": "Please specify mode=id or mode=first"}, status=400)