class LibvisException(Exception):
    """
    Base exception class.
    All libvis_modules-specific exceptions should subclass this class.
    """
class RepositoryNotFound(LibvisException):
    pass
class RepositoryCloneFailed(LibvisException):
    pass
class UnknownRepoType(LibvisException):
    pass
class VCSNotInstalled(LibvisException):
    pass

