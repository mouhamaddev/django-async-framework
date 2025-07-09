"""
URL configuration for examples project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import views.asyncapiview
import views.asyncview
import views.asyncratethrottle
import views.await_safe
import views.run_in_background
import views.async_error_view
import views.async_task

urlpatterns = [
    # AsyncView
    path("asyncview/", views.asyncview.MyAsyncView.as_view()),

    # AsyncAPIView
    path("asyncapiview/", views.asyncapiview.MyAsyncAPIView.as_view()),

    # AsyncRateThrottle
    path("asyncratethrottle/", views.asyncratethrottle.ThrottledStatusView.as_view()),

    # await_safe
    path("awaitsafe/", views.await_safe.AwaitSafeView.as_view()),

    # run_in_background
    path("runinbackground/", views.run_in_background.RunInBackgroundView.as_view()),

    # async_error_middleware
    path("asyncerror/", views.async_error_view.ErrorRaisingView.as_view()),

    # async_task
    path("asynctask/", views.async_task.AsyncTaskView.as_view()),
]
