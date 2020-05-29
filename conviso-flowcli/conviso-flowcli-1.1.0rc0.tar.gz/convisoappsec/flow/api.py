import requests
from urllib.parse import urljoin

PRODUCTION_API_URL = "https://app.conviso.com.br"
STAGING_API_URL = "https://homologa.conviso.com.br"
DEVELOPMENT_API_URL = "http://localhost:3000"
DEFAULT_API_URL = PRODUCTION_API_URL


class RequestsSession(requests.Session):

    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.base_url, url)

        return super().request(
            method, url, *args, **kwargs
        )

class DeployNotFoundException(Exception):
    pass


class Deploys(object):
    ENDPOINT = 'api/v2/deploys'
    LIST_BY_PROJECT_ENPOINT ="api/v2/deploys/deploys_by_project_api_code"

    def __init__(self, client):
        self.client = client

    def create(self, project_code, current_tag, previous_tag):
        previous_tag = previous_tag if previous_tag else None

        data = {
            'api_code': project_code,
            'deploy': {
                'current_tag': current_tag,
                'previous_tag': previous_tag,
            },
        }

        session = self.client.requests_session
        response = session.post(self.ENDPOINT, json=data)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_excep:
            is_http_client_error = lambda s: s >= 400 and s < 500

            status = http_excep.response.status_code

            if is_http_client_error(status):
                raise http_excep

            if not self.exists(project_code, current_tag):
                raise http_excep

    def list(self, project_code, current_tag=None):
        data = {
            'api_code': project_code,
        }

        if current_tag:
            data.update({
                'current_tag': current_tag
            })

        session = self.client.requests_session
        response = session.get(self.LIST_BY_PROJECT_ENPOINT, json=data)
        response.raise_for_status()

        return {
            "deploys": response.json()
        }


    def get(self, project_code, current_tag):
        if not current_tag:
            raise ValueError(
                "current_tag is required and must be not empty"
            )

        list_result = self.list(project_code, current_tag)

        try:
            deploys = list_result.get('deploys')
            return deploys[0]
        except IndexError as e:
            raise DeployNotFoundException(
                "Deploy for current_tag[%s] not found" % current_tag
            ) from e

    def exists(self, project_code, current_tag):
        try:
            deploy = self.get(project_code, current_tag)
        except DeployNotFoundException:
            return False

        return True



class Client(object):

    def __init__(self, url, key, insecure):
        self.url = url
        self.insecure = insecure
        self.key = key

    @property
    def requests_session(self):
        session = RequestsSession(self.url)
        session.verify = not self.insecure
        session.headers.update({
            'x-api-key': self.key
        })

        return session

    @property
    def deploys(self):
        return Deploys(self)

# TODO: Create Custom handle
# requests.exceptions.ConnectionError
# requests.exceptions.SSLError
# requests.exceptions.HTTPError
