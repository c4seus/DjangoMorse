from django.urls import path
from .views import MorseController

urlpatterns = [
    path("", MorseController.as_view(), name="home"),
]
