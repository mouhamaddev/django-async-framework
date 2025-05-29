In an async Django view, calling blocking code like `MyModel.objects.get(...)` directly can block the event loop.

`await_safe` is a utility function to safely run blocking synchronous code such as Django ORM calls inside asynchronous views or functions.

## Example Usage

```python
from async_framework.orm import await_safe

async def get_user(request):
    user = await await_safe(MyModel.objects.get)(id=5)
    return JsonResponse({"username": user.username})
```

## Chained ORM Method

```python
async def view(request):
    first_item = await await_safe(MyModel.objects.filter(active=True).first)()
    return JsonResponse({"name": first_item.name})
```

## How does it work?

`await_safe(callable)` wraps the function with:

```python
sync_to_async(callable, thread_sensitive=True)
```

This shifts the execution to a thread pool, preserving thread safety in Django’s ORM.
