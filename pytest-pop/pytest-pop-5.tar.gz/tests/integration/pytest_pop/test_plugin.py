import os
import pytest
import sys
import _pytest.config as conf


def test_code_dir(pytestconfig: conf.Config):
    assert sys.path[0] == pytestconfig.invocation_dir


def test_tpath_dir(pytestconfig: conf.Config):
    assert sys.path[1] == os.path.join(pytestconfig.invocation_dir, "tpath")


def test_os_sleep_secs(os_sleep_secs):
    if "CI_RUN" in os.environ:
        assert os_sleep_secs == 1.75
    else:
        assert os_sleep_secs == 0.5
