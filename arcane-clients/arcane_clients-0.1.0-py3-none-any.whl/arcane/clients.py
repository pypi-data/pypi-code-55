import requests
import backoff
import json

from arcane.requests import call_get_route, request_service


def get_client(client_id: str, CLIENTS_URL, firebase_api_key, auth_enabled=True, credentials_path: str = None, uid: str = None):
    url = f"{CLIENTS_URL}/api/clients?client_id={client_id}"
    client_list = call_get_route(
        url,
        firebase_api_key,
        claims={'features_rights': {'clients': 'Viewer'}, 'authorized_clients': [client_id]},
        auth_enabled=auth_enabled,
        credentials_path=credentials_path,
        uid=uid
    )
    return client_list[0] if len(client_list) > 0 else None


def get_client_old(client_id: str, CLIENTS_URL, firebase_api_key, auth_enabled=True, credentials_path: str = None, uid: str = None):
    url = f"{CLIENTS_URL}/api/clients/old?client_id={client_id}"
    old_client_list = call_get_route(
        url,
        firebase_api_key,
        claims={'features_rights': {'clients': 'Viewer'}, 'authorized_clients': [client_id]},
        auth_enabled=auth_enabled,
        credentials_path=credentials_path,
        uid=uid
    )
    return old_client_list[0] if len(old_client_list) > 0 else None


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
    user_list = json.loads(response.content.decode("utf8"))
    return user_list[0] if len(user_list) > 0 else None


def get_client_owner(client_id: str, CLIENTS_URL: str, COMMON_SERVICES_URL: str, firebase_api_key: str, auth_enabled=True, credentials_path: str = None, uid: str = None):
    client = get_client(client_id, CLIENTS_URL, firebase_api_key, auth_enabled, credentials_path, uid)
    if client is None:
        raise ValueError(f'Client {client_id} does not exist.')
    user = get_user(client['owner_id'], COMMON_SERVICES_URL, firebase_api_key, auth_enabled, credentials_path, uid)
    return user
