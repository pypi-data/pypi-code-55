from typing import Generic, Iterable, TypeVar

from ._cdata import CData
from ._ffi import ffi, lib
from ._result import Result
from ._sequence import SequenceABC
from ._state import State

__all__ = ["Results"]

T = TypeVar("T", bound=State)


class Results(Generic[T]):
    """
    Results.

    Parameters
    ----------
    imm_results
        Results pointer.
    results
        List of results.
    sequence
        Sequence.
    """

    def __init__(
        self, imm_results: CData, results: Iterable[Result[T]], sequence: SequenceABC,
    ):
        if imm_results == ffi.NULL:
            raise RuntimeError("`imm_results` is NULL.")
        self._imm_results = imm_results
        self._results = list(results)
        self._sequence = sequence

    def __len__(self) -> int:
        return len(self._results)

    def __getitem__(self, i) -> Result[T]:
        return self._results[i]

    def __iter__(self):
        for r in self._results:
            yield r

    def __del__(self):
        if self._imm_results != ffi.NULL:
            lib.imm_results_free(self._imm_results)

    def __repr__(self) -> str:
        return "[" + ",".join([str(r) for r in self]) + "]"
