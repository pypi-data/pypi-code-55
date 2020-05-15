import click


@click.group()
def google():
    pass


@google.command('filegive')
@click.argument('from_')
@click.argument('to')
@click.pass_context
def filegive(ctx, from_, to):
    instance = ctx.obj['INSTANCE']
    resp = instance.file_give(from_, to)
    click.echo('shared files:')
    for file in resp['result']:
        click.echo(f'  - {file}')


@google.group('user')
def user():
    pass


@user.command('rename')
@click.argument('account')
@click.argument('alias')
@click.pass_context
def create_alias(ctx, account, alias):
    instance = ctx.obj['INSTANCE']
    instance.rename_account(account, alias)
    click.echo('ok')
