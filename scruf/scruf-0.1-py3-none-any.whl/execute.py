import os
import shutil
import subprocess
import tempfile

from scruf import exception


class Executor(object):
    def __init__(self, shell="/bin/sh", cleanup=True, tmpdir="/tmp", env=os.environ):
        self.cleanup = cleanup
        self.shell = shell
        self.env = env

        # Might raise exception, so set this last
        self.testdir = self._mktestdir(tmpdir)

    def __del__(self):
        if self.cleanup and hasattr(self, "testdir"):
            shutil.rmtree(self.testdir)

    @staticmethod
    def _mktestdir(tmpdir):
        try:
            testdir = tempfile.mkdtemp(dir=tmpdir, suffix="scruf")
        except (PermissionError, FileNotFoundError) as e:
            raise FailedToCreateTestDirError(tmpdir, e)
        return testdir

    def execute(self, command):
        p = subprocess.Popen(
            [self.shell, "-"],
            cwd=self.testdir,
            env=self.env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
        )
        stdout, stderr = p.communicate(command)

        return Result(p.returncode, stdout, stderr)


class Result(object):
    def __init__(self, returncode, stdout="", stderr=""):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode

        self._stdout_lines = stdout.splitlines(True)
        self._stderr_lines = stderr.splitlines(True)
        self._stdout_iter = iter(self._stdout_lines)
        self._stderr_iter = iter(self._stderr_lines)

    def next_line(self, source):
        iterator = getattr(self, "_" + source + "_iter")
        try:
            return next(iterator)
        except StopIteration:
            raise OutOfLinesError(source)


class OutOfLinesError(exception.CramerError):
    def __init__(self, source):
        message = "No more lines available for {}".format(source)
        super().__init__(message)

        self.source = source


class FailedToCreateTestDirError(exception.CramerError):
    def __init__(self, dir_name, file_error):
        message = "Could not create temporary directory at {}: {}".format(
            dir_name, str(file_error)
        )
        super().__init__(message)

        self.dir_name = dir_name
