from enum import Enum

class MessageStatus(Enum):
    RUNNING = 'running'  # "info" level message
    SUCCESS = 'success'  # extract success
    ERROR = 'error'  # fatal issue
    WARNING = 'warning'  # non-fatal issue
