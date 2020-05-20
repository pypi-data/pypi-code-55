class AccessToken(object):
    __access_token: str = None
    __token_type: str = None
    __expires_in: int = None
    __scope: str = None

    def __init__(self, access_token: str, token_type: str, expires_in: int, scope: str):
        self.__access_token = access_token
        self.__token_type = token_type
        self.__expires_in = expires_in
        self.__scope = scope

    @property
    def access_token(self):
        return self.__access_token

    @property
    def token_type(self):
        return self.__token_type

    @property
    def expires_in(self):
        return self.__expires_in

    @property
    def scope(self):
        return self.__scope
