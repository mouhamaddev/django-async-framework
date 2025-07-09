from async_framework.views.api import AsyncAPIView
from async_framework.throttle import AsyncRateThrottle


class ThrottledStatusView(AsyncAPIView):
    throttle = AsyncRateThrottle(rate='5/second')

    async def get(self, request):
        if not await self.throttle.allow_request(request):
            return self.error("Rate limit exceeded", status=429)
        return self.success({"status": "OK", "info": "Service is running fine."})
