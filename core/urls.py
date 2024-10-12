from django.urls import path
from .views import *

urlpatterns = [
    path("", HomePageView.as_view(), name="homePage"),
    path('explorer/', ExplorerPageView.as_view(), name='explorerPage'),
    path('users/<int:pk>/', UserProfileView.as_view(), name='userProfilePage'),  
    path('users/edit-profile/', EditProfileView.as_view(), name='editProfilePage'),

    path('posts/<uuid:pk>/', PostDetailView.as_view(), name='postDetailPage'),  
    path('posts/edit/<uuid:pk>/', EditPostView.as_view(), name='editPost'),
    path('posts/delete/<uuid:pk>/', DeletePostView.as_view(), name='delPost'),  

    path('like/<uuid:post_id>/', LikePostView.as_view(), name='likePost'),  
    path('notifications/', NotificationPageView.as_view(), name='notificationsPage'),

    path('api/posts/', PostListView.as_view(), name='postList'),


]
