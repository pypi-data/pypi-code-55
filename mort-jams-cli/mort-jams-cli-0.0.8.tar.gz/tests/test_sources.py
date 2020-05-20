from pathlib import Path

from prodigyteams.main import cli
from typer.testing import CliRunner

from .conftest import broker_meta_response

runner = CliRunner()


def test_list_sources():
    result = runner.invoke(cli, ["sources", "list"])
    for source_id in broker_meta_response["sources"]:
        assert source_id in result.output


def test_add_source(tmp_path: Path):
    tmp_file = tmp_path / "file.txt"
    tmp_file.write_text("test text")
    result = runner.invoke(cli, ["sources", "add", str(tmp_file)])
    assert "Source successfully added" in result.output


def test_delete_source(tmp_path: Path):
    result = runner.invoke(cli, ["sources", "delete", "Reddit Insults"], input="y\n")
    assert "Source successfully deleted" in result.output
