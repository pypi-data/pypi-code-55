"""Ingest DetectDuplicatesTask tests"""

import datetime
import uuid
from unittest import mock

import pytest

from flywheel_cli.ingest import config
from flywheel_cli.ingest import errors
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.tasks import detect_duplicates


@pytest.fixture(scope="function")
def detect_duplicates_task():
    task = T.TaskOut(
        type="detect_duplicates",
        id=uuid.uuid4(),
        ingest_id=uuid.uuid4(),
        status="pending",
        retries=0,
        history=[],
        created=datetime.datetime.now(),
    )
    detect_duplicates_task = detect_duplicates.DetectDuplicatesTask(
        db=mock.Mock(),
        task=task,
        worker_config=mock.Mock(),
    )
    detect_duplicates_task.ingest_config = config.IngestConfig(
        src_fs="/tmp"
    )
    return detect_duplicates_task


@pytest.fixture(scope="function")
def create_item():
    def _create(**kwargs):
        kwargs.setdefault("id", uuid.uuid4())
        kwargs.setdefault("dir", "/dir")
        kwargs.setdefault("existing", False)
        return T.ItemWithContainerPath(**kwargs)
    return _create

def test_on_success(detect_duplicates_task):
    detect_duplicates_task._on_success()

    detect_duplicates_task.db.set_ingest_status.assert_called_once_with(
        status=T.IngestStatus.in_review,
    )
    detect_duplicates_task.db.review.assert_not_called()


def test_on_success_assume_yes(detect_duplicates_task):
    detect_duplicates_task.ingest_config.assume_yes = True

    detect_duplicates_task._on_success()

    detect_duplicates_task.db.set_ingest_status.assert_called_once_with(
        status=T.IngestStatus.in_review,
    )
    detect_duplicates_task.db.review.assert_called_once()


def test_on_error(detect_duplicates_task):
    detect_duplicates_task._on_error()

    detect_duplicates_task.db.fail.assert_called_once()


def test_run_dup_in_fw(detect_duplicates_task, create_item):
    db_mock = detect_duplicates_task.db
    db_mock.count_all_item.return_value = 3
    item_1 = create_item(
        filename="a.txt",
        existing=True,
        container_path="group/project",
    )
    item_2 = create_item(
        filename="b.txt",
        container_path="group/project/subject",
    )
    item_3 = create_item(
        filename="c.txt",
        existing=True,
        container_path="group/project/subject2",
    )
    db_mock.get_items_sorted_by_dst_path.return_value = [item_1, item_2, item_3]
    expected_error_code = errors.DuplicateFilepathInFlywheel.code

    detect_duplicates_task._run()

    assert detect_duplicates_task.insert_errors.mock_calls == [
        mock.call.push({"item_id": item_1.id, "code": expected_error_code}),
        mock.call.push({"item_id": item_3.id, "code": expected_error_code}),
        mock.call.flush(),
    ]


def test_run_dup_in_upload_set_first_items(detect_duplicates_task, create_item):
    db_mock = detect_duplicates_task.db
    db_mock.count_all_item.return_value = 3
    item_1 = create_item(
        filename="a.txt",
        container_path="group/project/subject",
    )
    item_2 = create_item(
        filename="a.txt",
        container_path="group/project/subject",
    )
    item_3 = create_item(
        filename="b.txt",
        container_path="group/project/subject2",
    )
    db_mock.get_items_sorted_by_dst_path.return_value = [item_1, item_2, item_3]
    expected_error_code = errors.DuplicateFilepathInUploadSet.code

    detect_duplicates_task._run()

    assert detect_duplicates_task.insert_errors.mock_calls == [
        mock.call.push({"item_id": item_2.id, "code": expected_error_code}),
        mock.call.push({"item_id": item_1.id, "code": expected_error_code}),
        mock.call.flush(),
    ]


def test_run_dup_in_upload_set_last_items(detect_duplicates_task, create_item):
    db_mock = detect_duplicates_task.db
    db_mock.count_all_item.return_value = 3
    item_1 = create_item(
        filename="a.txt",
        container_path="group/project/subject",
    )
    item_2 = create_item(
        filename="b.txt",
        container_path="group/project/subject",
    )
    item_3 = create_item(
        filename="b.txt",
        container_path="group/project/subject",
    )
    db_mock.get_items_sorted_by_dst_path.return_value = [item_1, item_2, item_3]
    expected_error_code = errors.DuplicateFilepathInUploadSet.code

    detect_duplicates_task._run()

    assert detect_duplicates_task.insert_errors.mock_calls == [
        mock.call.push({"item_id": item_3.id, "code": expected_error_code}),
        mock.call.push({"item_id": item_2.id, "code": expected_error_code}),
        mock.call.flush(),
    ]


def test_run_dup_in_upload_set_middle_items(detect_duplicates_task, create_item):
    db_mock = detect_duplicates_task.db
    db_mock.count_all_item.return_value = 4
    item_1 = create_item(
        filename="a.txt",
        container_path="group/project/subject",
    )
    item_2 = create_item(
        filename="b.txt",
        container_path="group/project/subject",
    )
    item_3 = create_item(
        filename="b.txt",
        container_path="group/project/subject",
    )
    item_4 = create_item(
        filename="b.txt",
        container_path="group/project/subject",
    )
    item_5 = create_item(
        filename="c.txt",
        container_path="group/project/subject",
    )
    db_mock.get_items_sorted_by_dst_path.return_value = [item_1, item_2, item_3, item_4, item_5]
    expected_error_code = errors.DuplicateFilepathInUploadSet.code

    detect_duplicates_task._run()

    assert detect_duplicates_task.insert_errors.mock_calls == [
        mock.call.push({"item_id": item_3.id, "code": expected_error_code}),
        mock.call.push({"item_id": item_4.id, "code": expected_error_code}),
        mock.call.push({"item_id": item_2.id, "code": expected_error_code}),
        mock.call.flush(),
    ]
