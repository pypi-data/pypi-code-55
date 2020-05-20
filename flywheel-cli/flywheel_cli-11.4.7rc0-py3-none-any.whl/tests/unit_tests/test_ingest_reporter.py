import copy
import datetime
import io
from unittest import mock
from uuid import uuid4

import pytest

import flywheel_cli.ingest.reporter as reporter_
from flywheel_cli.ingest import config
from flywheel_cli.ingest import schemas as T


@pytest.fixture(scope="function")
def reporter():
    client = mock.Mock()
    client.ingest = T.IngestOut(
        id=uuid4(),
        label="label",
        fw_host="host",
        fw_user="user",
        api_key="api_key",
        config=config.IngestConfig(src_fs="/tmp"),
        strategy_config=config.FolderConfig(),
        status="created",
        history=[],
        created=datetime.datetime.now()
    )

    client.report = T.Report(
        status="created",
        elapsed=[],
        errors=[]
    )

    client.progress = T.Progress()
    client.summary = T.Summary()

    cfg = config.ReporterConfig()

    rep = reporter_.Reporter(client, cfg)
    rep._fh = io.StringIO()

    return rep

def test_run_ok(mocker, reporter):
    print_final_report_mock = mocker.patch.object(reporter, "print_final_report")
    save_reports_mock = mocker.patch.object(reporter, "save_reports")
    time_mock = mocker.patch("flywheel_cli.ingest.reporter.time")
    sys_mock = mocker.patch("flywheel_cli.ingest.reporter.sys.exit")
    follow_scanning_mock = mocker.patch.object(reporter, "follow_scanning_status")

    ingest = T.IngestOut(
        id=uuid4(),
        label="label",
        fw_host="host",
        fw_user="user",
        api_key="api_key",
        config=config.IngestConfig(src_fs="/tmp"),
        strategy_config=config.FolderConfig(),
        status="created",
        history=[("created", 1)],
        created=datetime.datetime.now()
    )
    ingest_scanning = copy.deepcopy(ingest)
    ingest_scanning.status = T.IngestStatus.scanning
    ingest_scanning.history.append((T.IngestStatus.scanning, 2))
    ingest_finished = copy.deepcopy(ingest_scanning)
    ingest_finished.status = T.IngestStatus.finished
    ingest_finished.history.append((T.IngestStatus.finished, 3))

    report = T.Report(
        status="created",
        elapsed=[],
        errors=[]
    )

    client = mock.Mock()
    type(client).ingest = mock.PropertyMock(side_effect=[
        ingest,
        ingest_scanning,
        ingest_scanning,
        ingest_finished,
        ingest_finished,
    ])
    type(client).report = mock.PropertyMock(return_value=report)
    reporter.client = client

    reporter.run()

    sys_mock.assert_called_once_with(0)
    follow_scanning_mock.assert_called_once()

    print_final_report_mock.assert_called_once()
    save_reports_mock.assert_called_once()

    time_mock.sleep.assert_called_once_with(
        reporter.config.refresh_interval
    )

def test_run_failed(mocker, reporter):
    mocker.patch("flywheel_cli.ingest.reporter.Reporter.print_final_report")
    mocker.patch("flywheel_cli.ingest.reporter.Reporter.save_reports")
    mocker.patch("flywheel_cli.ingest.reporter.Reporter.print_status_history")
    sys_mock = mocker.patch("flywheel_cli.ingest.reporter.sys.exit")

    reporter.client.ingest = T.IngestOut(
        id=uuid4(),
        label="label",
        fw_host="host",
        fw_user="user",
        api_key="api_key",
        config=config.IngestConfig(src_fs="/tmp"),
        strategy_config=config.FolderConfig(),
        status="failed",
        history=[],
        created=datetime.datetime.now()
    )

    reporter.run()

    sys_mock.assert_called_once_with(1)

def test_run_error(mocker, reporter):
    mocker.patch("flywheel_cli.ingest.reporter.Reporter.print_final_report")
    mocker.patch("flywheel_cli.ingest.reporter.Reporter.save_reports")
    mocker.patch("flywheel_cli.ingest.reporter.Reporter.print_status_history")
    sys_mock = mocker.patch("flywheel_cli.ingest.reporter.sys.exit")

    reporter.client.ingest = T.IngestOut(
        id=uuid4(),
        label="label",
        fw_host="host",
        fw_user="user",
        api_key="api_key",
        config=config.IngestConfig(src_fs="/tmp"),
        strategy_config=config.FolderConfig(),
        status="finished",
        history=[],
        created=datetime.datetime.now()
    )

    reporter.client.report = T.Report(
        status="created",
        elapsed=[],
        errors=[T.TaskError(
            task=uuid4(),
            type="scan",
            message="message"
        )]
    )

    reporter.run()

    sys_mock.assert_called_once_with(1)

def test_print_status_history_no_last(mocker, reporter):
    follow_scanning_status_mock = mocker.patch("flywheel_cli.ingest.reporter.Reporter.follow_scanning_status")
    follow_resolving_status_mock = mocker.patch("flywheel_cli.ingest.reporter.Reporter.follow_resolving_status")

    ingest = T.IngestOut(
        id=uuid4(),
        label="label",
        fw_host="host",
        fw_user="user",
        api_key="api_key",
        config=config.IngestConfig(src_fs="/tmp"),
        strategy_config=config.FolderConfig(),
        status="created",
        created=datetime.datetime.now(),
        history=[
            ["created", 1],
            ["scanning", 2],
            ["resolving", 3],
        ]
    )

    reporter.print_status_history(ingest.history)
    assert reporter.last_reported_status_idx == 2

    follow_scanning_status_mock.assert_called_once()
    follow_resolving_status_mock.assert_called_once()

def test_print_status_history_with_last(mocker, reporter):
    follow_scanning_status_mock = mocker.patch("flywheel_cli.ingest.reporter.Reporter.follow_scanning_status")
    follow_resolving_status_mock = mocker.patch("flywheel_cli.ingest.reporter.Reporter.follow_resolving_status")

    ingest = T.IngestOut(
        id=uuid4(),
        label="label",
        fw_host="host",
        fw_user="user",
        api_key="api_key",
        config=config.IngestConfig(src_fs="/tmp"),
        strategy_config=config.FolderConfig(),
        status="created",
        created=datetime.datetime.now(),
        history=[
            ["created", 1],
            ["scanning", 2],
            ["resolving", 3],
            ["finished", 4],
        ]
    )
    reporter.last_reported_status_idx = 2

    reporter.print_status_history(ingest.history)
    assert reporter.last_reported_status_idx == 3

    follow_scanning_status_mock.assert_not_called()
    follow_resolving_status_mock.assert_not_called()

def test_follow_scanning_status(mocker, reporter):
    time_mock = mocker.patch("flywheel_cli.ingest.reporter.time")
    print_scan_progress_mock = mocker.patch("flywheel_cli.ingest.reporter.Reporter.print_scan_progress")
    client = AlteringAttrDict({
        "ingest": [
            T.IngestOut(
                id=uuid4(),
                label="label",
                fw_host="host",
                fw_user="user",
                api_key="api_key",
                config=config.IngestConfig(src_fs="/tmp"),
                strategy_config=config.FolderConfig(),
                status="scanning",
                history=[],
                created=datetime.datetime.now()
            ),
            T.IngestOut(
                id=uuid4(),
                label="label",
                fw_host="host",
                fw_user="user",
                api_key="api_key",
                config=config.IngestConfig(src_fs="/tmp"),
                strategy_config=config.FolderConfig(),
                status="resolving",
                history=[],
                created=datetime.datetime.now()
            )
        ]
    })
    reporter.client = client

    reporter.follow_scanning_status()

    time_mock.sleep.assert_called_once_with(reporter.config.refresh_interval)

    assert len(print_scan_progress_mock.mock_calls) == 2
    # new line
    assert_print(
        reporter,
        [""]
    )

def test_print_scan_progress(reporter):
    reporter.client.progress = T.Progress(
        bytes=T.StatusCount(
            total=123456
        ),
        scans=T.StatusCount(
            finished=10,
            total=20
        ),
        files=T.StatusCount(
            total=123
        )
    )

    reporter.print_scan_progress()

    assert_print(
        reporter,
        [{"msg":"10 / 20, 123 files, 120.6 KB", "replace":True}]
    )

def test_follow_resolving_status(mocker, reporter):
    spinner_mock = mocker.patch("flywheel_cli.ingest.reporter.TerminalSpinnerThread")
    time_mock = mocker.patch("flywheel_cli.ingest.reporter.time")

    client = AlteringAttrDict({
        "ingest": [
            T.IngestOut(
                id=uuid4(),
                label="label",
                fw_host="host",
                fw_user="user",
                api_key="api_key",
                config=config.IngestConfig(src_fs="/tmp"),
                strategy_config=config.FolderConfig(),
                status="resolving",
                history=[],
                created=datetime.datetime.now()
            ),
            T.IngestOut(
                id=uuid4(),
                label="label",
                fw_host="host",
                fw_user="user",
                api_key="api_key",
                config=config.IngestConfig(src_fs="/tmp"),
                strategy_config=config.FolderConfig(),
                status="uploading",
                history=[],
                created=datetime.datetime.now()
            )
        ]
    })

    reporter.client = client

    reporter.follow_resolving_status()

    # loop
    time_mock.sleep.assert_called_once_with(reporter.config.refresh_interval)

    spinner_mock.assert_called_once_with("Resolving containers", fh=reporter._fh)
    spinner_mock.return_value.start.assert_called_once()
    spinner_mock.return_value.stop.assert_called_once_with("Resolved containers")


def test_follow_detecting_duplicates_status(mocker, reporter):
    time_mock = mocker.patch("flywheel_cli.ingest.reporter.time")
    ingest = T.IngestOut(
        id=uuid4(),
        label="label",
        fw_host="host",
        fw_user="user",
        api_key="api_key",
        config=config.IngestConfig(src_fs="/tmp"),
        strategy_config=config.FolderConfig(),
        status="detecting_duplicates",
        history=[],
        created=datetime.datetime.now()
    )
    ingest_finished = copy.deepcopy(ingest)
    ingest_finished.status = T.IngestStatus.finished
    progress = T.Progress()
    progress.stages.detecting_duplicates.completed = 51
    progress.stages.detecting_duplicates.total = 100
    progress_2 = copy.deepcopy(progress)
    progress_2.stages.detecting_duplicates.completed += 1
    progress_3 = copy.deepcopy(progress_2)
    progress_3.stages.detecting_duplicates.completed += 1
    client = mock.Mock()
    type(client).ingest = mock.PropertyMock(side_effect=[
        ingest,
        ingest,
        ingest_finished,
    ])
    type(client).progress = mock.PropertyMock(side_effect=[
        progress,
        progress_2,
        progress_3,
    ])
    reporter.client = client

    reporter.follow_detecting_duplicates_status()

    assert_print(
        reporter,
        [
            {"msg": "51.0%", "replace": True},
            {"msg": "52.0%", "replace": True},
            {"msg": "53.0%", "replace": True}, # final print
            "",
        ],
    )


def test_follow_in_review_status_verbose(mocker, reporter):
    crayons_mock = mocker.patch("flywheel_cli.ingest.reporter.crayons.blue", side_effect=dummy_style)

    container = T.ContainerOut(
        id=uuid4(),
        level=0,
        src_context={"src1": "src1", "label": "label1"},
        dst_context={"dst": "ctx"},
        ingest_id=uuid4(),
        files_cnt=1,
        bytes_sum=2
    )
    reporter.client.tree = [container]

    reporter.client.summary = T.Summary(groups=5)
    reporter.config.assume_yes = True
    reporter.config.verbose = True
    reporter.client.ingest.status = T.IngestStatus("in_review")

    reporter.follow_in_review_status()

    assert_print(
        reporter,
        [
            "Hierarchy sample:\n",
            "`- NO_LABEL (2 bytes / 1 file) (using)",
            "Summary:",
            "  Groups: 5",
            "  Projects: 0",
            "  Subjects: 0",
            "  Sessions: 0",
            "  Acquisitions: 0",
            "  Files: 0",
            "  Packfiles: 0",
        ]
    )

def test_follow_in_review_status_not_verbose(mocker, reporter):
    container_mock = mocker.patch("flywheel_cli.ingest.reporter.ContainerTree")
    reporter.client.summary = T.Summary(groups=5, errors=[{
        "code": "TT01",
        "message": "Test error",
        "count": 2,
    }])
    reporter.config.assume_yes = True
    reporter.client.ingest.status = T.IngestStatus("in_review")

    reporter.follow_in_review_status()

    container_mock.assert_not_called()
    assert_print(
        reporter,
        [
            "Summary:",
            "  Groups: 5",
            "  Projects: 0",
            "  Subjects: 0",
            "  Sessions: 0",
            "  Acquisitions: 0",
            "  Files: 0",
            "  Packfiles: 0",
            "",
            "Errors summary:",
            "  Test error (TT01): 2"
        ]
    )

    reporter.client.review.assert_called_once()
    reporter.client.abort.assert_not_called()

def test_follow_in_review_status_assume_yes(reporter):
    reporter.config.assume_yes = True
    reporter.client.ingest.status = T.IngestStatus("in_review")

    reporter.follow_in_review_status()

    reporter.client.review.assert_called_once()
    reporter.client.abort.assert_not_called()

def test_follow_in_review_status_no_assume_review(mocker, reporter):
    prompt_mock = mocker.patch("flywheel_cli.ingest.reporter.util.confirmation_prompt", return_value=True)
    reporter.config.assume_yes = False
    reporter.client.ingest.status = T.IngestStatus("in_review")

    reporter.follow_in_review_status()

    reporter.client.review.assert_called_once()
    reporter.client.abort.assert_not_called()
    prompt_mock.assert_called_once_with("Confirm upload?")

def test_follow_in_review_status_no_assume_abort(mocker, reporter):
    prompt_mock = mocker.patch("flywheel_cli.ingest.reporter.util.confirmation_prompt", return_value=False)
    reporter.config.assume_yes = False
    reporter.client.ingest.status = T.IngestStatus("in_review")

    reporter.follow_in_review_status()

    reporter.client.review.assert_not_called()
    reporter.client.abort.assert_called_once()
    prompt_mock.assert_called_once_with("Confirm upload?")

def test_follow_in_review_bad_status(mocker, reporter):
    prompt_mock = mocker.patch("flywheel_cli.ingest.reporter.util.confirmation_prompt", return_value=False)
    reporter.config.assume_yes = False
    reporter.client.ingest.status = T.IngestStatus("uploading")

    reporter.follow_in_review_status()

    reporter.client.review.assert_not_called()
    reporter.client.abort.assert_not_called()

def test_follow_preparing_status(mocker, reporter):
    spinner_mock = mocker.patch("flywheel_cli.ingest.reporter.TerminalSpinnerThread")
    time_mock = mocker.patch("flywheel_cli.ingest.reporter.time")

    client = AlteringAttrDict({
        "ingest": [
            T.IngestOut(
                id=uuid4(),
                label="label",
                fw_host="host",
                fw_user="user",
                api_key="api_key",
                config=config.IngestConfig(src_fs="/tmp"),
                strategy_config=config.FolderConfig(),
                status="preparing",
                history=[],
                created=datetime.datetime.now()
            ),
            T.IngestOut(
                id=uuid4(),
                label="label",
                fw_host="host",
                fw_user="user",
                api_key="api_key",
                config=config.IngestConfig(src_fs="/tmp"),
                strategy_config=config.FolderConfig(),
                status="uploading",
                history=[],
                created=datetime.datetime.now()
            )
        ]
    })

    reporter.client = client

    reporter.follow_preparing_status()

    # loop
    time_mock.sleep.assert_called_once_with(reporter.config.refresh_interval)

    spinner_mock.assert_called_once_with("Preparing for ingest", fh=reporter._fh)
    spinner_mock.return_value.start.assert_called_once()
    spinner_mock.return_value.stop.assert_called_once_with("Preparing complete")

def test_follow_uploading_status(mocker, reporter):
    time_mock = mocker.patch("flywheel_cli.ingest.reporter.time")
    print_mock = mocker.patch("flywheel_cli.ingest.reporter.Reporter.print")

    dt = datetime.datetime.utcnow()
    dt2 = dt - datetime.timedelta(seconds=5)
    datetime_mock = mocker.patch("flywheel_cli.ingest.reporter.datetime.datetime")
    datetime_mock.utcnow.return_value = dt
    datetime_mock.utcfromtimestamp.return_value = dt2

    client = AlteringAttrDict({
        "ingest": [
            T.IngestOut(
                id=uuid4(),
                label="label",
                fw_host="host",
                fw_user="user",
                api_key="api_key",
                config=config.IngestConfig(src_fs="/tmp"),
                strategy_config=config.FolderConfig(),
                status="uploading",
                history=[
                    ["uploading", 0]
                ],
                created=datetime.datetime.now()
            ),
            T.IngestOut(
                id=uuid4(),
                label="label",
                fw_host="host",
                fw_user="user",
                api_key="api_key",
                config=config.IngestConfig(src_fs="/tmp"),
                strategy_config=config.FolderConfig(),
                status="finalizing",
                history=[
                    ["uploading", 0]
                ],
                created=datetime.datetime.now()
            ),
            T.IngestOut(
                id=uuid4(),
                label="label",
                fw_host="host",
                fw_user="user",
                api_key="api_key",
                config=config.IngestConfig(src_fs="/tmp"),
                strategy_config=config.FolderConfig(),
                status="finalizing",
                history=[
                    ["uploading", 0]
                ],
                created=datetime.datetime.now()
            )

        ],
        "progress": [
            T.Progress(
                items=T.StatusCount(
                    pending=3,
                    running=1,
                    finished=1,
                    total=5
                )
            ),
            T.Progress(
                items=T.StatusCount(
                    pending=2,
                    running=1,
                    finished=2,
                    total=5
                )
            )
        ]
    })

    reporter.client = client
    reporter.follow_uploading_status()
    # loop
    time_mock.sleep.assert_called_once_with(reporter.config.refresh_interval)

    assert print_mock.mock_calls ==  [
        mock.call("1 / 5 (0 failed), ETA: 0:00:20", replace=True),
        mock.call("2 / 5 (0 failed), ETA: 0:00:07", replace=True),
        mock.call(""),
        mock.call("Pending: 2"),
        mock.call("Running: 1"),
        mock.call("Total: 5")
    ]

def test_print_upload_progress_no_eta(mocker, reporter):
    mocker.patch("flywheel_cli.ingest.reporter.Reporter.compute_eta", return_value=None)
    reporter.print_upload_progress(
        progress=T.Progress(
            items=T.StatusCount(
                failed=2,
                finished=3,
                total=4
            )
        ),
        ingest=None,
        prev_eta=None
    )

    assert_print(
        reporter,
        [{"msg": "3 / 4 (2 failed), ETA: ~", "replace": True}]
    )

def test_print_upload_progress_eta(mocker, reporter):
    mocker.patch("flywheel_cli.ingest.reporter.Reporter.compute_eta", return_value={"eta": datetime.timedelta(seconds=12)})
    reporter.print_upload_progress(
        progress=T.Progress(
            items=T.StatusCount(
                failed=2,
                finished=3,
                total=4
            )
        ),
        ingest=None,
        prev_eta=None
    )

    assert_print(
        reporter,
        [{"msg": "3 / 4 (2 failed), ETA: 0:00:12", "replace": True}]
    )

def test_print_upload_summary(reporter):
    reporter.print_upload_summary(
        T.Progress(
            items=T.StatusCount(
                scanned=1,
                failed=2,
                finished=3,
                total=4
            )
        )
    )

    assert_print(
        reporter,
        [
            "Scanned: 1",
            "Failed: 2",
            "Total: 4",
        ]
    )

def test_print_final_report(mocker, reporter):
    crayons_mock = mocker.patch("flywheel_cli.ingest.reporter.crayons.magenta", side_effect=dummy_style)

    reporter.client.report = T.Report(
        status="finished",
        elapsed=[
            [T.IngestStatus("created"), 5],
            [T.IngestStatus("scanning"), 10]
        ],
        errors=[
            T.TaskError(
                task=uuid4(),
                type="scan",
                message="message1"
            ),
            T.TaskError(
                task=uuid4(),
                type="resolve",
                message="message2"
            ),
        ]
    )

    reporter.print_final_report()

    assert_print(
        reporter,
        [
            "Final report",
            "The following errors happend:",
            "scan: message1",
            "resolve: message2",
            "Created took: 0:00:05",
            "Scanning took: 0:00:10",
            "Total elapsed time: 0:00:15",
        ]
    )

    crayons_mock.assert_called_once_with(
        "Final report",
        bold=True
    )

def test_print_no_replace(reporter):
    reporter.print("test message1")
    assert_print(
        reporter,
        [
            "test message1"
        ]
    )
    assert reporter._fh.getvalue() == "test message1\n"

def test_print_replace(reporter):
    reporter.print(
        msg="test message1",
        replace=False
    )
    reporter.print(
        msg="test message2",
        replace=True
    )
    reporter.print(
        msg="test message3",
        replace=False
    )

    assert_print(
        reporter,
        [
            "test message1",
            {"msg": "test message2", "replace":True},
            "test message3",
        ]
    )
    assert reporter._fh.getvalue() == "test message1\n\rtest message2\033[Ktest message3\n"

def test_print_status_header(mocker, reporter):
    crayons_mock = mocker.patch("flywheel_cli.ingest.reporter.crayons.magenta", side_effect=dummy_style)
    dt = datetime.datetime(1900, 1, 2, 3, 4, 5)
    reporter.print_status_header("header_value", dt)

    assert reporter._fh.getvalue() == "Header value   [1900-01-02 03:04:05]\n"
    crayons_mock.assert_called_once_with(
        "Header value   ",
        bold=True
    )

def test_save_reports(mocker, reporter):
    save_stream_mock = mocker.patch("flywheel_cli.ingest.reporter.Reporter.save_stream_to_file", side_effect=["path1", "path2", "path3"])
    reporter.config = config.ReporterConfig(
        save_audit_log="audit_log_path",
        save_deid_log="deid_log_path",
        save_subjects="subjects_path"
    )

    reporter.save_reports()

    save_stream_mock.assert_has_calls([
        mock.call(
            reporter.client.save_audit_log,
            "audit_log_path",
            "save_audit_log"
        ),
        mock.call(
            reporter.client.save_deid_log,
            "deid_log_path",
            "save_deid_log"
        ),
        mock.call(
            reporter.client.save_subjects,
            "subjects_path",
            "save_subjects"
        ),
    ])

    assert_print(
        reporter,
        [
            "Saved save audit log to path1",
            "Saved save deid log to path2",
            "Saved save subjects to path3",
        ]
    )

def test_save_reports_empty(mocker, reporter):
    save_stream_mock = mocker.patch("flywheel_cli.ingest.reporter.Reporter.save_stream_to_file")
    reporter.save_reports()
    assert reporter._fh.getvalue() == ""
    save_stream_mock.assert_not_called()

def test_save_stream_to_file(mocker):
    fp = io.StringIO()
    file_mock = mock.MagicMock()
    file_mock.__enter__.return_value = fp
    open_mock = mocker.patch("flywheel_cli.ingest.reporter.open", return_value=file_mock)
    filepath_mock = mocker.patch("flywheel_cli.ingest.reporter.util.get_filepath", return_value="file_path")

    path = reporter_.Reporter.save_stream_to_file(
        stream=["line1\n", "line2\n"],
        path="path_arg",
        prefix="prefix"
    )

    assert fp.getvalue() == "line1\nline2\n"
    assert path == "file_path"

    filepath_mock.assert_called_once_with(
        "path_arg",
        prefix="prefix",
        extension="csv"
    )

    open_mock.assert_called_once_with("file_path", "w")

def test_save_stream_to_file_not_found(mocker):
    open_mock = mocker.patch("flywheel_cli.ingest.reporter.open")
    filepath_mock = mocker.patch("flywheel_cli.ingest.reporter.util.get_filepath")
    filepath_mock.side_effect = [FileNotFoundError(), "path2"]
    get_incremental_filename_mock = mocker.patch("flywheel_cli.ingest.reporter.util.get_incremental_filename")

    path = reporter_.Reporter.save_stream_to_file(
        stream=["line1\n", "line2\n"],
        path="path_arg",
        prefix="prefix"
    )

    assert path == "path2"
    assert len(filepath_mock.mock_calls) == 2
    get_incremental_filename_mock.assert_not_called()
    open_mock.assert_called_once_with("path2", "w")

def test_save_stream_to_file_exists(mocker):
    open_mock = mocker.patch("flywheel_cli.ingest.reporter.open")
    filepath_mock = mocker.patch("flywheel_cli.ingest.reporter.util.get_filepath")
    filepath_mock.side_effect = [FileExistsError(), None]
    get_incremental_filename_mock = mocker.patch("flywheel_cli.ingest.reporter.util.get_incremental_filename", return_value="path3")

    path = reporter_.Reporter.save_stream_to_file(
        stream=["line1\n", "line2\n"],
        path="path_arg",
        prefix="prefix"
    )

    assert path == "path3"
    assert len(filepath_mock.mock_calls) == 1
    get_incremental_filename_mock.assert_called_once_with("path_arg")
    open_mock.assert_called_once_with("path3", "w")

def test_compute_eta_none():
    eta = reporter_.Reporter.compute_eta(
        ingest=None,
        item_stats=T.StatusCount(),
        prev_eta=None
    )

    assert eta is None

def test_compute_eta_no_prev(mocker):
    dt = datetime.datetime.utcnow()
    dt2 = dt - datetime.timedelta(seconds=5)
    datetime_mock = mocker.patch("flywheel_cli.ingest.reporter.datetime.datetime")
    datetime_mock.utcnow.return_value = dt
    datetime_mock.utcfromtimestamp.return_value = dt2

    ingest = T.IngestOut(
        id=uuid4(),
        label="label",
        fw_host="host",
        fw_user="user",
        api_key="api_key",
        config=config.IngestConfig(src_fs="/tmp"),
        strategy_config=config.FolderConfig(),
        status="created",
        history=[["uploading", 0]],
        created=datetime.datetime.now()
    )

    stat = T.StatusCount(
        finished=1,
        pending=15,
        running=5
    )
    prev_eta = {}
    eta = reporter_.Reporter.compute_eta(
        ingest=ingest,
        item_stats=stat,
        prev_eta=prev_eta
    )

    # ellapsed time = 5.0
    # finished = 1
    # remaining tasks = 15 + 5  = 20
    # time = 5 * 20
    assert eta == {
        "eta": datetime.timedelta(seconds=100),
        "report_time": dt,
        "pending": 15,
        "finished": 1
    }
    assert eta == prev_eta

def test_compute_eta_with_prev(mocker):
    dt = datetime.datetime.utcnow()
    dt2 = dt - datetime.timedelta(seconds=5)
    datetime_mock = mocker.patch("flywheel_cli.ingest.reporter.datetime.datetime")
    datetime_mock.utcnow.return_value = dt
    datetime_mock.utcfromtimestamp.return_value = dt2

    stat = T.StatusCount(
        finished=1,
        pending=15,
        running=5
    )

    prev_eta = {
        "eta": datetime.timedelta(seconds=100),
        "report_time": dt2,
        "pending": 15,
        "finished": 1
    }

    eta = reporter_.Reporter.compute_eta(
        ingest=None,
        item_stats=stat,
        prev_eta=prev_eta
    )

    assert eta == {
        "eta": datetime.timedelta(seconds=95),
        "report_time": dt,
        "pending": 15,
        "finished": 1
    }
    assert eta == prev_eta

def test_get_upload_start_time_none():
    history = []

    ts = reporter_.Reporter.get_upload_start_time(history)

    assert ts is None

def test_get_upload_start_time():
    history = [
        ["created", 1],
        ["scanning", 2],
        ["resolving", 3],
        ["in_review", 4],
        ["preparing", 5],
        ["uploading", 6],
        ["finalizing", 7],
        ["finished", 8],
        ["failed", 9],
        ["aborted", 10],
    ]

    dt = datetime.datetime(1970, 1, 1, 0, 0, 6)
    ts = reporter_.Reporter.get_upload_start_time(history)

    assert ts == dt

# TerminalSpinnerThread tests
def test_spinner_run(mocker):
    magenta_mock = mocker.patch("flywheel_cli.ingest.reporter.crayons.magenta", side_effect=dummy_style)
    blue_mock = mocker.patch("flywheel_cli.ingest.reporter.crayons.blue", side_effect=dummy_style)
    time_mock = mocker.patch("flywheel_cli.ingest.reporter.time")
    mocker.patch("flywheel_cli.ingest.reporter.threading")
    print_mock = mocker.patch("flywheel_cli.ingest.reporter.TerminalSpinnerThread.print")

    spinner = reporter_.TerminalSpinnerThread("message")
    spinner._thread = mock.Mock()
    spinner._shutdown_event.is_set.side_effect = [False] * 14 + [True]
    spinner.run()

    assert print_mock.mock_calls == [
        mock.call("[   ] message\r"),
        mock.call("[=  ] message\r"),
        mock.call("[== ] message\r"),
        mock.call("[===] message\r"),
        mock.call("[ ==] message\r"),
        mock.call("[  =] message\r"),
        mock.call("[   ] message\r"),
        mock.call("[   ] message\r"),
        mock.call("[  =] message\r"),
        mock.call("[ ==] message\r"),
        mock.call("[===] message\r"),
        mock.call("[== ] message\r"),
        mock.call("[=  ] message\r"),
        mock.call("[   ] message\r")
    ]

    assert time_mock.sleep.call_count == 14
    time_mock.sleep.assert_called_with(0.2)

def test_spinner_start(mocker):
    thread_mock = mock.Mock()
    mocker.patch("flywheel_cli.ingest.reporter.threading.Thread", return_value=thread_mock)
    mocker.patch("flywheel_cli.ingest.reporter.stat.S_ISREG", return_value=False)

    spinner = reporter_.TerminalSpinnerThread("message")
    assert not spinner.is_running

    spinner.start()

    assert spinner.is_running
    assert spinner._thread == thread_mock
    assert spinner._thread.daemon
    spinner._thread.start.assert_called_once()
    assert not spinner._shutdown_event.is_set()

    #restart
    spinner.start()

    assert spinner.is_running
    assert spinner._thread == thread_mock
    assert spinner._thread.daemon
    spinner._thread.start.assert_called_once()
    assert not spinner._shutdown_event.is_set()

def test_spinner_stop(mocker):
    thread_mock = mock.Mock()
    mocker.patch("flywheel_cli.ingest.reporter.threading.Thread", return_value=thread_mock)
    blue_mock = mocker.patch("flywheel_cli.ingest.reporter.crayons.blue", side_effect=dummy_style)
    print_mock = mocker.patch("flywheel_cli.ingest.reporter.TerminalSpinnerThread.print")
    mocker.patch("flywheel_cli.ingest.reporter.stat.S_ISREG", return_value=False)

    spinner = reporter_.TerminalSpinnerThread("message")
    spinner.start()

    assert spinner.is_running
    assert spinner._thread == thread_mock
    assert spinner._thread.daemon
    spinner._thread.start.assert_called_once()
    assert not spinner._shutdown_event.is_set()

    spinner.stop("stop message")
    assert spinner._shutdown_event.is_set()
    thread_mock.join.assert_called_once()
    assert not spinner.is_running

    assert print_mock.mock_calls == [
        mock.call(""),
        mock.call("\033[Kstop message\n")
    ]

def test_spinner_print():
    fh = io.StringIO()
    spinner = reporter_.TerminalSpinnerThread("message", fh=fh)

    spinner.print("test message")
    assert spinner._fh.getvalue() == "test message"

def test_spinner_is_running():
    spinner = reporter_.TerminalSpinnerThread("message")
    assert not spinner.is_running

    spinner._thread = mock.Mock()
    assert spinner.is_running

    spinner._shutdown_event.set()
    assert not spinner.is_running

def assert_print(reporter, writes):
    def replace(msg):
        return f"\r{msg}\033[K"

    msg = ""
    for w in writes:
        if isinstance(w, dict):
            if "replace" in w and w["replace"]:
                msg += replace(w["msg"])
            else:
                msg += f"{w['msg']}\n"
        else:
            msg += f"{w}\n"

    assert reporter._fh.getvalue() == msg

def dummy_style(msg, *args, **kwargs):
    return msg

class AlteringAttrDict():
    def __init__(self, values):
        self.values = values
        self.value_pointers = dict.fromkeys(values.keys(), 0)
        self.children = {}

    def __getattr__(self, attr):
        try:
            value = self.values[attr]
            if isinstance(value, list):
                pointer = self.value_pointers[attr]
                value = self.values[attr][pointer]
                self.value_pointers[attr] += 1
        except KeyError:
            raise AttributeError(attr)
        if isinstance(value, dict):
            if attr not in self.children:
                self.children[attr] = AlteringAttrDict(value)
            value = self.children[attr]
        return value
