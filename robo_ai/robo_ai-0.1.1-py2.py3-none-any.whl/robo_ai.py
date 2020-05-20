from robo_ai.model.session import Session
from robo_ai.model.config import Config
from robo_ai.resources.assistants import AssistantsResource
from robo_ai.resources.base_resource import BaseResource
from robo_ai.resources.oauth import OauthResource


class RoboAi(object):
    __config: Config = None
    __base_resource: BaseResource = None
    __current_session = Session()

    def __init__(self, config: Config):
        self.__config = config
        self.__base_resource = BaseResource(self.__config, self.__current_session)

    def set_config(self, config: Config):
        self.__config = config

    def set_session_token(self, access_token: str):
        self.__current_session.access_token = access_token

    @property
    def oauth(self) -> OauthResource:
        return self.__base_resource.oauth

    @property
    def assistants(self) -> AssistantsResource:
        return self.__base_resource.assistants
