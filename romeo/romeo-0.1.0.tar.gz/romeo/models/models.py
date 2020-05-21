import sys
import click

from .add import add
from .list import list
from .remove import rm

@click.group()
def models():
    """
    Models summaries
    """
    pass

models.add_command(add)
models.add_command(list)
models.add_command(rm)

if __name__ == "__main__":
    sys.exit(models())
