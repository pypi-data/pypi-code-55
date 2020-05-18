import sys

from .console import Console
from . import operations, helpers, errors


class Executor:
    def __init__(self, console: Console):
        self.console = console
        self.ops = operations.Operation.registry.enum()
        self.script = "hyrontools"

    def print_welcome(self):
        self.print_cli_asset("header")
        self.console.print(f" - Python runtime: {sys.executable}")
        self.console.print(f" - Script name: {self.script}")
        self.print_cli_asset("breakline")

    def get_operation(self, name, check=True):
        if check and name not in self.ops:
            raise errors.CliExecutionError(
                f"Operation '{name}'' is undefined.")
        return operations.Operation.get(name, name, self.console)

    def dispatch(self, *args):
        op = self.get_operation(args[0])
        if not op.SILENT:
            self.print_welcome()
        result = op.parse_args(*args[1:])
        if not result.valid:
            result.raise_error()
        op.run(**result.args)

    def print_error(self, exception):
        self.console.newln()
        self.console.print(str(exception))
        self.console.newln()

    def print_cli_asset(self, asset):
        self.console.print(helpers.load_text_asset(f"cli_{asset}"))

    def print_usage(self):
        operations = map(lambda x: self.get_operation(x, False), self.ops)
        self.console.print_iter(
            "Usage", [op.usage for op in operations if not op.HIDDEN]
        )

    def entrypoint(self, *args):
        self.script = args[0]
        args = args[1:]

        try:
            if not args:
                raise errors.CliExecutionError(silent=True)
            self.dispatch(*args)
        except errors.CliExecutionError as e:
            if not e.silent:
                self.print_error(e)
            if e.showusage:
                self.print_usage()
            return 1
        except errors.CliRuntimeError as e:
            self.print_error(e)
            return 2
        except errors.CliSyntaxError as e:
            self.print_error(e)
            self.print_usage()
            return 3

        return 0
