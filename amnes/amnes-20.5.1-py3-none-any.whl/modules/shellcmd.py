"""This module contains all necessary definitions for the Shell Command Base Module.

Classes:
    ShellCommandBase: Base Module for executing shell command on AMNES Worker.
"""

import io
import os
import signal
import subprocess
import time
from subprocess import CalledProcessError, CompletedProcess, TimeoutExpired
from typing import BinaryIO, Optional, Union

from ..core.node_task import NodeTaskFiles, NodeTaskParams
from ..exec.worker.node_module import NodeModule, NodeModuleError
from .features import CustomFilesFeature


class ShellCommandBase(CustomFilesFeature, NodeModule):
    """Base Module for executing shell command on AMNES Worker.

    This base module provides an implementation of the `execute()` method
    for a Node Module, which will execute a specified shell command.

    Example configuration:

    ```yaml
    params:
      command: "myapp -a -b"
      stdout: "PIPE"
      stderr: "module_errors.txt"
      buffersize: 4096
      timeout: 120
      timeouterr: "False"
      sleep: 2
    files: {}
    ```

    The command must be a single string which will be passed to the underlying shell.
    Timeout is specified in seconds but can be `None`.
    By default, if the command execution times out, an error is raised.
    This behavior can be changed by setting `timeouterr` to `False`.
    Buffersize is passed to the subprocess call and uses its value options.
    Stdout and Stderr should be file names or "PIPE", "DEVNULL" or "STDOUT" which
    represent their special file descriptors documented for subprocess.
    If sleep is specified, its value in seconds will be waited before executing the
    shell command.

    Attributes:
        command (str): Shell command which should be executed by node module.
        buffersize (int): Buffersize used for STDOUT and STDERR by subprocess call.
        stdout (Union[int, BinaryIO]): Destination for subprocess call output.
        stderr (Union[int, BinaryIO]): Destination for subprocess call error output.
        timeout (int): Subprocess call timeout in seconds.
        timeouterr (bool): If subprocess timeout error should be an execution error.
        sleep (int): Seconds to sleep before command execution.
    """

    # pylint: disable=useless-super-delegation,too-many-instance-attributes
    def __init__(
        self, params: NodeTaskParams, files: NodeTaskFiles, workdir: str
    ) -> None:
        """Shell command base module constructor method.

        Args:
            params (NodeTaskParams): The parameters required for the execution of the
                                     NodeModule.
            files (NodeTaskFiles): The files required for the execution of the module.
            workdir (str): Working directory for the node module instance.
        """
        super().__init__(params, files, workdir)
        cfgdict = dict(self.params.pairs)
        self.command = cfgdict.get("command")  # type: ignore
        self.buffersize = cfgdict.get("buffersize")  # type: ignore
        self.stdout = cfgdict.get("stdout")  # type: ignore
        self.stderr = cfgdict.get("stderr")  # type: ignore
        self.timeout = cfgdict.get("timeout")  # type: ignore
        self.timeouterr = cfgdict.get("timeouterr")  # type: ignore
        self.sleep = cfgdict.get("sleep")  # type: ignore
        self._result_out: Optional[bytes] = None
        self._result_err: Optional[bytes] = None

    @property
    def command(self) -> str:
        """str: Shell command which should be executed by node module.

        Returns:
            str: Shell command which should be executed by node module.
        """
        return self.__command

    @command.setter
    def command(self, command: Optional[str]) -> None:
        """Sets shell command which should be executed by node module.

        Args:
            command (str): Shell command which should be executed by node module.

        Raises:
            NodeModuleError: If command is None, empty or invalid.
        """
        if command is None:
            raise NodeModuleError(
                message="Shell command not specified."
            ) from ValueError("Given shell command is None.")
        if (not isinstance(command, str)) or (not command) or (command.isspace()):
            raise NodeModuleError(
                message="Invalid or empty command specified."
            ) from ValueError(
                "Given shell command is not a non-empty, non-spaces string."
            )
        self.__command: str = command

    @property
    def buffersize(self) -> int:
        """int: Buffersize used for STDOUT and STDERR by subprocess call.

        Returns:
            int: Buffersize used for STDOUT and STDERR by subprocess call.
        """
        return self.__buffersize

    @buffersize.setter
    def buffersize(self, buffersize: Optional[str]) -> None:
        """Sets buffersize used for STDOUT and STDERR by subprocess call.

        Args:
            buffersize (int): Buffersize used for STDOUT and STDERR by subprocess call.

        Raises:
            NodeModuleError: If invalid buffersize is specified or buffersize is
                             not in permitted value range.
        """
        if buffersize is None:
            self.__buffersize = -1
            return
        if (
            (not isinstance(buffersize, str))
            or (not buffersize)
            or (buffersize.isspace())
        ):
            raise NodeModuleError(
                message="Invalid buffersize specified."
            ) from ValueError(
                "Given buffersize argument is not a non-empty, non-spaces string."
            )
        try:
            size = int(buffersize)
        except ValueError:
            raise NodeModuleError(
                message="Invalid buffersize specified."
            ) from TypeError("Given buffersize cannot be parsed to integer.")
        if size < 0:
            raise NodeModuleError(
                message="Buffersize is outside the permitted value range."
            ) from ValueError("Buffersize must be a non-negative integer.")
        self.__buffersize = size

    @property
    def stdout(self) -> Union[int, BinaryIO]:
        """Union[int, BinaryIO]: Destination for subprocess call output.

        Returns:
            Union[int, BinaryIO]: Destination for subprocess call output.
        """
        return self.__stdout

    @stdout.setter
    def stdout(self, stdout: Optional[str]) -> None:
        """Sets destination for subprocess call output.

        Args:
            stdout (Optional[str]): Output destination string of destination for
                                    subprocess call output.

        Raises:
            NodeModuleError: If invalid output destination string is specified or file
                             cannot be opened.
        """
        self.__stdout = self.__parse_std(stdout, "stdout")

    @property
    def stderr(self) -> Union[int, BinaryIO]:
        """Union[int, BinaryIO]: Destination for subprocess call error output.

        Returns:
            Union[int, BinaryIO]: Destination for subprocess call error output.
        """
        return self.__stderr

    @stderr.setter
    def stderr(self, stderr: Optional[str]) -> None:
        """int: Sets destination for subprocess call error output.

        Args:
            stderr (Optional[str]): Output destination string of destination for
                                    subprocess call error output.

        Raises:
            NodeModuleError: If invalid output destination string is specified or file
                             cannot be opened.
        """
        self.__stderr = self.__parse_std(stderr, "stderr")

    def __parse_std(self, std: Optional[str], desc: str) -> Union[int, BinaryIO]:
        """Parse output destination string to destination.

        Any value will be interpreted as a file path except:
            - `None`: Default PIPE of subprocess.
            - "PIPE": Default PIPE of subprocess.
            - "DEVNULL": Void file descriptor of OS.
            - "STDOUT" (only for stderr): Redirect stderr to stdout.

        Args:
            std (Optional[str]): Output destination string which should be parsed
                                 to destination.
            desc (str): Description of output for error messages.

        Returns:
            Parsed destination of output destination string.

        Raises:
            NodeModuleError: If invalid output destination string is specified or file
                             cannot be opened.
        """
        if std is None:
            return subprocess.PIPE
        if (not isinstance(std, str)) or (not std) or (std.isspace()):
            raise NodeModuleError(
                message=f"Invalid or empty {desc} specified."
            ) from ValueError(
                "Output destination string is not a non-empty, non-spaces string."
            )
        if std == "PIPE":
            return subprocess.PIPE
        if std == "DEVNULL":
            return subprocess.DEVNULL
        if std == "STDOUT":
            if desc == "stdout":
                raise NodeModuleError(
                    message=f"Invalid {desc} specified."
                ) from ValueError("STDOUT can only be used for 'stderr'.")
            return subprocess.STDOUT
        if os.path.sep in std:
            raise NodeModuleError(
                message=f"Value for {desc} contains a directory."
            ) from ValueError("File name must not contain diretories.")
        file = f"{self.workdir}{os.path.sep}{std}"
        self.add_custom_file(file)
        try:
            return open(file, "wb+")
        except OSError as oserr:
            self.remove_custom_file(file)
            raise NodeModuleError(message=f"Could not open file for {desc}.") from oserr

    @property
    def timeout(self) -> Optional[int]:
        """int: Subprocess call timeout in seconds.

        Returns:
            int: Subprocess call timeout in seconds.
        """
        return self.__timeout

    @timeout.setter
    def timeout(self, timeout: Optional[str]) -> None:
        """Sets subprocess call timeout in seconds.

        If `None` is specified, no timeout will be used.

        Args:
            timeout (int): Subprocess call timeout in seconds.

        Raises:
            NodeModuleError: If invalid timeout is specified or timeout is
                             not in permitted value range.
        """
        if timeout is None:
            self.__timeout = None
            return
        try:
            seconds = int(timeout)
        except ValueError:
            raise NodeModuleError(message="Invalid timeout specified.") from TypeError(
                "Given timeout cannot be parsed to integer."
            )
        if seconds < 1:
            raise NodeModuleError(message="Invalid timeout specified.") from ValueError(
                "Timeout is outside the permitted value range."
            )
        self.__timeout = seconds

    @property
    def timeouterr(self) -> bool:
        """bool: If subprocess timeout error should be an execution error.

        Returns:
            bool: If subprocess timeout error should be an execution error.
        """
        return self.__timeouterr

    @timeouterr.setter
    def timeouterr(self, timeouterr: Optional[str]) -> None:
        """Sets if subprocess timeout error should be an execution error.

        Args:
            timeouterr (bool): If subprocess timeout error should be an execution error.

        Raises:
            NodeModuleError: If invalid timeouterr flag is specified.
        """
        if (timeouterr is None) or (timeouterr == "True"):
            self.__timeouterr = True
        elif timeouterr == "False":
            self.__timeouterr = False
        else:
            raise NodeModuleError(
                message="Invalid timeouterr flag specified."
            ) from ValueError("Boolean flag must be 'True', 'False' or unset.")

    @property
    def sleep(self) -> Optional[int]:
        """int: Seconds to sleep before command execution.

        Returns:
            int: Seconds to sleep before command execution.
        """
        return self.__sleep

    @sleep.setter
    def sleep(self, sleep: Optional[str]) -> None:
        """Sets seconds to sleep before command execution.

        If `None` is specified, the command will be executed immediately.

        Args:
            sleep (int): Seconds to sleep before command execution.

        Raises:
            NodeModuleError: If invalid sleep value is specified or sleep value is
                             not in permitted value range.
        """
        if sleep is None:
            self.__sleep = None
            return
        try:
            seconds = int(sleep)
        except ValueError:
            raise NodeModuleError(
                message="Invalid sleep value specified."
            ) from TypeError("Given sleep value cannot be parsed to integer.")
        if seconds < 1:
            raise NodeModuleError(
                message="Invalid sleep value specified."
            ) from ValueError("Sleep value is outside the permitted value range.")
        self.__sleep = seconds

    @staticmethod
    def __run(
        *,
        command: str,
        timeout: Optional[int],
        bufsize: int,
        stdout: Union[int, BinaryIO],
        stderr: Union[int, BinaryIO],
        cwd: str,
    ) -> subprocess.CompletedProcess:
        """Run shell command with child process handling.

        If the execution times out, all processes spawned by the shell are killed.

        Args:
            command (str): Shell command which should be executed by node module.
            timeout: Optional[int]: Subprocess call timeout in seconds.
            bufsize (int): Buffersize used for STDOUT and STDERR by subprocess call.
            stdout (Union[int, BinaryIO]): Destination for subprocess call output.
            stderr (Union[int, BinaryIO]): Destination for subprocess call error output.
            cwd (str): Working directory for the command.

        Returns:
            CompletedProcess: Completed process object holding results and exit code.

        Raises:
            CalledProcessError: If executed command exited with a non-zero exit code.
            TimeoutExpired: If command execution timed out.
            BaseException: If any other exeception occurs on execution.
        """
        # pylint: disable=subprocess-popen-preexec-fn
        with subprocess.Popen(  # noqa: DUO116
            command,
            shell=True,
            bufsize=bufsize,
            stdout=stdout,
            stderr=stderr,
            cwd=cwd,
            preexec_fn=os.setsid,
        ) as process:
            try:
                p_stdout, p_stderr = process.communicate(None, timeout=timeout)
            except TimeoutExpired:
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                process.wait()
                raise
            except BaseException:
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                raise
            retcode = process.poll()
            if retcode:
                raise CalledProcessError(
                    retcode, process.args, output=p_stdout, stderr=p_stderr
                )
        return CompletedProcess(process.args, retcode, p_stdout, p_stderr)

    def execute(self) -> None:
        """Execution of shell command by using internal subprocess library."""
        super().execute()
        if self.sleep:
            time.sleep(self.sleep)
        try:
            result = ShellCommandBase.__run(  # noqa: DUO116
                command=self.command,
                timeout=self.timeout,
                bufsize=self.buffersize,
                stdout=self.stdout,
                stderr=self.stderr,
                cwd=self.workdir,
            )
        except subprocess.CalledProcessError as cperr:
            self._result_out = cperr.stdout
            self._result_err = cperr.stderr
            raise NodeModuleError(
                message=f"Command exited with code {cperr.returncode}."
            )
        except subprocess.TimeoutExpired as texp:
            self._result_out = texp.stdout
            self._result_err = texp.stderr
            if self.timeouterr:
                raise NodeModuleError(
                    message=f"Command execution timed out after {texp.timeout} seconds."
                )
            return
        self._result_out = result.stdout
        self._result_err = result.stderr

    def collect(self) -> None:
        """Store STDOUT and STDERR of executed shell command to persistent storage."""
        if not self.corrupt:
            super().collect()
            self.__collect_std(self.stdout, self._result_out)
            if not self.stderr == subprocess.STDOUT:
                self.__collect_std(self.stderr, self._result_err)

    def __collect_std(self, std: Union[int, BinaryIO], result: Optional[bytes]) -> None:
        """Store content of std destination to persistent storage.

        Args:
            std (Union[str, BinaryIO]): A destination for subprocess call output.
            result (bytes): In-Memory buffer of output.

        Raises:
            NodeModuleError: If PIPE is used for destination but in-memory buffer
                             is not set.
        """
        if isinstance(std, int):
            if std == subprocess.PIPE:
                if result is None:
                    raise NodeModuleError(
                        message="In-Memory buffer for output not set."
                    )
                with io.BytesIO(result) as stream:
                    self.store_io(stream)
        else:
            self.store_io(std)

    def cleanup(self) -> None:
        """Empty cleanup implementation."""
        super().cleanup()
