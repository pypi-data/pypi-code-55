import sys
import pkgutil

from ._votingclient import VotingClient
from ._cli import CLI

def test_dependencies ():
    dependencies = {'nacl': 'PyNaCl',
                    'requests': 'requests'}
    missing_packages = [dependencies[pkg] for pkg in dependencies
                        if pkgutil.find_loader(pkg) is None]
    if missing_packages:
        sys.stderr.write('The following Python packages are missing:\n')
        for dependency in missing_packages:
            sys.stderr.write('- ' + dependency + '\n')
        sys.stderr.write('Please install them using pip '
                         'or your distribution\'s package manager.\n')
        sys.exit(1)

def client ():
    import readline
    import os
    import atexit
    import argparse

    test_dependencies()

    hist = os.path.join(os.path.expanduser('~'), '.thc_evoting_client_hist')
    try:
        readline.read_history_file(hist)
        readline.set_history_length(100)
    except:
        pass
    atexit.register(readline.write_history_file, hist)

    print('# This is THC demo e-voting client.')

    ap = argparse.ArgumentParser(description='THC demo e-voting client.')
    opt = ap.add_mutually_exclusive_group(required=True)
    opt.add_argument('-n', '--new', action='store_true', default=False,
                     help='create a new vote')
    opt.add_argument('-s', '--secret', metavar='FILE', type=str,
                     help='path to a secret vote file')
    args = ap.parse_args()

    if args.new:
        srv = input('> Enter server address: ')
        vc = VotingClient.new(srv)
        if vc is None:
            sys.stderr.write('Wrong server address.\n')
            sys.exit(1)
        return CLI(vc).create_vote()
    elif args.secret is not None:
        print('Loading vote from ' + args.secret + '… ', end='')
        sys.stdout.flush()
        vc = VotingClient.from_file(args.secret)
        if vc is None:
            sys.stderr.write('Invalid vote file.\n')
            sys.exit(1)
        print('done.\n')
        return CLI(vc).main()

def main ():
    try:
        return client()
    except KeyboardInterrupt:
        sys.stderr.write('\nOk bye :).\n')
        sys.exit(1)

if __name__ == '__main__':
    main()
