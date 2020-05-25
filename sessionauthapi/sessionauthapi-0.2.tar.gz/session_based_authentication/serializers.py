from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions





class CustomTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields =    ["email","username","password","password2"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

 
    def save(self):
        user = User(email=self.validated_data['email'],username=self.validated_data['username'],)
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is deactivated."
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with given credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide email and password both."
            raise exceptions.ValidationError(msg)
        return data



