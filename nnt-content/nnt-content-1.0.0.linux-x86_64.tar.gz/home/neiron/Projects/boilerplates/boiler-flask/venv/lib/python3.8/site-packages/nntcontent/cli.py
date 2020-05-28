import os
import shutil
import click


@click.group()
def cli():
    """group for cli commands of this package"""


@cli.command()
def init():
    """Init project structure"""
    filename = 'src/__init__.py'
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write(f"from {os.path.basename(os.path.dirname(__file__))} import create_app\n")
            f.write("\n")
            f.write("\n")
            f.write("app = create_app()\n")

    if not os.path.exists('.env'):
        target = os.path.join(os.path.dirname(__file__), '.env.default')
        shutil.copy(target, '.env')
