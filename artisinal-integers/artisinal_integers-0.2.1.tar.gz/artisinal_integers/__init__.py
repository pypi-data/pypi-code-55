import requests

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class HTTPError(Error):
    """Exception raised for http errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class LimitError(Error):
    """Exception raised when user asks for too many integers at once."""

    def __init__(self, message):
        self.message = message


def create_brooklyn_integer(num=1):
    """Fetch Brooklyn Integers."""

    if num > 10:
      raise LimitError("Please request less than 10 integers at a time.")
      
    params = {
        'method': 'brooklyn.integers.create'
    }

    integers = []

    for x in range(num):

      try:
        r = requests.post("https://api.brooklynintegers.com/rest", data=params)
        r.raise_for_status()
      except requests.exceptions.RequestException as err:
        raise
      
      data = r.json()

      if data['stat'] != 'ok':
        err = str(data['error']['code']) + " " + data['error']['error']
        raise HTTPError(err)

      integers.append(r.json()['integer'])

    return integers