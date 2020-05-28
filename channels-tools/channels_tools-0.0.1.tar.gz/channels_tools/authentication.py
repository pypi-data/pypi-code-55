from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        kwargs = scope['url_route']['kwargs']

        print(kwargs)

        return self.inner(scope)
