from django.urls import path
from .views import *

urlpatterns = [
    path("", HomePageView.as_view(), name="homePage"),
    path('posts/<uuid:pk>/', PostDetailView.as_view(), name='postDetailPage'),  
    path('explorer/', ExplorerPageView.as_view(), name='explorerPage'),
    path('users/<int:pk>/', UserProfileView.as_view(), name='userProfilePage'),
    path('users/edit-profile/', EditProfileView.as_view(), name='editProfilePage'),  # Adicione uma barra no final
]
