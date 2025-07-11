# DAF Development Log

Version: 0.2.0

08-07-2025
- Added support for per-task timeouts in @async_task which allows automatic cancellation and retry of long-running tasks.

06-07-2025
- Added services dependency injection support to AsyncView. Developers can now define a services dictionary (or override services_attr) to register per-request service factories. These are resolved once per request and attached to the view instance.
- Added @async_task decorator and AsyncTask background worker to support fire-and-forget async tasks with optional retries and delay scheduling.

02-07-2025
- Added async_setup() hook to AsyncView for async preloading and shared request initialization.

Version: 0.1.0

29-05-2025
- Set up initial demo project to test and validate current feature implementations.
- Create GitHub actions workflow to automate documentation deployment.

26-05-2025
- Wrote tests for previously added features.

25-05-2025
- Initialized documentation.
- Added main project intro, installation instructions, and quickstart guide.
- Documented usage and design in the tutorial section for the current features.

21-5-2025
- Integrated throttling logic directly into AsyncAPIView. Now rate limits will be enforced automatically during request dispatch.

20-5-2025
- Designed the architecture for the rate limiter AsyncRateThrottle that protects endpoints by limiting requests per user/IP.

17-5-2025
- Extended AsyncAPIView to automatically parse JSON request bodies into request.data before dispatching the view.
- Added helper methods: .success() and .error() to streamline standard JSON API responses.

16-5-2025
- Built async_error_middleware to catch and return JSON error responses from async views.
- Fixed coroutine handling issues using Django’s @sync_and_async_middleware to safely support both sync and async requests in middleware.

15-5-2025
- Created the first class: AsyncView. It enforces that all HTTP method handlers are async def and properly awaited.
- Implemented async-safe ORM access using await_safe() to prevent blocking the event loop. Previously, a 1s async API call + 1s ORM query took 2s total, now both can run concurrently in ~1s.
- Built run_in_background() utility for fire-and-forget async jobs without blocking the response.

22-02-2025
- Bith!