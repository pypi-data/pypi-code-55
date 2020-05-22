from dataclasses import dataclass
from .apicredentials import APICredentials
from .apiconstants import APIConstants
import requests
import json
from requests.exceptions import ConnectionError

@dataclass(order=False)
class APIOperations:
    """
    ecrm Operation class


    @:param test: ecrm enviroment

    """

    credentials: APICredentials
    test: bool = False

    def __raise__(self,msg):
        raise Exception(msg)

    def __check__parameters(self,credentials: APICredentials,services: list, services_keys: list) -> str:
        if not isinstance(credentials, APICredentials):
            self.__raise__("Incorrect Credentials")

        if not isinstance(self.test, bool):
            self.__raise__("Incorrect Enviroment")

        if not isinstance(services, list) or len(services) == 0:
            self.__raise__("Incorrect Services")

        for service in services:
            if not isinstance(service, dict):
                self.__raise__("Incorrect Service Format")

            else:
                for key in services_keys:
                    if not isinstance(key,str) or not key in service:
                        self.__raise__("Incorrect Service Format")

        if self.test:
            return APIConstants.URL_ENVIROMENT_TEST
        else:
            return APIConstants.URL_ENVIROMENT_PROD

    #Services Methods
    def servicesvalidate(self, services: list):

        url = self.__check__parameters(self.credentials,services,['service_type','service_name'])

        try:
            response = requests.post( f'{url}/services/contract/validate_srv/',
                                                 params={
                                                     'lst': json.dumps(services)},
                                                 auth=self.credentials.getAuth())
        except ConnectionError as error:
            return {'success': False, 'error': 'Network Error', 'error_detail': str(error)}

        if response.status_code != 200:
            return {'success': False, 'error': response.reason, 'error_detail': response.reason}

        response_json = response.json()

        if response_json['success']:
            return {'success': True, 'data': response_json['data']}

        return {'success': False, 'error': response_json['errormsg'], 'error_detail': response_json['errormsg']}

    def servicespayment(self, services: list, order_id: str, source: str, payment_type: str, currency: str):

        url = self.__check__parameters(self.credentials,services,['account_state_eid','service_typology','service_name','real_import'])

        if not isinstance(order_id,str) or len(order_id) == 0:
            self.__raise__("Incorrect Order ID")

        elif not isinstance(source,str) or len(source) == 0:
            self.__raise__("Incorrect Source")

        elif not isinstance(payment_type,str) or len(payment_type) == 0:
            self.__raise__("Incorrect payment Type")

        elif not isinstance(currency,str) or len(currency) == 0:
            self.__raise__("Incorrect Currency")

        try:
            response = requests.post(
                f'{url}/services/paymentms/add_virtual_extern_payment',
                params={'transaction_number': order_id,
                        'source_type': source,
                        'payment_type': payment_type,
                        'currency': currency,
                        'lst_invoices': json.dumps(services)},
                auth=self.credentials.getAuth())

        except ConnectionError as error:
            return {'success': False, 'error': 'Network Error', 'error_detail': str(error)}

        if response.status_code != 200:
            return {'success': False, 'error': response.reason, 'error_detail': response.reason}

        response_json = response.json()

        if response_json['success']:
            return {'success': True, 'data': response_json['data']}

        return {'success': False, 'error': response_json['errormsg'], 'error_detail': response_json['errormsg']}


