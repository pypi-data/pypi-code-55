import pytest

from imm import Alphabet


def test_alphabet():
    abc = Alphabet.create(b"ACGT", b"X")
    assert abc.length == 4

    assert abc.has_symbol(b"A")
    assert abc.has_symbol(b"C")
    assert abc.has_symbol(b"G")
    assert abc.has_symbol(b"T")

    assert abc.symbol_idx(b"A") == 0
    assert abc.symbol_idx(b"C") == 1
    assert abc.symbol_idx(b"G") == 2
    assert abc.symbol_idx(b"T") == 3

    assert abc.symbol_id(0) == b"A"
    assert abc.symbol_id(1) == b"C"
    assert abc.symbol_id(2) == b"G"
    assert abc.symbol_id(3) == b"T"

    assert abc.symbols == b"ACGT"

    assert str(abc) == "{ACGT}"
    assert repr(abc) == "<Alphabet:{ACGT}>"

    with pytest.raises(TypeError):
        Alphabet.create("ACGTç", b"X")

    with pytest.raises(RuntimeError):
        Alphabet.create("ACGTç".encode(), b"X")
