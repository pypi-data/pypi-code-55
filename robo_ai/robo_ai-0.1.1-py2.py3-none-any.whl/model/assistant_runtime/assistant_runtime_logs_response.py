import attr

from robo_ai.model.assistant_runtime.assistant_runtime_logs import AssistantRuntimeLogs
from robo_ai.model.base_response import BaseResponse


@attr.s(auto_attribs=True)
class AssistantRuntimeLogsResponse(BaseResponse):
    content: AssistantRuntimeLogs = None
