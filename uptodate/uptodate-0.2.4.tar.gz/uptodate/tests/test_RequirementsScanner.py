import pytest

from rich.console import Console
from unittest.mock import patch, mock_open
from uptodate.core import RequirementsScanner


@pytest.fixture
def scanner():
    console = Console()
    return RequirementsScanner(console)


@pytest.fixture
def open_mock():
    read_data = '\n'.join(['click==6.7', 'pytest==3.2.5', 'celery[redis]==4.0.2'])

    return mock_open(read_data=read_data)


def test_get_dependences(scanner, open_mock):
    file_path = 'requirements.txt'
    with patch("builtins.open", open_mock) as mock_file:
        dependences = scanner.get_dependences(file_path)

        mock_file.assert_called_once_with(file_path, 'r')

    assert dependences == {'click': '6.7', 'pytest': '3.2.5'}


def test_is_supported(scanner):
    assert scanner._is_supported('click==6.7') is True
    assert scanner._is_supported('click.zip') is False
    assert scanner._is_supported('celery[redis]') is False
