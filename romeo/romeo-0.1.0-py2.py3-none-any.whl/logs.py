import sys
import click

@click.command()
def logs(): 
    """
    Show logs.
    """
    pass

if __name__ == "__main__":
    sys.exit(logs())
