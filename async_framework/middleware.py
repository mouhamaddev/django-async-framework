import asyncio
import traceback
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.utils.decorators import sync_and_async_middleware
from typing import Callable, Union, Awaitable


@sync_and_async_middleware
def async_error_middleware(
    get_response: Union[Callable[[HttpRequest], HttpResponse], Callable[[HttpRequest], Awaitable[HttpResponse]]]
) -> Callable[[HttpRequest], Union[HttpResponse, Awaitable[HttpResponse]]]:
    """
    Middleware to catch unhandled exceptions in both sync and async views.
    Returns detailed JSON error responses instead of Django's HTML debug page.

    This should be added to Django's MIDDLEWARE setting:
        MIDDLEWARE = [
            ...
            'async_framework.middleware.async_error_middleware',
            ...
        ]

    Args:
        get_response: The next middleware or view to call.

    Returns:
        A middleware function that handles errors gracefully.
    """

    # Async path
    if asyncio.iscoroutinefunction(get_response):
        async def middleware(request: HttpRequest) -> HttpResponse:
            try:
                return await get_response(request)
            except Exception as e:
                tb = traceback.format_exc()
                print(f"[Async Error] {e}\n{tb}")
                return JsonResponse({
                    "error": str(e),
                    "type": e.__class__.__name__,
                    "trace": tb,
                }, status=500)
        return middleware

    # Sync path
    def middleware(request: HttpRequest) -> HttpResponse:
        try:
            return get_response(request)
        except Exception as e:
            tb = traceback.format_exc()
            print(f"[Sync Error] {e}\n{tb}")
            return JsonResponse({
                "error": str(e),
                "type": e.__class__.__name__,
                "trace": tb,
            }, status=500)
    return middleware
