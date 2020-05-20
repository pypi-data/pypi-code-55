class NoMessageRecipients(Exception):
    """
    Raised when Message Recipients are not specified.
    """
    pass

class InvalidAmount(Exception):
    """
    Raised when an invalid currency amount is specified
    """
    pass
