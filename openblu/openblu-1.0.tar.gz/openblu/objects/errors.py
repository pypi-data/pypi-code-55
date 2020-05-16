"""File containing the exceptions for the OpenBlu API wrapper"""


class OpenBluError(Exception):
    """Generic base class for all OpenBlu API errors"""
    ...


class UnauthorizedAccess(OpenBluError):
    """This error is raised when an invalid access_key is provided to the endpoint"""
    ...


class ServerNotFound(OpenBluError):
    """Exception raised when an invalid server UUID is provided to the API"""
    ...
