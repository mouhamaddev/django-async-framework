import asyncio

from django.views import View

from django.http import HttpRequest, HttpResponse
from typing import Any

from .service_resolver import _resolve_services

class AsyncView(View):
    """
    AsyncView is the base class for writing fully asynchronous Django views.

    1) All HTTP method handlers must be defined as async def.  
        If you use a regular function by mistake, a TypeError is raised to protect the
        async event loop.

    2) Define an async_setup() method to run custom async logic before the request is handled
        for preloading data, fetching related models, or any per-request setup.
        Usage of this hook is optional, but recommended for async-safe operations.

    3) Declare a services dictionary (or override services_attr) with factories for services
        your view depends on.  
        They're resolved once per request and attached to the view instance, so your code
        stays clean and DRY.
    
    Usage:
        class MyView(AsyncView):
            services = {
                "reporting": lambda: ReportingService(),
            }

            async def async_setup(self, request, *args, **kwargs):
                self.user = await User.objects.aget(pk=request.user.pk)

            async def get(self, request):
                data = await self.services.reporting.get_report(self.user)
                return JsonResponse(data)
    """

    services_attr = "services"  # Default services attribute name, can be overridden in subclasses.

    async def http_method_not_allowed(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Async-compatible version of the default method-not-allowed handler.
        """
        return HttpResponse(f"Method {request.method} not allowed", status=405)

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
        await _resolve_services(self)

        # Call the handler and await its result
        return await handler(request, *args, **kwargs)

    async def async_setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        """
        Override this in your views to preload data (async-safe).
        """
        pass
