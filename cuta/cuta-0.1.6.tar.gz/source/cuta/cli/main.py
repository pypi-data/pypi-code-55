from typing import List

import typer

import cuta


base = typer.Typer()


@base.command("create")
def create(name: str):
    """
    Create

    Create a new application with the given name.
    """
    api = cuta.from_env()
    api.apps.create(name=name)


@base.command("shell")
def shell(name: str = None):
    """
    Shell

    Start an interactive environment for the given application. If
    no application is given, the current application will be used.
    """
    api = cuta.from_env()
    app = api.apps.get(name)
    app.interact()


@base.command("add")
def add_(deps: List[str], env: str = None):
    """
    Add dependencies

    Add packages required by an application. By default, the
    dependencies will be added to the runtime environment but the
    target environment can be given. For example, development-only
    dependencies (i.e. testing frameworks, linters, etc.) can be
    added to the "dev" environment.
    """
    api = cuta.from_env()
    app = api.apps.get()
    app.add_dependencies(list(deps), env=env)


@base.command("remove")
def remove(deps: List[str], env: str = None):
    """
    Remove dependencies

    Remove packages required by an application.
    """
    api = cuta.from_env()
    app = api.apps.get()
    app.remove_dependencies(list(deps), env=env)


@base.command("build")
def build():
    """
    Build

    Build the current application.
    """
    api = cuta.from_env()
    app = api.apps.get()
    app.build()


@base.command("deploy")
def deploy():
    """
    Deploy

    Deploy the current application.
    """
    api = cuta.from_env()
    app = api.apps.get()
    app.deploy()


@base.command("destroy")
def destroy():
    """
    Destroy

    Destroy application deployment.
    """
    api = cuta.from_env()
    app = api.apps.get()
    app.destroy()
