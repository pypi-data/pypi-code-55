import os
from typing import Callable

from robo_ai.model.assistant_runtime.assistant_runtime_logs_response import AssistantRuntimeLogsResponse
from robo_ai.model.assistant_runtime.assistant_runtime_response import AssistantRuntimeResponse
from robo_ai.resources.client_resource import ClientResource, RequestMethod


class AssistantRuntimesResource(ClientResource):

    def create(self, assistant_uuid: str, package_file_path: str, base_runtime: str,
               progress_callback: Callable[[int], None] = None):
        return self.__deploy(RequestMethod.POST, assistant_uuid, package_file_path, base_runtime, progress_callback)

    def update(self, assistant_uuid: str, package_file_path: str, base_runtime: str,
               progress_callback: Callable[[int], None] = None):
        return self.__deploy(RequestMethod.PUT, assistant_uuid, package_file_path, base_runtime, progress_callback)

    def stop(self, assistant_uuid: str):
        url = self.__get_runtime_url(assistant_uuid) + '/stop'
        response = self.execute_request(RequestMethod.POST, url, response_class=AssistantRuntimeResponse)
        return response

    def start(self, assistant_uuid: str):
        url = self.__get_runtime_url(assistant_uuid) + '/start'
        response = self.execute_request(RequestMethod.POST, url, response_class=AssistantRuntimeResponse)
        return response

    def remove(self, assistant_uuid: str):
        url = self.__get_runtime_url(assistant_uuid)
        self.execute_request(RequestMethod.DELETE, url)

    def get(self, assistant_uuid: str) -> AssistantRuntimeResponse:
        url = self.__get_runtime_url(assistant_uuid)
        response = self.execute_request(RequestMethod.GET, url, response_class=AssistantRuntimeResponse)
        return response

    def get_logs(self, assistant_uuid: str) -> AssistantRuntimeLogsResponse:
        url = self.__get_runtime_url(assistant_uuid) + '/logs'
        response = self.execute_request(RequestMethod.GET, url, response_class=AssistantRuntimeLogsResponse)
        return response

    def __deploy(self, method: RequestMethod, assistant_uuid: str, package_file_path: str, base_runtime: str,
                 progress_callback: Callable[[int], None] = None):
        url = self.__get_runtime_url(assistant_uuid)
        with open(package_file_path, 'rb') as package_file:
            data = {
                'runtimeBase': base_runtime,
                'file': (os.path.basename(package_file_path), package_file, 'application/zip'),
            }

            def progress_callback_wrapper(monitor):
                progress_callback(monitor.bytes_read)

            callback = None
            if progress_callback:
                callback = progress_callback_wrapper

            response = self.execute_request(method, url, data=data, response_class=AssistantRuntimeResponse,
                                            progress_callback=callback)
            return response

    @staticmethod
    def __get_runtime_url(assistant_uuid: str):
        return '/api/assistants/{0}/runtime'.format(assistant_uuid)
