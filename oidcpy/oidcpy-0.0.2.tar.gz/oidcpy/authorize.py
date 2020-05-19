import jwt
import os
import requests
from jwcrypto import jwk
from functools import wraps
from flask import request


class AuthorizeError(Exception):
    def __init__(self, message, status=401):
        super().__init__(message)
        self.status = status


def retrieve_public_key(url):
    response = requests.get(url, verify=False)
    key = jwk.JWK.from_json(response.content)
    return key.export_to_pem()


def read_public_key(filename):
    with open(filename, "rb") as f1:
        key = f1.read()
        return key

key_location = os.getenv('KEY_LOCATION', None)

if not key_location:
    raise AuthorizeError('key location not set', 500)

if os.path.exists(key_location):
    public_key = read_public_key(key_location)
else:
    public_key = retrieve_public_key(key_location)


def validate_auth_header(headers, audience, scopes):
    if 'Authorization' not in headers:
        raise AuthorizeError('Missing authorization header')

    auth_header = headers['Authorization']
    scheme, token = auth_header.split(' ')

    if scheme.lower() != 'bearer':
        raise AuthorizeError('Authorization scheme not supported')
    claims = jwt.decode(str.encode(token), public_key,
                        audience=audience, algorithms='RS256')

    required_scopes = set(scopes.split(' '))
    granted_scopes = set(claims['scope'].split(' '))

    if not required_scopes.issubset(granted_scopes):
        raise AuthorizeError('required scope missing')

    return claims


def authorize(audience, scopes):
    """
      Decorator to validate the authorization header of the incoming request.
      Pass required audience and scopes as arguments
    """
    def decorator(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            try:
                claims = validate_auth_header(request.headers, audience, scopes)
                request.view_args['claims'] = claims
            except Exception as ex:
                raise AuthorizeError('authorize failed') from ex
            return func(*args, **kwargs)
        return decorated
    return decorator
