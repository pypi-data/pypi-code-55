from typing import NoReturn
import os
import json

import click

import utils_api_client.rest


def fatal_error(err: utils_api_client.rest.ApiException) -> NoReturn:
    body = json.loads(err.body)
    error = body['error']
    click.echo(click.style(f"error #{error['code']}: {error['message']}", fg='red'))
    os._exit(1)  # sys.exit hangs for some reason? idk
