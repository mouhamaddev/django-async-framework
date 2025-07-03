# DAF Development Log

Version: 1.0

15-5-2025
- Created my first class: AsyncView, enabling fully async class-based views by enforcing that all HTTP method handlers are async def and properly awaited.
- Implemented async-safe ORM access using await_safe() to prevent blocking the event loop. Previously, a 1s async API call + 1s ORM query took 2s total — now both can run concurrently in ~1s.
- Built run_in_background() utility for fire-and-forget async jobs (e.g., syncing, polling, etc.) without blocking the response.

16-5-2025
- Built async_error_middleware to catch and return JSON error responses from async views.
- Fixed coroutine handling issues using Django’s @sync_and_async_middleware to safely support both sync and async requests in middleware.

17-5-2025
- Extended AsyncAPIView to automatically parse JSON request bodies into request.data before dispatching the view.
- Added helper methods like .success() and .error() to streamline standard JSON API responses.

20-5-2025
- Designed the architecture for AsyncRateThrottle, an async-compatible rate limiter that protects endpoints by limiting requests per user/IP.

21-5-2025
- Integrated throttling logic directly into AsyncAPIView. Now rate limits will be enforced automatically during request dispatch.

26-05-2025
- Initialized documentation.
- Added main project intro, installation instructions, and quickstart guide.
- Documented usage and design in the tutorial section for the current features.

26-05-2025
- Wrote tests for current features.

28-05-2025
- Refined documentation for clarity and corrected minor errors.

29-05-2025
- Set up initial demo project to test and validate current feature implementations.
- Create GitHub actions workflow to automate documentation deployment.

02-07-2025:
- Added async_setup() hook to AsyncView for async preloading and shared request initialization.