#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import requests
from requests.exceptions import ConnectionError
from rich.console import Console

from collections import defaultdict

COLUMN_GAP = 4

config = {}
console = Console()


@click.group()
@click.option('-A', '--api-endpoint', default='http://127.0.0.1:8053', help='dyns API endpoint')
def cli(api_endpoint):
    endpoint = api_endpoint.rstrip('/')
    if not endpoint.startswith('http'):
        endpoint = f'http://{endpoint}'

    config['api_endpoint'] = endpoint
    config['api_prefix'] = f'{endpoint}/api/v1'


@cli.command()
def ls():
    try:
        res = requests.get(f"{config['api_prefix']}/records")
    except ConnectionError:
        console.print(f"[red bold]ERROR[/] unable to connect dyns API endpoint - [blue]{config['api_endpoint']}[/]")
        return

    records = res.json()
    headers = ['id', 'domain', 'ttl', 'rtype', 'value']
    columns = defaultdict(list)
    for r in records:
        for h in headers:
            columns[h].append(str(r[h]))

    column_widths = {}
    for h in headers:
        column_widths[h] = max([len(h), *[len(v) for v in columns[h]]]) + COLUMN_GAP

    console.print(f"[yellow bold]{''.join([h.ljust(column_widths[h], ' ').upper() for h in headers])}[/]")
    for i in range(len(columns['domain'])):
        print(''.join([columns[h][i].ljust(column_widths[h], ' ') for h in headers]))


@cli.command()
@click.option('-r', '--rtype', default='A', help='DNS record type')
@click.option('-t', '--ttl', default=30, help='record TTL in seconds')
@click.option('-E', '--elapsed-after', default='', help='record lifetime in seconds')
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

    try:
        res = requests.post(f"{config['api_prefix']}/records", json=req)
    except ConnectionError:
        console.print(f"[red bold]ERROR[/] unable to connect dyns API endpoint - [blue]{config['api_endpoint']}[/]")
        return

    if res.status_code != 201:
        console.print(f"[red bold]ERROR[/] invalid parameters")
        return

    result = res.json()
    console.print(f"[green bold]OK[/] - [white]{result['id']}[/]")


@cli.command()
@click.option('-d', '--domain', default=False, is_flag=True, help='delete all domain records')
@click.option('-I', '--record-id', default=False, is_flag=True, help='delete record by its ID')
@click.argument('value')
def delete(domain, record_id, value):
    if domain == record_id:
        console.print(f"[red bold]ERROR[/] use -d/--domain or -I/--record-id to specify value type")
        return

    try:
        if domain:
            res = requests.delete(f"{config['api_prefix']}/domains/{value}")
        else:
            res = requests.delete(f"{config['api_prefix']}/records/{value}")
    except ConnectionError:
        console.print(f"[red bold]ERROR[/] unable to connect dyns API endpoint - [blue]{config['api_endpoint']}[/]")
        return

    if res.status_code != 204:
        console.print(f"[red bold]ERROR[/] invalid parameters")
        return

    console.print(f"[green bold]OK[/]")
