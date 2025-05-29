import time

from django.http import JsonResponse
from django.contrib.auth.models import User

# Import async_framework modules
from async_framework.views.core import AsyncView
from async_framework.views.api import AsyncAPIView
from async_framework.throttle import AsyncRateThrottle
from async_framework.orm import await_safe
from async_framework.utils import run_in_background


# AsyncView
class DemoAsyncView(AsyncView):
    async def get(self, request):
        time.sleep(1)
        return JsonResponse({"message": "This view is fully async!"})
    

# AsyncAPIView
class DemoAsyncAPIView(AsyncAPIView):
    async def get(self, request):
        data = request.data
        time.sleep(1)
        return self.success({"echo": data})


# AsyncAPIView
class AsyncRateThrottleView(AsyncAPIView):
    throttle = AsyncRateThrottle(rate='5/second') # Time units supported: second, minute, and hour

    async def get(self, request):
        if not await self.throttle.allow_request(request):
            return self.error("Rate limit exceeded", status=429)
        return self.success({"msg": "Allowed!"})

  
# await_safe
class GetUserView(AsyncView):
    async def get(self, request):
        user = await await_safe(User.objects.filter(is_active=True).first)()
        if not user:
            return JsonResponse({"error": "No active user found"}, status=404)
        return JsonResponse({"username": user.username})


# run_in_background
class SignUpUserView(AsyncView):
    def create_user_in_db(self, user_data):
        return 123

    async def send_welcome_email(self, user_id: int):
        time.sleep(2)  # Simulate email sending delay

    def user_signup(self, user_data):
        new_user_id = self.create_user_in_db(user_data)

        # send welcome email in background without waiting
        run_in_background(self.send_welcome_email, new_user_id)

        return "Signup complete!"
    
    async def get(self, request): # Using GET method for simplicity
        user_data = {}
        result = self.user_signup(user_data)
        return JsonResponse({"message": result})