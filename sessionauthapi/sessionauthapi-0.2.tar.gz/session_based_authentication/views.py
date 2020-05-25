from django.shortcuts import render

# Create your views here.
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import parsers, renderers, status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .serializers import LoginSerializer, UserSerializer, CustomTokenSerializer
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth import get_user_model


# this class is used to handles request and serialize 
# it to convert data into json format
class UserAPIView(GenericAPIView):
    serializer_class = UserSerializer
    def get(self, request):
        users = User.objects.all()
        serailizer = UserSerializer(users, many=True)
        return Response(serailizer.data, status=200)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "successfully registered a new user"
        else:
            data = serializer.errors
        return Response(data)


#to get all users and update any user
class UserDetailView(APIView):
    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist as e:
            return Response( {"error": "Given question object not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serailizer = UserSerializer(instance)
        return Response(serailizer.data)

    def put(self, request, id=None):
        instance = self.get_object(id)
        serializer = UserSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.erros, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return Response(status=204)



class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    # def post(self,request):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        return Response({"status": "logged in successfully "}, status=200)



class LogoutView(GenericAPIView):
    serializer_class = LoginSerializer
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        django_logout(request)
        return Response({'data':"logged out successfully!!"},status=204)





