"""Provides factory method to create tasks."""

from .detect_duplicates import DetectDuplicatesTask
from .finalize import FinalizeTask
from .prepare import PrepareTask
from .upload import UploadTask
from .resolve import ResolveTask
from .scan import ScanTask


TASK_MAP = {
    "scan": ScanTask,
    "resolve": ResolveTask,
    "detect_duplicates": DetectDuplicatesTask,
    "prepare": PrepareTask,
    "upload": UploadTask,
    "finalize": FinalizeTask,
}


def create_task(client, task, worker_config):
    """Create executable task from task object"""
    task_cls = TASK_MAP.get(task.type)
    if not task_cls:
        raise Exception(f"Invalid task type: {task.type}")
    return task_cls(client, task, worker_config)
