from async_framework.views.core import AsyncView

class ErrorRaisingView(AsyncView):
    async def get(self, request):
        raise ValueError("Something went wrong")
