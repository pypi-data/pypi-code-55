# Copyright (c) 2017 Civic Knowledge. This file is licensed under the terms of the
# MIT License, included in this distribution as LICENSE

"""

"""

from os import remove
from os.path import exists
import argparse
from metapack.cli.core import prt, err, warn
from metapack.cli.core import  get_config as _get_config
from metapack.cli.core import MetapackCliMemo as _MetapackCliMemo
from metapack import Downloader
from github import Github

downloader = Downloader.get_instance()

class ArgumentError(Exception): pass

class MetapackCliMemo(_MetapackCliMemo):

    def __init__(self, args, downloader):
        super().__init__(args, downloader)

def github(subparsers):
    """
    Using this function requires  a Github token to be set in the ~/.metapack.yaml  file:

        github:
            token: < ... token ... >

    """


    parser = subparsers.add_parser('github',
                                   help='Create and modify github repositories',
                                   description=github.__doc__,
                                   formatter_class=argparse.RawDescriptionHelpFormatter,
                                   )

    parser.set_defaults(run_command=run_github)

    #parser.add_argument('-j', '--json', default=False, action='store_true',
    #                    help='Display configuration and diagnostic information ad JSON')

    subparsers = parser.add_subparsers()

    ## Initialize a local repository

    load = subparsers.add_parser('init', help='Initialize a Package')
    load.set_defaults(sub_command=run_init_cmd)
    # load.add_argument('-C', '--clean', default=False, action='store_true',
    #                  help='Delete everything from the database first')
    # load.add_argument('urls', nargs='*', help="Database or Datapackage URLS")

    ## Create a remote instance

    info = subparsers.add_parser('remote', help='Create a remote for this package')
    info.set_defaults(sub_command=run_remote_cmd)

    #info.add_argument('url', help="Database or Datapackage URL")

    parser.add_argument('metatabfile', nargs='?', help="Path to a notebook file or a Metapack package")


def run_github(args):
    m = MetapackCliMemo(args, downloader)

    args.sub_command(m)



def get_config():
    config = _get_config()

    if config is None:
        err("No metatab configuration found. Can't get Github credentials. Maybe create '~/.metapack.yaml'")

    if not config.get('github', {}).get('token'):
        err('No token set in config file at github.token')

    return config

def get_token():

    return get_config().get('github', {}).get('token')

def get_or_new_github_repo(g, m):

    from github import UnknownObjectException

    org_name = get_config().get('github').get('organization')

    org = g.get_organization(org_name)

    try:
        repo = org.get_repo( m.doc.nonver_name)
    except UnknownObjectException:
        repo = org.create_repo( m.doc.nonver_name, description=m.doc.description)

    return repo

def get_or_init_local_repo(m):
    """Either get the repo, or initialize and commit everything"""

    import git

    try:
        r = git.Repo(m.doc.ref.fspath.parent)

    except git.exc.InvalidGitRepositoryError:
        r = git.Repo.init(m.doc.ref.fspath.parent)
        r.git.add('-A')
        r.git.commit('-a','-m','Initial Commit')

    return r



def run_init_cmd(m):

    from git.exc import GitCommandError

    g = Github(get_token())

    remote_r = get_or_new_github_repo(g, m)
    local_r = get_or_init_local_repo(m)

    try:
        origin = local_r.remote('origin')
    except (ValueError, GitCommandError):
        origin = local_r.create_remote('origin', remote_r.clone_url)
        #local_r.create_head('master', origin.refs.master)
        local_r.git.push('--set-upstream','origin','master')

    prt(f'Initialized local and remote {origin.refs.master} at {remote_r.clone_url}')


def run_remote_cmd(m):
    pass

