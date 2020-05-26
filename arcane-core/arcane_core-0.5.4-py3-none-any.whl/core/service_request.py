from typing import Optional, Dict, Callable

import json
import backoff
import requests

from arcane.firebase import generate_token, initialize_app


def request_service(method: str,
                    url: str,
                    firebase_api_key: str,
                    claims: object,
                    uid: str = 'adscale@arcane.run',
                    headers: Optional[Dict] = None,
                    retry_decorator: Callable[[requests.request], requests.request] = lambda f: f,
                    auth_enabled: bool = True,
                    credentials_path: str = None,
                    **kwargs) -> requests.Response:
    """ call service while adding a google generated token to it """

    if headers is None:
        headers = {"content-type": "application/json"}
    if auth_enabled:
        try:
            google_token = generate_token(firebase_api_key, claims, uid)
        except ValueError as err:
            if str(err).startswith('The default Firebase app does not exist.') and\
                    credentials_path is not None:
                initialize_app(credentials_path)
                google_token = generate_token(firebase_api_key, claims, uid)
            else:
                raise err
        headers.update(Authorization=f'bearer {google_token}')

    @retry_decorator
    def request_with_retries():
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response

    return request_with_retries()


def call_get_route(url: str, firebase_api_key: str, claims: object, auth_enabled: bool, credentials_path: str = None, uid: str = None):
    response = request_service('GET',
                               url,
                               firebase_api_key,
                               claims=claims,
                               uid=uid,
                               auth_enabled=auth_enabled,
                               retry_decorator=backoff.on_exception(
                                    backoff.expo,
                                    (ConnectionError, requests.HTTPError, requests.Timeout),
                                    3
                                ),
                               credentials_path=credentials_path)
    response.raise_for_status()
    return json.loads(response.content.decode("utf8"))


def get_client_old(client_id: str, CLIENTS_URL, firebase_api_key, auth_enabled=True, credentials_path: str = None, uid: str = None):
    url = f"{CLIENTS_URL}/api/clients/old?client_id={client_id}"
    return call_get_route(
        url,
        firebase_api_key,
        claims={'features_rights': {'clients': 'Viewer'}, 'authorized_clients': [client_id]},
        auth_enabled=auth_enabled,
        credentials_path=credentials_path,
        uid=uid
    )


def get_client(client_id: str, CLIENTS_URL, firebase_api_key, auth_enabled=True, credentials_path: str = None, uid: str = None):
    url = f"{CLIENTS_URL}/api/clients?client_id={client_id}"
    return call_get_route(
        url,
        firebase_api_key,
        claims={'features_rights': {'clients': 'Viewer'}, 'authorized_clients': [client_id]},
        auth_enabled=auth_enabled,
        credentials_path=credentials_path,
        uid=uid
    )


def get_user(user_id: str, COMMON_SERVICES_URL: str, firebase_api_key: str, auth_enabled=True, credentials_path: str = None, uid: str = None):
    response = request_service('GET',
                               url=f"{COMMON_SERVICES_URL}/api/users?user_id={user_id}",
                               firebase_api_key=firebase_api_key,
                               claims={'features_rights': {'users': 'Viewer'}},
                               uid=uid,
                               auth_enabled=auth_enabled,
                               retry_decorator=backoff.on_exception(
                                        backoff.expo,
                                        (ConnectionError, requests.HTTPError, requests.Timeout),
                                        3
                                    ),
                               credentials_path=credentials_path)
    response.raise_for_status()
    return json.loads(response.content.decode("utf8"))


def get_client_owner(client_id: str, CLIENTS_URL: str, COMMON_SERVICES_URL: str, firebase_api_key: str, auth_enabled=True, credentials_path: str = None, uid: str = None):
    client = get_client(client_id, CLIENTS_URL, firebase_api_key, auth_enabled, credentials_path, uid)[0]
    user = get_user(client['owner_id'], COMMON_SERVICES_URL, firebase_api_key, auth_enabled, credentials_path, uid)[0]
    return user
