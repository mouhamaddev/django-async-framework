
import asyncio
import json

from django.http import JsonResponse

from daf.core import AsyncView


class AsyncAPIView(AsyncView):
    """
    A base class for creating asynchronous API views.

    Example:
        class MyView(AsyncAPIView):
            async def post(self, request):
                data = request.data
                # Perform async operations here
                return self.success({"echo": data})
    """
    
    async def dispatch(self, request, *args, **kwargs):
        # This runs BEFORE Django calls the actual post(), put(), etc. and injects request.data

        if request.method in ("POST", "PUT", "PATCH"):
            try:
                body = await request.body

                if body:
                    request.data = json.loads(body)
                else:
                    request.data = {}
            except Exception:
                request.data = {}
        else:
            request.data = {}

        return await super().dispatch(request, *args, **kwargs)

    def success(self, data=None, status=200):
        return JsonResponse({"success": True, "data": data}, status=status)

    def error(self, message, status=400):
        return JsonResponse({"success": False, "error": message}, status=status)