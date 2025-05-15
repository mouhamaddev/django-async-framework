from asgiref.sync import sync_to_async
import asyncio
import functools

def await_safe(callable_or_queryset_method):
    """
    Wrap a blocking ORM call inside sync_to_async.
    Example:
        await await_safe(MyModel.objects.get)(id=5)
        await await_safe(MyModel.objects.filter(...).first)()
    """
    return sync_to_async(callable_or_queryset_method, thread_sensitive=True)