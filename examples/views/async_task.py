import asyncio
from django.http import JsonResponse
from async_framework.views.core import AsyncView
from async_framework.utils import async_task


@async_task(retries=1, delay=1.5)
async def heavy_operation(user_id):
    print(f"Starting heavy operation for user {user_id}")
    await asyncio.sleep(2)  # simulate long task
    print(f"Completed heavy operation for user {user_id}")


class AsyncTaskView(AsyncView):
    async def get(self, request):
        user_id = 123
        
        heavy_operation.delay(user_id)

        return JsonResponse({"message": "Heavy operation scheduled, returning immediately."})
