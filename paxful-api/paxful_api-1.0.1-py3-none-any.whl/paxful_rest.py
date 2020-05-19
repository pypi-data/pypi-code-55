from __future__ import absolute_import, unicode_literals, division

import time
import hmac
import simplejson

from urllib.parse import urlencode,quote
from hashlib import sha256

from paxful.exceptions import RequestError


class RestClient(object):
    """REST client using HMAC SHA256 Authentication

    :param url: Paxful URL.
    :type url: str | unicode
    :param api_key: Paxful API key.
    :type api_key: str | unicode
    :param api_secret: Paxful API secret.
    :type api_secret: str | unicode
    :param timeout: Number of seconds to wait for Paxful to respond to an API request.
    :type timeout: int | float
    :param session: User-defined requests.Session object.
    :type session: requests.Session
    """

    http_success_status_codes = {200, 201, 202}

    def __init__(self, url, api_key, api_secret, timeout, session):
        self._url = url
        self._api_key = str(api_key)                        # creates a string of api-key using str() func/
        self._hmac_key = str(api_secret).encode('utf-8')
        self._timeout = timeout
        self._session = session

    def _handle_response(self, resp):
        """Handle the response from Paxful.

        :param resp: Response from Paxful.
        :type resp: requests.models.Response
        :return: Response body.
        :rtype: dict
        :raise quadriga.exceptions.RequestError: If HTTP OK was not returned.
        """
        http_code = resp.status_code
        if http_code not in self.http_success_status_codes:
            raise RequestError(
                response=resp,
                message='[HTTP {}] {}'.format(http_code, resp.reason)
            )
        try:
            body = resp.json()
        except simplejson.decoder.JSONDecodeError:
            return resp.content
        except ValueError:
            raise RequestError(
                response=resp,
                message='[HTTP {}] response body: {}'.format(
                    http_code,
                    resp.text
                )
            )
        else:
            if 'error' in body:
                error_code = body['error'].get('code', '?')
                raise RequestError(
                    response=resp,
                    message='[HTTP {}][ERR {}] {}'.format(
                        resp.status_code,
                        error_code,
                        body['error'].get('message', 'no error message')
                    ),
                    error_code=error_code
                )
            return body

    def post(self, endpoint, payload=None):
        """Send HTTP Post to Paxful

        :param endpoint: API endpoint, the end of the url string that points to a given resource
        :param payload: Request payload containing request parameters
        :return: response:
        """

        nonce = int(time.time())

        if payload is None:                                 # init payload to empty dict in case none is provided
            payload = {}
        payload['apikey'] = self._api_key
        payload['nonce'] = nonce

        # Urlencode - quote function is used to replace ' ' with '%20'
        payload = urlencode(sorted(payload.items()), quote_via=quote)

        # Generate APISEAL
        apiseal = hmac.new(
            key=self._hmac_key,
            msg=payload.encode('utf-8'),
            digestmod=sha256
        ).hexdigest()

        # Create request payload
        data_with_apiseal = payload + '&apiseal=' + apiseal
        headers = {'Accept': 'application/json; version=1', 'Content-Type': 'text/plain'}

        response = self._session.post(
            url=self._url + endpoint,
            data=data_with_apiseal,
            headers=headers
        )
        # return response
        return self._handle_response(response)

