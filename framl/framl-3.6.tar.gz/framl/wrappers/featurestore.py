
import json
import os
import time
import jwt
import requests
import subprocess
import warnings
requests.packages.urllib3.disable_warnings()


class FeatureStore:
    HOST = os.getenv('FEATURE_STORE_HOST') or "https://feature-store-api-rzhg37iauq-ez.a.run.app"

    def __init__(self):
        self.token = ""
        self.token_exp = 0
        self._get_token()

    def _get_token(self):
        if time.time()+10 > self.token_exp:
            token = FeatureStore._fetch_token()
            self.token = token["bearer"]
            self.token_exp = token["expiration"]
        return self.token

    @staticmethod
    def _fetch_token() -> dict:
        if os.environ.get('FRAML_ENV') != "production":
            warnings.warn("using local identity token")
            result = subprocess.run(["gcloud", "auth", "print-identity-token"], stdout=subprocess.PIPE)
            bearer = result.stdout.decode('utf-8').replace("\n", "")
            exp = jwt.decode(bearer, algorithms='RS256', verify=False)['exp']

        else:
            metadata_server_token_url = 'http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience='
            token_request_url = metadata_server_token_url + FeatureStore.HOST
            token_request_headers = {'Metadata-Flavor': 'Google'}

            # Fetch the token
            token_response = requests.get(token_request_url, headers=token_request_headers)
            bearer = token_response.content.decode("utf-8")
            exp = jwt.decode(bearer, algorithms='RS256', verify=False)['exp']

        return {"bearer": bearer, "expiration": exp}

    def get(self, view: str, id: str):
        # Provide the token in the request to the receiving service
        receiving_service_headers = {
            'Authorization': f'bearer {self._get_token()}',
            'Content-type':  'application/json; charset=utf-8',
        }

        # sending the request. Please make sure the payload is a valid json string
        r = requests.get(url=f"{FeatureStore.HOST}/kinds/{view}/{id}",
                         headers=receiving_service_headers,
                         verify=False
                         )
        r.encoding = 'utf-8'
        if r.status_code == 401:
            raise Exception("service account does not have access to the FeatureStore")

        return r

    def get_bulk(self, view: str, ids: list):
        # Provide the token in the request to the receiving service
        receiving_service_headers = {
            'Authorization': f'bearer {self._get_token()}',
            'Content-type':  'application/json; charset=utf-8',
        }

        # sending the request. Please make sure the payload is a valid json string
        r = requests.post(url=f"{FeatureStore.HOST}/kinds/{view}",
                          data=json.dumps({"ids": ids}),
                          headers=receiving_service_headers,
                          verify=False)
        r.encoding = 'utf-8'
        if r.status_code == 401:
            raise Exception("service account does not have access to the FeatureStore")

        return r