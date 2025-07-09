import asyncio
import uuid
from async_framework.views.api import AsyncAPIView


class MyAsyncAPIView(AsyncAPIView):
    async def post(self, request):
        data = request.data

        subject = data.get("subject")
        message = data.get("message")

        if not subject or not message:
            return self.error("Subject and message are required.", status=400)

        await asyncio.sleep(0.3)  # simulate async I/O

        ticket_id = str(uuid.uuid4())
        return self.success({
            "ticket_id": ticket_id,
            "message": "Your support request was received!"
        })
