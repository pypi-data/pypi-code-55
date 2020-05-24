# PYTHON_ARGCOMPLETE_OK
"""Command line interface 'alfa-ci'"""

import argparse
import subprocess
import sys
from pathlib import Path
import argcomplete

from alfaci.version import PKG_VERSION
from alfaci.repo import init_repo


class ArgumentParser(argparse.ArgumentParser):
    """Specialized arg parser with custom error handling"""
    def error(self, message):
        self.print_help(sys.stderr)
        self.exit(2, '%s: error: %s\n' % (self.prog, message))


def print_shell_setup(_args):
    """Print the argcomplete bash hook to be eval'ed by the user"""
    print(
        subprocess.run(['register-python-argcomplete', 'alfa-ci'],
                       capture_output=True,
                       check=True).stdout.decode('UTF-8'))


def print_version(_args):
    """Print the package version defined in the setup.py metadata"""
    print(PKG_VERSION)


def init(_args):
    """Initialize the current working directory as environment repo"""
    repo = init_repo(Path.cwd())
    print('Initialized empty alfa-ci repository in %s' % repo.location)


def main():
    """Main entry function called from the CLI"""
    parser = ArgumentParser(description='Manage alfa-ci environments.')
    subparsers = parser.add_subparsers(title='COMMANDS')

    shell_setup_parser = subparsers.add_parser(
        'shell-setup',
        add_help=False,
        help='run \'eval "$(alfa-ci shell-setup)"\' to enable shell completion'
        ', e.g. from your ~/.bashrc')
    shell_setup_parser.set_defaults(func=print_shell_setup)

    version_parser = subparsers.add_parser('version',
                                           add_help=False,
                                           help='show version number and exit')
    version_parser.set_defaults(func=print_version)

    init_parser = subparsers.add_parser('init',
                                        add_help=False,
                                        help='initialize environment repo')
    init_parser.set_defaults(func=init)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
        sys.exit(0)
    else:
        parser.print_help()
        sys.exit(2)


if __name__ == '__main__':
    main()
