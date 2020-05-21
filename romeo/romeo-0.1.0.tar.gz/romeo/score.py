import sys
import click

@click.command()
def score(): 
    """
    Scores the model.
    """
    pass

if __name__ == "__main__":
    sys.exit(score())
