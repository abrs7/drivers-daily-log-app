from django.urls import path
from .views import ping, plan_trip

urlpatterns = [
    path("ping", ping),
    path("plan", plan_trip),
]
