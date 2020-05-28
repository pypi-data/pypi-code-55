from auth0.v3.authentication import GetToken
import os


def get_access_token(service: str):
    '''Get access token'''
    auth0_domain = os.environ["AUTH_DOMAIN"]
    non_interactive_client_id = os.environ["AUTH_CLIENT_ID"]
    non_interactive_client_secret = os.environ["AUTH_CLIENT_SECRET"]
    get_token = GetToken(auth0_domain)
    return get_token.client_credentials(non_interactive_client_id,
                                        non_interactive_client_secret, service)
