### 1. Installation

Install Django Async Framework from PyPI:

```bash
pip install djangoasyncframework
```

Then, add it to your Django `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    "async_framework",
]
```

### 2. Create Your First Async API View

Create a new Django view using `AsyncAPIView`:

```python
from async_framework.views.api import AsyncAPIView

class HelloWorldView(AsyncAPIView):
    async def get(self, request):
        return self.success({"message": "Hello from async!"})
```

This defines a fully async compatible GET view that returns a simple JSON response.

### 3. Add the View to Your URLs

In your `urls.py`:

```python
from django.urls import path
from .views import HelloWorldView

urlpatterns = [
    path("hello/", HelloWorldView.as_view()),
]
```

### 4. Try It Out

Run your Django development server:

```bash
python manage.py runserver
```

Then go to: [http://localhost:8000/hello/](http://localhost:8000/hello/)

You should see:

```json
{
  "message": "Hello from async!"
}
```

## What’s Next?

Want to explore more features? Check out the [tutorial](tutorial/asyncview.md).