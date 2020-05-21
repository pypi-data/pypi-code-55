import sys
import click

@click.command()
def clean(): 
    """
    Clean temporary files.
    """
    pass

if __name__ == "__main__":
    sys.exit(clean())
