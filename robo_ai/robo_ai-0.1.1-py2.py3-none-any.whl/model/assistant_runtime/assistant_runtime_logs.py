from typing import List

import attr


@attr.s(auto_attribs=True)
class AssistantRuntimeLogs(object):
    assistantUuid: str = None
    lines: List[str] = None
