# coding: utf-8

from typing import (List, Dict, TextIO)

from datetime import datetime as dt

from pathlib import Path
from argparse import ArgumentParser

from jinja2 import (Environment, PackageLoader, select_autoescape)

import izitest.betterprint

from .betterprint import *
from .path import *
from .testfile import *

__all__ = [
    "Testsuite",
    "init_testsuite"
]


class Testsuite(object):
    """Testsuite object.

    Attributes:
        exec (List[str]): executable to test (may be followed by arguments).
        dir (Path): path to directory containing tests.
        ref (List[str]): reference executable (may be followed by arguments).
        report (Path): path to html report file (if None, no report will be generated).
        testfiles (List[Path]): files composing the testsuite.
        status (Dict[str, int]): status of executed tests (WARNING! it is only updated when calling retrieve_status).
    """

    def __init__(self, exec: List[str], dir=Path("./tests"), ref: List[str] = None,
                 quiet=False, memcheck=False, cat: List[str] = None, report: Path = None):
        """Create a new Testsuite object.

        Args:
            exec (List[str]): executable to test (may be followed by arguments).
            dir (Path, optional): path to directory containing tests. Defaults to "./tests".
            ref (List[str], optional): reference executable (may be followed by arguments). Defaults to None.
            quiet (bool, optional): bool indicating if Testsuite should be quiet. Defaults to False.
            memcheck (bool, optional): bool indicating if memory checks are performed. Defaults to False.
            cat (List[str], optional): category filter (if None, all categories are "active"). Defaults to None.
            report (Path, optional): path to html report file (if None, no report is generated). Defaults to None.
        """

        self.exec: List[str] = exec
        self.dir: Path = dir
        self.ref: List[str] = ref
        self.report: Path = report

        self.quiet: bool = quiet
        if self.quiet:
            izitest.betterprint.G_QUIET = True

        self.memcheck: bool = memcheck
        self.cat: List[str] = cat

        self.testfiles: List[Testfile] = []
        self.status: Dict[str, int] = None

        # Must be sorted using str (string representation) to have a 'tree-like' order
        yamlfiles: List[Path] = sorted(self.dir.rglob("*.yaml"), key=str)
        if cat is None:
            self.testfiles = [Testfile(f) for f in yamlfiles]
        else:
            for f in yamlfiles:
                if any(c in str(f) for c in cat):
                    self.testfiles.append(Testfile(f))

        printinfo("Discovered", end=' ')
        printinfo(len(self.testfiles), bold=True, end=' ')
        printinfo("file(s)")

    def __str__(self):
        return f"Testing {' '.join(self.exec)} (dir: '{self.dir}')"

    def __repr__(self):
        return f"Exec: {' '.join(self.exec)}\n" + \
            f"Ref: {' '.join(self.ref) if self.ref is not None else 'None'}" + '\n' \
            f"Dir: {self.dir}\n" + \
            f"Report: {self.report}\n" + \
            f"Categories: {self.cat if self.cat is not None else 'all'}\n" + \
            f"Testfiles: {list(str(f) for f in self.testfiles)}\n" + \
            f"Status: {self.status}"

    def run(self) -> int:
        """Run the Testsuite.

        Returns:
            int: the return code of the Testsuite (0 if "Passed" or "Skipped", 1 otherwise)
        """
        printinfo("Running Testsuite")

        status: int = 0
        for tf in self.testfiles:
            if tf.run(self.ref, self.exec) == 1:
                status = 1

        if self.report is not None:
            self.retrieve_status()

            template = Environment(loader=PackageLoader("izitest", "jinja2"),
                                   autoescape=select_autoescape("html")).get_template('report.html.j2')

            timestamp = dt.now().strftime("%Y-%m-%d at %T")
            report = template.render(testsuite=self, timestamp=timestamp)

            with open(self.report, 'w') as f:
                f.write(report)

        return status

    def retrieve_status(self):
        """Retrieve Testsuite status.

        The status is the number of Tests passed/failed/...
        """
        self.status = {
            "Passed": 0,
            "Failed": 0,
            "Skipped": 0,
            "Timed out": 0
        }

        for tf in self.testfiles:
            for t in tf.tests:
                self.status[t.status] += 1

        return self.status


def init_testsuite() -> Testsuite:
    """Parse CLI arguments and create a Testsuite object.

    Also check if exec (and ref, if any) are regular executable files and testdir is a valid directory.

    Returns:
        Testsuite: created Testsuite object.

    Raises:
        Exception: if arguments checks fail.
    """

    parser = ArgumentParser(description="Easily build a test suite.", allow_abbrev=True)

    parser.add_argument("exec", type=str, help="path to the executable you want to test")
    parser.add_argument("--ref", metavar="ref", type=str, help="specify a reference executable")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="run silently, do not output ANYTHING (even errors)!")
    parser.add_argument("-d", "--testdir", metavar="dir", type=Path, default=Path("./tests"),
                        help="path to the test suite directory (default is './tests')")
    parser.add_argument("-c", "--cat", metavar="cat", nargs='+', type=str,
                        help="run only the tests of specified categories")
    parser.add_argument("-m", "--memcheck", action="store_true",
                        help="if set, it will check for any memory leak using valgrind (see https://valgrind.org/)")
    parser.add_argument("-r", "--report", metavar="file", nargs='?', type=Path, const=Path("./report.html"),
                        help="generate an html report (default path is './report.html')")

    args = parser.parse_args()

    check_dir(args.testdir)

    args.exec = args.exec.split(' ')
    args.exec[0] = which(args.exec[0])

    if args.ref is not None:
        args.ref = args.ref.split(' ')
        args.ref[0] = which(args.ref[0])

    return Testsuite(args.exec, args.testdir, args.ref, args.quiet, args.memcheck, args.cat, args.report)
