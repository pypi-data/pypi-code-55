import pytest

from unittest.mock import patch, Mock

from uptodate.core import PyPI


@pytest.fixture
def pypi():
    return PyPI()


@pytest.fixture
def dependences():
    return ['click', 'pytest']


@pytest.fixture
def json_mock():
    m = Mock()
    m.json.side_effect = [
        {'info': {'version': '6.7'}},
        {'info': {'version': '3.2.5'}}
    ]

    return m


@pytest.fixture
def latest_versions():
    return {'click': '6.7', 'pytest': '3.2.5'}


def test_get_versions(pypi, dependences, latest_versions, json_mock):
    with patch('requests.get') as mock_request:
        mock_request.return_value = json_mock
        versions = pypi.get_versions(dependences)

    assert versions == latest_versions
