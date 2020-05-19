"""Contains the CLI commands."""

import click
import logging
import yaml
from pathlib import Path
from importlib import metadata
from . import pkgname
from .document import Document, DocumentError

logger = logging.getLogger(__name__)

# click entrypoint
@click.group()
@click.version_option(metadata.version(pkgname))
@click.pass_context
def main(ctx):

    """Happy Doc."""

    ## Run the program
    try:
        # load main controller in context
        ctx.obj = Document()

    except DocumentError as e:
        click.echo(str(e))


@main.command()
@click.argument('source', type=click.File('r'))
@click.argument('target', type=click.Path(exists=False, writable=True, dir_okay=False))
@click.pass_obj
def convert(document, source, target):

    """Convert a template to PDF."""

    try:
        document.convert('happydev.css', source, target)
    except DocumentError as e:
        click.echo(e)


@main.command()
@click.argument('template', required=False)
@click.argument('path', type=click.Path(exists=False, writable=True, dir_okay=False), required=False)
@click.pass_obj
def template(document, template, path):

    """Generate a new document from template."""

    try:
        if not template:
            # list available templates
            click.echo([f.name for f in document.templates])

        else:
            # convert path type
            docpath = Path(path)
            # create new file from template
            document.create(docpath, template)

    except DocumentError as e:
        click.echo(e)
