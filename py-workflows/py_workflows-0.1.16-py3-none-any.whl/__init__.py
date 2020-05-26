from __future__ import annotations

from workflows.file_task import FileTask
from workflows.task import Task


__all__ = ["FileTask", "Task"]
__version__ = "0.1.16"
_ = FileTask.run  # dead: disable
