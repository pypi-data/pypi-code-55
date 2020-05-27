from enum import Enum


class HTTPVerb(Enum):
    get = "GET"
    post = "POST"
    put = "PUT"
    delete = "DELETE"
    options = "OPTIONS"
    head = "HEAD"
    patch = "PATCH"
