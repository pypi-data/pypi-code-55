from django.shortcuts import render
from rest_framework import parsers, renderers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import LoginSerializer
from django.contrib.auth import login as django_login, logout as django_logout


# Create your views here.

class LoginView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        return Response({"status": "logged in successfully "}, status=200)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        django_logout(request)
        return Response({'data':"logged out successfully!!"},status=204)


