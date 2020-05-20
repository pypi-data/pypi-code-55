from robo_ai.model.assistant.assistant_list_response import AssistantListResponse
from robo_ai.model.assistant.assistant_response import AssistantResponse
from robo_ai.resources.assistant_runtimes import AssistantRuntimesResource
from robo_ai.resources.client_resource import ClientResource, RequestMethod


class AssistantsResource(ClientResource):

    def _register_resources(self):
        self._add_resource('runtimes', AssistantRuntimesResource)

    def get_list(self, page=1) -> AssistantListResponse:
        params = {'page': page}
        url = '/api/assistants'
        return self.execute_request(RequestMethod.GET, url, params=params, response_class=AssistantListResponse)

    def get_assistant(self, uuid: str) -> AssistantResponse:
        url = '/api/assistants/uuid/' + uuid
        return self.execute_request(RequestMethod.GET, url, response_class=AssistantResponse)

    @property
    def runtimes(self) -> AssistantRuntimesResource:
        return self._get_resource('runtimes')
