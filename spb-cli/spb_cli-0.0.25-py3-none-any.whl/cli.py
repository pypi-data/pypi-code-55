import click
import rich
import rich.table
import rich.console
import os

import spb
from spb.cli_core.helper import Helper
from spb.session import Session

console = rich.console.Console()
helper = Helper()

@click.group()
@click.version_option(version=spb.__version__, message='%(version)s')
def cli():
    pass


@cli.command()
# @click.option('--profile_name', prompt='Profile Name', default='default')
@click.option('--account_name', prompt='Account Name')
@click.option('--access_key', prompt='Access Key')
def config(account_name, access_key):
    profile_name = 'default'
    helper.set_config(profile_name, account_name, access_key)


@cli.command()
def project():
    helper.describe_projects()


@cli.command()
@click.argument('directory_path')
@click.option('--project_name')
def init(directory_path, project_name):
    for _ in range(3):
        project_name = click.prompt('Project Name')
        if not helper.check_project(project_name):
            click.echo('No such project. Try again.')
            project_name = None
        else:
            break
    if not project_name:
        return
    helper.init_project(directory_path, project_name)


@cli.command()
@click.argument('dataset_name')
@click.option('--log', 'log_file')
# @click.option('--log', 'log_file', type=click.File('a'))
@click.option('-f', '--force', 'is_force', default=False, is_flag=True)
def upload(dataset_name, log_file, is_force):
    helper.upload(dataset_name, log_file, is_force)


@cli.command()
@click.option('--log', 'log_file')
# @click.option('--log', 'log_file', type=click.File('a'))
def download(log_file):
    helper.download(log_file)


@cli.command()
def version():
    click.echo(spb.__version__)
