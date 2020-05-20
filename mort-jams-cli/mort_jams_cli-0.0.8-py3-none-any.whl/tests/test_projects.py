from prodigyteams.main import cli
from typer.testing import CliRunner

runner = CliRunner()


def test_list_projects():
    result = runner.invoke(cli, ["projects", "list"])
    assert "Test Project" in result.output
