# -*- coding: utf-8 -*-
"""TPU Device Interface."""
from .server import cTPUDevice


# pylint: disable=too-few-public-methods
class TPUDevice(cTPUDevice):
    """Python wrapper for cython device implementation."""

    def __new__(cls, *args, **kw):
        """Pass control to Cython implementation."""
        return super().__new__(cls, *args, **kw)
