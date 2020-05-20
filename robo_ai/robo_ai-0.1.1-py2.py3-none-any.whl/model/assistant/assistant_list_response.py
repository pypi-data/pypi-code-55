from typing import List

from robo_ai.model.assistant.assistant import Assistant
from robo_ai.model.paginated_base_response import PaginatedBaseResponse
import attr


@attr.s(auto_attribs=True)
class AssistantListResponse(PaginatedBaseResponse):
    content: List[Assistant] = []
