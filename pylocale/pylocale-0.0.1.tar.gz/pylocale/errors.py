class NoSuchLocaleError(Exception):
    """Raised when a translation file is not found."""
    pass


class ParserInvalidLineError(Exception):
    """Raised when some line in a locale file is invalid."""
    pass


class NoSuchKeyError(Exception):
    """Raised when an unexisting key accessed."""
    pass
