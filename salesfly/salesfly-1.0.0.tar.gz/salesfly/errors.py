class APIError(Exception):
    """
    Base class for all API exceptions
    """
    pass


class APIConnectionError(APIError):
    """
    Exceptions that occur because of problems connecting to the api server
    """
    pass


class APITimeoutError(APIError):
    """
    Exception which is thrown when a request is not processed within the timeout
    """
    pass


class ResponseError(APIError):
    """
    Exception which is thrown when response status code is not 200 or 201
    """
    def __init__(self, status, msg="", code=""):
        self.status = status
        self.msg = msg
        self.code = code
