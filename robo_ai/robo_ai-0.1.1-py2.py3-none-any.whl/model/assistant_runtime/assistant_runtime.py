import attr

from robo_ai.model.assistant_runtime.assistant_runtime_status import AssistantRuntimeStatus


@attr.s(auto_attribs=True)
class AssistantRuntime(object):
    assistantUuid: str = None
    status: AssistantRuntimeStatus = None
    createdAt: str = None
    engine: str = None
    provider: str = None
