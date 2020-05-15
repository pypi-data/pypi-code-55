import click


@click.group()
def token():
    pass


@token.command('create')
@click.pass_context
def create(ctx):
    instance = ctx.obj['INSTANCE']
    resp = instance.create_token()
    click.echo(resp.result)


@token.command('delete')
@click.argument('token')
@click.pass_context
def delete(ctx, token):
    instance = ctx.obj['INSTANCE']
    instance.delete_token(token)
    click.echo('ok')


@token.group()
def scopes():
    pass


@scopes.command('list')
@click.argument('token')
@click.pass_context
def scopes_list(ctx, token):
    instance = ctx.obj['INSTANCE']
    resp = instance.list_scopes(token)
    click.echo('scopes:')
    for scope in resp['result']:
        click.echo(f'  - {scope}')


@scopes.command('grant')
@click.argument('token')
@click.argument('scope')
@click.pass_context
def scopes_grant(ctx, token, scope):
    instance = ctx.obj['INSTANCE']
    instance.grant_scope(token, scope)
    click.echo('ok')


@scopes.command('revoke')
@click.argument('token')
@click.argument('scope')
@click.pass_context
def scope_revoke(ctx, token, scope):
    instance = ctx.obj['INSTANCE']
    instance.revoke_scope(token, scope)
    click.echo('ok')
