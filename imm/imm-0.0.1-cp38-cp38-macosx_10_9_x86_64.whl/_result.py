from typing import Generic, TypeVar

from ._cdata import CData
from ._ffi import ffi, lib
from ._path import Path
from ._sequence import SubSequence
from ._state import State
from ._step import Step

__all__ = ["Result"]

T = TypeVar("T", bound=State)


class Result(Generic[T]):
    """
    Result.

    Parameters
    ----------
    imm_result
        Result pointer.
    path
        Path.
    sequence
        Sequence.
    """

    def __init__(
        self, imm_result: CData, path: Path[Step[T]], sequence: SubSequence,
    ):
        if imm_result == ffi.NULL:
            raise RuntimeError("`imm_result` is NULL.")
        self._imm_result = imm_result
        self._path = path
        self._sequence = sequence

    @property
    def loglikelihood(self) -> float:
        return lib.imm_result_loglik(self._imm_result)

    @property
    def path(self) -> Path[Step[T]]:
        return self._path

    @property
    def sequence(self) -> SubSequence:
        return self._sequence

    def __del__(self):
        if self._imm_result != ffi.NULL:
            lib.imm_result_free(self._imm_result)

    def __repr__(self) -> str:
        return str(self.loglikelihood)
