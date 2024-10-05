from django.urls import *
from .views import *

urlpatterns = [
    path("", HomePageView.as_view(), name="homePage"),
    path('posts/<uuid:pk>/', PostDetailView.as_view(), name='postDetailPage'),  # URL para detalhe do post
    path('explorer/', ExplorerPageView.as_view(), name='explorerPage'),
]