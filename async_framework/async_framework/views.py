import asyncio
from django.http import HttpResponse
from django.http import JsonResponse

def hello_world(request):
    return HttpResponse("Hello, World!")


async def async_hello_world(request):
    return HttpResponse("Hello, World!")


async def delayed_response(request):
    await asyncio.sleep(3)
    
    return JsonResponse({"message": "This response was delayed by 3 seconds!"})
