from pathlib import Path

from prodigyteams.main import cli
from typer.testing import CliRunner

runner = CliRunner()


def test_list_packages():
    result = runner.invoke(cli, ["packages", "list"])
    assert "prodigy" in result.output
    assert "prodigyteams" in result.output


def test_add_package(tmp_path: Path):
    tmp_file = tmp_path / "file.txt"
    tmp_file.write_text("test text")
    result = runner.invoke(cli, ["packages", "add", str(tmp_file)])
    assert "Package successfully added." in result.output


def test_list_package():
    result = runner.invoke(cli, ["packages", "list-package", "prodigy"])
    assert (
        "prodigy-1.8.3-cp35.cp36.cp37-cp35m.cp36m.cp37m-macosx_10_13_x86_64.whl"
        in result.output
    )


def test_download_package_binary():
    result = runner.invoke(
        cli,
        [
            "packages",
            "download",
            "prodigy",
            "prodigy-1.8.3-cp35.cp36.cp37-cp35m.cp36m.cp37m-macosx_10_13_x86_64.whl",
        ],
    )
    assert "Package file successfully downloaded to" in result.output


def test_delete_package():
    result = runner.invoke(cli, ["packages", "delete", "dummy"], input="y\n")
    assert "Package successfully deleted" in result.output
