from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signUpPage'),
    path('signin/', SignInView.as_view(), name='signInPage'),
    path('logout/', LogoutView.as_view(), name='logoutPage'),
]
