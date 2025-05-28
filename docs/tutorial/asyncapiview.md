`AsyncAPIView` is a base class for creating asynchronous API views, built on top of `AsyncView`. It helps handling async HTTP requests with JSON payload parsing, success/error JSON responses, and optional async throttling support.

## Example Usage

```python
from daf.views.api import AsyncAPIView

class MyView(AsyncAPIView):
    async def post(self, request):
        data = request.data
        # Perform async operations here
        return self.success({"echo": data})
```

## How Does It Work?

1. For mutating HTTP methods (`POST`, `PUT`, `PATCH`), it reads and parses the JSON request body asynchronously.
2. If throttling is enabled by setting the `throttle` attribute, the view will await the throttle's `allow_request` method. If the request is blocked, a 429 error is returned.
3. Otherwise, it delegates to the async method handler (like `post`, `get`, etc.) implemented by the subclass.
4. The `success` and `error` methods simplify returning JSON responses with consistent formatting.
