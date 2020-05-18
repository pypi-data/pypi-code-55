class ValidationError(RuntimeError):
    """
        Represents a validation failure during the argumaent parse phase
    """

    def __init__(self, msg: str, syntax=True):
        self.msg = msg
        self.syntax = syntax
