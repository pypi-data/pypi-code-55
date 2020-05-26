from typing import List, Optional

import requests
import urllib.parse


BASE_URL = "https://app.gosms.cz"


def get_access_token(client_id: str, client_secret: str) -> requests.Response:
    """
    Vrátí token a platnost

    :return: {
        "access_token":"AccessTokenIU78JO",
        "expires_in":3600,
        "token_type":"bearer",
        "scope":"user"
    }
    """
    url = urllib.parse.urljoin(BASE_URL, "/oauth/v2/token")
    resp = requests.post(url, data={'client_id': client_id,
                                    'client_secret': client_secret,
                                    'grant_type': 'client_credentials'})

    return resp


def get_organization_detail(token: str) -> requests.Response:
    url = urllib.parse.urljoin(BASE_URL, "/api/v1/")
    return requests.get(url, headers={'Authorization': token})


def send_sms(token: str, message: str, recipients: List[str], channel: int, expected_send_start: Optional[str] = None) -> requests.Response:
    """
    Odešle zprávu zadaným recipientům.

    {
        "recipients": {
            "invalid": ["Peter"]
        },
        "link": "api/v1/messages/1"
    }

    """
    url = urllib.parse.urljoin(BASE_URL, "/api/v1/messages/")
    data = {
        'message': message,
        'recipients': recipients,
        'channel': channel,
    }

    if expected_send_start is not None:
        data.update({
            'expected_send_start': expected_send_start
        })

    return requests.post(url, json=data, headers={'Authorization': token})
