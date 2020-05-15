from django.contrib.auth import user_logged_out
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (
    UserSerializer,
    UserWithDetailSerializer,
    UserLoginSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related(
        'extended_user'
    ).prefetch_related(
        'groups'
    ).all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def validate_account(self, request, pk=None) -> Response:
        from .services import validate_account_user
        activation_key = request.POST.get('activation_key')
        message, error = validate_account_user(
            user_pk=pk,
            activation_key=activation_key
        )
        if error:
            raise serializers.ValidationError({'_error': message, 'is_error': error})
        return Response({'result': message})

    @action(detail=True, methods=['post'])
    def add_permission(self, request, pk=None):
        from .services import user_add_permission
        permission_id = int(request.POST.get('permission_id'))
        user = user_add_permission(
            permission_id=permission_id,
            user_id=pk
        )
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_group(self, request, pk=None):
        id_group = int(request.POST.get('id_group'))
        from .services import user_add_group
        user = user_add_group(
            grupo_id=id_group,
            user_id=pk
        )
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        from .services import user_change_password
        password_old = request.POST.get('password_old')
        password = request.POST.get('password')
        password_2 = request.POST.get('password_2')
        user_change_password(
            user_id=pk,
            password_new=password,
            password_new_confirmation=password_2,
            password_old=password_old
        )
        return Response({'result': 'La contraseña se ha cambiado correctamente'})

    @action(detail=True, methods=['post'])
    def change_password_other(self, request, pk=None):
        from .services import user_change_password_other
        password = request.POST.get('password')
        password_2 = request.POST.get('password_2')
        user_change_password_other(
            current_user_id=self.request.user.id,
            user_id=pk,
            password_new=password,
            password_new_confirmation=password_2
        )
        return Response({'result': 'La contraseña se ha cambiado correctamente'})

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def validate_new_username(self, request) -> Response:
        validacion_reponse = {}
        from .services import user_exist_username
        username = self.request.GET.get('username', None)
        if user_exist_username(username=username):
            raise serializers.ValidationError({'username': 'Ya exite'})
        return Response(validacion_reponse)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def ask_restore_password(self, request) -> Response:
        from .services import ask_restore_password_account_user
        username = self.request.POST.get('username', None)
        ask_restore_password_account_user(username=username)
        return Response({'result': 'El correo de recuperación de contraseña se ha enviado correctamente'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def set_restored_password(self, request, pk=None) -> Response:
        from .services import set_restored_password
        activation_key = request.POST.get('activation_key')
        password = self.request.POST.get('password', None)
        password_2 = self.request.POST.get('password_2', None)
        message, error = set_restored_password(
            user_pk=pk,
            new_password_2=password_2,
            new_password=password,
            activation_key=activation_key
        )
        if error:
            raise serializers.ValidationError({'_error': message, 'is_error': error})
        return Response({'result': message})

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def validate_username_login(self, request) -> Response:
        from .services import user_exist_username
        validacion_reponse = {}
        username = self.request.GET.get('username', None)
        if not user_exist_username(username=username):
            raise serializers.ValidationError({'username': 'Este usuario no existe'})
        return Response(validacion_reponse)

    @action(detail=True, methods=['post'])
    def generate_security_qr(self, request, pk=None):
        from .services import user_create_security_qr
        qr = user_create_security_qr(user_id=pk)
        return Response(qr)

    @action(detail=True, methods=['post'])
    def get_security_qr(self, request, pk=None):
        from .services import user_show_security_qr
        qr = user_show_security_qr(user_id=pk)
        return Response(qr)

    @action(detail=True, methods=['post'])
    def change_security_pin(self, request, pk=None):
        from .services import user_change_pin
        pin = request.POST.get('pin')
        password = request.POST.get('password')
        user_change_pin(user_id=pk, password=password, pin=pin)
        return Response({'result': 'El pin se ha cambiado correctamente'})

    @action(detail=True, methods=['post'])
    def change_security_pin_other(self, request, pk=None):
        from .services import user_change_pin_other
        pin = request.POST.get('pin')
        user_change_pin_other(current_user_id=self.request.user.id, user_id=pk, pin=pin)
        return Response({'result': 'El pin se ha cambiado correctamente'})

    @action(detail=True, methods=['post'])
    def upload_profile_image(self, request, pk=None):
        profile_image = self.request.FILES['profile_image']
        user = User.objects.get(pk=pk)
        extended_user = user.extended_user
        extended_user.profile_image = profile_image
        extended_user.save()
        user = User.objects.get(pk=pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class LoginViewSet(viewsets.ModelViewSet):
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request) -> Response:
        from django.http import QueryDict
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        import re
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if re.search(regex, username):
            username = User.objects.values_list('username', flat=True).filter(email__iexact=username)[0]

        ordinary_dict = {'username': username, 'password': password}
        query_dict = QueryDict('', mutable=True)
        query_dict.update(ordinary_dict)
        from .services import user_get_token
        serializer = self.get_serializer(data=query_dict)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = user_get_token(user_id=user.id)
        return Response({
            "user": UserWithDetailSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        })

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def load_user(self, request) -> Response:
        if self.request.user.is_anonymous:
            serializer = UserWithDetailSerializer(None, context={'request': request})
            return Response(serializer.data)
        serializer = UserWithDetailSerializer(self.request.user, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request) -> Response:
        request._auth.delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def logoutall(self, request) -> Response:
        request.user.auth_token_set.all().delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        return Response(None, status=status.HTTP_204_NO_CONTENT)
