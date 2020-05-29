#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import requests
from requests.exceptions import ConnectionError
from rich.console import Console
import toml
from toml.decoder import TomlDecodeError

from collections import defaultdict
import os

COLUMN_GAP = 4
DEFAULT_ENDPOINT = 'http://127.0.0.1:8053'
VERSION = 'v1.3.0'

config = {}
console = Console()


def call(method_func, url, **kwargs):
    try:
        res = method_func(url, **kwargs)
    except ConnectionError:
        if config['api_endpoint'] == DEFAULT_ENDPOINT:
            console.print(f"[red bold]ERROR[/] unable to connect default dyns API endpoint - [blue]{config['api_endpoint']}[/], run [green]`dynsctl --help`[/] for details")
        else:
            console.print(f"[red bold]ERROR[/] unable to connect dyns API endpoint - [blue]{config['api_endpoint']}[/]")
        return None

    if res.status_code >= 500:
        console.print("[red bold]ERROR[/] remote service error, please report a bug or contact your administrator")
        return None
    if res.status_code == 400:
        console.print("[red bold]ERROR[/] invalid parameters")
        return None
    if res.status_code == 403:
        console.print(f"[red bold]ERROR[/] endpoint {config['api_endpoint']} is not a leader")
        return None
    if res.status_code == 404:
        console.print(f"[red bold]ERROR[/] not available for now, try again later")
        return None

    return res


def load_endpoint():
    home_dir = os.getenv('HOME')
    dynsrc = os.path.join(home_dir, '.dynsrc')
    settings = toml.load(dynsrc)
    return settings['dynsctl']['leader_endpoint']


@click.group()
@click.option('-A', '--api-endpoint', default='', help=f'dyns API endpoint, defaults to {DEFAULT_ENDPOINT}')
def cli(api_endpoint):
    if api_endpoint != '':
        endpoint = api_endpoint
    else:
        try:
            endpoint = load_endpoint()
        except (ValueError, KeyError, TomlDecodeError):
            console.print(f'[magenta bold]WARNING[/] use default dyns API endpoint - [blue]{DEFAULT_ENDPOINT}[/]')
            endpoint = DEFAULT_ENDPOINT

    endpoint = endpoint.strip('/')
    if endpoint.startswith(':'):
        endpoint = f'http://127.0.0.1{endpoint}'
    if not endpoint.startswith('http'):
        endpoint = f'http://{endpoint}'

    config['api_endpoint'] = endpoint
    config['api_prefix'] = f'{endpoint}/api/v1'


@cli.command()
@click.option('-d', '--domain', default='', help='list records of domain name')
def ls(domain):
    if isinstance(domain, str) and domain != '':
        res = call(requests.get, f"{config['api_prefix']}/domains/{domain}/records")
    else:
        res = call(requests.get, f"{config['api_prefix']}/records")

    if res is None:
        return
    records = res.json()

    headers = ['id', 'domain', 'ttl', 'rtype', 'value', 'lifetime']
    columns = defaultdict(list)
    for r in records:
        r['lifetime'] = r.get('elapsed_after', 'Inf.')
        for h in headers:
            columns[h].append(str(r[h]))

    column_widths = {}
    for h in headers:
        column_widths[h] = max([len(h), *[len(v) for v in columns[h]]]) + COLUMN_GAP

    console.print(f"[yellow bold]{''.join([h.ljust(column_widths[h], ' ').upper() for h in headers])}[/]")
    for i in range(len(columns['id'])):
        row = ''.join([columns[h][i].ljust(column_widths[h], ' ') for h in headers])
        print(row)


@cli.command()
def nodes():
    res = call(requests.get, f"{config['api_prefix']}/members")
    if res is None:
        return
    nodes = res.json()

    headers = ['id', 'address', 'role']
    columns = defaultdict(list)
    for n in nodes:
        for h in headers:
            columns[h].append(str(n[h]))

    column_widths = {}
    for h in headers:
        column_widths[h] = max([len(h), *[len(v) for v in columns[h]]]) + COLUMN_GAP

    console.print(f"[yellow bold]{''.join([h.ljust(column_widths[h], ' ').upper() for h in headers])}[/]")
    for i in range(len(columns['id'])):
        row = ''.join([columns[h][i].ljust(column_widths[h], ' ') for h in headers])
        print(row)


@cli.command()
@click.option('-r', '--rtype', default='A', help='DNS record type, defaults to A')
@click.option('-t', '--ttl', default=30, help='record TTL in seconds, defaults to 30')
@click.option('-E', '--elapsed-after', default='', help='record lifetime duration like 100s and 3d, infinite if not specified')
@click.argument('domain')
@click.argument('value')
def add(rtype, ttl, elapsed_after, domain, value):
    req = {
        'domain': domain,
        'rtype': rtype,
        'ttl': ttl,
        'value': value
    }
    if isinstance(elapsed_after, str) and elapsed_after != '':
        req['elapsed_after'] = elapsed_after

    res = call(requests.post, f"{config['api_prefix']}/records", json=req)
    if res is None:
        return

    console.print(f"[green bold]OK[/]")


@cli.command()
@click.option('-d', '--domain', default='', help='delete all records of domain name')
@click.option('-I', '--record-id', default='', help='delete one record by its ID')
def delete(domain, record_id):
    if domain != '' and record_id != '':
        console.print(f"[red bold]ERROR[/] use -d/--domain and -I/--record-id cannot be used together")
        return

    if domain != '':
        res = call(requests.delete, f"{config['api_prefix']}/domains/{domain}")
    elif record_id != '':
        res = call(requests.delete, f"{config['api_prefix']}/records/{record_id}")
    else:
        console.print(f"[red bold]ERROR[/] missing required option, run [green]`dynsctl delete --help`[/] for details")
        return

    if res is None:
        return

    console.print(f"[green bold]OK[/]")


@cli.command()
def version():
    print(f'Client: {VERSION}')

    server_version = 'UNKNOWN'
    try:
        res = requests.get(f"{config['api_prefix']}/version")
        assert res.status_code == 200
        server_version = res.text
    except:
        pass
    print(f'Server: {server_version}')
