import os
import click

from rich.console import Console

try:
    from uptodate.core import UpToDate
except Exception:
    from core import UpToDate  # type: ignore


DEFAULT_FILE_PATH = 'requirements.txt'

console = Console()


@click.command()
@click.argument('file_paths', nargs=-1, type=click.Path(exists=True))
def up_to_date(file_paths):
    """Scan requirements.txt file for dependences which are not up to date"""

    if len(file_paths) == 0:
        if os.path.isfile(DEFAULT_FILE_PATH):
            file_paths = (DEFAULT_FILE_PATH,)
        else:
            console.print('No requirements file found', style='yellow')

    uptodate = UpToDate(console)
    for file_path in file_paths:
        uptodate.check(file_path)


if __name__ == '__main__':
    up_to_date()
