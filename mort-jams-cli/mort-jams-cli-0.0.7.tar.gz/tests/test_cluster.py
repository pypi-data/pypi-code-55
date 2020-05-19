from prodigyteams.main import cli
from typer.testing import CliRunner

runner = CliRunner()


def test_cluster_info():
    result = runner.invoke(cli, ["cluster", "info"])
    assert "http://localhost:8080" in result.output


def test_cluster_verify():
    result = runner.invoke(cli, ["cluster", "verify"])
    print(result.output)
    assert "Found (3) problems!" in result.output
