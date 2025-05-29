import asyncio
import json

from django.http import JsonResponse

from async_framework.views.core import AsyncView


class AsyncAPIView(AsyncView):
    """
    A base class for creating asynchronous API views.
    """
    
    async def dispatch(self, request, *args, **kwargs):
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

        # Throttle check
        throttle_class = getattr(self, "throttle", None)
        if throttle_class:
            throttle = throttle_class
            if isinstance(throttle_class, type):  # allow class or instance
                throttle = throttle_class()
            allowed = await throttle.allow_request(request)
            if not allowed:
                return self.error("Rate limit exceeded", status=429)

        return await super().dispatch(request, *args, **kwargs)

    def success(self, data=None, status=200):
        return JsonResponse({"success": True, "data": data}, status=status)

    def error(self, message, status=400):
        return JsonResponse({"success": False, "error": message}, status=status)