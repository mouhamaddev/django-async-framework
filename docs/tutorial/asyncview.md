> `AsyncView` is the foundation of Async framework.
> It currently performs one main job: it ensures that all your HTTP methods are async def. This protects the event loop and ensures you're writing non-blocking views.
>
> Its implementation is minimal right now, but AsyncView will serve as the base class for all future async features in Async framework.

## Example Usage

```python
from async_framework.views.core import AsyncView
from django.http import JsonResponse

class MyAsyncView(AsyncView):
    async def get(self, request):
        # Simulate async operation
        await some_async_task()
        return JsonResponse({"message": "This view is fully async!"})
```

## How Does It Work?

1. It overrides the standard dispatch method.
2. Before calling the handler, it checks if the handler is async. If not, it raises a TypeError.
3. It awaits the handler to properly handle the asynchronous execution flow.

Note: This means that you cannot accidentally write synchronous handlers when using AsyncView, and your view methods must be written as async def.
