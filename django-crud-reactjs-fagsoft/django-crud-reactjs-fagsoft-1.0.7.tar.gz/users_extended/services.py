import random
from datetime import timedelta

from django.contrib.auth.models import User, Permission, Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from knox.models import AuthToken
from rest_framework import serializers
from utils.functions.functions import encrypt, decrypt
import crypt
import string

from users_extended.models import ExtendedUser


def send_registration_email(user: User, email: str):
    subject, from_email, to = 'Validación Registro', '%s <%s>' % ('La Página', 'prueba@gmail.com'), email
    activation_key = decrypt(user.extended_user.registration_token)
    context = {
        "domain": 'http://127.0.0.1:8000',
        "user": user,
        "activation_key": activation_key
    }
    text_content = render_to_string('emails/registration_email.html', context=context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(text_content, "text/html")
    msg.send()


def ask_restore_password_account_user(
        username: str
):
    user = None
    import re
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, username):
        if User.objects.filter(email__iexact=username).exists():
            user = User.objects.filter(email__iexact=username)[0]
    else:
        if User.objects.filter(username__iexact=username).exists():
            user = User.objects.filter(username__iexact=username)[0]
    if user is not None:
        if hasattr(user, 'extended_user'):
            extended_user = user.extended_user
        else:
            extended_user = ExtendedUser.objects.create(user=user)
        now = timezone.now()
        word = generate_word(30)
        extended_user.registration_token = encrypt(word)
        extended_user.registration_expiration = now + timedelta(days=2)
        extended_user.save()

        subject, from_email, to = 'Validación Registro', '%s <%s>' % ('La Página', 'prueba@gmail.com'), user.email
        activation_key = decrypt(extended_user.registration_token)
        context = {
            "domain": 'http://127.0.0.1:8000',
            "user": user,
            "activation_key": activation_key
        }
        text_content = render_to_string('emails/restore_password.html', context=context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(text_content, "text/html")
        msg.send()

    else:
        raise serializers.ValidationError({'_error': 'El usuario no existe'})


def create_update_user(
        user: User = None,
        **validated_data
) -> User:
    registration = validated_data.pop('registration') if 'registration' in validated_data else False
    extended_user_values = validated_data.pop('extended_user') if 'extended_user' in validated_data else None
    validated_data.pop('groups', None)
    validated_data.pop('user_permissions', None)
    email = validated_data.get('email', None)
    now = timezone.now()
    exist_email_qs = User.objects.filter(email__iexact=email)
    if user is not None:
        exist_email_qs = exist_email_qs.exclude(pk=user.pk)
    if exist_email_qs.exists():
        raise serializers.ValidationError({'email': 'Ya existe un usuario con este email, utilizar otro'})
    if user is None:
        user = User.objects.create_user(is_active=not registration, **validated_data)
    else:
        for attr, value in validated_data.items():
            if hasattr(user, attr):
                setattr(user, attr, value)
        if registration:
            user.is_active = False
        user.save()
    if not hasattr(user, 'extended_user'):
        extended_user = ExtendedUser.objects.create(user_id=user.id)
    else:
        extended_user = user.extended_user
    if extended_user_values is not None:
        for attr, value in extended_user_values.items():
            if hasattr(extended_user, attr):
                setattr(extended_user, attr, value)
    if registration:
        extended_user.registration_token = encrypt(generate_word(40))
        extended_user.registration_expiration = now + timedelta(days=7)
    extended_user.save()
    user.refresh_from_db()
    if registration:
        send_registration_email(user, email)
    return user


def validate_account_user(
        activation_key: str,
        user_pk: int
) -> [str, bool]:
    user = User.objects.get(pk=user_pk)
    was_activated = user.is_active
    same_activation_key = False
    expired_link = True
    if not was_activated:
        if hasattr(user, 'extended_user'):
            same_activation_key = decrypt(user.extended_user.registration_token) == activation_key
        if same_activation_key:
            expired_link = timezone.now().date() > user.extended_user.registration_expiration
            if expired_link:
                message = 'El link de activación para "%s" ha caducado, registrase de nuevo.' % user.username
            else:
                extended_user = user.extended_user
                extended_user.registration_token = None
                extended_user.registration_expiration = None
                extended_user.save()
                user.is_active = True
                user.save()
                message = 'Se ha activado correctamente la cuenta de "%s".' % user.username
        else:
            message = 'El token de activación para "%s" no coincide.' % user.username
    else:
        same_activation_key = True
        expired_link = False
        message = 'La cuenta para "%s" ya se había activado.' % user.username
    error = not same_activation_key or expired_link
    return message, error


def set_restored_password(
        activation_key: str,
        user_pk: int,
        new_password: str,
        new_password_2: str,
) -> [str, bool]:
    if new_password != new_password_2:
        message = 'La contraseña y su confirmación no coinciden, por favor verificar las dos.'
        return message, True

    user = User.objects.get(pk=user_pk)
    extended_user = user.extended_user
    if extended_user.registration_token is None or extended_user.registration_expiration is None:
        message = 'Este link ya ha sido utilizado, o no sirve para restaurar contraseña'
        return message, True

    same_activation_key = decrypt(user.extended_user.registration_token) == activation_key
    expired_link = timezone.now().date() > user.extended_user.registration_expiration
    if same_activation_key:
        if expired_link:
            message = 'El link de cambio de contraseña para "%s" ha caducado, solicitelo de nuevo.' % user.username
        else:
            extended_user.registration_token = None
            extended_user.registration_expiration = None
            extended_user.save()
            user.set_password(new_password)
            user.save()
            message = 'Se ha cambiado correctamente la contraseña de "%s".' % user.username
    else:
        message = 'El token de cambio de contraseña para "%s" no coincide.' % user.username
    error = not same_activation_key or expired_link
    return message, error


def set_security_pin(user_id: int, raw_pin: str) -> [User, str]:
    user = User.objects.get(pk=user_id)
    if hasattr(user, 'extended_user'):
        extended_user = user.extended_user
        extended_user.security_pin = crypt.crypt(raw_pin)
        extended_user.save()
        return user, extended_user.security_pin
    else:
        return None, None


def user_validate_security_pin(user_id: int, raw_pin: str):
    user = User.objects.get(pk=user_id)
    if hasattr(user, 'extended_user'):
        return crypt.crypt(raw_pin, user.extended_user.security_pin) == user.extended_user.security_pin
    return False


def user_get_token(
        user_id: int
) -> str:
    user = User.objects.get(pk=user_id)
    now = timezone.now()
    expired_tokens = user.auth_token_set.filter(expiry__lt=now)
    expired_tokens.delete()
    tokens = user.auth_token_set.all()
    if hasattr(user, 'extended_user'):
        extended_user = user.extended_user
    else:
        extended_user = ExtendedUser.objects.create(user=user)
    if not extended_user.multi_sessions:
        tokens.delete()
    else:
        qty_sessions_allowed = extended_user.multi_sessions_qty
        if qty_sessions_allowed > 0:
            already_open = tokens.count()
            if qty_sessions_allowed - already_open == 0:
                tokens.order_by('created')[0].delete()
    _, token = AuthToken.objects.create(user)
    return token


def user_exist_username(
        username: str
) -> bool:
    import re
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, username):
        if User.objects.filter(email__iexact=username).exists():
            return True
    else:
        if User.objects.filter(username=username).exists():
            return True
    return False


def user_validate_security_qr(user_id: int, raw_qr: str):
    user = User.objects.get(pk=user_id)
    if hasattr(user, 'extended_user'):
        return decrypt(user.extended_user.security_qr) == raw_qr
    return False


def user_show_security_qr(user_id: int) -> str:
    user = User.objects.get(pk=user_id)
    if hasattr(user, 'extended_user'):
        return decrypt(user.extended_user.security_qr)
    return ''


def generate_word(size, pre=None, pos=None) -> str:
    characters = list(string.ascii_letters + "-._~")
    word = ''
    for x in range(size):
        word += random.choice(characters)
    if pre:
        word = str(pre) + word
    if pos:
        word += str(pos)
    return word


def user_create_security_qr(user_id: int) -> str:
    user = User.objects.get(pk=user_id)
    if hasattr(user, 'extended_user'):
        new_qr = generate_word(30, user.id, user.id)
        extended_user = user.extended_user
        encrypted_new_qr = encrypt(new_qr)
        extended_user.security_qr = encrypted_new_qr
        extended_user.save()
        return new_qr
    return ''


def user_change_pin(
        user_id: int,
        password: str,
        pin: str
) -> User:
    user = User.objects.get(pk=user_id)
    if hasattr(user, 'extended_user'):
        if not user.check_password(password):
            raise serializers.ValidationError(
                {'_error': 'La contraseña suministrada no coincide con el usuario, es necesario para cambiar el PIN'})
        user = set_security_pin(
            user_id=user_id,
            raw_pin=pin
        )
    return user


def user_change_pin_other(
        current_user_id: int,
        user_id: int,
        pin: str
) -> User:
    current_user = User.objects.get(pk=current_user_id)
    change_pin_other_user = current_user.has_perm('users_extended.change_pin_other_user')
    if not change_pin_other_user:
        raise serializers.ValidationError({'_error': 'No tiene permiso de cambiar el pin de otro usuario'})
    user = User.objects.get(pk=user_id)
    if hasattr(user, 'extended_user'):
        user = set_security_pin(
            user_id=user_id,
            raw_pin=pin
        )
    return user


def user_change_password(
        user_id: int,
        password_old: str,
        password_new: str,
        password_new_confirmation: str
) -> User:
    user = User.objects.get(pk=user_id)
    if not user.check_password(password_old):
        raise serializers.ValidationError({'_error': 'La contraseña suministrada no coincide con el user'})
    if not password_new == password_new_confirmation:
        raise serializers.ValidationError({'_error': 'La contraseña nueva con su confirmación no coincide'})
    user.set_password(password_new)
    user.save()
    return user


def user_change_password_other(
        current_user_id: int,
        user_id: int,
        password_new: str,
        password_new_confirmation: str
) -> User:
    current_user = User.objects.get(pk=current_user_id)
    user = User.objects.get(pk=user_id)
    change_password_other_user = current_user.has_perm('users_extended.change_password_other_user')
    if not change_password_other_user:
        raise serializers.ValidationError({'_error': 'No tiene permiso de cambiar la contraseña de otro usuario'})
    if not password_new == password_new_confirmation:
        raise serializers.ValidationError({'_error': 'La contraseña nueva no coincide con su confirmación'})
    user.set_password(password_new)
    user.save()
    return user


def user_add_permission(
        permission_id: int,
        user_id: int
) -> User:
    user = User.objects.get(pk=user_id)
    permission = Permission.objects.get(id=permission_id)
    has_group = user.user_permissions.filter(id=permission_id).exists()
    if not has_group:
        user.user_permissions.add(permission)
    else:
        user.user_permissions.remove(permission)
    return user


def user_add_group(
        grupo_id: int,
        user_id: int
) -> User:
    user = User.objects.get(pk=user_id)
    group = Group.objects.get(id=grupo_id)

    has_group = user.groups.filter(id=grupo_id).exists()
    if not has_group:
        user.groups.add(group)
    else:
        user.groups.remove(group)
    return user
