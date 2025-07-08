import time


class AsyncRateThrottle:
    """
    A simple rate throttle for async views.
    This throttle allows a certain number of requests per time unit.
    For example, '10/minute' allows 10 requests per minute.
    
    Usage:
        class MyView(AsyncAPIView):
            throttle = AsyncRateThrottle(rate='5/second')

            async def get(self, request):
                if not await self.throttle.allow_request(request):
                    return self.error("Rate limit exceeded", status=429)
                return self.success({"msg": "Allowed!"})

        from async_framework.throttle import AsyncRateThrottle
    """

    def __init__(self, rate='10/minute'):
        self.num_requests, self.duration = self.parse_rate(rate)
        self.history = {} # {identifier: [timestamp1, timestamp2, ...]}

    def parse_rate(self, rate):
        num, unit = rate.split('/')
        num = int(num)
        if unit == 'second':
            return num, 1
        elif unit == 'minute':
            return num, 60
        elif unit == 'hour':
            return num, 3600
        else:
            raise ValueError("Unsupported time unit")

    async def allow_request(self, request):
        ident = self.get_identifier(request)
        now = time.time()

        request_times = self.history.get(ident, [])

        # Clean up timestamps older than duration
        request_times = [ts for ts in request_times if now - ts < self.duration]

        if len(request_times) >= self.num_requests:
            return False

        # Allow it and store this request time
        request_times.append(now)
        self.history[ident] = request_times
        return True

    def get_identifier(self, request):
        return request.META.get('REMOTE_ADDR', 'anonymous')
