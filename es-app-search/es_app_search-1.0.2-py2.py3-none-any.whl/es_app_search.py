import requests


class ESClient:
    def __init__(self, api_endpoint: str, private_key: str):
        self.prefix = api_endpoint + '/api/as/v1/engines'
        self.private_key = private_key
        self.session = requests.Session()
        self.session.headers = {'Authorization': f'Bearer {private_key}'}

    def search(self, engine_name: str, query: str, size: int = 20, current: int = 1):
        """
        :param engine_name: Name of the engine
        :param query: A string or number used to find related documents
        :param size: Number of results per page. Must be between 1 and 100
        :param current: Page number to return. Must be greater or equal to 1
        """
        url = self.prefix + f'/{engine_name}/search'
        data = {"query": query, "page": {"size": size, "current": current}}
        return self.session.post(url, json=data)

    def create_synonym(self, engine_name: str, synonyms: []):
        """
        Create a synonym set.

        :param engine_name: Name of the engine
        :param synonyms: List of synonyms
        :return: ID and list of synonyms

        """
        url = self.prefix + f'/{engine_name}/synonyms'
        data = {'synonyms': synonyms}
        return self.session.post(url, json=data)

    def get_synonyms(self, engine_name: str, size: int = 20, current: int = 1):
        """
        Get all synonyms.

        :param engine_name: Name of the engine
        :param size: Number of results per page. Must be between 1 and 100
        :param current: Page number to return. Must be greater or equal to 1
        """
        url = self.prefix + f'/{engine_name}/synonyms'
        data = {'page': {'size': size, 'current': current}}
        return self.session.get(url, json=data)
