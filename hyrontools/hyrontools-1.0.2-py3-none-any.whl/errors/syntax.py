class CliSyntaxError(RuntimeError):
    """
        Represents an error in a CLI operation syntax.
        Will trigger CLI to display usage info.
    """

    def __init__(self, invocation: str, msg: str):
        self.invocation = invocation
        self.msg = msg

    def __str__(self):
        return f"Syntax error for '{self.invocation}' operation: {self.msg}"
