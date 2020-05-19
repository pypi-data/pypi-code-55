import sys
import os
from loguru import logger
import click
import asyncio
from asyncio.subprocess import PIPE, STDOUT
from typing import List


def setup_logger():

    logger.remove()
    logger.add(
        sys.stdout,
        enqueue=True,
        level="DEBUG",
        format="<green>{time:HH:mm:ss zz}</green> | <cyan>{process}</cyan> | <level>{message}</level>",
    )


async def _command_loop(cmd: List[str], cwd: str = None, timeout: int = 600) -> int:

    timeout = 600
    if not cwd:
        cwd = os.getcwd()
    # start child process
    try:
        assert (
            cmd is not None and len(cmd) > 0
        ), "Trying to run a command loop without commands"
        process = None
        returncode = -1
        process = await asyncio.create_subprocess_exec(
            cmd[0], *cmd[1:], cwd=cwd, stdout=PIPE, stderr=STDOUT
        )
        assert process is not None, "Something went wrong creating the process"
        logger.info(f"Process for {cmd} started pid:{process.pid}")

        while True:  # type: ignore
            try:
                line = await process.stdout.readline()  # type: ignore
            except asyncio.TimeoutError:
                logger.error(
                    f"Process has timed out while reading line, timeout set to {timeout}"
                )
                raise

            if not line:
                logger.info("Output for process has finished")
                break
            try:
                line = line.decode()
            except AttributeError:
                # Probably already a string
                pass
            logger.info(line.strip())
        logger.info("Waiting for process to finish")
        await process.wait()
        returncode = process.returncode
        logger.info(f"Process finish with return code {returncode}")
    except Exception as exc:
        error_str = f"Something went wrong with running the command {cmd}, killing the process. Error: {exc}"
        logger.error(error_str)
        if process:
            process.kill()
    return returncode


def run_command_with_output(cmd: List[str], cwd: str = None, timeout: int = 600) -> int:
    """Runs a command line tool printing the stdout as it runs, NOTE: This requires python 3.8

    Arguments:
        cmd {List[str]} -- [List of arguments to run on the commandline]

    Keyword Arguments:
        cwd {str}     -- [Current working directory]
        timeout {int} -- [Max time between stdout lines to judge if the program is stuck] (default: {600})

    Returns:
        int -- [0 if successful, -1 if there's an error]
    """

    loop = asyncio.get_event_loop()
    if loop.is_closed:
        loop = asyncio.new_event_loop()
    try:
        returncode = loop.run_until_complete(_command_loop(cmd, cwd, timeout))
    finally:
        loop.close()
    logger.info(f"Command: {cmd} has completed with the return code: {returncode}")
    return returncode


class command:
    def __init__(self, name=None, cls=click.Command, **attrs):
        self.name = name
        self.cls = cls
        self.attrs = attrs

    def __call__(self, method):
        def __command__(this):
            def wrapper(*args, **kwargs):
                return method(this, *args, **kwargs)

            if hasattr(method, "__options__"):
                options = method.__options__
            return self.cls(self.name, callback=wrapper, params=options, **self.attrs)

        method.__command__ = __command__
        return method


class option:
    def __init__(self, *param_decls, **attrs):
        self.param_decls = param_decls
        self.attrs = attrs

    def __call__(self, method):
        if not hasattr(method, "__options__"):
            method.__options__ = []

        method.__options__.append(
            click.Option(param_decls=self.param_decls, **self.attrs)
        )
        return method


class Cli:
    def __new__(cls, *args, **kwargs):
        self = super(Cli, cls).__new__(cls, *args, **kwargs)
        self._cli = click.Group()

        # Wrap instance options
        self.__option_callbacks__ = set()
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if hasattr(attr, "__options__") and not hasattr(attr, "__command__"):
                self._cli.params.extend(attr.__options__)
                self.__option_callbacks__.add(attr)

        # Wrap commands
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if hasattr(attr, "__command__"):
                command = attr.__command__(self)
                # command.params.extend(_options)
                self._cli.add_command(command)

        return self

    def run(self):
        """Run the CLI application."""
        self()

    def __call__(self):
        """Run the CLI application."""
        self._cli()
