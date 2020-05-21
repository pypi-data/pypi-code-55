import configparser
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
@click.option('--profile_name', prompt='Profile Name', default='default')
@click.option('--account_name', prompt='Account Name')
@click.option('--access_key', prompt='Access Key')
def config(profile_name, account_name, access_key):
    while profile_name != 'default':
        access_key = click.prompt('Authentication failed. Please try again')

    # Repeat getting input until validated.
    while not Session(account_name=account_name, access_key=access_key).validate():
        click.echo('Authentication failed. Please try again')
        account_name = click.prompt('Account Name')
        access_key = click.prompt('Access_key')

    # Write Config
    credential_path = os.path.expanduser('~') + '/.spb/config'
    credential_path = credential_path.replace(os.sep, '/')

    os.makedirs('/'.join(credential_path.split(os.sep)[:-1]), exist_ok=True)

    ret = {
        'account_name': account_name,
        'access_key': access_key,
    }

    config = configparser.ConfigParser()
    config[profile_name] = ret

    with open(credential_path, 'w') as f:
        config.write(f)

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
@click.option('--log', 'log_file', type=click.File('a'))
@click.option('-f', '--force', 'is_force', default=False, is_flag=True)
def upload(dataset_name, log_file, is_force):
    helper.upload(dataset_name, log_file, is_force)


@cli.command()
@click.option('--log', 'log_file', type=click.File('a'))
def download(log_file):
    helper.download(log_file)


@cli.command()
def version():
    click.echo(spb.__version__)
