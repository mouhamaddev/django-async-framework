`async_error_middleware` is a middleware designed to catch exceptions in both synchronous and asynchronous views, returning a JSON response instead of the default HTML error page.

## Example Usage

To use the middleware, add it to your Django `settings.py`:

```python
MIDDLEWARE = [
    # other middleware
    'async_framework.middleware.async_error_middleware',
]
```

View that raises an exception:

```python
from django.http import JsonResponse

async def my_async_view(request):
    raise ValueError("Something went wrong")
```

Resulting JSON response:

```json
{
  "error": "Something went wrong",
  "type": "ValueError",
  "trace": "Traceback (most recent call last):\n  File ... \nValueError: Something went wrong"
}
```
