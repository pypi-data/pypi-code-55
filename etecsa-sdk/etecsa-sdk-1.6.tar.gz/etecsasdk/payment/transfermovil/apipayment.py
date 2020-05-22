from dataclasses import dataclass
import requests
import validators
from .apipayload import APIPayload
from .apicredentials import APICredentials
from requests.exceptions import ConnectionError

@dataclass(order=False)
class APIPayment:
    """
        transfermovil payment class

        @:param url: app url
        @:param ssl_verify: verify ssl certificate

    """

    url: str
    ssl_verify: bool

    def charge(self,credential: APICredentials, payload: APIPayload) -> dict:
        if not validators.url(self.url):
            raise Exception("Incorrect url")
        if not isinstance(self.ssl_verify, bool):
            raise Exception("Incorrect ssl_verified")
        if not isinstance(credential, APICredentials):
            raise Exception("Incorrect credentials")
        if not isinstance(payload,APIPayload):
            raise Exception("Incorrect payload")

        try:
            response = requests.post(self.url,
                                     headers=credential.getheaders(),
                                     json=payload.getPayload(),
                                     verify=self.ssl_verify)
        except ConnectionError as error:
            return {'success': False, 'error': 'Network Error', 'error_detail': str(error)}

        if response.status_code != 200:
            return {'success': False, 'error': response.reason, 'error_detail' : None}
        else:
            json = response.json()

            if json['PayOrderResult']['Success'] != True:
                return {'success': False, 'error': json['PayOrderResult']['Resultmsg']}

            return {'success': True}






