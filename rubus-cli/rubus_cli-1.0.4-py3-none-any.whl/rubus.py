import click
import requests
import os
import rubus.admin as a
import rubus.authentication as auth
import rubus.device as d
import rubus.http as http


class Config(object):
    """Config contains the global configuration for Rubus CLI."""

    def __init__(self):
        try:
            baseURL = os.environ['RUBUS_HOSTNAME']
        except Exception:
            baseURL = 'http://localhost:1323'
        self.baseURL = baseURL
        self.headers = None


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@pass_config
def cli(config):
    '''Rubus CLI allows to interact with a running instance of Rubus API.'''
    pass


@cli.command()
@click.option('--info', is_flag=True, help='Display the user\'s credentials.')
@click.option('--login', is_flag=True, help='Log in to receive a token for your session.')
@click.option('--update', is_flag=True, help='Update your credentials.')
@pass_config
def authentication(config, info, login, update):
    try:
        if login:
            auth.login(config.baseURL)
        else:
            config.headers = http.create_headers()
            if info:
                auth.info(config)
            elif update:
                auth.update(config)
    except requests.ConnectionError:
        click.echo('Server is not responding, please try again later.')


@cli.command()
@click.option('--add_user', is_flag=True, help='Create a new user.')
@click.option('--delete_user', help='Delete an existing user.')
@click.option('--list_user', is_flag=True, help='List all the users.')
@click.option('--add_device', is_flag=True, help='Add a new device.')
@click.option('--delete_device', is_flag=True, help='Delete an existing device.')
@pass_config
def admin(config, add_user, delete_user, list_user, add_device, delete_device):
    config.headers = http.create_headers()
    try:
        if add_user:
            a.create_user(config)
        elif delete_user:
            a.delete_user(config, delete_user)
        elif list_user:
            a.list_user(config)
        elif add_device:
            a.add_device(config)
        elif delete_device:
            a.delete_device(config)
    except requests.ConnectionError:
        click.echo('Server is not responding, please try again later.')


@cli.command()
@click.option('--list', is_flag=True, help='List all the available devices.')
@click.option('--get', help='Get information about a device.')
@click.option('--acquire', help='Acquire a device.')
@click.option('--release', help='Release a device.')
@click.option('--deploy', help='Deploy a device.')
@click.option('--on', help='The device\'s id to turn on.')
@click.option('--off', help='The device\'s id to turn off.')
@pass_config
def device(config, list, get, acquire, release, deploy, on, off):
    config.headers = http.create_headers()
    try:
        if list:
            d.list(config)
        elif get:
            d.get(config, get)
        elif acquire:
            d.acquire(config, acquire)
        elif release:
            d.release(config, release)
        elif deploy:
            d.deploy(config, deploy)
        elif on:
            d.on(config, on)
        elif off:
            d.off(config, off)
    except requests.ConnectionError:
        click.echo('Server is not responding, please try again later.')
