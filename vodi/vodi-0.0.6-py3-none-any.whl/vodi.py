from vodi.ReleaseCommand import ReleaseCommand
from vodi.EnvCommand import EnvCommand
from vodi.LoginCommand import LoginCommand
from vodi.ProjectCommand import ProjectCommand

from vodi import Environments
from vodi import Projects
import click
import os

releaseCommand = ReleaseCommand()
envCommand = EnvCommand()
loginCommand = LoginCommand()
projectsCommand = ProjectCommand()

@click.group()
def cli():
    pass

@cli.command(help='login to an environment')
@click.argument('environment')
def login(environment):
    loginCommand.login(Environments.envs[environment])

@cli.command(help='logout from an environment')
def logout():
    loginCommand.logout()

@cli.group(help='retrive information')
def get():
    pass

@get.command(help='get a list of environments')
def envs():
    envCommand.printAll()

@get.command('releases', help= 'get a list o releases')
def get_releases():
    click.echo("not implemented yet")

@get.command('release', help='get informations on a release')
@click.argument('release')
def get_release(release):
    click.echo("not implemented yet")

@get.command(help='get information on an environment')
@click.argument('environment')
def env(environment):
    envCommand.print(Environments.envs[environment])

@get.command(help='get information on a project')
@click.argument('project')
def project(project):
    projectsCommand.print(project)

@get.command(help='get information all projects')
def projects():
    projectsCommand.printAll()

@cli.command()
def release():
    releaseCommand.doRelease()

@cli.command()
def rollback():
    releaseCommand.doRollback()

@cli.group(help="clone repos or environments")
def clone():
    pass

@clone.command('repo', help="git clone a project to a local directory")
@click.argument('project')
@click.argument('repo')
@click.argument('destination', required=False)
def cloneRepo(project, repo, destination):
    click.echo('not implemented yet')

@clone.command('env', help="Either create a new environment or overwrite it with deployments from an existing source environment")
@click.argument('sourceEnv')
@click.argument('destinationEnv')
def cloneEnv(sourceEnv, destinationEnv):
    click.echo('not implemented yet')

if __name__ == '__main__':
    cli()