import pytest

from imm import Alphabet, Sequence


def test_sequence():
    alphabet = Alphabet.create(b"ACGT", b"X")
    seq = Sequence.create(b"ACAAAGATX", alphabet)

    assert len(seq) == 9
    assert bytes(seq) == b"ACAAAGATX"

    assert str(seq) == "ACAAAGATX"
    assert repr(seq) == "<Sequence:ACAAAGATX>"

    Sequence.create(b"ACGXXT", alphabet)

    with pytest.raises(RuntimeError):
        Sequence.create(b"ACGWT", alphabet)

    with pytest.raises(RuntimeError):
        Sequence.create("ACGTç".encode(), alphabet)
