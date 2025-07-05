import asyncio

from django.views import View

from django.http import HttpRequest, HttpResponse
from typing import Any

from .service_resolver import _resolve_services

class AsyncView(View):
    """
    Enforces all HTTP method handlers
    to be defined as async functions.
    # TODO: Update the comment above to better reflect the usage details.
    # TODO: And add more details about the services attribute and its usage.
    """

    services_attr = "services"  # Default services attribute name, can be overridden in subclasses.

    async def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Overrides the default dispatch method to support async method handling.
        Ensures that the method handler is an async def,
        and awaits its execution.

        Args:
            request: The HTTP request object.
            *args, **kwargs: Additional arguments passed to the view.

        Returns:
            The awaited response from the async handler.
        """

        # Dynamically get the handler method based on the request's HTTP method
        handler = getattr(self, request.method.lower(), self.http_method_not_allowed)

        # Ensure the handler is an asynchronous function
        if not asyncio.iscoroutinefunction(handler):
            raise TypeError(f"{handler.__name__} must be async")

        await self.async_setup(request, *args, **kwargs)
        await self._resolve_services()

        # Call the handler and await its result
        return await handler(request, *args, **kwargs)

    async def async_setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        """
        Override this in your views to preload data (async-safe).
        """
        pass
