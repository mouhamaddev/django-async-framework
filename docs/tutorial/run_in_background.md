`run_in_background` is a simple yet essential utility function designed to help running asynchronous tasks in the background. It provides a fire-and-forget mechanism for coroutine functions to trigger async operations that run concurrently alongside the application.

This function is one of the core building blocks of the Async Framework, but it is still in its early stages of development. At present, it focuses on the core functionality of launching background async tasks with basic error handling. Future versions may introduce advanced capabilities.

## Example Usage
```python
from async_framework.utils import run_in_background

async def send_welcome_email(user_id: int):
    await some_async_email_service.send(user_id)

def user_signup(user_data):
    new_user_id = create_user_in_db(user_data)
    
    # send welcome email in background without waiting
    run_in_background(send_welcome_email, new_user_id)
    
    return "Signup complete!"
```

Note: Since `run_in_background` does not wait for or monitor the completion of the task it starts, it’s not suitable for use cases where you need to track results or handle complex error recovery.