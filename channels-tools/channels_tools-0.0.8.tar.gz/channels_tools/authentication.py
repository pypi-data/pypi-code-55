from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser


def channels_authentication(scope):
    kwargs = scope['url_route']['kwargs']
    if 'token' in kwargs.keys():
        token = kwargs['token']
        token_obj = Token.objects.filter(key=token)
        if token_obj.exists():
            user = token_obj.first().user
        else:
            user = AnonymousUser()
    else:
        user = AnonymousUser()

    scope['user'] = user
    return scope
