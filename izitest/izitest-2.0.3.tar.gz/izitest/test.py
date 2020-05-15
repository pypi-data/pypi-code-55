# coding: utf-8

from typing import (List, Dict, Any)

from subprocess import (CompletedProcess, TimeoutExpired, run as sprun)

from .betterprint import *
from .testcase import *

__all__ = [
    "Test"
]


class Test(object):
    def __init__(self, raw_test: Dict):
        """Create a new Test object.

        Args:
            raw_test (Dict): yaml dictionnary representation of the test.

        Raises:
            Exception: if any problem occurred when parsing the test.
        """
        if raw_test["name"] is None:
            raise Exception

        checks = raw_test.get("checks", ["same_stdout", "same_stderr", "same_retcode"])

        self.name: str = raw_test["name"]
        self.desc: str = raw_test.get("desc", "")
        self.args: List[str] = raw_test.get("args", [])
        self.stdin: str = raw_test.get("stdin", "")

        self.expect: Dict[str, Any]
        if "expect" in raw_test:
            self.expect = raw_test["expect"] or {
                "stdout": "",
                "stderr": "",
                "retcode": 0
            }
        else:
            self.expect = None

        self.timeout: int = raw_test.get("timeout", 5)
        self.skip: bool = raw_test.get("skip", False)

        self.testcases: List[Testcase] = [Testcase(c) for c in checks]
        self.status: str = ""

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}{f' {self.args}' if self.args else ''}" + \
            f"{self.testcases if len(self.testcases) > 0 else ''}"

    def run(self, ref: List[str], exec: List[str]) -> int:
        """Run the Test.

        It will run both tested and reference executable before performing
        any given check.

        Args:
            exec (List[str]): tested executable.
            ref (List[str]): reference executable.

        Returns:
            int: the return code of the Test (0 if "Passed" or "Skipped", 1 otherwise)
        """
        printinfo("Test", indent=2, end=' ')
        prettyprint(self.name, Color.CYAN, bold=True)

        if self.skip:
            self.status = "Skipped"
            printstatus(self.status, indent=3)
            return 0

        ref_proc: CompletedProcess
        test_proc: CompletedProcess

        if self.expect is not None:
            ref_proc = fake_run_exec(self.expect)
        elif ref is None:
            self.status = "Skipped"
            printwarning("No ref exec", bold=True, indent=3)
            return 0
        else:
            try:
                ref_proc = run_exec(ref + self.args, self.stdin, self.timeout)
            except TimeoutExpired:
                self.status = "Timed out"
                printerror("Ref executable timed out", indent=3)
                return 1

        try:
            test_proc = run_exec(exec + self.args, self.stdin, self.timeout)
        except TimeoutExpired:
            self.status = "Timed out"
            printerror("Tested executable timed out", indent=3)
            return 1

        for tc in self.testcases:
            tc.check(ref_proc, test_proc)

        self.status = "Failed" if any(tc.status == "Failed" for tc in self.testcases) else "Passed"

        return 0 if self.status == "Passed" else 1


def run_exec(exec: List[str], stdin: str, timeout: int) -> CompletedProcess:
    """Run an executable.

    Args:
        exec (List[str]): executable to run (can be followed by arguments).
        stdin (str): input of the program.
        timeout (int): timeout (in sec).

    Returns:
        CompletedProcess: the completed process.

    Raises:
        TimeoutExpired: if the timeout expired.
    """
    return sprun(exec, input=stdin, capture_output=True, timeout=timeout, text=True)


def fake_run_exec(expect: Dict[str, Any]) -> CompletedProcess:
    """Fake the run of an executable.

    Args:
        expect (dict): a dictionnary containing the expected outputs (stdout, stderr, retcode)

    Returns:
        CompletedProcess: a completed process, as if it was run by sp.run()
    """
    # 'or' prevent fake_values to be None, instead they are replaced by a default value
    fake_stdout = expect.get("stdout", '') or ''
    fake_stderr = expect.get("stderr", '') or ''
    fake_retcode = expect.get("retcode", 0) or 0

    return CompletedProcess('', fake_retcode, fake_stdout, fake_stderr)
