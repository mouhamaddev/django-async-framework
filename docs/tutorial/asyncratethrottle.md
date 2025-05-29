`AsyncRateThrottle` is a simple asynchronous rate-limiting utility designed for use with async views. It allows restricting the number of requests a client can make within a specified time window.

## Example Usage

```python
from async_framework.throttle import AsyncRateThrottle
from async_framework.views.api import AsyncAPIView

class AsyncRateThrottleView(AsyncAPIView):
    throttle = AsyncRateThrottle(rate='5/second') # Time units supported: second, minute, and hour

    async def get(self, request):
        if not await self.throttle.allow_request(request):
            return self.error("Rate limit exceeded", status=429)
        return self.success({"msg": "Allowed!"})
```

## How Does It Work?

1. You instantiate it with a rate string like `'10/minute'`.
2. The rate is parsed into a number of requests and a time duration in seconds.
3. For each request, it fetches the client identifier (defaulting to the remote IP).
4. It removes timestamps older than the current window from its in-memory history.
5. If the number of requests within the window exceeds the allowed number, it rejects the request.
6. Otherwise, it records the current request time and permits the request.

Important Note: The throttle uses an in-memory dictionary to store request history, so it works best in single-process environments.
For multi-process or distributed deployments, a shared cache or database-backed throttle would be necessary.