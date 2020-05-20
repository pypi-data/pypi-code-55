from prodigyteams.main import cli
from typer.testing import CliRunner

runner = CliRunner()


def test_list_tasks():
    result = runner.invoke(cli, ["tasks", "list"])
    assert "Is Docs NER" in result.output
