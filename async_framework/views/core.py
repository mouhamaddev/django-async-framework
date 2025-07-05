import asyncio
import inspect

from django.views import View

from django.http import HttpRequest, HttpResponse
from typing import Any

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

    async def _resolve_services(self):
        """
        Resolves services defined in the view.
        
        This method looks for a dictionary of service definitions
        in the view and initializes them, allowing for both synchronous
        and asynchronous service factories.
        """

        attr_name = getattr(self, "services_attr", "services")
        service_defs = getattr(self, attr_name, None)

        if not isinstance(service_defs, dict):
            return  # nothing to resolve

        resolved = {}

        # Iterate over the service definitions and resolve each one.
        # If a service definition is callable, it will be called to get the value.
        # If the value is awaitable, it will be awaited.
        # If an exception occurs during resolution, it will raise a RuntimeError
        # with a message indicating which service failed to initialize.
        if not service_defs:
            return
        
        if not isinstance(service_defs, dict):
            raise TypeError(f"Expected 'services' to be a dictionary, got {type(service_defs).__name__}")
        
        if not all(isinstance(key, str) for key in service_defs.keys()):
            raise TypeError("All keys in 'services' must be strings")
        
        if not all(callable(factory) or isinstance(factory, (str, int, float, bool, dict, list)) for factory in service_defs.values()):
            raise TypeError("All values in 'services' must be callable or basic types (str, int, float, bool, dict, list)")
        
        for key, factory in service_defs.items():
            try:
                if callable(factory):
                    value = factory()
                else:
                    value = factory

                if inspect.isawaitable(value):
                    value = await value

                resolved[key] = value

            except Exception as e:
                raise RuntimeError(f"Failed to initialize service '{key}': {e}")

        setattr(self, attr_name, resolved)
