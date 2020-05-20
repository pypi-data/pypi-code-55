from __future__ import absolute_import

import logging
import os

import fire

from ddc.task_lint import start_lint
from ddc.task_meta import start_meta
from ddc.info import print_about_version


class Cli(object):
    """Devision Developers Cli Lib"""

    def __init__(self) -> None:
        super().__init__()
        self.cwd = os.getcwd()

    def meta(self, workdir=None):
        """
        Start Meta App in dev mode
        :param workdir: str. By default is current dir
        :return:
        """
        if not workdir:
            workdir = self.cwd
        logging.info("Work dir: " + workdir)
        start_meta(self.cwd)

    def lint(self, lang="py", workdir=None):
        """
        Start lint of current directory
        :param workdir: str. By default is current dir
        :param lang: str Can be: [ py | php ]
        :return:
        """
        if not workdir:
            workdir = self.cwd
        logging.info("Work dir: " + workdir)
        start_lint(workdir, lang)

    def version(self):
        """Show the ddc version information"""
        print_about_version()


def main():
    fire.Fire(Cli, name="ddc")


if __name__ == "__main__":
    main()
