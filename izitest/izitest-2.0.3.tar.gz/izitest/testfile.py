# coding: utf-8

from typing import (List, Dict)

from pathlib import Path

import yaml

from .betterprint import *
from .test import *

__all__ = [
    "Testfile"
]


class Testfile(object):
    def __init__(self, path: Path):
        self.path: Path = path
        self.tests: List[Test] = []

        with open(self.path, 'r') as f:
            raw_tests: List = yaml.safe_load(f.read())

        if raw_tests is not None:
            for rt in raw_tests:
                try:
                    t = Test(rt)
                    self.tests.append(t)
                except:
                    continue

    def __str__(self):
        return f"{self.path} ({len(self.tests)})"

    def __repr__(self):
        return f"{self.path} {self.tests}"

    def run(self, ref: List[str], exec: List[str]) -> int:
        """Run all tests in the Testfile

        Args:
            exec (List[str]): tested executable.
            ref (List[str]): reference executable.

        Returns:
            int: the return code of the Testfile (0 if "Passed" or "Skipped", 1 otherwise)
        """
        printinfo("Running tests in", indent=1, end=' ')
        prettyprint(str(self.path), Color.BLUE, bold=True)

        if len(self.tests) == 0:
            printwarning("No test to run", indent=2)

        status: int = 0
        for t in self.tests:
            if t.run(ref, exec) == 1:
                status = 1

        return status
