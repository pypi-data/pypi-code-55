import datetime
import re
import uuid
from unittest import mock

import pytest

from flywheel_cli.ingest import config
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.tasks import abstract


class ExampleTask(abstract.Task):
    def _run(self):
        pass

@pytest.fixture(scope="function")
def example_task():
    task_out = T.TaskOut(
        type="prepare",
        id=uuid.uuid4(),
        ingest_id=uuid.uuid4(),
        status="pending",
        retries=0,
        history=[],
        created=datetime.datetime.utcnow()
    )
    task = ExampleTask(
        db=mock.Mock(),
        task=task_out,
        worker_config=mock.Mock()
    )
    task.ingest_config = config.IngestConfig(src_fs="/tmp")

    return task


def test_task_error_message(example_task, mocker):
    class FooException(Exception):
        pass
    example_task._run = mock.Mock(side_effect=FooException("Foo bar"))
    datetime_mock = mocker.patch.object(abstract, "datetime")
    datetime_mock.datetime.utcnow.return_value = datetime.datetime(1900, 1, 2, 3, 4, 5)

    example_task.run()

    assert example_task.db.update_task.call_count == 1
    args, kwargs = example_task.db.update_task.call_args
    assert len(args) == 1
    assert len(kwargs.items()) == 2
    assert args[0] == example_task.task.id
    assert kwargs["status"] == T.TaskStatus.failed
    expected_msg = (
        r"filename: (\/.*), "
        r"line number: \d+, "
        "type: test_task_error_message.<locals>.FooException, "
        "message: Foo bar, "
        "timestamp: 1900-01-02T03:04:05$"
    )
    assert re.match(expected_msg, kwargs["error"])
