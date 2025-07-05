import asyncio
import functools
from asgiref.sync import sync_to_async

from typing import Callable, Coroutine, TypeVar, Any

_R = TypeVar("_R")


def await_safe(callable_or_queryset_method: Callable[..., _R]) -> Callable[..., Coroutine[Any, Any, _R]]:
    """
    Wrap a blocking ORM call inside sync_to_async to safely run it
    in an asynchronous context without blocking the event loop.

    Usage:
        await await_safe(MyModel.objects.get)(id=5)

    Args:
        callable_or_queryset_method (callable):
            A synchronous ORM callable or queryset method that needs to
            be executed asynchronously.

    Returns:
        An awaitable coroutine wrapping the original callable, that
        runs the blocking ORM call in a thread-safe way using
        sync_to_async.

    Performance note:
        Prevents blocking the event loop.  For example, if you had an
        async API call taking 1s plus a 1s ORM query executed synchronously,
        total runtime was 2s sequentially.
        Using this function allows them to run concurrently, reducing total
        time closer to 1s.
    """
    # Wrap the synchronous callable using sync_to_async with thread sensitivity
    return sync_to_async(callable_or_queryset_method, thread_sensitive=False)