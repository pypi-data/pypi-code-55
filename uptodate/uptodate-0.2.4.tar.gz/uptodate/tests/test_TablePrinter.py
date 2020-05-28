import pytest
import click

from uptodate.core import TablePrinter, Row


@pytest.fixture
def printer():
    return TablePrinter()


@pytest.fixture
def rows():
    return [
        Row(name='click', current_version='5.0', latest_version='6.7'),
        Row(name='pytest', current_version='3.0.0', latest_version='3.2.5'),
    ]


@pytest.fixture
def empty_rows():
    return []


def test_draw(printer, rows):
    table = printer.draw(rows)

    assert table.row_count == len(rows)


def test_empty(printer, empty_rows):
    table = printer.draw(empty_rows)

    assert table.row_count == 0
