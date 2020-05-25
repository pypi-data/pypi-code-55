from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from .views import (LoginView, LogoutView, UserAPIView, UserDetailView)

urlpatterns = [
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('users', UserAPIView.as_view()),
    path('users/<int:id>', UserDetailView.as_view()),
    path('api/rest-auth/', include('rest_auth.urls')),
]
