import attr


@attr.s(auto_attribs=True)
class AssistantParam(object):
    name: str = None
    value: str = None
    mandatory: bool = False
    default_value: str = None
    created: str = None
    updated: str = None
