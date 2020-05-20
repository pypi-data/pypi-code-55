import attr

from robo_ai.model.base_response import BaseResponse


@attr.s(auto_attribs=True)
class PaginatedBaseResponse(BaseResponse):
    content: object = None
    size: int = None
    page: int = None
    pageElements: int = None
    totalElements: int = None
