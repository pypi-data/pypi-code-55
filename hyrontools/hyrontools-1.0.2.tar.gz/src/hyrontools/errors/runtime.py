class CliRuntimeError(RuntimeError):
    """
        Represents an error encountered while running an operation.
    """

    def __init__(self, invocation: str, msg: str):
        self.invocation = invocation
        self.msg = msg

    def __str__(self):
        return f"Runtime error for '{self.invocation}' operation: {self.msg}"
