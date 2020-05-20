"""Provides ScanTask class."""

import logging

from ..scanners.factory import create_scanner
from .. import schemas as T
from .abstract import Task

log = logging.getLogger(__name__)


class ScanTask(Task):
    """Scan a given path using the given scanner."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.insert_items = self.db.batch_writer_insert_item()
        self.insert_tasks = self.db.batch_writer_insert_task(depends_on=self.insert_items)
        self.insert_errors = self.db.batch_writer_insert_error(depends_on=self.insert_tasks)

    def _run(self):
        """Scan files in a given folder."""
        scanner_type = self.task.context["scanner"]["type"]
        dirpath = self.task.context["scanner"]["dir"]
        opts = self.task.context["scanner"].get("opts")
        scanner = create_scanner(
            scanner_type,
            self.ingest_config,
            self.strategy_config,
            self.worker_config,
            self.walker,
            opts=opts,
            context=self.task.context,
            get_subject_code_fn=self.db.resolve_subject,
        )
        for scan_result in scanner.scan(dirpath):
            if isinstance(scan_result, T.ItemIn):
                self.insert_items.push(scan_result.dict())
            elif isinstance(scan_result, T.TaskIn):
                self.insert_tasks.push(scan_result.dict())
            elif isinstance(scan_result, T.Error):
                scan_result.task_id = self.task.id
                self.insert_errors.push(scan_result.dict())
            else:
                raise ValueError(f"Unexpected type: {type(scan_result)}")

        self.insert_items.flush()
        self.insert_tasks.flush()
        self.insert_errors.flush()

    def _on_success(self):
        self.db.start_resolving()

    def _on_error(self):
        self.db.fail()
