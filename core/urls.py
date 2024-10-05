from django.urls import *
from .views import *

urlpatterns = [
    path("", HomePageView.as_view(), name="homePage"),

    path('explorer/', ExplorerPageView.as_view(), name='explorerPage'),
]