__all__ = "FirebaseAuthentication", "firebase_app"

import logging

from django.conf import settings
from django.contrib.auth.models import User

import firebase_admin
from rest_framework import authentication, exceptions

from . import exceptions

credentials = firebase_admin.credentials.Certificate(settings.FIREBASE_PATH)
firebase_app = firebase_admin.initialize_app(credentials)


class FirebaseAuthentication(authentication.BaseAuthentication):

    @staticmethod
    def get_auth_token(request):
        try:
            return request.META.get('HTTP_AUTHORIZATION')
        except Exception:
            raise exceptions.NoAuthToken()

    @staticmethod
    def firebase_verify_token(token):
        try:
            return firebase_admin.auth.verify_id_token(token).get('uid')
        except Exception:
            raise exceptions.InvalidAuthToken()

    @staticmethod
    def get_user_with_uid(uid):
        try:
            return User.objects.get(username=uid)
        except User.DoesNotExist:
            raise exceptions.UserNotFound()

    def authenticate(self, request):
        token = self.get_auth_token(request)
        logging.debug(token)
        uid = self.firebase_verify_token(token)
        logging.debug(uid)
        return self.get_user_with_uid(uid)
