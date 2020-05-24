import jwt
import os
import requests
from jwcrypto import jwk
from functools import wraps
from flask import request

from .crypto import read_file


class AuthorizeError(Exception):
    """
      Error thrown when authorization failed.
      Holds `status` field with suggested response code.
      Holds `message` field with description of failure. 
    """
    def __init__(self, message, status=401):
        super().__init__(message)
        self.status = status


def retrieve_public_key(url, verify_ssl=True):
    response = requests.get(url, verify=verify_ssl)
    key = jwk.JWK.from_json(response.content)
    return key.export_to_pem()


key_location = os.getenv('KEY_LOCATION', None)

if not key_location:
    raise AuthorizeError('key location not set', 500)

verify_ssl = os.getenv('VERIFY_SSL', 'FALSE') == 'TRUE'

if os.path.exists(key_location):
    public_key = read_file(key_location)
else:
    public_key = retrieve_public_key(key_location, verify_ssl)


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
