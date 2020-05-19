from __future__ import absolute_import, unicode_literals


class PaxfulError(Exception):
    """Base (catch-all) client exception."""


class RequestError(PaxfulError):
    """Raised when an API request to  fails.


    :ivar message: Error message.
    :vartype message: str | unicode
    :ivar url:  API endpoint.
    :vartype url: str | unicode
    :ivar body: Raw response body from Pax.
    :vartype body: str | unicode
    :ivar headers: Response headers.
    :vartype headers: requests.structures.CaseInsensitiveDict
    :ivar http_code: HTTP status code.
    :vartype http_code: int
    :ivar error_code: Error code from Pax.
    :vartype error_code: int
    :ivar response: Response object.
    :vartype response: requests.Response
    """

    def __init__(self, response, message, error_code=None):
        self.message = message
        self.url = response.url
        self.body = response.text
        self.headers = response.headers
        self.http_code = response.status_code
        self.error_code = error_code
        self.response = response
        Exception.__init__(self, message)


class InvalidCurrencyError(PaxfulError):
    """Raised when an invalid major currency is given."""


class InvalidOrderBookError(PaxfulError):
    """Raised when an invalid order book is given."""
