from django.urls import *
from .views import HomePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="homePage"),
]