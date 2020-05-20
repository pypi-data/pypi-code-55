class Config(object):
    __base_endpoint: str = None
    __http_auth: dict = {
        'username': None,
        'password': None
    }

    def __init__(self, base_endpoint: str, http_auth: dict):
        self.__base_endpoint = base_endpoint
        self.__http_auth = http_auth

    @property
    def base_endpoint(self) -> str:
        return self.__base_endpoint

    @property
    def http_auth(self) -> dict:
        return self.__http_auth

    @property
    def http_auth_username(self) -> str:
        return self.__http_auth['username']

    @property
    def http_auth_password(self) -> str:
        return self.__http_auth['password']
