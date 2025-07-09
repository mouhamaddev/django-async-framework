# views/run_in_background.py
import asyncio
from django.http import JsonResponse
from async_framework.views.core import AsyncView
from async_framework.utils import run_in_background


async def fake_email_service_send(user_id: int):
    await asyncio.sleep(1)
    print(f"Welcome email sent to user {user_id}")


class RunInBackgroundView(AsyncView):
    async def get(self, request):
        user_id = 42
        
        run_in_background(fake_email_service_send, user_id)

        return JsonResponse({"message": "Signup complete, email is being sent in background."})
