import attr

from robo_ai.model.assistant_runtime.assistant_runtime import AssistantRuntime
from robo_ai.model.base_response import BaseResponse


@attr.s(auto_attribs=True)
class AssistantRuntimeResponse(BaseResponse):
    content: AssistantRuntime = None
