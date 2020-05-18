from dataclasses import dataclass
from .helpers import default
from .errors import CliSyntaxError, CliRuntimeError, ValidationError


@dataclass
class ArgumentParseResult:
    invocation: str
    valid: bool = False
    args: dict = default(dict)
    error: ValidationError = None

    def raise_error(self):
        if self.error.syntax:
            raise CliSyntaxError(self.invocation, self.error.msg)
        raise CliRuntimeError(self.invocation, self.error.msg)
