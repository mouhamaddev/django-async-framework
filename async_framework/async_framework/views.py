import asyncio
from django.http import HttpResponse
from django.http import JsonResponse

from async_framework.models import Entity

from daf.core import AsyncView
from daf.orm import await_safe
from daf.utils import run_in_background


def hello_world(request):
    return HttpResponse("Hello, World!")


async def async_hello_world(request):
    return HttpResponse("Hello, World!")


async def delayed_response(request):
    await asyncio.sleep(3)
    
    return JsonResponse({"message": "This response was delayed by 3 seconds!"})


class PingView(AsyncView):
    async def get(self, request):
        await asyncio.sleep(1) # Simulate a delay
        return JsonResponse({"message": "pong", "status": "async"})


class DBView(AsyncView):
    async def get(self, request):
        entity = await await_safe(lambda: Entity.objects.all().last())()
        return JsonResponse({"entity_id": entity.id if entity else None})
    

class RunInBackgroundView(AsyncView):
    async def some_async_job(user_id):
        # Simulate a long-running task
        await asyncio.sleep(5)
        print(f"Job done for user {user_id}")

    async def get(self, request):
        run_in_background(self.some_async_job, request.user.id)
        return JsonResponse({"status": "Started in background"})