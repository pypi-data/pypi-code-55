import os

import click


@click.command()
@click.argument('ipaddr')
@click.pass_context
def dnscheck(ctx, ipaddr):
    instance = ctx.obj['INSTANCE']
    resp = instance.check_dns(ipaddr=ipaddr)
    if resp['status'] == 'error':
        error = resp['error']
        click.echo(click.style(f"error #{error['code']}: {error['message']}", fg='red'))
        os._exit(1)
    else:
        click.echo('hostnames:')
        for hostname in resp['hostnames']:
            click.echo(f'  - {hostname}')
        click.echo('ipaddrs:')
        for ipaddr in resp['ipaddrs']:
            click.echo(f'  - {ipaddr}')
