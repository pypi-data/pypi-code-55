import datetime
import inspect
import io
import logging
import multiprocessing as mp
import os
import re
from uuid import UUID, uuid4

import pytest
import sqlalchemy as sqla
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from flywheel_cli.ingest import config, errors
from flywheel_cli.ingest import models as M
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.client import db as ingest_db_client, db_transactions
from flywheel_cli.ingest.errors import IngestIsNotDeletable


def test_create_from_url():
    client = ingest_db_client.DBClient.from_url("sqlite:///:memory:")

    assert isinstance(client, ingest_db_client.DBClient)
    assert client.url == "sqlite:///:memory:"
    assert client._ingest_id is None

def test_create_from_url_with_uuid():
    uuid = uuid4()
    client = ingest_db_client.DBClient.from_url("sqlite:///:memory:", uuid)

    assert isinstance(client, ingest_db_client.DBClient)
    assert client.url == "sqlite:///:memory:"
    assert client._ingest_id == uuid

def test_create_sqlite():
    client = ingest_db_client.DBClient("sqlite:///:memory:")
    assert client.engine.name == "sqlite"
    assert client.check_connection()


def test_check_connection_fail():
    client = ingest_db_client.DBClient("sqlite:///:memory:")
    assert client.engine.name == "sqlite"
    client.engine = None
    assert not client.check_connection()


def test_create_pg():
    client = ingest_db_client.DBClient(
        "postgresql://user:pass@localhost:1234/db")
    assert client.engine.name == "postgresql"
    assert not client.check_connection()


def test_create_ingest(db_client):
    ingest = db_client.create_ingest(
        config.IngestConfig(
            src_fs="/tmp"
        ),
        config.FolderConfig(),
        T.FWAuth(
            api_key="api_key",
            host="flywheel.test",
            user="test@flywheel.test",
            is_admin=True,
        )
    )

    assert isinstance(ingest, T.IngestOutAPI)
    assert isinstance(ingest.id, UUID)
    assert isinstance(ingest.created, datetime.datetime)
    assert ingest.status == "created"
    assert ingest.config.src_fs == "/tmp"
    assert ingest.fw_host == "flywheel.test"
    assert ingest.fw_user == "test@flywheel.test"
    assert db_client.ingest == ingest


def test_get_ingests_empty(db_client):
    assert list(db_client.list_ingests()) == []


def test_get_ingests(db_client, data):
    ingest_id_1 = data.create("Ingest")
    ingest_id_2 = data.create("Ingest")

    ingests = db_client.list_ingests()
    assert inspect.isgenerator(ingests)
    ingests = list(ingests)
    assert len(ingests) == 2
    assert {ingest.id for ingest in ingests} == {ingest_id_1, ingest_id_2}


def test_get_ingest_nonexistent_id(db_client):
    with pytest.raises(NoResultFound):
        db_client.bind(uuid4())
        db_client.ingest


def test_get_ingest(db_client, data):
    ingest_id = data.create("Ingest")
    assert db_client.ingest.id == ingest_id


def test_start_ingest(db_client, data):
    data.create("Ingest")

    ingest = db_client.start()
    assert ingest.status == "scanning"
    assert len(list(db_client.get_all_task(M.Task.type == T.TaskType.scan))) == 1


def test_set_ingest_status(db_client, data):
    data.create("Ingest")
    ingest = db_client.set_ingest_status("scanning")
    assert ingest.status == "scanning"
    ingest = db_client.set_ingest_status("failed")
    assert ingest.status == "failed"


def test_set_ingest_status_invalid(db_client, data):
    data.create("Ingest")
    db_client.set_ingest_status("scanning")

    with pytest.raises(ValueError):
        db_client.set_ingest_status("created")


def test_set_ingest_status_idempotent(db_client, data):
    data.create("Ingest")
    ingest = db_client.set_ingest_status("scanning")
    assert ingest.status == "scanning"
    ingest = db_client.set_ingest_status("scanning")
    assert ingest.status == "scanning"


def test_abort_ingest(db_client, data):
    data.create("Ingest")
    ingest = db_client.abort()
    assert ingest.status == "aborted"
    last_history = ingest.history[-1]
    assert last_history[0] == "aborted"
    # abort idempotent
    ingest = db_client.abort()
    assert last_history == ingest.history[-1]


def test_next_task_none(db_client):
    task = db_client.next_task('worker')
    assert task is None


def test_next_task(db_client, data):
    ingest_id = data.create("Ingest")
    data.create(
        "Task",
        status='running',
        worker='worker',
        type='scan',
        ingest_id=ingest_id
    )
    task_pending_id = data.create(
        "Task",
        status='pending',
        worker='worker',
        type='scan',
        ingest_id=ingest_id
    )

    task = db_client.next_task('worker')
    assert task.id == task_pending_id

# Ingest-bound methods


def test_ingest_property(db_client, data):
    ingest_id = data.create("Ingest")
    assert db_client.ingest.id == ingest_id


def test_load_subject_csv(db_client, data):
    data.create(
        "Ingest",
        strategy_config={},
        config={
            "src_fs": "/tmp",
            "subject_config": {
                "code_serial": 1,
                "code_format": "code-{SubjectCode}",
                "map_keys": []
            }
        }
    )

    f = io.BytesIO(b"code-{SubjectCode}\ncode-1,code_a\ncode-2,code_b\n")
    db_client.load_subject_csv(f)
    subjects = list(db_client.subjects)
    assert subjects == ['code-{SubjectCode}\n',
                        'code-1,code_a\n', 'code-2,code_b\n']


def test_statuses(db_client, data):
    data.create("Ingest")
    assert db_client.ingest.status == 'created'
    db_client.start()
    assert db_client.ingest.status == 'scanning'
    db_client.set_ingest_status("resolving")
    db_client.set_ingest_status("in_review")
    assert db_client.ingest.status == 'in_review'
    db_client.review()
    assert db_client.ingest.status == 'preparing'
    db_client.abort()
    assert db_client.ingest.status == 'aborted'


def test_progress(db_client, data):
    ingest_id = data.create("Ingest")
    data.create(
        "Task",
        status='completed',
        worker='worker',
        type='scan',
        ingest_id=ingest_id,
        completed=100,
        total=100,
    )
    data.create(
        "Task",
        status='failed',
        worker='worker',
        type='scan',
        ingest_id=ingest_id,
        completed=55,
        total=99,
    )
    data.create(
        "Task",
        status='running',
        worker='worker',
        type='prepare',
        ingest_id=ingest_id,
        completed=55,
        total=100,
    )
    item_id = data.create("Item", bytes_sum=99)
    data.create(
        "Task",
        status='running',
        worker='worker',
        type='upload',
        ingest_id=ingest_id,
        item_id=item_id,
    )

    progress = db_client.progress
    assert progress.scans.total == 2
    assert progress.scans.completed == 1
    assert progress.scans.failed == 1
    assert progress.items.running == 1
    assert progress.items.total == 1
    assert progress.files.total == 1
    assert progress.bytes.total == 99
    assert progress.stages.scanning.completed == 155
    assert progress.stages.scanning.total == 199
    assert progress.stages.preparing.completed == 55
    assert progress.stages.preparing.total == 100


def test_summary(db_client, data):
    ingest_id = data.create("Ingest")
    levels = [0, 1, 2, 3, 4]
    for level in levels:
        cnt = level + 1
        for _ in range(cnt):
            data.create(
                "Container",
                ingest_id=ingest_id,
                level=level,
                src_context={}
            )
    item_id = data.create("Item")
    error = errors.DuplicateFilepathInFlywheel
    data.create("Error", item_id=item_id, code=error.code)
    data.create("Error", item_id=item_id, code=error.code)

    summary = db_client.summary
    assert summary.groups == 1
    assert summary.projects == 2
    assert summary.subjects == 3
    assert summary.sessions == 4
    assert summary.acquisitions == 5
    assert len(summary.errors) == 1
    assert summary.errors[0].code == error.code
    assert summary.errors[0].message == error.message
    assert summary.errors[0].description == error.description
    assert summary.errors[0].count == 2


def test_report(db_client, data):
    ingest_id = data.create("Ingest")
    task_id = data.create(
        "Task",
        status="failed",
        worker="worker",
        type="scan",
        ingest_id=ingest_id,
    )
    data.create(
        "Error",
        task_id=task_id,
        code="UNKNOWN",
        message="foo bar error",
    )
    db_client.start()

    report = db_client.report
    assert report.status == "scanning"
    # TODO
    assert report.elapsed == {}
    assert len(report.errors) == 1
    assert report.errors[0].code == "UNKNOWN"
    assert report.errors[0].message == "foo bar error"


def test_tree(db_client, data):
    ingest_id = data.create("Ingest")
    data.create(
        "Container",
        ingest_id=ingest_id,
        level=0,
        src_context={}
    )
    data.create(
        "Container",
        ingest_id=ingest_id,
        level=1,
        src_context={}
    )
    tree = list(db_client.tree)
    assert len(tree) == 2
    # TODO add more assertions


def test_audit_logs(db_client, data):
    ingest_id = data.create("Ingest")
    container_id = data.create(
        "Container",
        ingest_id=ingest_id,
        level=1,
        src_context={},
        dst_path="dst_path"
    )
    item_id = data.create(
        'Item',
        dir="/dir",
        type="file",
        files=[],
        files_cnt=10,
        bytes_sum=1234,
        filename='testfile',
    )
    item_id2 = data.create(
        'Item',
        dir="/dir2",
        type="file",
        files=[],
        files_cnt=10,
        bytes_sum=1234,
        filename='testfile2',
        existing=True
    )
    item_id3 = data.create(
        'Item',
        dir="/dir3",
        filename='testfile3',
        existing=True,
        skipped=True,
    )
    item_id4 = data.create(
        'Item',
        dir="/dir4",
        filename='testfile4',
        skipped=True,
        existing=True,
    )
    item_id5 = data.create(
        'Item',
        dir="/dir5",
        filename='testfile5',
    )
    unknown_error = errors.BaseIngestError
    dup_fw_error = errors.DuplicateFilepathInFlywheel
    dup_upload_set_error = errors.DuplicateFilepathInUploadSet
    data.create(
        "Error",
        item_id=item_id4,
        code=dup_upload_set_error.code,
    )
    data.create(
        "Error",
        item_id=item_id4,
        code=dup_fw_error.code,
    )
    data.create(
        "Error",
        item_id=item_id5,
        code=unknown_error.code,
        message="Foo bar error message"
    )
    data.create(
        "Task",
        status='completed',
        worker='worker',
        type='scan',
        ingest_id=ingest_id,
        item_id=item_id
    )
    data.create(
        "Task",
        status='failed',
        worker='worker',
        type='scan',
        ingest_id=ingest_id,
        item_id=item_id2,
    )
    data.create(
        "Task",
        status='failed',
        worker='worker',
        type='upload',
        item_id=item_id5,
    )
    logs = list(db_client.audit_logs)
    assert logs == [
        'src_path,dst_path,status,existing,error_code,error_message\n',
        '/tmp/dir/testfile,dst_path/testfile,completed,False,,\n',
        '/tmp/dir2/testfile2,dst_path/testfile2,failed,True,UNKNOWN,Unknown error\n',
        '/tmp/dir3/testfile3,dst_path/testfile3,skipped,True,,\n',
        '/tmp/dir4/testfile4,dst_path/testfile4,skipped,True,DD01,File Path Conflict in Upload Set\n',
        '/tmp/dir4/testfile4,dst_path/testfile4,skipped,True,DD02,File Path Conflict in Flywheel\n',
        '/tmp/dir5/testfile5,dst_path/testfile5,failed,False,UNKNOWN,Foo bar error message\n',
    ]


def test_deid_logs(db_client, data):
    ingest_id = data.create(
        "Ingest",
        strategy_config={},
        config={
            "src_fs": "/tmp",
            "deid_profile": "minimal",
            "deid_profiles": [
                {'name': 'minimal', 'description': 'Dsc', 'dicom': {
                    'fields': [
                        {'name': 'PatientBirthDate', 'remove': True},
                        {'name': 'PatientName', 'remove': True},
                        {'name': 'PatientID', 'remove': False}
                    ]}}
            ],
            "de_identify": True
        }
    )

    data.create(
        "DeidLog",
        src_path="src_path",
        tags_before={
            "StudyInstanceUID": "b1",
            "SeriesInstanceUID": "b2",
            "SOPInstanceUID": "b3",
            "PatientBirthDate": "b4",
            "PatientName": "b5",
            "PatientID": "b6",
        },
        tags_after={
            "StudyInstanceUID": "a1",
            "SeriesInstanceUID": "a2",
            "SOPInstanceUID": "a3",
            "PatientID": "a6",
        },
        ingest_id=ingest_id
    )

    logs = list(db_client.deid_logs)

    assert logs == ['src_path,type,StudyInstanceUID,SeriesInstanceUID,SOPInstanceUID,PatientBirthDate,PatientName,PatientID\n',
                    'src_path,before,b1,b2,b3,b4,b5,b6\n', 'src_path,after,a1,a2,a3,,,a6\n']


def test_subjects(db_client, data):
    ingest_id = data.create(
        "Ingest",
        strategy_config={},
        config={
            "src_fs": "/tmp",
            "subject_config": {
                "code_serial": 1,
                "code_format": "code-{SubjectCode}",
                "map_keys": []
            }
        }
    )
    data.create("Subject", ingest_id=ingest_id,
                code="code-1", map_values=['code_a'])
    subjects = list(db_client.subjects)
    assert subjects == ['code-{SubjectCode}\n', 'code-1,code_a\n']


def test_api_key(db_client, data, defaults):
    data.create("Ingest")
    key = db_client.api_key
    assert key == defaults.Ingest.api_key


def test_add(db_client, data):
    data.create("Ingest")
    task = T.TaskIn(type="scan")
    _task = db_client.add(task)
    assert _task.id is not None


def test_get(db_client, data):
    ingest_id = data.create("Ingest")
    tid = data.create(
        "Task",
        status='failed',
        worker='worker',
        type='scan',
        ingest_id=ingest_id,
    )

    task = db_client.get('Task', tid)
    assert task.id == tid
    assert task.ingest_id == ingest_id
    assert task.status == 'failed'


def test_get_all(db_client, data):
    ingest_id = data.create("Ingest")
    tid1 = data.create(
        "Task",
        status='failed',
        worker='worker',
        type='scan',
        ingest_id=ingest_id,
    )
    tid2 = data.create(
        "Task",
        status='failed',
        worker='worker',
        type='scan',
        ingest_id=ingest_id,
    )

    # TODO conditions test
    tasks = list(db_client.get_all('Task'))
    assert len(tasks) == 2
    for task in tasks:
        assert task.id in [tid1, tid2]


def test_update(db_client, data):
    ingest_id = data.create("Ingest")
    tid = data.create(
        "Task",
        status='pending',
        worker='worker',
        type='scan',
        ingest_id=ingest_id,
    )
    task = db_client.get('Task', tid)
    assert task.id == tid
    assert task.ingest_id == ingest_id
    assert task.status == 'pending'

    task = db_client.update('Task', tid, status='failed')
    assert task.id == tid
    assert task.ingest_id == ingest_id
    assert task.status == 'failed'


def test_bulk_insert(db_client, data):
    data.create("Ingest")

    mappings = [
        {
            'status': 'pending',
            'worker': 'worker',
            'type': 'scan'
        },
        {
            'status': 'failed',
            'worker': 'worker',
            'type': 'scan'
        }
    ]

    db_client.bulk('insert', 'Task', mappings)
    tasks = list(db_client.get_all('Task'))
    assert len(tasks) == 2
    for task in tasks:
        assert task.status in ['pending', 'failed']


def test_bulk_update(db_client, data):
    ingest_id = data.create("Ingest")
    tid1 = data.create(
        "Task",
        status='pending',
        worker='worker',
        type='scan',
        ingest_id=ingest_id,
    )
    tid2 = data.create(
        "Task",
        status='running',
        worker='worker',
        type='scan',
        ingest_id=ingest_id,
    )

    mappings = [
        {
            'id': tid1,
            'status': 'failed',
        },
        {
            'id': tid2,
            'status': 'failed',
        }
    ]

    db_client.bulk('update', 'Task', mappings)
    tasks = list(db_client.get_all('Task'))
    assert len(tasks) == 2
    for task in tasks:
        assert task.status == 'failed'


def test_start_resolving_has_unfinished_task(db_client, data):
    ingest_id = data.create("Ingest")
    db_client.start()
    data.create(
        "Task",
        status='pending',
        worker='worker',
        type='scan',
        ingest_id=ingest_id,
    )
    ingest = db_client.start_resolving()
    assert ingest.id == ingest_id
    assert ingest.status == "scanning"


def test_start_resolving(db_client, data):
    ingest_id = data.create("Ingest")
    db_client.start()
    for task in db_client.get_all('Task'):
        db_client.update('Task', task.id, status='completed')

    ingest = db_client.start_resolving()
    assert ingest.id == ingest_id
    assert ingest.status == "resolving"


def test_resolve_subject_existing(db_client, data):
    ingest_id = data.create("Ingest")
    data.create("Subject", ingest_id=ingest_id,
                code="code-1", map_values=['code_a'])
    subject = db_client.resolve_subject(['code_a'])
    assert subject == 'code-1'
    # TODO check that another subject was not created (count)


def test_resolve_subject_non_existing(db_client, data):
    data.create(
        "Ingest",
        strategy_config={},
        config={
            "src_fs": "/tmp",
            "subject_config": {
                "code_serial": 1,
                "code_format": "code-{SubjectCode}",
                "map_keys": []
            }
        }
    )
    subject = db_client.resolve_subject(['code_a'])
    assert subject == 'code-2'
    # TODO check that another subject was not created (count)


def test_start_finalizing(db_client, data):
    ingest_id = data.create("Ingest")
    db_client.start()
    for task in db_client.get_all('Task'):
        db_client.update('Task', task.id, status='completed')

    db_client.set_ingest_status("resolving")
    db_client.set_ingest_status("in_review")
    db_client.set_ingest_status("preparing")
    db_client.set_ingest_status("uploading")

    ingest = db_client.start_finalizing()
    assert ingest.id == ingest_id
    assert ingest.status == "finalizing"


def test_fail(db_client, data):
    ingest_id = data.create("Ingest")
    db_client.start()

    ingest = db_client.fail()
    assert ingest.id == ingest_id
    assert ingest.status == "failed"


def test_batch_writer_push(db_client, data):
    ingest_id = data.create("Ingest")
    tid = data.create(
        "Task",
        status='pending',
        worker='worker',
        type='scan',
        ingest_id=ingest_id,
    )

    batch_writer = db_client.batch_writer(
        type_='update', model_name='Task', batch_size=1)
    batch_writer.push({'id': tid, 'status': 'running'})

    task = db_client.get('Task', tid)
    assert task.id == tid
    assert task.ingest_id == ingest_id
    assert task.status == 'running'


def test_batch_writer_flush(db_client, data):
    ingest_id = data.create("Ingest")
    tid = data.create(
        "Task",
        status='pending',
        worker='worker',
        type='scan',
        ingest_id=ingest_id,
    )

    batch_writer = db_client.batch_writer(
        type_='update', model_name='Task', batch_size=10)
    batch_writer.push({'id': tid, 'status': 'running'})

    task = db_client.get('Task', tid)
    assert task.id == tid
    assert task.ingest_id == ingest_id
    assert task.status == 'pending'

    batch_writer.flush()

    task = db_client.get('Task', tid)
    assert task.id == tid
    assert task.ingest_id == ingest_id
    assert task.status == 'running'


def test_batch_writer_flush_depends_on(db_client, data):
    ingest_id = data.create("Ingest")
    tid1 = data.create(
        "Task",
        status='pending',
        worker='worker',
        type='scan',
        ingest_id=ingest_id,
    )
    tid2 = data.create(
        "Task",
        status='pending',
        worker='worker',
        type='scan',
        ingest_id=ingest_id,
    )

    batch_writer1 = db_client.batch_writer(
        type_='update', model_name='Task', batch_size=10)
    batch_writer1.push({'id': tid1, 'status': 'running'})

    batch_writer2 = db_client.batch_writer(
        type_='update',
        model_name='Task',
        batch_size=10,
        depends_on=batch_writer1
    )
    batch_writer2.push({'id': tid2, 'status': 'running'})

    task = db_client.get('Task', tid1)
    assert task.status == 'pending'
    task = db_client.get('Task', tid2)
    assert task.status == 'pending'

    batch_writer2.flush()

    task = db_client.get('Task', tid1)
    assert task.status == 'running'
    task = db_client.get('Task', tid2)
    assert task.status == 'running'


def test_batch_writer_flush_depends_on_other_side(db_client, data):
    ingest_id = data.create("Ingest")
    tid1 = data.create(
        "Task",
        status='pending',
        worker='worker',
        type='scan',
        ingest_id=ingest_id,
    )
    tid2 = data.create(
        "Task",
        status='pending',
        worker='worker',
        type='scan',
        ingest_id=ingest_id,
    )

    batch_writer1 = db_client.batch_writer(
        type_='update', model_name='Task', batch_size=10)
    batch_writer1.push({'id': tid1, 'status': 'running'})

    batch_writer2 = db_client.batch_writer(
        type_='update',
        model_name='Task',
        batch_size=10,
        depends_on=batch_writer1
    )
    batch_writer2.push({'id': tid2, 'status': 'running'})

    task = db_client.get('Task', tid1)
    assert task.status == 'pending'
    task = db_client.get('Task', tid2)
    assert task.status == 'pending'

    batch_writer1.flush()

    task = db_client.get('Task', tid1)
    assert task.status == 'running'
    task = db_client.get('Task', tid2)
    assert task.status == 'pending'


    batch_writer2.flush()

    task = db_client.get('Task', tid1)
    assert task.status == 'running'
    task = db_client.get('Task', tid2)
    assert task.status == 'running'


def test_batch_writer_via_attribute(db_client, data):
    data.create("Ingest")

    batch_writer = db_client.batch_writer_update_task()
    assert batch_writer.type == 'update'
    assert batch_writer.model_name == 'Task'


def test_unknown_attribute(db_client):
    with pytest.raises(AttributeError):
        db_client.random_attr


def test_add_transaction(db_client, data):
    ingest_id = data.create("Ingest")
    d = db_client.sessionmaker()
    task = M.Task(type="scan", ingest_id=ingest_id)
    _task = db_transactions.add(d, task)
    assert _task.id is not None
    assert _task.ingest_id == ingest_id
    assert isinstance(_task, T.TaskOut)
    d.commit()
    d.close()


def test_get_transaction(db_client, data):
    ingest_id = data.create("Ingest")
    d = db_client.sessionmaker()
    ingest = db_transactions.get(d, M.Ingest, ingest_id)
    assert ingest.id == ingest_id
    assert isinstance(ingest, T.IngestOut)
    d.commit()
    d.close()


def test_get_all_transaction(db_client, data):
    ingest_id1 = data.create("Ingest")
    ingest_id2 = data.create("Ingest")
    d = db_client.sessionmaker()
    query = sqla.orm.Query(M.Ingest)
    ingests = db_transactions.get_all(d, query, T.IngestOut)
    assert len(ingests) == 2
    for i in ingests:
        assert i.id in [ingest_id1, ingest_id2]
        assert isinstance(i, T.IngestOut)
    d.commit()
    d.close()


def test_update_transaction(db_client, data):
    ingest_id = data.create("Ingest")
    d = db_client.sessionmaker()
    ingest = db_transactions.update(d, M.Ingest, ingest_id, status='failed')
    assert ingest.id == ingest_id
    assert isinstance(ingest, T.IngestOut)
    assert ingest.status == 'failed'
    d.commit()
    d.close()


def test_bulk_transaction(db_client, data):
    ingest_id = data.create("Ingest")
    d = db_client.sessionmaker()

    mappings = [
        {
            'status': 'pending',
            'worker': 'worker',
            'type': 'scan',
            'ingest_id': ingest_id
        },
        {
            'status': 'running',
            'worker': 'worker',
            'type': 'resolve',
            'ingest_id': ingest_id
        }
    ]

    update_mappings = [
        {
            'id': None,
            'status': 'failed',
        },
        {
            'id': None,
            'status': 'failed',
        }
    ]

    db_transactions.bulk(d, 'insert', M.Task, mappings)
    query = sqla.orm.Query(M.Task)
    tasks = db_transactions.get_all(d, query, T.TaskOut)
    assert len(tasks) == 2
    ids = []
    for i in range(len(tasks)):
        task = tasks[i]
        assert task.id is not None
        assert task.status in ['pending', 'running']
        update_mappings[i]['id'] = str(task.id)
        ids.append(str(task.id))

    db_transactions.bulk(d, 'update', M.Task, update_mappings)
    tasks = db_transactions.get_all(d, query, T.TaskOut)
    assert len(tasks) == 2
    for i in range(len(tasks)):
        task = tasks[i]
        assert str(task.id) in ids
        assert task.status == 'failed'
    d.commit()
    d.close()


def test_start_transaction(db_client, data):
    ingest_id = data.create("Ingest")
    assert len(list(db_client.get_all_task(
        M.Task.type == T.TaskType.scan))) == 0

    d = db_client.sessionmaker()
    ingest = db_transactions.start(d, ingest_id)
    d.commit()
    d.close()

    assert ingest.id == ingest_id
    assert isinstance(ingest, T.IngestOut)
    assert ingest.status == 'scanning'

    assert len(list(db_client.get_all_task(
        M.Task.type == T.TaskType.scan))) == 1


def test_review_transaction(db_client, data):
    ingest_id = data.create("Ingest")
    db_client.start()
    db_client.set_ingest_status("resolving")
    db_client.set_ingest_status("in_review")

    tasks = list(db_client.get_all('Task'))
    assert len(tasks) == 1

    d = db_client.sessionmaker()
    changes = [T.ReviewChange(path="path", skip=True)]
    db_transactions.review(d, ingest_id, changes)
    d.commit()

    # TODO check if the created task is a preparing type
    tasks = list(db_client.get_all('Task'))
    assert len(tasks) == 2

    query = sqla.orm.Query(M.Review)
    reviews = db_transactions.get_all(d, query, T.ReviewChange)
    assert len(reviews) == 1
    assert reviews[0].path == 'path'
    assert reviews[0].skip

    d.close()


def test_abort_transaction(db_client, data):
    ingest_id = data.create("Ingest")
    db_client.start()
    tasks = list(db_client.get_all('Task'))
    assert len(tasks) == 1
    for task in tasks:
        assert task.status == 'pending'

    ingest = db_client.ingest
    assert ingest.status == 'scanning'

    d = db_client.sessionmaker()
    ingest = db_transactions.abort(d, ingest_id)
    d.commit()

    assert ingest.status == 'aborted'

    tasks = list(db_client.get_all('Task'))
    assert len(tasks) == 1
    for task in tasks:
        assert task.status == 'canceled'

    ingest = db_transactions.abort(d, ingest_id)
    d.commit()
    assert ingest.status == 'aborted'
    d.close()


def test_next_task_transaction(db_client, data):
    ingest_id = data.create("Ingest")
    tid1 = data.create(
        "Task",
        status='running',
        type='scan',
        ingest_id=ingest_id
    )
    tid2 = data.create(
        "Task",
        status='pending',
        type='scan',
        ingest_id=ingest_id,
    )

    tasks = list(db_client.get_all('Task'))
    assert len(tasks) == 2
    for task in tasks:
        assert task.id in [tid1, tid2]

    d = db_client.sessionmaker()
    next_task = db_transactions.next_task(d, 'worker')
    assert next_task.id == tid2
    assert next_task.status == 'running'
    assert next_task.worker == 'worker'

    next_task = db_transactions.next_task(d, 'worker')
    assert next_task is None
    d.commit()
    d.close()


def test_get_progress_transaction(db_client, data):
    ingest_id = data.create("Ingest")
    data.create(
        "Task",
        status='completed',
        worker='worker',
        type='scan',
        ingest_id=ingest_id
    )

    d = db_client.sessionmaker()
    progress = db_transactions.get_progress(d, ingest_id)
    assert progress.scans.total == 1
    assert progress.scans.completed == 1
    assert progress.items.total == 0
    assert progress.files.total == 0
    assert progress.bytes.total == 0
    d.commit()
    d.close()


def test_get_summary_transaction(db_client, data):
    ingest_id = data.create("Ingest")
    levels = [0, 1, 2, 3, 4]
    for level in levels:
        cnt = level + 1
        for _ in range(cnt):
            data.create(
                "Container",
                ingest_id=ingest_id,
                level=level,
                src_context={}
            )

    d = db_client.sessionmaker()
    summary = db_transactions.get_summary(d, ingest_id)
    assert summary.groups == 1
    assert summary.projects == 2
    assert summary.subjects == 3
    assert summary.sessions == 4
    assert summary.acquisitions == 5
    d.commit()
    d.close()


def test_get_report_transaction(db_client, data):
    ingest_id = data.create("Ingest")
    task_id = data.create(
        "Task",
        status="failed",
        worker="worker",
        type="scan",
        ingest_id=ingest_id,
    )
    data.create(
        "Error",
        task_id=task_id,
        code="FFFF",
        message="foo bar error"
    )
    db_client.start()

    d = db_client.sessionmaker()
    report = db_transactions.get_report(d, ingest_id)
    d.commit()
    assert report.status == "scanning"
    # TODO
    assert report.elapsed == {}
    assert len(report.errors) == 1
    assert report.errors[0].code == "FFFF"
    assert report.errors[0].message == "foo bar error"
    d.close()


def test_start_singleton_transaction(db_client, data):
    ingest_id = data.create("Ingest")

    d = db_client.sessionmaker()
    ingest = db_transactions.update(
        d, M.Ingest, ingest_id, status='uploading')
    d.commit()
    tasks = list(db_client.get_all('Task'))
    assert len(tasks) == 0

    ingest = db_transactions.start_singleton(d, ingest_id, 'finalize')
    d.commit()
    assert ingest.status == 'finalizing'
    tasks = list(db_client.get_all('Task'))
    assert len(tasks) == 1
    assert tasks[0].type == 'finalize'
    d.close()


def test_has_unfinished_tasks_transaction(db_client, data):
    ingest_id = data.create("Ingest")
    tasks = list(db_client.get_all('Task'))
    assert len(tasks) == 0

    d = db_client.sessionmaker()
    assert not db_transactions.has_unfinished_tasks(d, ingest_id)

    tid = data.create(
        "Task",
        status='pending',
        type='scan',
        ingest_id=ingest_id
    )

    tasks = list(db_client.get_all('Task'))
    assert len(tasks) == 1
    assert tasks[0].status == 'pending'
    assert db_transactions.has_unfinished_tasks(d, ingest_id)

    db_client.update('Task', tid, status='running')
    tasks = list(db_client.get_all('Task'))
    assert len(tasks) == 1
    assert tasks[0].status == 'running'
    assert db_transactions.has_unfinished_tasks(d, ingest_id)

    db_client.update('Task', tid, status='failed')
    tasks = list(db_client.get_all('Task'))
    assert len(tasks) == 1
    assert tasks[0].status == 'failed'
    assert not db_transactions.has_unfinished_tasks(d, ingest_id)
    d.commit()
    d.close()


def test_resolve_subject_transaction(db_client, data):
    def get_all_subjects(d):
        query = sqla.orm.Query(M.Subject)
        return db_transactions.get_all(d, query, T.SubjectOut)

    ingest_id = data.create(
        "Ingest",
        strategy_config={},
        config={
            "src_fs": "/tmp",
            "subject_config": {
                "code_serial": 0,
                "code_format": "code-{SubjectCode}",
                "map_keys": []
            }
        }
    )

    d = db_client.sessionmaker()

    subjects = get_all_subjects(d)
    assert len(subjects) == 0

    subject = db_transactions.resolve_subject(d, ingest_id, ['code_a'])
    assert subject == 'code-1'
    subjects = subjects = get_all_subjects(d)
    assert len(subjects) == 1

    subject = db_transactions.resolve_subject(d, ingest_id, ['code_a'])
    assert subject == 'code-1'
    subjects = subjects = get_all_subjects(d)
    assert len(subjects) == 1
    d.commit()
    d.close()


def test_set_ingest_status_transaction(db_client, data):
    ingest_id = data.create("Ingest")

    ingest = db_client.ingest
    assert ingest.status == 'created'

    d = db_client.sessionmaker()
    ingest = db_transactions.set_ingest_status(d, ingest_id, 'scanning')
    assert ingest.status == 'scanning'
    d.commit()
    d.close()


def test_fail_ingest_transaction(db_client, data):
    ingest_id = data.create("Ingest")

    d = db_client.sessionmaker()
    ingest = db_transactions.set_ingest_status(d, ingest_id, 'scanning')
    d.commit()

    assert ingest.status == 'scanning'

    ingest = db_transactions.fail_ingest(d, ingest_id)
    d.commit()
    assert ingest.status == 'failed'
    d.close()


def test_load_subject_csv_transaction(db_client, data):
    ingest_id = data.create(
        "Ingest",
        strategy_config={},
        config={
            "src_fs": "/tmp",
            "subject_config": {
                "code_serial": 1,
                "code_format": "code-{SubjectCode}",
                "map_keys": []
            }
        }
    )
    f = io.BytesIO(b"code-{SubjectCode}\ncode-1,code_a\ncode-2,code_b\n")
    d = db_client.sessionmaker()
    db_transactions.load_subject_csv(d, ingest_id, f)
    d.commit()
    subjects = list(db_client.subjects)
    assert subjects == ['code-{SubjectCode}\n',
                        'code-1,code_a\n', 'code-2,code_b\n']
    d.close()


def test_get_ingest_helper(db_client, data):
    ingest_id = data.create("Ingest")

    d = db_client.sessionmaker()
    ingest = db_transactions._get_ingest(d, ingest_id)
    assert ingest.id == ingest_id

    # TODO for update test
    ingest = db_transactions._get_ingest(d, ingest_id, True)
    d.commit()
    assert ingest.id == ingest_id

    d.close()


def test_for_update_helper():
    # TODO
    pass


def test_cancel_pending_tasks_helper(db_client, data):
    ingest_id = data.create("Ingest")
    data.create(
        "Task",
        status='pending',
        type='scan',
        ingest_id=ingest_id
    )

    tasks = list(db_client.get_all('Task'))
    assert len(tasks) == 1
    assert tasks[0].status == 'pending'
    d = db_client.sessionmaker()
    db_transactions._cancel_pending_tasks(d, ingest_id)
    d.commit()

    tasks = list(db_client.get_all('Task'))
    assert len(tasks) == 1
    assert tasks[0].status == 'canceled'

    d.close()


def test_cancel_pending_tasks_helper_running(db_client, data):
    ingest_id = data.create("Ingest")
    data.create(
        "Task",
        status='running',
        type='scan',
        ingest_id=ingest_id
    )

    tasks = list(db_client.get_all('Task'))
    assert len(tasks) == 1
    assert tasks[0].status == 'running'
    d = db_client.sessionmaker()
    db_transactions._cancel_pending_tasks(d, ingest_id)
    d.commit()

    tasks = list(db_client.get_all('Task'))
    assert len(tasks) == 1
    assert tasks[0].status == 'running'
    d.close()


def test_csv_field_str_helper():
    assert ingest_db_client._csv_field_str(None) == ""
    assert ingest_db_client._csv_field_str("str") == "str"
    assert ingest_db_client._csv_field_str("x,y,z") == '"x,y,z"'


def test_get_paginate_order_by_col_helper():
    assert str(ingest_db_client._get_paginate_order_by_col(
        M.Review)) == 'Review.id'
    assert str(ingest_db_client._get_paginate_order_by_col(
        M.Container)) == 'Container.path'


def test_iter_query(db_client, data):
    ingest_id = data.create("Ingest")
    d = db_client.sessionmaker()

    mappings = []
    for i in range(20):
        mappings.append(
            {
                'level': 1,
                'src_context': {},
                'ingest_id': ingest_id,
                'path': 'path' + str(i)
            }
        )
    db_transactions.bulk(d, 'insert', M.Container, mappings)
    d.commit()

    model_cls = M.Container
    order_by = ingest_db_client._get_paginate_order_by_col(model_cls)
    query = sqla.orm.Query(model_cls).filter(model_cls.ingest_id == ingest_id)

    ids = []
    for t in db_client._iter_query(query, [order_by], model_cls.schema_cls(), 5):
        if str(t.id) not in ids:
            ids.append(str(t.id))

    assert len(ids) == len(mappings)
    d.close()


def test_delete_ingest_status_raise(db_client, data):
    ingest_id = data.create("Ingest")
    # un-bind
    db_client._ingest_id = None

    with pytest.raises(IngestIsNotDeletable):
        db_client.delete_ingest(ingest_id)


def test_delete_ingest_running_tasks_raise(db_client, data):
    ingest_id = data.create("Ingest")
    data.create(
        "Task",
        status='running',
        worker='worker',
        type='scan',
        ingest_id=ingest_id,
    )

    d = db_client.sessionmaker()
    db_transactions.update(d, M.Ingest, ingest_id, status='failed')
    d.commit()
    d.close_all()

    with pytest.raises(IngestIsNotDeletable):
        db_client.delete_ingest(ingest_id)


def test_delete_ingest_simple(db_client, data, ingest_subjects, ingest_deid_logs, ingest_reviews):
    """Delete Subject, DeidLog, Review"""
    ingest_id1 = data.create("Ingest")
    ingest_id2 = data.create("Ingest")

    ingest_subjects(ingest_id1, 3)
    ingest_subjects(ingest_id2, 3)

    ingest_deid_logs(ingest_id1, 3)
    ingest_deid_logs(ingest_id2, 3)

    ingest_reviews(ingest_id1, 3)
    ingest_reviews(ingest_id2, 3)

    db_client.abort()
    d = db_client.sessionmaker()

    assert d.query(M.Subject.id).count() == 6
    assert d.query(M.DeidLog.id).count() == 6
    assert d.query(M.Review.id).count() == 6

    db_client.delete_ingest(ingest_id2)

    subjects = d.query(M.Subject)
    assert subjects.count() == 3
    for subject in subjects.all():
        assert subject.ingest_id == ingest_id1

    deid_logs = d.query(M.DeidLog)
    assert deid_logs.count() == 3
    for log in deid_logs.all():
        assert log.ingest_id == ingest_id1

    reviews = d.query(M.Review)
    assert reviews.count() == 3
    for review in reviews.all():
        assert review.ingest_id == ingest_id1

    ingests = d.query(M.Ingest)
    assert ingests.count() == 1
    assert ingests.all()[0].id == ingest_id1
    d.close_all()


def test_delete_ingest_containers(db_client, data, ingest_containers):
    ingest_id1 = data.create("Ingest")
    ingest_id2 = data.create("Ingest")

    ingest_containers(ingest_id1)
    ingest_containers(ingest_id2)

    db_client.abort()
    d = db_client.sessionmaker()

    assert d.query(M.Container.id).count() == 10
    containers = d.query(M.Container)

    db_client.delete_ingest(ingest_id2)

    containers = d.query(M.Container)
    assert containers.count() == 5
    for container in containers.all():
        assert container.ingest_id == ingest_id1
    d.close_all()


def test_delete_ingest_full(db_client, data, ingest_subjects, ingest_deid_logs, ingest_reviews, ingest_containers):
    def add_tasks(ingest_id):
        for _ in range(3):
            data.create(
                "Task",
                status='pending',
                type='scan',
                ingest_id=ingest_id
            )

    def add_items(ingest_id):
        container_id = data.create(
            "Container",
            ingest_id=ingest_id,
            level=0,
            src_context={}
        )
        for _ in range(3):
            data.create(
                'Item',
                dir="dir",
                type="file",
                files=[],
                files_cnt=10,
                bytes_sum=1234,
                filename='testfile',
                container_id=container_id,
                ingest_id=ingest_id
            )

    ingest_id1 = data.create("Ingest")
    ingest_id2 = data.create("Ingest")

    ingest_subjects(ingest_id1, 3)
    ingest_subjects(ingest_id2, 3)

    ingest_deid_logs(ingest_id1, 3)
    ingest_deid_logs(ingest_id2, 3)

    ingest_reviews(ingest_id1, 3)
    ingest_reviews(ingest_id2, 3)

    ingest_containers(ingest_id1)
    ingest_containers(ingest_id2)

    add_tasks(ingest_id1)
    add_tasks(ingest_id2)

    add_items(ingest_id1)
    add_items(ingest_id2)

    db_client.abort()
    d = db_client.sessionmaker()

    assert d.query(M.Subject.id).count() == 6
    assert d.query(M.DeidLog.id).count() == 6
    assert d.query(M.Review.id).count() == 6
    assert d.query(M.Container.id).count() == 12 # 10 + 2 for tasks
    assert d.query(M.Task.id).count() == 6
    assert d.query(M.Item.id).count() == 6

    db_client.delete_ingest(ingest_id2)

    subjects = d.query(M.Subject)
    assert subjects.count() == 3

    deid_logs = d.query(M.DeidLog)
    assert deid_logs.count() == 3

    reviews = d.query(M.Review)
    assert reviews.count() == 3

    containers = d.query(M.Container)
    assert containers.count() == 6

    tasks = d.query(M.Task)
    assert tasks.count() == 3
    for task in tasks.all():
        assert task.ingest_id == ingest_id1

    items = d.query(M.DeidLog)
    assert items.count() == 3
    for item in items.all():
        assert item.ingest_id == ingest_id1

    ingests = d.query(M.Ingest)
    assert ingests.count() == 1
    assert ingests.all()[0].id == ingest_id1

    d.close_all()


# TODO unify and move engine/session creation to code
# TODO use the same fixtures in ingest api and cli

def test_get_items_sorted_by_dst_path(db_client, data):
    ingest_id = data.create("Ingest")
    db_client.bind(ingest_id)
    container_id_1 = data.create(
        "Container",
        id=uuid4(),
        path="group/project_a",
        level=1,
        src_context={"group": {"_id": "group"}, "project": {"label": "project_a"}}
    )
    container_id_2 = data.create(
        "Container",
        id=uuid4(),
        path="group/project_b",
        level=1,
        src_context={"group": {"_id": "group"}, "project": {"label": "project_a"}}
    )
    item_id_1 = data.create(
        "Item",
        id=UUID("00000000-0000-0000-0000-000000000003"),
        files=["a.txt"],
        files_cnt=1,
        bytes_sum=1,
        filename="a.txt",
        container_id=container_id_2,
        ingest_id=ingest_id,
    )
    item_id_2 = data.create(
        "Item",
        id=UUID("00000000-0000-0000-0000-000000000002"),
        files=["a.txt"],
        files_cnt=1,
        bytes_sum=1,
        filename="a.txt",
        container_id=container_id_2,
        ingest_id=ingest_id,
    )
    item_id_3 = data.create(
        "Item",
        id=UUID("00000000-0000-0000-0000-000000000001"),
        files=["b.txt"],
        files_cnt=1,
        bytes_sum=1,
        filename="b.txt",
        container_id=container_id_1,
        ingest_id=ingest_id,
    )
    items = list(db_client.get_items_sorted_by_dst_path())
    assert items[0].id == item_id_3
    assert items[0].container_path == "group/project_a"
    assert items[0].filename == "b.txt"
    assert items[1].id == item_id_2
    assert items[1].container_path == "group/project_b"
    assert items[1].filename == "a.txt"
    assert items[2].id == item_id_1
    assert items[2].container_path == "group/project_b"
    assert items[2].filename == "a.txt"


def test_count_all(db_client, data):
    ingest_id = data.create("Ingest")
    db_client.bind(ingest_id)
    for i in range(11):
        data.create("Item")

    assert db_client.count_all_item() == 11


def test_find_one_ingest_dependent(db_client, data):
    ingest_id = data.create("Ingest")
    ingest_id_2 = data.create("Ingest")
    container_id = data.create(
        "Container",
        level=0,
        path="group",
        src_context={"group": {"_id": "group"}},
        ingest_id=ingest_id
    )
    container_id_2 = data.create(
        "Container",
        level=0,
        path="group",
        src_context={"group": {"_id": "group"}},
        ingest_id=ingest_id_2
    )
    db_client.bind(ingest_id)
    container = db_client.find_one_container(M.Container.path == "group")
    assert container_id == container.id


def test_find_one_multiple_results(db_client, data):
    ingest_id = data.create("Ingest")
    data.create(
        "Container",
        level=0,
        path="group",
        src_context={"group": {"_id": "group"}},
    )
    data.create(
        "Container",
        level=0,
        path="group",
        src_context={"group": {"_id": "group"}},
    )
    db_client.bind(ingest_id)
    with pytest.raises(MultipleResultsFound):
        db_client.find_one_container(M.Container.path == "group")


def test_find_one_no_result(db_client, data):
    ingest_id = data.create("Ingest")
    db_client.bind(ingest_id)
    with pytest.raises(NoResultFound):
        db_client.find_one_container(M.Container.path == "group")


# fixtures for ingest_delete
@pytest.fixture(scope="function")
def ingest_subjects(data):
    def add_ingest_subjects(ingest_id, count):
        for i in range(count):
            data.create_with_model(
                M.Subject(
                    ingest_id=ingest_id,
                    code=f"code-{i}",
                    map_values=[f"code-{i}"]
                )
            )
    return add_ingest_subjects


@pytest.fixture(scope="function")
def ingest_deid_logs(data):
    def add_ingest_deid_logs(ingest_id, count):
        for _ in range(count):
            data.create_with_model(
                M.DeidLog(
                    ingest_id=ingest_id,
                    src_path="src_path",
                    tags_before={},
                    tags_after={}
                )
            )
    return add_ingest_deid_logs


@pytest.fixture(scope="function")
def ingest_reviews(data):
    def add_ingest_reviews(ingest_id, count):
        for _ in range(count):
            data.create_with_model(
                M.Review(
                    ingest_id=ingest_id,
                    path="path"
                )
            )
    return add_ingest_reviews


@pytest.fixture(scope="function")
def ingest_containers(data):
    def add_ingest_containers(ingest_id):
        container = data.create_with_model(
            M.Container(
                ingest_id=ingest_id,
                level=T.ContainerLevel.group,
                src_context={}
            ),
            keep_session_open=True
        )

        container = data.create_with_model(
            M.Container(
                ingest_id=ingest_id,
                parent_id=container.id,
                level=T.ContainerLevel.project,
                src_context={}
            ),
            keep_session_open=True
        )

        container = data.create_with_model(
            M.Container(
                ingest_id=ingest_id,
                parent_id=container.id,
                level=T.ContainerLevel.subject,
                src_context={}
            ),
            keep_session_open=True
        )

        container = data.create_with_model(
            M.Container(
                ingest_id=ingest_id,
                parent_id=container.id,
                level=T.ContainerLevel.session,
                src_context={}
            ),
            keep_session_open=True
        )

        container = data.create_with_model(
            M.Container(
                ingest_id=ingest_id,
                parent_id=container.id,
                level=T.ContainerLevel.acquisition,
                src_context={}
            ),
            keep_session_open=True
        )

        data.close_session()

    return add_ingest_containers

# TODO use the same fixtures in ingest api and cli

@pytest.fixture(scope="function")
def db_client(request):
    url = request.param
    db = ingest_db_client.DBClient(request.param)

    if db.engine.name != "sqlite":
        M.Base.metadata.create_all(db.engine)

    yield db

    if db.engine.name == "postgresql":
        # delete all tables to start with a fresh db in the next test
        connection = db.engine.raw_connection()
        cursor = connection.cursor()
        cursor.execute("SET statement_timeout = '5s';")
        cursor.execute('DROP SCHEMA public CASCADE;')
        cursor.execute('CREATE SCHEMA public;')
        cursor.execute('GRANT ALL ON SCHEMA public TO public;')
        connection.commit()
        connection.close()

    elif db.engine.name == "sqlite" and url.find(':memory:') == -1:
        # delete the db file
        file_path = url[len('sqlite:///'):]
        os.remove(file_path)


@pytest.fixture(scope="function")
def defaults(attr_dict):
    """Return default kwargs for creating DB models with"""
    return attr_dict(dict(
        Ingest=dict(
            api_key="flywheel.test:admin-apikey",
            fw_host="flywheel.test",
            fw_user="admin@flywheel.test",
            config={
                "src_fs": "/tmp"
            },
            strategy_config={},
        ),
        Task={},
        Container={},
        Item=dict(
            type="file",
            dir="/dir",
            files=["foo.txt"],
            filename="foo.txt",
            existing=False,
            files_cnt=1,
            bytes_sum=1,
        ),
        Error={},
        Review={},
        Subject={},
        DeidLog={},
    ))


@pytest.fixture(scope="function")
def data(db_client, defaults):
    """Return Data instance for simple DB record creation"""
    return Data(db_client, defaults)

class Data:
    """DB record creation helper"""

    def __init__(self, db, defaults):
        self.db = db
        self.defaults = defaults
        self.session = None

    def create(self, cls_name, **kwargs):
        cls = getattr(M, cls_name)
        cls_defaults = self.defaults.get(cls_name, {})
        for key, value in cls_defaults.items():
            kwargs.setdefault(key, value)
        if cls_name == "Container" and isinstance(kwargs.get("level"), str):
            kwargs["level"] = getattr(T.ContainerLevel, kwargs["level"])
        record = cls(**kwargs)
        result = self.db.call_db(db_transactions.add, record)
        if cls_name == "Ingest":
            self.db.bind(result.id)
            ref_cls_names = [
                name for name in self.defaults if name != "Ingest"]
            for ref_cls_name in ref_cls_names:
                self.defaults[ref_cls_name]["ingest_id"] = result.id
        elif cls_name == "Container":
            self.defaults["Container"]["parent_id"] = result.id
            self.defaults["Item"]["container_id"] = result.id

        if hasattr(result, 'id'):
            return result.id
        return None

    def create_with_model(self, model, keep_session_open=False):
        if not keep_session_open:
            session = self.db.sessionmaker()
        else:
            if not self.session:
                self.session = self.db.sessionmaker()
            session = self.session

        session.add(model)
        session.commit()

        if not keep_session_open:
            session.close_all()

        return model

    def close_session(self):
        if self.session:
            self.session.close_all()
