import asyncio
import functools
import traceback

from typing import Callable


# --- AsyncTask ---

class AsyncTask:
    """
    A simple async task wrapper that allows scheduling async functions to run
    in the background with optional retries and delays.
    This class provides a decorator-like interface to define async tasks that can
    be scheduled to run later.
    
    Usage:
        @async_task(retries=3, delay=2)
        async def send_welcome_email(user_id):
            print(f"Sending email to user {user_id}")
            # simulate network call
            await asyncio.sleep(0.5)
            print(f"Email sent to user {user_id}")

        # In some async view
        await send_welcome_email.delay(123)

    Args:
        func (Callable): The async function to be wrapped as a task.
        retries (int): Number of times to retry the task on failure.
        delay (float): Delay in seconds before executing the task.

    Methods:
        __call__(*args, **kwargs): Directly call the wrapped async function.
        delay(*args, **kwargs): Schedule the task to run asynchronously with given args.

    Static Methods:
        _start_worker(): Start the background worker that processes queued tasks.
        _worker_loop(): The main loop that processes tasks from the queue.

    Returns:
        None: The task is scheduled to run in the background.
    """

    _queue = asyncio.Queue()
    _worker_started = False

    def __init__(self, func: Callable, retries: int = 0, delay: float = 0, timeout: float = None):
        self.func = func
        self.retries = retries
        self._delay = delay
        self.timeout = timeout

        functools.update_wrapper(self, func)

    async def __call__(self, *args, **kwargs):
        # Direct call runs immediately (like normal function)
        return await self.func(*args, **kwargs)

    def delay(self, *args, **kwargs):
        """
        Schedule the task to run asynchronously with given args.
        Returns immediately.
        """
        if not AsyncTask._worker_started:
            AsyncTask._start_worker()

        # Enqueue the task call info
        AsyncTask._queue.put_nowait((self, args, kwargs, 0))  # 0 retries done

    @staticmethod
    def _start_worker():
        """ Start the background worker that processes queued tasks.
            This method should be called once to initialize the worker loop."""
        AsyncTask._worker_started = True
        # loop = asyncio.get_event_loop()
        loop = asyncio.get_running_loop()
        loop.create_task(AsyncTask._worker_loop())

    @staticmethod
    async def _worker_loop():
        """ The main loop that processes tasks from the queue.
            This runs in the background and handles retries and delays."""
        while True:
            task, args, kwargs, attempt = await AsyncTask._queue.get()
            try:
                if task._delay > 0:
                    await asyncio.sleep(task._delay)

                if task.timeout:
                    await asyncio.wait_for(task.func(*args, **kwargs), timeout=task.timeout)
                else:
                    await task.func(*args, **kwargs)

            except Exception:
                if attempt < task.retries:
                    print(f"Task failed, retrying attempt {attempt+1}/{task.retries}") # TODO: Log the error
                    traceback.print_exc()
                    # Re-enqueue with incremented attempt count
                    AsyncTask._queue.put_nowait((task, args, kwargs, attempt + 1))
                else:
                    print("Task failed after retries, giving up:") # TODO: Log the error
                    traceback.print_exc()

            AsyncTask._queue.task_done()


# --- async_task decorator ---

def async_task(retries: int = 0, delay: float = 0, timeout: float = None):
    """
    Decorator to wrap an async function as an AsyncTask.
    """
    def decorator(func):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("@async_task can only decorate async functions")
        return AsyncTask(func, retries=retries, delay=delay, timeout=timeout)
    return decorator
