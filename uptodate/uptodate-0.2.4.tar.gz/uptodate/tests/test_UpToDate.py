import pytest

from rich.console import Console
from uptodate.core import UpToDate, Row


@pytest.fixture
def uptodate():
    console = Console()
    return UpToDate(console)


@pytest.fixture
def dependences():
    return {'click': '6.7', 'pytest': '3.0.0'}


@pytest.fixture
def latest_versions():
    return {'click': '6.7', 'pytest': '3.2.5'}


@pytest.fixture
def rows():
    return [Row(name='pytest', current_version='3.0.0', latest_version='3.2.5')]


def test_prepare_rows(uptodate, dependences, latest_versions, rows):
    prepared_rows = uptodate._prepare_rows(dependences, latest_versions)

    assert prepared_rows == rows
