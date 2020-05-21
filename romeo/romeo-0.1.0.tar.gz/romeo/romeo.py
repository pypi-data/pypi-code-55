import sys
import click

from .init import init
from .clean import clean
from .train import train
from .score import score
from .logs import logs
from .models import models

@click.group()
def romeo():
    """Console script for romeo."""
    pass

romeo.add_command(init)
romeo.add_command(clean)
romeo.add_command(train)
romeo.add_command(score)
romeo.add_command(logs)
romeo.add_command(models)

if __name__ == "__main__":
    sys.exit(romeo())
