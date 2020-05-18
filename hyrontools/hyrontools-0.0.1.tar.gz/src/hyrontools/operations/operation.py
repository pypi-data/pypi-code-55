from abc import abstractmethod
from textwrap import dedent, indent
from plugable import Plugable

from ..console import Console
from ..argument_parse_result import ArgumentParseResult
from ..errors import ValidationError


class Operation(Plugable):
    """
        This abstract class represents a CLI operation.
        CLI operations use their docstrings as help text,
        and are invoked using their class registry names.
    """

    ARGC = 0  # If you have an set length of expected args
    ARGV = ()  # Tuple of arg names for set length ops
    HIDDEN = False  # Hidden ops don't show in usage
    SILENT = False  # Silent ops mute executor output

    def __init__(self, invocation: str, console: Console):
        self.invocation = invocation
        self.console = console

    @abstractmethod
    def run(self, **kwargs):
        raise NotImplementedError()

    def postvalidate(self, **kwargs):
        pass

    def prepare_args(self, args):
        return dict(zip(args, self.ARGV))

    def prevalidate(self, args):
        if len(args) != self.ARGC:
            raise ValidationError(
                f"'{self.invocation}' takes {self.ARGC} arguments")

    def parse_args(self, *args) -> ArgumentParseResult:
        result = ArgumentParseResult(self.invocation)

        try:
            self.prevalidate(args)
            kwargs = self.prepare_args(args)
            self.postvalidate(**kwargs)
            result.args = kwargs
            result.valid = True
        except ValidationError as e:
            result.error = e
            result.valid = False

        return result

    @property
    def usage(self):
        linesep = self.console.linesep
        usage = indent(dedent(self.__doc__).strip(), "    | ")

        return f"{self.invocation}:{linesep}{usage}{linesep}"

    @staticmethod
    def assert_artifacts(rulebook):
        if not rulebook.artifacts:
            raise ValidationError(
                f"Rulebook '{rulebook.title}' contain any artifacts",
                False
            )
