import attr

from robo_ai.model.assistant.assistant import Assistant
from robo_ai.model.base_response import BaseResponse


@attr.s(auto_attribs=True)
class AssistantResponse(BaseResponse):
    content: Assistant = None
