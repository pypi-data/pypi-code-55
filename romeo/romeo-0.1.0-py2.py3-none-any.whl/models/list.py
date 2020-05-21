import sys
import click

@click.command()
def list(): 
    """
    List models.
    """
    pass

if __name__ == "__main__":
    sys.exit(list())
