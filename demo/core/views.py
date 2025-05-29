import time
from django.http import JsonResponse

from async_framework.views.core import AsyncView
from async_framework.views.api import AsyncAPIView


# AsyncView
class MyAsyncView(AsyncView):
    async def get(self, request):
        time.sleep(1)
        return JsonResponse({"message": "This view is fully async!"})
    

# AsyncAPIView
class MyAsyncAPIView(AsyncAPIView):
    async def get(self, request):
        data = request.data
        time.sleep(1)
        return self.success({"echo": data})