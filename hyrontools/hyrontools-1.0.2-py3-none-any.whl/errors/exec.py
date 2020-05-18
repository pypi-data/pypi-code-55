class CliExecutionError(RuntimeError):
    """
        Represents an error encountered in the executor.
    """

    def __init__(self, msg: str = "", silent=False, showusage=True):
        self.msg = msg
        self.silent = silent
        self.showusage = showusage

    def __str__(self):
        return self.msg
