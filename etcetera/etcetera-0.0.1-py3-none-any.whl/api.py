from typing import Optional
from .config import Config
from .engine import Engine
from .repo import Repo


def dataset(name:str, auto_pull=False, config=None):
    '''Returns :class:`etcetera.Dataset` object, given a dataset name.

    Args:
        name (str):               the name of the dataset
        auto_pull(bool):          if set, automatically pulls the dataset from the cloud
        config (etcetera.Config): configuration to use
    '''
    if config is None:
        config = Config.load()

    engine = Engine(config.home)
    if not engine.is_local_dataset(name):
        if not auto_pull:
            raise RuntimeError(f'Local dataset {name} not found. Please pull it.')

        pull(name, config=config)

    return engine.dataset(name)


def pull(name:str, force=False, config=None):
    '''Pull dataset from cloud storage.

    Args:
        name (str):               dataset name
        force (bool):             if True, overrides the existing local dataset
        config (etcetera.Config): configuration to use
    '''
    if config is None:
        config = Config.load()

    repo = Repo.load(config.url, **config.conf)

    engine = Engine(config.home)
    engine.pull(name, repo, force=force)


def push(name:str, force=False, config=None):
    '''Pushes dataset to the cloud.

    Args:
        name (str):      dataset name
        force (bool):    if true, overrides remote dataset
        config (etcetera.Config):  configuration to use
    '''
    if config is None:
        config = Config.load()

    repo = Repo.load(config.url, **config.conf)

    engine = Engine(config.home)
    engine.push(name, repo, force=force)


def register(dirname:str, name:Optional[str]=None, force=False, config=None):
    '''Register local directory as a dataset.

    Args:
        dirname (str):     path to the local directory with data
        name (str):        dataset name (if not specified, directory name is used)
        force (bool):      allows overriding existing dataset
        config (etcetera.Config): configuration to use
    '''
    if config is None:
        config = Config.load()

    engine = Engine(config.home)
    engine.register(dirname, name, force=force)


def purge(name:str, config=None):
    '''Deletes local dataset.

    Args:
        name (str): dataset name
        config (etcetera.Config): configuration to use
    '''
    if config is None:
        config = Config.load()

    engine = Engine(config.home)
    engine.purge(name)


def ls(remote=False, config=None):
    '''Lists datasets.

    By the default, local datasets are listed.

    Args:
        remote (bool): if True, list remote datasets
        config (etcetera.Config): configuration to use
    '''
    if config is None:
        config = Config.load()

    if remote:
        repo = Repo.load(config.url, **config.conf)
        for x in repo.ls():
            if x.endswith('.tgz'):
                yield x[:-4]
    else:
        engine = Engine(config.home)
        yield from engine.ls()


def main():
    import argparse

    parser = argparse.ArgumentParser(prog='etc', description='etc command-line engine')

    subparsers = parser.add_subparsers(dest='cmd', help='command')

    parser_ls = subparsers.add_parser('ls')
    parser_ls.add_argument('-r', '--remote', action='store_true', help='List remote repository')

    parser_register = subparsers.add_parser('register', help='Register directory as a dataset')
    parser_register.add_argument('directory', help='dataset directory')
    parser_register.add_argument('name', default=None, help='dataset name')
    parser_register.add_argument('-f', '--force', action='store_true', help='Force override if local dataset exists')

    parser_pull = subparsers.add_parser('pull', help='Pull dataset from repository')
    parser_pull.add_argument('name', help='Dataset name')
    parser_pull.add_argument('-f', '--force', action='store_true', help='Force download even if local dataset exists')

    parser_push = subparsers.add_parser('push', help='Push dataset to the repository')
    parser_push.add_argument('name', help='Dataset name')
    parser_push.add_argument('-f', '--force', action='store_true', help='Force upload even if dataset exists in the repository')

    parser_purge = subparsers.add_parser('purge', help='Purge local dataset')
    parser_purge.add_argument('name', help='Dataset name')

    args = parser.parse_args()

    if args.cmd == 'ls':
        for x in ls(remote=args.remote):
            print(x)

    elif args.cmd == 'register':
        register(args.directory, args.name, force=args.force)

    elif args.cmd == 'pull':
        pull(args.name, force=args.force)

    elif args.cmd == 'push':
        push(args.name, force=args.force)

    elif args.cmd == 'purge':
        purge(args.name)

    else:
        parser.error('Unknown command')


if __name__ == '__main__':
    main()