from json.decoder import JSONDecodeError
from typing import List

from .api import get_access_token, get_organization_detail, send_sms
from .exceptions import GoSmsApiException


def send_batch_sms(client_id: str, client_secret: str, message: str, recipients: List[str]):
    """
    Odešle dávku SMSek na seznam čísel. Použije se první channel v organizaci.
    """

    resp = get_access_token(client_id, client_secret)
    if resp.status_code != 200:
        raise GoSmsApiException(error="can't get access token", status=resp.status_code, reason=resp.content)

    try:
        token = "{} {}".format(resp.json()['token_type'].capitalize(), resp.json()['access_token'])
    except (KeyError, AttributeError, JSONDecodeError):
        raise GoSmsApiException(error="can't get access token", status=400, reason='missing "access token" in response')

    resp = get_organization_detail(token)
    if resp.status_code != 200:
        raise GoSmsApiException(error="can't get organization information", status=resp.status_code, reason=resp.content)

    try:
        channel = resp.json()['channels'][0]['id']
    except (KeyError, JSONDecodeError, IndexError):
        raise GoSmsApiException(error="can't get channel information", status=400, reason='missing "channel" in response')

    send_sms(token, message, recipients, channel)
