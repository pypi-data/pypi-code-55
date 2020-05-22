from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (LoginView, LogoutView)

 
urlpatterns = [
    path('access_token/', TokenObtainPairView.as_view()),
    path('refresh_token/', TokenRefreshView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
]