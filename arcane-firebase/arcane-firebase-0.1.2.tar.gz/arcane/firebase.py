from typing import Dict, Union

import requests
import json
from firebase_admin import (
    auth as firebase_auth,
    credentials,
    initialize_app as firebase_initialize_app
)

PUBSUB_UID = 'pubsub@arcane.run'
_verify_token_url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken'


def generate_token(firebase_api_key: str,
                   claims: Dict[str, Union[Dict, str]] = None,
                   uid=PUBSUB_UID) -> str:
    """
    generates a custom token with custom uid and claims.
    Warning: Firebase app must already be initialised
    """
    custom_token = firebase_auth.create_custom_token(uid, developer_claims=claims)

    body = {'token': custom_token.decode(), 'returnSecureToken': True}
    params = {'key': firebase_api_key}
    resp = requests.request('post', _verify_token_url, params=params, json=body)
    if resp.status_code != 200:
        try:
            print(resp.json())
        except json.decoder.JSONDecodeError:
            resp.raise_for_status()
    resp.raise_for_status()
    return resp.json()['idToken']


def initialize_app(credentials_path: str) -> None:
    cred = credentials.Certificate(credentials_path)
    firebase_initialize_app(cred)
