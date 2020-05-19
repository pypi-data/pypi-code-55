from etcetera import api

def main():
    import argparse

    parser = argparse.ArgumentParser(prog='etc', description='etcetera: managing cloud-hosted datasets')

    subparsers = parser.add_subparsers(dest='cmd', help='command')

    parser_ls = subparsers.add_parser('ls', help='List datasets')
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
        for x in api.ls(remote=args.remote):
            print(x)

    elif args.cmd == 'register':
        api.register(args.directory, args.name, force=args.force)

    elif args.cmd == 'pull':
        api.pull(args.name, force=args.force)

    elif args.cmd == 'push':
        api.push(args.name, force=args.force)

    elif args.cmd == 'purge':
        api.purge(args.name)

    else:
        parser.error('Unknown command')


if __name__ == '__main__':
    main()
