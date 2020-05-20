from __future__ import absolute_import
import fire

from ddc.task_meta import start_meta
from ddc.info import __version__


class Cli(object):
    """Devision Developers Cli Lib. Version {v}""".format(v=__version__)

    def meta(self):
        """Start Meta App in dev mode"""
        start_meta()


def main():
    fire.Fire(Cli(), name='ddc')


if __name__ == '__main__':
    main()
