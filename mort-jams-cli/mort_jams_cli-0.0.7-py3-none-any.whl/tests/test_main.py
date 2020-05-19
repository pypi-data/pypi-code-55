from prodigyteams.main import cli
from typer.testing import CliRunner

runner = CliRunner()


def test_login():
    result = runner.invoke(cli, ["login"])
    assert "Login successful" in result.output


def test_version():
    result = runner.invoke(cli, ["--version"])
    assert "Prodigy Teams CLI version:" in result.output
