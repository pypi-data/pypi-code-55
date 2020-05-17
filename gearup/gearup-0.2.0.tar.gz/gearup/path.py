import os
from .meta import typing

class ensure_directory(object, metaclass=typing):
  def __init__(self, exists_ok=False):
    self.exists_ok = exists_ok

  def __call__(self, value):
    os.makedirs(value, exist_ok=self.exists_ok)
    return value

