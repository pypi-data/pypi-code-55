

import click
from git_util import git_util


@click.group()
def cli():
    pass


@cli.command()
@click.argument('repo-input')
@click.option('--git-host-local-path', type=click.Path())
def clone(repo_input, git_host_local_path):

    result, repo_path = git_util.clone(repo_input, git_host_local_path)

    if result:
        print(f"Repo '{repo_input}' cloned to '{repo_path}'")
    else:
        raise NotImplementedError
