import asyncio

from typing import Awaitable, Callable, TypeVar

_R = TypeVar("_R")


# --- run_in_background ---

def run_in_background(coro_func: Callable[..., Awaitable[_R]], *args, **kwargs) -> asyncio.Task[_R]:
    """
    Schedule an async coroutine function to run in the background (fire-and-forget).
    
    This function wraps the coroutine and ensures that any exceptions raised
    during execution are caught and logged, preventing unhandled exceptions
    from crashing the event loop.

    Usage:
        run_in_background(some_async_task, arg1, arg2, key=value)

    Args:
        coro_func (coroutine function): The async function to be executed in the background.
        *args: Positional arguments to pass to the coroutine function.
        **kwargs: Keyword arguments to pass to the coroutine function.

    Returns:
        None
    """
    async def wrapper():
        try:
            await coro_func(*args, **kwargs)
        except Exception as e:
            print(f"[Background Task Error] {e}")

    # Schedule the wrapper coroutine as a background task
    asyncio.create_task(wrapper())
