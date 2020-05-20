from __future__ import absolute_import
import fire

from ddc.task_meta import start_meta
from ddc.info import __version__, print_about_version


class Cli(object):
    """Devision Developers Cli Lib"""

    def meta(self):
        """Start Meta App in dev mode"""
        start_meta()

    def version(self):
        """Show the ddc version information"""
        print_about_version()


def main():
    fire.Fire(Cli(), name='ddc')


if __name__ == '__main__':
    main()
