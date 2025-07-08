> `AsyncView` is the foundation of the Async framework.
> It currently performs **three** main jobs:
>
> 1. Enforces `async def`: All your HTTP method handlers (`get`, `post`, etc.) must be asynchronous. This protects the event loop and ensures your views are non-blocking.
> 2. Provides an `async_setup()` hook: Runs once before the HTTP handler. Use it to preload data, inject context, or run per-request async logic that multiple handlers can share.
> 3. Supports services dependency injection: Define a `services` dictionary (or override the `services_attr`) to register per-request service factories. These are resolved once per request and attached to your view instance, keeping your code clean and DRY.

## Example Usage

```python
from async_framework.views.core import AsyncView
from django.http import JsonResponse

class MyAsyncView(AsyncView):
    services = {
        "analytics": lambda: AnalyticsService(),
    }

    async def async_setup(self, request, *args, **kwargs):
        self.user_data = await load_user_data_async(request.user)

    async def get(self, request):
        report = await self.services["analytics"].generate_report(self.user_data)
        return JsonResponse({"report": report})
```

## How Does It Work?

1. Overrides `dispatch()` to fully support `async def` methods.
2. Validates that the handler (e.g., `get`, `post`) is asynchronous. If not, it raises a `TypeError`.
3. Awaits `async_setup()` to perform any per-request async initialization (optional).
4. Resolves all defined services in `self.services` using their factory functions. These can be sync or async.
5. Finally, awaits the actual handler method.

> This pattern keeps your views minimal, safe, and composable — and allows clean injection of services, like logging, analytics, business logic, or database wrappers.
