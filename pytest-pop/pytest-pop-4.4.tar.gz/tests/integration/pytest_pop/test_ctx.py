import pytest


@pytest.fixture
def acct_subs():
    return []


@pytest.fixture
def acct_profile():
    return "default"


def test_context(ctx):
    assert "test" in ctx
    assert "acct" in ctx
    assert "run_name" in ctx
