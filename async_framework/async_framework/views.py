import asyncio
from django.http import HttpResponse
from django.http import JsonResponse

from async_framework.models import Entity

from daf.core import AsyncView
from daf.orm import await_safe, run_in_background


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
