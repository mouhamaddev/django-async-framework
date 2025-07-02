> `AsyncView` is the foundation of Async framework.
> It currently performs two main jobs:
>
> 1. Ensures that all your HTTP method handlers (`get`, `post`, etc.) are defined as `async def`. This protects the event loop and enforces non-blocking views.
> 2. Provides an async lifecycle hook `async_setup()` that runs **once before** the HTTP handler, allowing you to preload data, inject dependencies, or run async checks that multiple handlers can share.
>
> Its implementation is minimal right now, but AsyncView will serve as the base class for all future async features in Async framework.

## Example Usage

```python
from async_framework.views.core import AsyncView
from django.http import JsonResponse

class MyAsyncView(AsyncView):
    async def async_setup(self, request, *args, **kwargs):
        # Runs before each HTTP method handler
        self.user_data = await load_user_data_async(request.user)

    async def get(self, request):
        return JsonResponse({"user_data": self.user_data})
```

## How Does It Work?

1. Overrides the standard `dispatch` method.
2. Before calling the handler, it checks if the handler is async. If not, it raises a `TypeError`.
3. Awaits the new async lifecycle hook `async_setup()` — allowing any async initialization or preloading.
4. Awaits the HTTP handler method (e.g., `get()`, `post()`).

> This pattern avoids duplication of async setup code in each handler and keeps your views clean and efficient.
