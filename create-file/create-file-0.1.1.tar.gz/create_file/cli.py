
import click
from pathlib import Path


@click.command()
@click.argument('file-path', type=click.Path())
def cli(file_path):

    file_path_object = Path(file_path)
    file_path_object.parent.mkdir(parents=True, exist_ok=True)

    if file_path_object.exists():
        print(f"[-] File already exists at: '{str(file_path_object)}'")
        return False

    else:
        file_path_object.touch()
        print(f"[v] File created at: '{str(file_path_object)}'")


if __name__ == "__main__":
    cli()
