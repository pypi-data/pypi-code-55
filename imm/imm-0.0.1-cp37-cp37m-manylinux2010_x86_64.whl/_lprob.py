from math import inf, isinf, isnan, nan
from typing import Iterable

from ._ffi import ffi, lib

__all__ = [
    "lprob_add",
    "lprob_invalid",
    "lprob_is_valid",
    "lprob_is_zero",
    "lprob_normalize",
    "lprob_zero",
]


def lprob_add(a: float, b: float) -> float:
    return lib.imm_lprob_add(a, b)


def lprob_zero() -> float:
    return -inf


def lprob_invalid() -> float:
    return nan


def lprob_is_zero(x: float):
    return isinf(x) and x < 0


def lprob_is_valid(x: float):
    return not isnan(x)


def lprob_normalize(arr: Iterable[float]):
    from array import array

    pyarr = list(arr)
    size = len(pyarr)
    carr = ffi.new(f"double[{size}]", pyarr)

    err: int = lib.imm_lprob_normalize(carr, size)
    if err != 0:
        raise RuntimeError("Failed to normalize.")

    return array("d", carr)
