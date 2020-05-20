from enum import Enum


class AssistantRuntimeStatus(Enum):
    UPDATING = "UPDATING"
    CREATING = "CREATING"
    CREATED = "CREATED"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    REMOVING = "REMOVING"
    REMOVED = "REMOVED"
    UNKNOWN = "UNKNOWN"
    DEAD = "DEAD"
