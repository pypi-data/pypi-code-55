import json
import atexit
import os
import os.path

import click

import utils_api_client

import utils_cli.api_token
import utils_cli.dnscheck
import utils_cli.netidcheck
import utils_cli.google
from utils_cli.util import fatal_error


@click.group()
@click.option('-c', '--credentials', default='~/.config/utils-api-credentials.json',
              type=click.Path(), help='File containing API credentials.')
@click.option('-b', '--base-url', default=None,
              type=str, help='API base URL.')
@click.pass_context
def root(ctx, credentials, base_url):
    ctx.ensure_object(dict)
    with open(os.path.expanduser(credentials), 'r') as f:
        credentials = json.load(f)
    config = utils_api_client.Configuration()
    if base_url is not None:
        config.host = base_url
    elif credentials.get('host'):
        config.host = credentials['host']
    else:
        config.host = "http://localhost:5000"
    config.api_key['Utils-API-Token'] = credentials['token']
    ctx.obj['INSTANCE'] = utils_api_client.DefaultApi(utils_api_client.ApiClient(config))


root.add_command(utils_cli.api_token.token)
root.add_command(utils_cli.dnscheck.dnscheck)
root.add_command(utils_cli.netidcheck.netid)
root.add_command(utils_cli.google.google)


def main():
    try:
        atexit.register(lambda: os._exit(0))
        root()
    except utils_api_client.rest.ApiException as err:
        fatal_error(err)
