from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers


# from knox.models import AuthToken


# class AuthTokenSerializer(serializers.Serializer):
#     class Meta:
#         model = AuthToken
#         fields = [
#             'created',
#             'expiry',
#             'digest',
#         ]


class UserSerializer(serializers.ModelSerializer):
    to_string = serializers.SerializerMethodField()
    profile_image_url = serializers.SerializerMethodField()
    security_pin = serializers.CharField(source='extended_user.security_pin', allow_null=True, required=False)
    security_qr = serializers.CharField(source='extended_user.security_qr', allow_null=True, required=False)
    city_name = serializers.CharField(source='extended_user.city.name', read_only=True)
    city = serializers.IntegerField(source='extended_user.city_id', allow_null=True, required=False)
    alias = serializers.CharField(source='extended_user.alias', allow_null=True, required=False)
    gender = serializers.CharField(source='extended_user.gender', allow_null=True, required=False)
    registration = serializers.BooleanField(default=False, allow_null=True, required=False)
    # encrypted = serializers.BooleanField(default=False, allow_null=True, required=False)
    multi_sessions = serializers.NullBooleanField(
        source='extended_user.multi_sessions',
        default=False
    )
    multi_sessions_qty = serializers.IntegerField(
        source='extended_user.multi_sessions_qty',
        allow_null=True,
        required=False
    )
    date_of_birth = serializers.DateField(
        source='extended_user.date_of_birth',
        format="%Y-%m-%d",
        input_formats=['%Y-%m-%dT%H:%M:%S.%fZ', 'iso-8601'],
        allow_null=True,
        required=False
    )

    def get_profile_image_url(self, obj):  # pragma: no cover
        return obj.extended_user.profile_image.url if hasattr(
            obj,
            'extended_user'
        ) and obj.extended_user.profile_image else None

    def get_to_string(self, instance):  # pragma: no cover
        return ('%s %s' % (instance.first_name, instance.last_name)).title()

    def create(self, validated_data):
        from .services import create_update_user
        user = create_update_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        from .services import create_update_user
        user = create_update_user(user=instance, **validated_data)
        return user

    class Meta:
        model = User
        fields = [
            'id',
            'registration',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'is_staff',
            'password',
            'username',
            # 'encrypted',
            'last_login',
            'date_joined',
            'alias',
            'is_superuser',
            'groups',
            'user_permissions',
            'to_string',
            'profile_image_url',
            'security_pin',
            'city',
            'city_name',
            'security_qr',
            'multi_sessions',
            'multi_sessions_qty',
            'gender',
            'date_of_birth',
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }


class UserWithDetailSerializer(UserSerializer):
    pass


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError({'_error': 'El usuario y la contraseña no coinciden con ningún usuario!'})
