import click


@click.group()
def netid():
    pass


@netid.group()
def admin():
    pass


@admin.command('check')
@click.argument('netid')
@click.pass_context
def check_admin(ctx, netid):
    instance = ctx.obj['INSTANCE']
    resp = instance.check_admin(netid)
    click.echo('true' if resp['result'] else 'false')


@admin.command('list')
@click.pass_context
def list_admins(ctx):
    instance = ctx.obj['INSTANCE']
    resp = instance.list_admins()
    click.echo('admins:')
    for admin in resp['result']:
        click.echo(f'  - {admin}')


@netid.group()
def user():
    pass


@user.command('check')
@click.argument('netid')
@click.pass_context
def check_user(ctx, netid):
    instance = ctx.obj['INSTANCE']
    resp = instance.check_user(netid)
    click.echo('true' if resp['result'] else 'false')
