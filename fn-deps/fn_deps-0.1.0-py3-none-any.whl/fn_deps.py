#!/usr/bin/env python3

import json
import os
import site
import sys
from pathlib import Path
import re

import click

import sh
from git import Repo
from termcolor import colored
from terminaltables import SingleTable


@click.group()
def cli():
    pass


@cli.command()
@click.argument("version")
@click.option("--path", default=".", help="The root of the dependencies")
@click.option("--username", default=None, help="PyPi username")
@click.option("--password", default=None, help="PyPi password")
@click.option("--dryrun/--no-dryrun", default=False, help="Perform dryrun")
def publish(version, path, username, password, dryrun):
    path = Path(path)

    if (path / "pyproject.toml").exists():
        publish_poetry(path, version, username, password, dryrun)
    else:
        click.echo("Currently only poetry projects are supported")


def publish_poetry(path, version_bump, username, password, dryrun):
    repo = Repo(path)

    branch = repo.active_branch
    branch = branch.name
    if branch != "master":
        click.echo(f"The repo at {path} is not on master")
        return False

    num_changes = len(repo.head.commit.diff(None))
    if num_changes:
        click.echo(f"This repo at {path} has uncommitted changed")
        return False

    previous_commit = sh.git("rev-parse", "HEAD").strip()

    with sh.pushd(path):
        try:
            sh.git.pull("--ff-only", "origin", "master")

            click.echo(sh.poetry("version", version_bump))

            version = sh.poetry("version", "--no-ansi")

            sh.dephell("deps", "convert")

            sh.git("add", "setup.py")

            click.echo(f"Commit {version}")

            sh.git("commit", "-a", "-m", f"Update version to {version} and publish")

            click.echo(f"Building {version}")

            sh.poetry("build")

            click.echo(f"Pushing {version}")
            if not dryrun:
                pattern = r"\d+\.\d+\.\d+.*"
                tag_version = re.search(pattern, str(version)).group()
                sh.git("tag", "-a", f"v{tag_version}", "-m", f"Release v{tag_version}")
                sh.git("push", "origin", "master")
                sh.git("push", "origin", "--tags")

            click.echo(f"Publishing {version}")

            if not dryrun:
                if username and password:
                    sh.poetry("publish", "-u", username, "-p", password)
                else:
                    sh.poetry("publish")

            click.echo(f"Published {version}")

            if dryrun:
                raise Exception("Reverting for dry run")

        except Exception as e:
            click.echo(e)
            sh.git("reset", previous_commit)
            sh.git("reset", "--hard")
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
