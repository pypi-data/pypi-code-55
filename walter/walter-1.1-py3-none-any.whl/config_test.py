import pytest

from . import config
from .na import NA


def test_works_properly():
    c = config.Config("ACME Inc", "Widget", sources=[{"FOO": "bar"}])
    assert c("FOO") == "bar"


def test_cast():
    c = config.Config("ACME Inc", "Widget", sources=[{"FOO": "1"}])
    assert c("FOO", cast=int) == 1


def test_cast_bool():
    c = config.Config("ACME Inc", "Widget", sources=[{"FOO": "False"}])
    assert c("FOO", cast=bool) is False


def test_cast_bool_error():
    c = config.Config("ACME Inc", "Widget", sources=[{"FOO": "hello"}])
    with pytest.raises(config.ConfigError):
        c("FOO", cast=bool)


def test_default():
    c = config.Config("ACME Inc", "Widget", sources=[{}])
    # In actual use we probably wouldn't see a cast to int with a float
    # default; we're using this to
    assert c("FOO", cast=int, default=1.0) == 1.0


def test_missing():
    c = config.Config("ACME Inc", "Widget", sources=[{"FOO": "bar"}])
    with pytest.raises(config.ConfigError):
        c("BAR")


def test_context_manager():
    with pytest.raises(config.ConfigErrors):
        with config.Config("ACME", "Widget", sources=[{"FOO": "bar"}]) as c:
            assert c("BAR") is NA


def test_collect_keys():
    with pytest.raises(config.ConfigErrors):
        with config.Config("ACME", "Widget", sources=[{"FOO": "bar"}]) as c:
            c("FOO")
            c("BAR")
            c("BAZ")
    assert c.values == ["FOO", "BAR", "BAZ"]
