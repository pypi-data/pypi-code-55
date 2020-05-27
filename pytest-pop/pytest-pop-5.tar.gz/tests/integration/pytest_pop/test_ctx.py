import mock
import os
import pytest

ACCT_KEY = "BjN1KRcfbWPO6G12328vA-3omHGGUxu9z3NvPV-MxOI="
ACCT_FILE = os.path.join(os.path.dirname(__file__), "acct_profile.fernet")


@pytest.fixture
def hub(hub):
    for dyne in ("acct", "exec", "states"):
        hub.pop.sub.add(dyne_name=dyne)
        if dyne in ("corn", "exec", "states"):
            hub.pop.sub.load_subdirs(getattr(hub, dyne), recurse=True)

    # Get the account information from environment variables
    with mock.patch.dict("os.environ", {"ACCT_KEY": ACCT_KEY, "ACCT_FILE": ACCT_FILE,}):
        with mock.patch("sys.argv", ["pytest_pop"]):
            hub.pop.config.load(["idem", "acct"], "idem", parse_cli=False)

    yield hub


@pytest.fixture
def acct_subs():
    return ["cloud"]


@pytest.fixture
def acct_profile():
    return "test_cloud_development"


def test_context(hub, ctx):
    assert "run_name" in ctx
    assert "test" in ctx
    assert "acct" in ctx
