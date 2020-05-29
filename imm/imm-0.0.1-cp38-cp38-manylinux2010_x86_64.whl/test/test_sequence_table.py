from math import log

import pytest

from imm import Alphabet, Sequence, SequenceTable, lprob_is_zero
from imm.testing import assert_allclose


def test_sequence_table():
    alphabet = Alphabet.create(b"ACGT", b"X")
    seqt = SequenceTable.create(alphabet)

    with pytest.raises(RuntimeError):
        seqt.normalize()

    seqt.add(Sequence.create(b"AGTG", alphabet), log(0.2))
    seqt.add(Sequence.create(b"T", alphabet), log(1.2))

    assert_allclose(seqt.lprob(Sequence.create(b"AGTG", alphabet)), log(0.2))
    assert_allclose(seqt.lprob(Sequence.create(b"T", alphabet)), log(1.2))
    assert lprob_is_zero(seqt.lprob(Sequence.create(b"", alphabet)))

    with pytest.raises(RuntimeError):
        seqt.lprob(Sequence.create(b"AT", Alphabet.create(b"AT", b"X")))

    with pytest.raises(RuntimeError):
        seqt.add(Sequence.create(b"AT", Alphabet.create(b"AT", b"X")), log(0.2))

    seqt.normalize()

    assert_allclose(seqt.lprob(Sequence.create(b"AGTG", alphabet)), log(0.2 / 1.4))
    assert_allclose(seqt.lprob(Sequence.create(b"T", alphabet)), log(1.2 / 1.4))
