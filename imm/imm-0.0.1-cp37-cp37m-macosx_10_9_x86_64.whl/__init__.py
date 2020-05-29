from . import testing, wrap
from ._alphabet import Alphabet
from ._alphabet_table import AlphabetTable
from ._cdata import CData
from ._dp import DP
from ._fragment import Fragment, FragStep
from ._hmm import HMM
from ._input import Input
from ._interval import Interval
from ._lprob import (
    lprob_add,
    lprob_invalid,
    lprob_is_valid,
    lprob_is_zero,
    lprob_normalize,
    lprob_zero,
)
from ._model import Model
from ._output import Output
from ._path import Path
from ._result import Result
from ._results import Results
from ._sequence import Sequence, SequenceABC, SubSequence
from ._sequence_table import SequenceTable
from ._state import MuteState, NormalState, State, StateType, TableState
from ._step import Step
from ._testit import test

try:
    from ._ffi import lib
except Exception as e:
    _ffi_err = """
It is likely caused by a broken installation of this package.
Please, make sure you have a C compiler and try to uninstall
and reinstall the package again."""

    raise RuntimeError(str(e) + _ffi_err)

__version__ = "0.0.1"


__all__ = [
    "Alphabet",
    "AlphabetTable",
    "CData",
    "DP",
    "FragStep",
    "Fragment",
    "HMM",
    "Input",
    "Interval",
    "Model",
    "MuteState",
    "NormalState",
    "Output",
    "Path",
    "Result",
    "Results",
    "Sequence",
    "SequenceABC",
    "SequenceTable",
    "State",
    "StateType",
    "Step",
    "SubSequence",
    "TableState",
    "build_ext",
    "lib",
    "lprob_add",
    "lprob_invalid",
    "lprob_is_valid",
    "lprob_is_zero",
    "lprob_normalize",
    "lprob_zero",
    "test",
    "testing",
    "wrap",
]
