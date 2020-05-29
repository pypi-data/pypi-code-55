from __future__ import annotations

from typing import Type

from ._cdata import CData
from ._ffi import ffi, lib
from ._model import Model

__all__ = ["Output"]


class Output:
    """
    IMM file writer.

    Parameters
    ----------
    imm_output
        Output pointer.
    """

    def __init__(self, imm_output: CData):
        if imm_output == ffi.NULL:
            raise RuntimeError("`imm_output` is NULL.")
        self._imm_output = imm_output

    @classmethod
    def create(cls: Type[Output], filepath: bytes) -> Output:
        return cls(lib.imm_output_create(filepath))

    def write(self, model: Model):
        err: int = lib.imm_output_write(self._imm_output, model.imm_model)
        if err != 0:
            raise RuntimeError("Could not write model.")

    def close(self):
        err: int = lib.imm_output_close(self._imm_output)
        if err != 0:
            raise RuntimeError("Could not close output.")

    def __del__(self):
        if self._imm_output != ffi.NULL:
            self.close()
            lib.imm_output_destroy(self._imm_output)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        del exception_type
        del exception_value
        del traceback
        self.close()
