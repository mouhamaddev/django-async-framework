import asyncio
import functools

def run_in_background(coro_func, *args, **kwargs):
    """
    Fire-and-forget async function runner.
    Example: run_in_background(some_task, user_id=5)
    """
    async def wrapper():
        try:
            await coro_func(*args, **kwargs)
        except Exception as e:
            # TODO: logging
            print(f"[Background Task Error] {e}")

    asyncio.create_task(wrapper())
