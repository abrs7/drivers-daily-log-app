from django.urls import path
from .views import ping, log_sheet

urlpatterns = [
    path("ping", ping),
    path("<int:day>.png", log_sheet),
]
