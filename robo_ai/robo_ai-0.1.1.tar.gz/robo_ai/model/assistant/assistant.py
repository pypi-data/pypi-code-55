from typing import List

import attr

from robo_ai.model.assistant.assistant_param import AssistantParam


@attr.s(auto_attribs=True)
class Assistant(object):
    uuid: str = None
    name: str = None
    description: str = None
    created: str = None
    updated: str = None
    status: str = None
    assistantService: str = None
    params: List[AssistantParam] = []
