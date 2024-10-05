from django.urls import path
from .views import SignupView, SigninView, LogoutView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signUpPage'),
    path('signin/', SigninView.as_view(), name='signInPage'),
    path('logout/', LogoutView.as_view(), name='logoutPage'),
]
