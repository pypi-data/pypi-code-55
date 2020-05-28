from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        path = scope['path']
        values = path.split('/')
        if len(values) == 3:
            token = Token.objects.filter(key=values[2])
            if token.exists():
                scope['user'] = token.first().user
            else:
                scope['user'] = AnonymousUser()

        return self.inner(scope)


def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))
