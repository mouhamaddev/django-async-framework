import asyncio
from async_framework.views.core import AsyncView
from django.http import JsonResponse


class AnalyticsService:
    async def generate_report(self, user_data):
        await asyncio.sleep(0.2)  # simulate async I/O
        return {
            "user_id": user_data.get("id"),
            "activity_score": 87,
            "report_type": "weekly"
        }


async def load_user_data_async(user):
    await asyncio.sleep(0.1)  # simulate async I/O
    return {
        "id": user.id if user and hasattr(user, "id") else 1,
        "name": "Example User",
        "email": "user@example.com"
    }


class MyAsyncView(AsyncView):
    services = {
        "analytics": lambda: AnalyticsService(),
    }

    async def async_setup(self, request, *args, **kwargs):
        self.user_data = await load_user_data_async(request.user)

    async def get(self, request):
        report = await self.services["analytics"].generate_report(self.user_data)
        return JsonResponse({"report": report})
