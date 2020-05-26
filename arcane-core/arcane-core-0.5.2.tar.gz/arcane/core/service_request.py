from typing import Optional, Dict, Callable

import json
import backoff
import requests

from arcane.firebase import generate_token


def request_service(method: str,
                    url: str,
                    firebase_api_key: str,
                    claims: object,
                    uid: str = 'adscale@arcane.run',
                    headers: Optional[Dict] = None,
                    retry_decorator: Callable[[requests.request], requests.request] = lambda f: f,
                    auth_enabled: bool = True,
                    **kwargs) -> requests.Response:
    """ call service while adding a google generated token to it """

    if headers is None:
        headers = {"content-type": "application/json"}
    if auth_enabled:
        google_token = generate_token(firebase_api_key, claims, uid)
        headers.update(Authorization=f'bearer {google_token}')

    @retry_decorator
    def request_with_retries():
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response

    return request_with_retries()


def call_get_route(url: str, firebase_api_key: str, claims: object, auth_enabled: bool):
    response = request_service('GET',
                               url,
                               firebase_api_key,
                               claims=claims,
                               auth_enabled=auth_enabled,
                               retry_decorator=backoff.on_exception(
                                    backoff.expo,
                                    (ConnectionError, requests.HTTPError, requests.Timeout),
                                    3
                                ))
    response.raise_for_status()
    return json.loads(response.content.decode("utf8"))


def get_client_old(client_id: str, CLIENTS_URL, firebase_api_key, auth_enabled=True):
    url = f"{CLIENTS_URL}/api/clients/old?client_id={client_id}"
    return call_get_route(url, firebase_api_key, claims={'features_rights': {'clients': 'Viewer'}}, auth_enabled=auth_enabled)


def get_client(client_id: str, CLIENTS_URL, firebase_api_key, auth_enabled=True):
    url = f"{CLIENTS_URL}/api/clients?client_id={client_id}"
    return call_get_route(url, firebase_api_key, claims={'features_rights': {'clients': 'Viewer'}}, auth_enabled=auth_enabled)
