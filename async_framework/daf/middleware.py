import asyncio
from django.http import JsonResponse
from django.utils.decorators import sync_and_async_middleware
import traceback

@sync_and_async_middleware
def async_error_middleware(get_response):
    """
    Catches errors in async views and returns detailed JSON responses.
    This middleware should be added to the MIDDLEWARE setting in Django settings.
    Example:
        MIDDLEWARE = [
            ...
            'daf.middleware.async_error_middleware',
            ...
        ]
    """
    if asyncio.iscoroutinefunction(get_response):
        async def middleware(request):
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

    def middleware(request):
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
