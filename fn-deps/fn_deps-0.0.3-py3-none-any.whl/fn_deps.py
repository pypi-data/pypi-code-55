#!/usr/bin/env python3

import json
import os
import site
import sys
from pathlib import Path

import click

import sh
from git import Repo
from termcolor import colored
from terminaltables import SingleTable


@click.group()
def cli():
    pass


@cli.command()
@click.option("--path", default=".", help="The root of the dependencies")
@click.option("--username", default=None, help="PyPi username")
@click.option("--password", default=None, help="PyPi password")
@click.argument("version")
def publish(version, path, username, password):
    path = Path(path)

    if (path / "pyproject.toml").exists():
        publish_poetry(path, version, username, password)
    else:
        click.echo("Currently only poetry projects are supported")


# @cli.command()
# @click.option("--path", default=".", help="The root of the dependencies")
# @click.option("--username", default=None, help="PyPi username")
# @click.option("--password", default=None, help="PyPi password")
# @click.argument("version")
def publish_poetry(path, version, username=None, password=None):
    repo = Repo(path)

    branch = repo.active_branch
    branch = branch.name
    if branch != "master":
        click.echo(f"The repo at {path} is not on master")
        return False

    num_changes = len(repo.head.commit.diff(None))
    if num_changes:
        click.echo(f"This repo at {path} has uncommited changed")
        return False

    previous_commit = sh.git("rev-parse", "HEAD").strip()

    with sh.pushd(path):
        try:
            sh.git.pull("--ff-only", "origin", "master")

            sh.poetry("version", version)

            sh.dephell("deps", "convert")

            sh.git("add", "setup.py")
            sh.git(
                "commit",
                "-a",
                "-m",
                f"Update version to {sh.poetry('version')} and publish",
            )

            click.echo(f"Building {sh.poetry('version')}")

            sh.poetry("build")

            click.echo(f"Pushing {sh.poetry('version')}")

            sh.git("push", "origin", "master")

            click.echo(f"Publishing {sh.poetry('version')}")

            if username and password:
                sh.poetry("publish", "-u", username, "-p", password)
            else:
                sh.poetry("publish")

            click.echo(f"Published {sh.poetry('version')}")

        except Exception as e:
            click.echo(e)
            sh.git("reset", "--hard")
            sh.git("reset", previous_commit)
            click.echo(f"Reverted to previous commit {previous_commit}")

    return True


# def activate_venv():

#     bin_dir = os.path.abspath("venv/bin")
#     base = bin_dir

#     # prepend bin to PATH (this file is inside the bin directory)
#     os.environ["PATH"] = os.pathsep.join(
#         [bin_dir] + os.environ.get("PATH", "").split(os.pathsep)
#     )
#     os.environ["VIRTUAL_ENV"] = base  # virtual env is right above bin directory

#     # add the virtual environments libraries to the host python import mechanism
#     prev_length = len(sys.path)
#     for lib in "lib".split(os.pathsep):
#         path = os.path.realpath(os.path.join(bin_dir, lib))
#         site.addsitedir(path)
#     sys.path[:] = sys.path[prev_length:] + sys.path[0:prev_length]

#     sys.real_prefix = sys.prefix
#     sys.prefix = base


# @cli.command()
# @click.option("--path", default=".", help="The root of the dependencies")
# @click.option("--username", default=None, help="PyPi username")
# @click.option("--password", default=None, help="PyPi password")
# @click.argument("version")
# def publish_dash(path, version, username=None, password=None):
#     repo = Repo(path)

#     branch = repo.active_branch
#     branch = branch.name
#     if branch != "master":
#         click.echo(f"The repo at {path} is not on master")
#         return False

#     num_changes = len(repo.head.commit.diff(None))
#     if num_changes:
#         click.echo(f"This repo at {path} has uncommitted changed")
#         return False

#     previous_commit = sh.git("rev-parse", "HEAD")

#     with sh.pushd(path):
#         try:
#             activate_venv()
#             print(sh.python("--version"))
#             # sh.git("pull", "--ff-only", "origin", "master")
#             sh.npm("version", version)

#             with open("package.json") as f:
#                 package_json = json.load(f)
#                 package_version = package_json["version"]
#                 package_name = package_json["name"]

#             click.echo(f"Building npm package {package_name}=={package_version}")
#             sh.npm("run", "build")

#             click.echo(f"Building python package {package_name}=={package_version}")
#             sh.python("setup.py", "sdist")

#             sh.git("commit", "-a", "-m", f"Publish version {package_version}")
#             # sh.git("push", "origin", "master")

#             click.echo(f"Uploading python package {package_name}=={package_version}")
#             sh.twine("upload", "dist/*")
#             sh.rm("-rf", "dist")

#             click.echo(f"Publishing NPM package {package_name}=={package_version}")
#             sh.npm("publish")

#         except Exception as e:

#             # sh.git("reset", "--hard", previous_commit)
#             raise


if __name__ == "__main__":
    cli()
