from django.views import View
import asyncio

class AsyncView(View):
    async def dispatch(self, request, *args, **kwargs):
        handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        if not asyncio.iscoroutinefunction(handler):
            raise TypeError(f"{handler.__name__} must be async")
        return await handler(request, *args, **kwargs)
