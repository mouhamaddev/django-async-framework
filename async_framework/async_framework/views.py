from django.http import HttpResponse

def hello_world(request):
    return HttpResponse("Hello, World!")


async def async_hello_world(request):
    return HttpResponse("Hello, World!")
