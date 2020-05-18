# -*- coding: utf-8 -*-
"""TPU Program Interface."""
import os

from .server import cTPUProgram


# pylint: disable=too-few-public-methods
class TPUProgram(cTPUProgram):
    """Program implements container for TPU binary and DeviceBuffers for weights, SDP, features and output."""

    def __new__(cls, program: str, *args, **kw):
        """Check program path and pass control to Cython implementation."""
        if not os.path.isfile(program):
            raise FileNotFoundError("Program not found: {}".format(program))

        return super().__new__(cls, program, *args, **kw)

    def __init__(self, program: str):
        """Save program path before creating program instance."""
        self.program = program
        super().__init__()
