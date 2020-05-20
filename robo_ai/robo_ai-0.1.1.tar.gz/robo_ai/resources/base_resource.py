from robo_ai.resources.assistants import AssistantsResource
from robo_ai.resources.client_resource import ClientResource
from robo_ai.resources.oauth import OauthResource


class BaseResource(ClientResource):
    def _register_resources(self):
        self._add_resource('assistants', AssistantsResource)
        self._add_resource('oauth', OauthResource)

    @property
    def assistants(self) -> AssistantsResource:
        return self._get_resource('assistants')

    @property
    def oauth(self) -> OauthResource:
        return self._get_resource('oauth')
