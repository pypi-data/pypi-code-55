# coding: utf-8

from typing import Tuple

from subprocess import CompletedProcess

from .betterprint import *
from .checks import run_check

__all__ = [
    "Testcase"
]


class Testcase(object):
    """Testcase object.

    It represents an "instance" of a check.

    Attributes:
        check_name (str): name of the check it perform.
        status (str): status of the check ("Passed" or "Failed").
        diff (str): diff between ref and test.
    """

    def __init__(self, check_name: str):
        """Create a new Testcase object.

        Args:
            check_name (str): name of check it perform.
        """
        self.check_name: str = check_name
        self.status: str = ""
        self.diff: str = ""

    def __str__(self):
        return f"{self.check_name} [{self.status}]"

    def __repr__(self):
        return str(self)

    def check(self, ref: CompletedProcess, test: CompletedProcess):
        """Perform the check.

        It updates status and diff.

        Args:
            ref (CompletedProcess): ref.
            test (CompletedProcess): test.
        """
        printinfo(self.check_name, indent=3, end=' ')

        result: Tuple[bool, str] = run_check(self.check_name, ref, test)
        self.status = "Passed" if result[0] else "Failed"
        self.diff = result[1]

        printstatus(self.status)
