import sys

import click

from client.client import ShipaException
from commands import constant


@click.group()
def cli_create():
    pass


@cli_create.command("create", short_help=constant.CMD_APP_CREATE)
@click.argument("appname", required=True)
@click.argument("platform", required=False)
@click.option('-d', '--description', help=constant.OPT_APP_CREATE_DESCRIPTION)
@click.option('-f', '--dependency-file', help=constant.OPT_APP_CREATE_DEPENDENCY, multiple=True)
@click.option('-g', '--tag', help=constant.OPT_APP_CREATE_TAG, multiple=True)
@click.option('-p', '--plan', help=constant.OPT_APP_CREATE_PLAN)
@click.option('-r', '--router', help=constant.OPT_APP_CREATE_ROUTER)
@click.option('--router-opts', help=constant.OPT_APP_CREATE_ROUTER_opt, multiple=True)
@click.option('-t', '--team', help=constant.OPT_APP_CREATE_TEAM)
@click.option('-o', '--pool', help=constant.OPT_APP_CREATE_POOL)
@click.pass_obj
def create(ctx, appname, platform, description, dependency_file, tag, plan, router, router_opts, team, pool):
    """Creates a new app using the given name and platform."""

    ctx.check_valid()
    try:
        for router_opt in router_opts:
            opt = router_opt.split('=')
            if len(opt) != 2:
                raise ShipaException('router-opts format is key=value')
        ctx.client.app_create(appname, team=team, pool=pool, platform=platform, description=description,
                              dependency_file=dependency_file, tag=tag, plan=plan, router=router,
                              router_opts=router_opts)

    except ShipaException as e:
        print('{0}'.format(str(e)))
        sys.exit(1)


@click.group()
def cli_remove():
    pass


@cli_remove.command("remove", short_help=constant.CMD_APP_REMOVE)
@click.option('-a', '--app', 'appname', help=constant.OPT_APP_REMOVE_APP, required=True)
@click.pass_obj
def remove(ctx, appname):
    """If the app is bound to any service instance, all binds will be removed before the app gets deleted"""

    ctx.check_valid()
    try:
        ctx.client.app_remove(appname=appname)
        ctx.client.autoscale_check()
        print('App {0} has been removed!'.format(appname))

    except ShipaException as e:
        print('{0}'.format(str(e)))
        sys.exit(1)


@click.group()
def cli_deploy():
    pass


@cli_deploy.command("deploy", short_help=constant.CMD_APP_DEPLOY)
@click.option('-a', '--app', 'appname', help=constant.OPT_APP_DEPLOY_APP, required=True)
@click.option('-d', '--directory', help=constant.OPT_APP_DEPLOY_DIRECTORY, default='.')
@click.option('--steps', help=constant.OPT_APP_DEPLOY_STEPS, default=1)
@click.option('--step-interval', help=constant.OPT_APP_DEPLOY_STEP_INTERVAL, default='1s')
@click.option('--step-weight', help=constant.OPT_APP_DEPLOY_STEP_WEIGHT, default=100)
@click.pass_obj
def deploy(ctx, appname, directory, steps, step_interval, step_weight):
    """Deploys set of directories to shipa server."""

    ctx.check_valid()
    try:
        ctx.client.app_deploy(appname=appname, directory=directory, steps=steps, step_interval=step_interval,
                              step_weight=step_weight)
        ctx.client.autoscale_check()
        print('App {0} has been deployed!'.format(appname))

    except ShipaException as e:
        print('{0}'.format(str(e)))
        sys.exit(1)


@click.group()
def cli_move():
    pass


@cli_remove.command("move", short_help=constant.CMD_APP_REMOVE)
@click.option('-a', '--app', 'appname', help=constant.OPT_APP_REMOVE_APP, required=True)
@click.option('-p', '--pool', help=constant.OPT_APP_CREATE_POOL, required=True)
@click.pass_obj
def move(ctx, appname, pool):
    """ Moves app to another pool """

    ctx.check_valid()
    try:
        ctx.client.app_move(appname=appname, pool=pool)
        ctx.client.autoscale_check()
        print('App {0} has been moved!'.format(appname))

    except ShipaException as e:
        print('{0}'.format(str(e)))
        sys.exit(1)


cli = click.CommandCollection(sources=[cli_create, cli_remove, cli_deploy, cli_move])
