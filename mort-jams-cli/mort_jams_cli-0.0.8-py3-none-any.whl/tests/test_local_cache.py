import json
from datetime import datetime, timedelta
from pathlib import Path
from unittest import mock

from prodigyteams import utils
from prodigyteams.utils import local_cache


@local_cache(expire_seconds=30)
def func_no_args():
    return "Hello World"


@local_cache(expire_seconds=30)
def func_args(arg1: str, arg2: int):
    return [f"{arg1} {arg2}"]


@local_cache(expire_seconds=30)
def func_kwargs(*, kwarg1: str, kwarg2: int):
    return {"data": f"{kwarg1} {kwarg2}"}


@local_cache(expire_seconds=30)
def func_args_kwargs(arg1: str, arg2: int, *, kwarg1: str, kwarg2: int):
    return f"{arg1} {arg2} - {kwarg1} {kwarg2}"


def get_test_cache_data(expire: str):
    cache_data = {
        "tests.test_local_cache:func_no_args": {
            "": {"data": "Hello Cache", "expire": expire}
        },
        "tests.test_local_cache:func_args": {
            "foo-2": {"data": ["cache 2"], "expire": expire}
        },
        "tests.test_local_cache:func_kwargs": {
            "kwarg1:bar_kwarg2:3": {"data": {"data": "cache 3"}, "expire": expire}
        },
        "tests.test_local_cache:func_args_kwargs": {
            "foo-2kwarg1:bar_kwarg2:3": {"data": "cache 2 - cache 3", "expire": expire}
        },
    }
    return cache_data


def test_save_local_cache(tmp_path: Path):
    cache_path: Path = tmp_path / "cache.json"
    with mock.patch.object(utils, "get_cache_path", return_value=cache_path):
        result = func_no_args()
        assert result == "Hello World"
        result = func_args("foo", 2)
        assert result == ["foo 2"]
        result = func_kwargs(kwarg1="bar", kwarg2=3)
        assert result == {"data": "bar 3"}
        result = func_args_kwargs("foo", 2, kwarg1="bar", kwarg2=3)
        assert result == "foo 2 - bar 3"
    cache_text = cache_path.read_text()
    cache_data = json.loads(cache_text)
    assert (
        cache_data["tests.test_local_cache:func_no_args"][""]["data"] == "Hello World"
    )
    assert cache_data["tests.test_local_cache:func_args"]["foo-2"]["data"] == ["foo 2"]
    assert cache_data["tests.test_local_cache:func_kwargs"]["kwarg1:bar_kwarg2:3"][
        "data"
    ] == {"data": "bar 3"}
    assert (
        cache_data["tests.test_local_cache:func_args_kwargs"][
            "foo-2kwarg1:bar_kwarg2:3"
        ]["data"]
        == "foo 2 - bar 3"
    )


def test_read_local_cache(tmp_path: Path):
    cache_path: Path = tmp_path / "cache.json"
    expire_datetime = datetime.now() + timedelta(minutes=10)
    expire = expire_datetime.isoformat()
    cache_data = get_test_cache_data(expire)
    cache_text = json.dumps(cache_data)
    cache_path.write_text(cache_text)
    with mock.patch.object(utils, "get_cache_path", return_value=cache_path):
        result = func_no_args()
        assert result == "Hello Cache"
        result = func_args("foo", 2)
        assert result == ["cache 2"]
        result = func_kwargs(kwarg1="bar", kwarg2=3)
        assert result == {"data": "cache 3"}
        result = func_args_kwargs("foo", 2, kwarg1="bar", kwarg2=3)
        assert result == "cache 2 - cache 3"


def test_expire_local_cache(tmp_path: Path):
    cache_path: Path = tmp_path / "cache.json"
    expire_datetime = datetime.now() - timedelta(minutes=10)
    expire = expire_datetime.isoformat()
    cache_data = get_test_cache_data(expire)
    cache_text = json.dumps(cache_data)
    cache_path.write_text(cache_text)
    with mock.patch.object(utils, "get_cache_path", return_value=cache_path):
        result = func_no_args()
        assert result == "Hello World"
        result = func_args("foo", 2)
        assert result == ["foo 2"]
        result = func_kwargs(kwarg1="bar", kwarg2=3)
        assert result == {"data": "bar 3"}
        result = func_args_kwargs("foo", 2, kwarg1="bar", kwarg2=3)
        assert result == "foo 2 - bar 3"
    cache_text = cache_path.read_text()
    cache_data = json.loads(cache_text)
    assert (
        cache_data["tests.test_local_cache:func_no_args"][""]["data"] == "Hello World"
    )
    assert cache_data["tests.test_local_cache:func_args"]["foo-2"]["data"] == ["foo 2"]
    assert cache_data["tests.test_local_cache:func_kwargs"]["kwarg1:bar_kwarg2:3"][
        "data"
    ] == {"data": "bar 3"}
    assert (
        cache_data["tests.test_local_cache:func_args_kwargs"][
            "foo-2kwarg1:bar_kwarg2:3"
        ]["data"]
        == "foo 2 - bar 3"
    )


def test_read_local_cache_other_args(tmp_path: Path):
    cache_path: Path = tmp_path / "cache.json"
    expire_datetime = datetime.now() + timedelta(minutes=10)
    expire = expire_datetime.isoformat()
    cache_data = get_test_cache_data(expire)
    cache_text = json.dumps(cache_data)
    cache_path.write_text(cache_text)
    with mock.patch.object(utils, "get_cache_path", return_value=cache_path):
        result = func_no_args()
        assert result == "Hello Cache"
        result = func_args("foo", 2)
        assert result == ["cache 2"]
        result = func_args("foo", 3)
        assert result == ["foo 3"]
        result = func_kwargs(kwarg1="bar", kwarg2=3)
        assert result == {"data": "cache 3"}
        result = func_kwargs(kwarg1="baz", kwarg2=3)
        assert result == {"data": "baz 3"}
        result = func_args_kwargs("foo", 2, kwarg1="bar", kwarg2=3)
        assert result == "cache 2 - cache 3"
        result = func_args_kwargs("foo", 3, kwarg1="bar", kwarg2=3)
        assert result == "foo 3 - bar 3"
    cache_text = cache_path.read_text()
    cache_data = json.loads(cache_text)
    assert cache_data["tests.test_local_cache:func_args"]["foo-3"]["data"] == ["foo 3"]
    assert cache_data["tests.test_local_cache:func_kwargs"]["kwarg1:baz_kwarg2:3"][
        "data"
    ] == {"data": "baz 3"}
    assert (
        cache_data["tests.test_local_cache:func_args_kwargs"][
            "foo-3kwarg1:bar_kwarg2:3"
        ]["data"]
        == "foo 3 - bar 3"
    )


def test_invalid_expire_cache(tmp_path: Path):
    cache_path: Path = tmp_path / "cache.json"
    expire = "invalid expire"
    cache_data = get_test_cache_data(expire)
    cache_text = json.dumps(cache_data)
    cache_path.write_text(cache_text)
    with mock.patch.object(utils, "get_cache_path", return_value=cache_path):
        result = func_no_args()
        assert result == "Hello World"
        result = func_args("foo", 2)
        assert result == ["foo 2"]
        result = func_kwargs(kwarg1="bar", kwarg2=3)
        assert result == {"data": "bar 3"}
        result = func_args_kwargs("foo", 2, kwarg1="bar", kwarg2=3)
        assert result == "foo 2 - bar 3"
    cache_text = cache_path.read_text()
    cache_data = json.loads(cache_text)
    assert (
        cache_data["tests.test_local_cache:func_no_args"][""]["data"] == "Hello World"
    )
    assert cache_data["tests.test_local_cache:func_args"]["foo-2"]["data"] == ["foo 2"]
    assert cache_data["tests.test_local_cache:func_kwargs"]["kwarg1:bar_kwarg2:3"][
        "data"
    ] == {"data": "bar 3"}
    assert (
        cache_data["tests.test_local_cache:func_args_kwargs"][
            "foo-2kwarg1:bar_kwarg2:3"
        ]["data"]
        == "foo 2 - bar 3"
    )


def test_invalid_cache_file(tmp_path: Path):
    cache_path: Path = tmp_path / "cache.json"
    cache_path.write_text("invalid")
    with mock.patch.object(utils, "get_cache_path", return_value=cache_path):
        result = func_no_args()
        assert result == "Hello World"
        result = func_args("foo", 2)
        assert result == ["foo 2"]
        result = func_kwargs(kwarg1="bar", kwarg2=3)
        assert result == {"data": "bar 3"}
        result = func_args_kwargs("foo", 2, kwarg1="bar", kwarg2=3)
        assert result == "foo 2 - bar 3"
    cache_text = cache_path.read_text()
    cache_data = json.loads(cache_text)
    assert (
        cache_data["tests.test_local_cache:func_no_args"][""]["data"] == "Hello World"
    )
    assert cache_data["tests.test_local_cache:func_args"]["foo-2"]["data"] == ["foo 2"]
    assert cache_data["tests.test_local_cache:func_kwargs"]["kwarg1:bar_kwarg2:3"][
        "data"
    ] == {"data": "bar 3"}
    assert (
        cache_data["tests.test_local_cache:func_args_kwargs"][
            "foo-2kwarg1:bar_kwarg2:3"
        ]["data"]
        == "foo 2 - bar 3"
    )
