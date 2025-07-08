The `@async_task` decorator and `AsyncTask` class provide a simple, lightweight in-memory async task queue system designed to help scheduling asynchronous functions to run in the background without blocking the main request/response cycle.

This system supports:

* Scheduling async functions to run later (fire-and-forget style)
* Optional retrying on failure, with configurable retry count
* Optional delay before task execution
* Automatic background worker that processes tasks asynchronously


You could use this function when your application performs time-consuming async operations such as sending emails, calling external APIs, or processing data and you don’t want to block the user’s request and make them wait.

## Example Usage
```python
from async_framework.utils import async_task

@async_task(retries=1, delay=1.5)
async def heavy_operation(user_id):
    print(f"Starting heavy operation for user {user_id}")
    await asyncio.sleep(2)
    print(f"Completed heavy operation for user {user_id}")

# Schedule task to run in background
heavy_operation.delay(123)

# Continue handling request without waiting
```

* `retries` (int): Number of times to retry on failure (default 0)
* `delay` (float): Delay in seconds before running the task (default 0)


## Scheduling Tasks

Call the `.delay()` method on the decorated function to schedule the task asynchronously:

```python
send_welcome_email.delay(42)
```

<br>

**Notes**:
* Currently, the queue is **in-memory and single-process**, meaning tasks are lost if the app restarts and no distributed processing is supported.
* Suitable for lightweight async tasks or during early development.
* Future plans may include persistent queues, task logging and tracking, and multi-worker support.

