"""Provides DetectDuplicatesTask class"""

from typing import Type

from .. import errors
from .. import schemas as T
from .abstract import Task


class DetectDuplicatesTask(Task):
    """Detecting duplicated data task"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.insert_errors = self.db.batch_writer_insert_error()

    def _run(self):
        self.report_progress(total=self.db.count_all_item())

        prev_item = None
        prev_item_conflict = False
        for item in self.db.get_items_sorted_by_dst_path():
            # filepath conflicts in Flywheel
            if item.existing:
                self._add_error(item, errors.DuplicateFilepathInFlywheel)

            # filepath conflicts in upload set
            if prev_item and prev_item.container_path == item.container_path and prev_item.filename == item.filename:
                self._add_error(item, errors.DuplicateFilepathInUploadSet)
                prev_item_conflict = True
            else:
                if prev_item_conflict:
                    # mark prev_item also as duplicate if we found any similar item
                    self._add_error(prev_item, errors.DuplicateFilepathInUploadSet)
                prev_item = item
                prev_item_conflict = False

            # update progress
            self.report_progress(completed=1)

        # check last prev_item
        # filepath conflict in upload set
        if prev_item_conflict:
            self._add_error(prev_item, errors.DuplicateFilepathInUploadSet)

        self.insert_errors.flush()

    def _add_error(
        self,
        item: T.ItemWithContainerPath,
        error_type: Type[errors.BaseIngestError]
    ) -> None:
        """Add error for the specified item with the specified error type"""
        self.insert_errors.push(
            T.Error(item_id=item.id, code=error_type.code).dict(exclude_none=True)
        )

    def _on_success(self):
        self.db.set_ingest_status(status=T.IngestStatus.in_review)
        if self.ingest_config.assume_yes:
            # ingest was started with assume yes so accept the review
            self.db.review()

    def _on_error(self):
        self.db.fail()
